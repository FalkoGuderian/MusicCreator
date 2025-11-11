#!/usr/bin/env python3
"""
Strategy 1: Sequential Generation with Continuity
Generates long-form music compositions by creating multiple clips with continuation prompts
and concatenating them seamlessly.
"""

import asyncio
import websockets
import json
import uuid
import time
import os
import sys
import argparse
import requests
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

async def generate_single_clip(websocket, prompt, seconds, output_file, clip_number, total_clips, progress, task):
    """
    Generate a single music clip using MusicGPT WebSocket API
    """
    generation_id = str(uuid.uuid4())
    chat_id = str(uuid.uuid4())

    progress.update(task, description=f"[bold cyan]CLIP {clip_number}/{total_clips}[/bold cyan] - Starting generation...")

    # Send generation request
    request = {
        "GenerateAudioNewChat": {
            "id": generation_id,
            "chat_id": chat_id,
            "prompt": prompt,
            "secs": seconds
        }
    }

    await websocket.send(json.dumps(request))
    progress.update(task, description=f"[bold cyan]CLIP {clip_number}/{total_clips}[/bold cyan] - Request sent, monitoring progress...")

    generation_started = False
    start_time = time.time()
    timeout = 600  # 10 minutes per clip
    last_progress = 0

    while time.time() - start_time < timeout:
        try:
            # Check if file was created (fallback detection)
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                if file_size > 50000:  # >50KB (reasonable size for audio)
                    progress.update(task, description=f"[bold green]CLIP {clip_number}/{total_clips} - File detected! Generation completed.[/bold green]")
                    return True

            # Set a timeout for receiving messages (check every 1 second)
            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
            data = json.loads(message)

            if "Generation" in data:
                gen_data = data["Generation"]

                if "Start" in gen_data:
                    progress.update(task, description=f"[bold cyan]CLIP {clip_number}/{total_clips}[/bold cyan] - Generation started!")
                    generation_started = True

                elif "Progress" in gen_data:
                    current_progress = gen_data["Progress"]["progress"] * 100
                    if current_progress > last_progress:
                        progress.update(task, completed=current_progress, description=f"[bold cyan]CLIP {clip_number}/{total_clips}[/bold cyan] - Generating...")
                        last_progress = current_progress

                elif "Result" in gen_data:
                    progress.update(task, completed=100, description=f"[bold green]CLIP {clip_number}/{total_clips} - Generation completed![/bold green]")

                    # Download the file
                    file_path = gen_data["Result"]["relpath"]
                    file_url = f"http://localhost:8642/files/{file_path}"

                    progress.update(task, description=f"[bold cyan]CLIP {clip_number}/{total_clips}[/bold cyan] - Downloading file...")
                    try:
                        response = requests.get(file_url, timeout=30)
                        response.raise_for_status()

                        with open(output_file, 'wb') as f:
                            f.write(response.content)

                        file_size = len(response.content)
                        progress.update(task, description=f"[bold green]CLIP {clip_number}/{total_clips} - Saved {file_size / 1024 / 1024:.2f} MB[/bold green]")
                        return True

                    except Exception as e:
                        progress.update(task, description=f"[bold red]CLIP {clip_number}/{total_clips} - Download failed: {e}[/bold red]")
                        return False

                elif "Error" in gen_data:
                    progress.update(task, description=f"[bold red]CLIP {clip_number}/{total_clips} - Generation failed: {gen_data['Error']['error']}[/bold red]")
                    return False

            elif "Chats" in data:
                # Ignore chats messages
                pass

            elif "Error" in data:
                progress.update(task, description=f"[bold red]CLIP {clip_number}/{total_clips} - Server error: {data['Error']}[/bold red]")
                return False

        except asyncio.TimeoutError:
            # No message received within timeout, continue checking
            continue

    # Timeout reached
    if not generation_started:
        progress.update(task, description=f"[bold red]CLIP {clip_number}/{total_clips} - Generation never started[/bold red]")
        return False
    else:
        progress.update(task, description=f"[bold red]CLIP {clip_number}/{total_clips} - Generation timeout[/bold red]")
        return False

async def generate_composition_sequential(base_prompt, num_clips, seconds_per_clip, output_dir, final_name):
    """
    Generate a complete music composition using Strategy 1: Sequential Generation
    """
    print("🎵 STRATEGY 1: Sequential Generation with Continuity")
    print("=" * 60)
    print(f"Creating {num_clips} clips × {seconds_per_clip}s = {num_clips * seconds_per_clip}s total composition")
    print(f"Base prompt: {base_prompt}")
    print(f"Output directory: {output_dir}")
    print(f"Final composition: {final_name}")
    print()

    return await generate_clips_and_concatenate(base_prompt, num_clips, seconds_per_clip, output_dir, final_name, strategy="sequential")

async def generate_composition_hierarchical(base_prompt, structure_name, seconds_per_section, output_dir, final_name):
    """
    Generate a complete music composition using Strategy 3: Hierarchical Generation
    """
    print("🎵 STRATEGY 3: Hierarchical Generation with Structure")
    print("=" * 60)

    # Generate section definitions
    sections = generate_hierarchical_sections(base_prompt, structure_name, seconds_per_section)
    num_sections = len(sections)
    total_duration = num_sections * seconds_per_section

    print(f"Structure: {structure_name.upper()}")
    print(f"Sections: {num_sections} × {seconds_per_section}s = {total_duration}s total composition")
    print(f"Base prompt: {base_prompt}")
    print(f"Output directory: {output_dir}")
    print(f"Final composition: {final_name}")
    print()

    # Display section breakdown
    print("Section Breakdown:")
    for i, section in enumerate(sections, 1):
        print(f"  {i}. {section['id'].upper()}: {section['description']}")
    print()

    return await generate_clips_and_concatenate(base_prompt, num_sections, seconds_per_section, output_dir, final_name,
                                               strategy="hierarchical", sections=sections, structure_name=structure_name)

async def generate_composition_ai_sequential(base_prompt, num_clips, seconds_per_clip, output_dir, final_name):
    """
    Generate a complete music composition using Strategy AI: AI-Generated Sequential Prompts
    """
    print("🎵 STRATEGY AI: AI-Generated Sequential Prompts")
    print("=" * 60)

    # Generate AI prompts for sequential composition
    ai_prompts, sliding_window_contexts = generate_ai_prompts(base_prompt, num_clips)

    print(f"Creating {num_clips} clips × {seconds_per_clip}s = {num_clips * seconds_per_clip}s total composition")
    print(f"Base prompt: {base_prompt}")
    print(f"AI-generated prompts: {len(ai_prompts)} creative variations")
    print(f"Output directory: {output_dir}")
    print(f"Final composition: {final_name}")
    print()

    # Display AI-generated prompts (full prompts sent to MusicGPT)
    print("AI-Generated Prompts:")
    for i, prompt in enumerate(ai_prompts, 1):
        print(f"  {i}. {prompt}")
    print()

    return await generate_clips_and_concatenate(base_prompt, num_clips, seconds_per_clip, output_dir, final_name,
                                               strategy="ai_sequential", ai_prompts=ai_prompts, sliding_window_contexts=sliding_window_contexts)

async def generate_composition_ai_hierarchical(base_prompt, structure_name, seconds_per_section, output_dir, final_name):
    """
    Generate a complete music composition using Strategy AI: AI-Generated Hierarchical Prompts
    """
    print("🎵 STRATEGY AI: AI-Generated Hierarchical Prompts with Structure")
    print("=" * 60)

    # Generate section definitions with AI prompts
    sections = generate_ai_sections(base_prompt, structure_name, seconds_per_section)
    num_sections = len(sections)
    total_duration = num_sections * seconds_per_section

    print(f"Structure: {structure_name.upper()}")
    print(f"Sections: {num_sections} × {seconds_per_section}s = {total_duration}s total composition")
    print(f"Base prompt: {base_prompt}")
    print(f"AI-generated prompts: {len(sections)} creative variations")
    print(f"Output directory: {output_dir}")
    print(f"Final composition: {final_name}")
    print()

    # Display section breakdown with AI prompts
    print("AI-Generated Section Prompts:")
    for i, section in enumerate(sections, 1):
        print(f"  {i}. {section['id'].upper()}: {section['description']}")
        print(f"     Prompt: {section['prompt']}")
    print()

    return await generate_clips_and_concatenate(base_prompt, num_sections, seconds_per_section, output_dir, final_name,
                                               strategy="ai_hierarchical", sections=sections, structure_name=structure_name)

async def generate_clips_and_concatenate(base_prompt, num_clips, seconds_per_clip, output_dir, final_name, strategy="sequential", sections=None, structure_name=None, ai_prompts=None, sliding_window_contexts=None):
    """
    Common function for generating clips and concatenating them
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Check if final composition already exists
    final_path = os.path.join(output_dir, final_name)
    if os.path.exists(final_path):
        file_size = os.path.getsize(final_path)
        if file_size > 100000:  # >100KB
            print(f"[INFO] Final composition already exists: {final_path}")
            print(f"Size: {file_size / 1024 / 1024:.2f} MB")
            print("Skipping generation. Delete the file to regenerate.")

            # Still generate and save prompts for documentation
            used_prompts = []
            num_clips = len([f for f in os.listdir(output_dir) if f.startswith('clip_') and f.endswith('.wav')])

            for i in range(1, num_clips + 1):
                if strategy == "sequential":
                    if i == 1:
                        prompt = base_prompt
                    else:
                        prompt = f"{base_prompt}, continuation part {i}, maintaining the same emotional depth and style"
                    section_info = f"CLIP {i}/{num_clips}"
                else:  # hierarchical
                    section = sections[i-1]
                    prompt = section['prompt']
                    section_info = f"SECTION {i}/{num_clips} ({section['id'].upper()}: {section['description']})"

                clip_filename = f"clip_{i:02d}.wav"
                used_prompts.append({
                    'clip_number': i,
                    'section_info': section_info,
                    'prompt': prompt,
                    'duration': seconds_per_clip,
                    'filename': clip_filename
                })

            # Save prompts to text file
            prompts_filename = final_name.replace('.wav', '_prompts.txt')
            prompts_path = os.path.join(output_dir, prompts_filename)

            print(f"\n[PROMPTS] Saving generation prompts to: {prompts_filename}")
            with open(prompts_path, 'w', encoding='utf-8') as f:
                f.write(f"MusicCreator Composition Prompts\n")
                f.write(f"{'='*50}\n\n")
                f.write(f"Generation Strategy: {strategy.title()}\n")
                if strategy == "hierarchical":
                    f.write(f"Musical Structure: {structure_name.upper()}\n")
                f.write(f"Base Prompt: {base_prompt}\n")
                f.write(f"Total Duration: {num_clips * seconds_per_clip} seconds\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                f.write(f"Individual Section Prompts:\n")
                f.write(f"{'-'*30}\n\n")

                for prompt_data in used_prompts:
                    f.write(f"Section {prompt_data['clip_number']}: {prompt_data['section_info']}\n")
                    f.write(f"Duration: {prompt_data['duration']} seconds\n")
                    f.write(f"File: {prompt_data['filename']}\n")
                    f.write(f"Prompt: {prompt_data['prompt']}\n\n")

            print(f"[PROMPTS] Successfully saved prompts to {prompts_filename}")
            return True

    uri = "ws://localhost:8642/ws"

    try:
        async with websockets.connect(uri) as websocket:
            # Receive initial server messages
            print("Connecting to MusicGPT...")
            for _ in range(2):
                message = await websocket.recv()
                data = json.loads(message)
                if "Info" in data:
                    print(f"Connected to: {data['Info']}")

            clip_files = []
            success_count = 0
            used_prompts = []  # Track all prompts used

            # Create progress bar for individual clips
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=Console(),
                refresh_per_second=2
            ) as progress:

                # Generate each clip/section
                for i in range(1, num_clips + 1):
                    if strategy == "sequential":
                        if i == 1:
                            # First clip uses base prompt
                            prompt = base_prompt
                        else:
                            # Subsequent clips use continuation prompts
                            prompt = f"{base_prompt}, continuation part {i}, maintaining the same emotional depth and style"
                        section_info = f"CLIP {i}/{num_clips}"
                    elif strategy == "ai_sequential":
                        # Use the full sliding window context + base prompt + scene prompt for MusicGPT
                        context_text = sliding_window_contexts[i-1]['context_text']
                        if context_text.strip():
                            # Include previous scenes context in the prompt sent to MusicGPT
                            prompt = f"{base_prompt}\n\n{context_text}\n\nCurrent scene: {ai_prompts[i-1]}"
                        else:
                            # First scene has no previous context
                            prompt = ai_prompts[i-1]
                        section_info = f"CLIP {i}/{num_clips} (AI Sliding Window)"
                    else:  # hierarchical or ai_hierarchical
                        section = sections[i-1]
                        prompt = section['prompt']
                        section_info = f"SECTION {i}/{num_clips} ({section['id'].upper()}: {section['description']})"

                    clip_filename = f"clip_{i:02d}.wav"
                    clip_path = os.path.join(output_dir, clip_filename)

                    # Check if clip already exists
                    if os.path.exists(clip_path):
                        file_size = os.path.getsize(clip_path)
                        if file_size > 50000:  # >50KB
                            print(f"[{section_info}] Using existing clip: {clip_filename}")
                            clip_files.append(clip_path)
                            # Track the prompt that would have been used for this clip/section
                            used_prompts.append({
                                'clip_number': i,
                                'section_info': section_info,
                                'prompt': prompt,
                                'duration': seconds_per_clip,
                                'filename': clip_filename
                            })
                            success_count += 1
                            continue

                    # Create progress task for this clip
                    task = progress.add_task(f"[bold cyan]{section_info}[/bold cyan] - Initializing...", total=100)

                    # Generate new clip
                    success = await generate_single_clip(websocket, prompt, seconds_per_clip, clip_path, i, num_clips, progress, task)

                    if success:
                        clip_files.append(clip_path)
                        # Track the prompt used for this clip/section
                        used_prompts.append({
                            'clip_number': i,
                            'section_info': section_info,
                            'prompt': prompt,
                            'duration': seconds_per_clip,
                            'filename': clip_filename
                        })
                        success_count += 1
                        progress.update(task, completed=100, description=f"[bold green]{section_info} - Completed![/bold green]")
                    else:
                        progress.update(task, description=f"[bold red]{section_info} - Failed![/bold red]")
                        print(f"[ERROR] Failed to generate {section_info.lower()}")
                        return False

                    # Small delay between clips to avoid overwhelming the server
                    if i < num_clips:
                        print(f"[INFO] Waiting 2 seconds before next clip...")
                        await asyncio.sleep(2)

            print(f"\n[SUMMARY] Generated {success_count}/{num_clips} clips successfully")

            if success_count != num_clips:
                print("[ERROR] Not all clips generated successfully")
                return False

            # Concatenate all clips
            print("\n[CONCATENATION] Combining all clips into final composition...")
            print(f"Input clips: {len(clip_files)}")
            print(f"Output file: {final_path}")

            # Create file list for FFmpeg
            file_list_path = os.path.join(output_dir, "file_list.txt")
            with open(file_list_path, 'w') as f:
                for clip_file in clip_files:
                    # Use relative path from output directory
                    rel_path = os.path.relpath(clip_file, output_dir)
                    f.write(f"file '{rel_path}'\n")

            # Save prompts to text file before changing working directory
            prompts_filename = final_name.replace('.wav', '_prompts.txt')
            prompts_path = os.path.abspath(os.path.join(output_dir, prompts_filename))

            print(f"\n[PROMPTS] Saving generation prompts to: {prompts_path}")
            try:
                # Ensure output directory exists
                os.makedirs(output_dir, exist_ok=True)

                with open(prompts_path, 'w', encoding='utf-8') as f:
                    f.write(f"MusicCreator - Prompts Sent to MusicGPT\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(f"Generation Strategy: {strategy.title()}\n")
                    if strategy in ["hierarchical", "ai_hierarchical"]:
                        f.write(f"Musical Structure: {structure_name.upper()}\n")
                    f.write(f"Base Prompt: {base_prompt}\n")
                    f.write(f"Total Duration: {num_clips * seconds_per_clip} seconds\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                    f.write(f"Prompts Sent to MusicGPT:\n")
                    f.write(f"{'-'*25}\n\n")

                    for prompt_data in used_prompts:
                        f.write(f"Clip {prompt_data['clip_number']}: {prompt_data['section_info']}\n")
                        f.write(f"Duration: {prompt_data['duration']} seconds\n")
                        f.write(f"File: {prompt_data['filename']}\n")
                        f.write(f"Prompt Sent to MusicGPT:\n")
                        f.write(f"<StartMusicGPT>\n{prompt_data['prompt']}\n<EndMusicGPT>\n\n")
                        f.write(f"{'-'*50}\n\n")

                print(f"[PROMPTS] Successfully saved prompts to {prompts_filename}")
            except Exception as e:
                print(f"[ERROR] Failed to save prompts file: {e}")
                # Don't fail the entire composition for prompts saving error
                print("[INFO] Composition files were created successfully, but prompts documentation failed")

            # Run FFmpeg concatenation from output directory
            original_dir = os.getcwd()
            os.chdir(output_dir)

            try:
                cmd = [
                    "ffmpeg", "-f", "concat", "-safe", "0",
                    "-i", "file_list.txt", "-c", "copy", final_name
                ]

                print(f"[CONCATENATION] Running: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

                if result.returncode == 0:
                    # Check final file
                    if os.path.exists(final_name):
                        final_size = os.path.getsize(final_name)
                        expected_duration = num_clips * seconds_per_clip

                        print("\n[CONCATENATION] SUCCESS!")
                        print(f"Final file: {final_name}")
                        print(f"Size: {final_size / 1024 / 1024:.2f} MB")
                        print(f"Expected duration: ~{expected_duration} seconds")

                        # Get actual duration using FFmpeg
                        duration_cmd = ["ffmpeg", "-i", final_name, "-f", "null", "-"]
                        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)

                        # Extract duration from output
                        for line in duration_result.stderr.split('\n'):
                            if 'Duration:' in line:
                                duration_str = line.split('Duration:')[1].split(',')[0].strip()
                                print(f"Actual duration: {duration_str}")
                                break

                        # Generate MP3 version
                        mp3_name = final_name.replace('.wav', '.mp3')

                        print(f"\n[MP3 CONVERSION] Creating MP3 version: {mp3_name}")
                        mp3_cmd = [
                            "ffmpeg", "-i", final_name,
                            "-codec:a", "libmp3lame", "-qscale:a", "2",
                            mp3_name
                        ]

                        print(f"[MP3] Running: {' '.join(mp3_cmd)}")
                        mp3_result = subprocess.run(mp3_cmd, capture_output=True, text=True, timeout=300)

                        if mp3_result.returncode == 0 and os.path.exists(mp3_name):
                            mp3_size = os.path.getsize(mp3_name)
                            print(f"[MP3] SUCCESS! Created {mp3_name} ({mp3_size / 1024 / 1024:.2f} MB)")
                        else:
                            print("[MP3] Conversion failed, but WAV file is available")

                        print("\n🎵 COMPOSITION COMPLETE!")
                        print(f"WAV File: {os.path.join(output_dir, final_name)}")
                        print(f"MP3 File: {os.path.join(output_dir, mp3_name)}")
                        if strategy == "sequential":
                            print(f"Strategy: Sequential Generation")
                            print(f"Total clips: {num_clips}")
                            print(f"Clip duration: {seconds_per_clip}s each")
                        else:
                            print(f"Strategy: Hierarchical Generation")
                            print(f"Structure: {sections[0]['id'].split('_')[0] if sections else 'Unknown'}")  # Extract structure name
                            print(f"Total sections: {num_clips}")
                            print(f"Section duration: {seconds_per_clip}s each")
                        print(f"Total duration: {expected_duration}s")
                        print(f"Style: {base_prompt.split(',')[0] if ',' in base_prompt else base_prompt}")

                        return True
                    else:
                        print("[ERROR] Final file was not created")
                        return False
                else:
                    print("[ERROR] FFmpeg concatenation failed")
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
                    return False

            except subprocess.TimeoutExpired:
                print("[ERROR] FFmpeg concatenation timed out")
                return False
            finally:
                os.chdir(original_dir)

                # Clean up file list
                if os.path.exists(file_list_path):
                    os.remove(file_list_path)

    except Exception as e:
        print(f"[ERROR] WebSocket connection failed: {e}")
        return False

    # Save prompts to text file (outside WebSocket context)
    try:
        prompts_filename = final_name.replace('.wav', '_prompts.txt')
        prompts_path = os.path.join(output_dir, prompts_filename)

        print(f"\n[PROMPTS] Saving generation prompts to: {prompts_filename}")
        with open(prompts_path, 'w', encoding='utf-8') as f:
            f.write(f"MusicCreator Composition Prompts\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Generation Strategy: {strategy.title()}\n")
            if strategy in ["hierarchical", "ai_hierarchical"]:
                f.write(f"Musical Structure: {structure_name.upper()}\n")
            f.write(f"Base Prompt: {base_prompt}\n")
            f.write(f"Total Duration: {num_clips * seconds_per_clip} seconds\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"Individual Section Prompts:\n")
            f.write(f"{'-'*30}\n\n")

            for prompt_data in used_prompts:
                f.write(f"Section {prompt_data['clip_number']}: {prompt_data['section_info']}\n")
                f.write(f"Duration: {prompt_data['duration']} seconds\n")
                f.write(f"File: {prompt_data['filename']}\n")
                f.write(f"Prompt: {prompt_data['prompt']}\n\n")

        print(f"[PROMPTS] Successfully saved prompts to {prompts_filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save prompts file: {e}")
        # Don't fail the entire composition for prompts saving error
        print("[INFO] Composition files were created successfully, but prompts documentation failed")

# Define musical structures for hierarchical generation
MUSICAL_STRUCTURES = {
    "simple": [
        ("intro", "Introduction section"),
        ("main", "Main body section"),
        ("outro", "Conclusion section")
    ],
    "song": [
        ("intro", "Introduction section"),
        ("verse1", "First verse section"),
        ("chorus1", "First chorus section"),
        ("verse2", "Second verse section"),
        ("chorus2", "Second chorus section"),
        ("bridge", "Bridge section"),
        ("chorus3", "Final chorus section"),
        ("outro", "Outro section")
    ],
    "classical": [
        ("exposition", "Exposition section presenting main themes"),
        ("development", "Development section exploring and varying themes"),
        ("recapitulation", "Recapitulation section restating main themes"),
        ("coda", "Coda section providing final conclusion")
    ]
}

def generate_hierarchical_sections(base_prompt, structure_name, seconds_per_section):
    """
    Generate section definitions for hierarchical strategy
    """
    if structure_name not in MUSICAL_STRUCTURES:
        raise ValueError(f"Unknown structure: {structure_name}. Available: {list(MUSICAL_STRUCTURES.keys())}")

    sections = []
    structure = MUSICAL_STRUCTURES[structure_name]

    for section_id, section_description in structure:
        # Create section-specific prompt
        section_prompt = f"{base_prompt}, {section_description.lower()}, maintaining the same emotional depth and style"
        sections.append({
            'id': section_id,
            'description': section_description,
            'prompt': section_prompt,
            'duration': seconds_per_section
        })

    return sections

def generate_ai_prompts(base_prompt, num_clips, structure_name=None):
    """
    Generate coherent and interesting prompts using OpenRouter AI with base prompt + sliding window scene approach
    Uses a fixed base prompt for general music/song setup, then adds scene-specific prompts via sliding window
    Returns both the final prompts and the sliding window context for documentation
    """
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = os.getenv('OPENROUTER_MODEL', 'x-ai/grok-4-fast')

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")

    # Determine number of prompts needed
    if structure_name:
        # For hierarchical AI, use the structure to determine number of sections
        if structure_name not in MUSICAL_STRUCTURES:
            raise ValueError(f"Unknown structure: {structure_name}. Available: {list(MUSICAL_STRUCTURES.keys())}")
        num_prompts = len(MUSICAL_STRUCTURES[structure_name])
        structure_info = f" using a {structure_name} musical structure with {num_prompts} sections"
    else:
        # For sequential AI, use the specified number of clips
        num_prompts = num_clips
        structure_info = f" with {num_prompts} sequential parts"

    print(f"[AI] Generating {num_prompts} scene prompts using {model} with base prompt + sliding window approach...")

    # NEW APPROACH: Base prompt defines general setup, then scene prompts are added via sliding window
    scene_prompts = []  # Scene-specific prompts that will be combined with base prompt
    sliding_window_contexts = []  # Track the context used for each generation

    for i in range(num_prompts):
        current_section = i + 1

        # Create context from sliding window: current scene + last 2 scenes (max 3 total)
        context_info = ""
        previous_scene_list = []
        if scene_prompts:
            # For sliding window: include current scene + up to 2 previous scenes
            # But exclude scenes that would make total > 3
            total_available = len(scene_prompts) + 1  # +1 for current scene
            if total_available <= 3:
                # Include all previous scenes
                scenes_to_include = scene_prompts
            else:
                # Include last 2 scenes to keep total at 3
                scenes_to_include = scene_prompts[-2:]

            if scenes_to_include:
                context_info = f"\n\nPrevious scenes for continuity:\n"
                for j, prev_scene in enumerate(scenes_to_include, len(scene_prompts) - len(scenes_to_include) + 1):
                    context_info += f"Scene {j}: {prev_scene}\n"
                    previous_scene_list.append(f"Scene {j}: {prev_scene}")

        # Create the AI prompt for this scene with context from previous scenes
        system_prompt = """You are a creative music composition assistant. Your task is to generate a single scene-specific prompt that will be combined with a base prompt for music generation.

Guidelines for creating the scene prompt:
- Focus on scene-specific elements like mood shifts, tempo changes, instrumentation variations, or structural developments
- Make the scene unique and creative while ensuring it flows from ALL previous scenes
- Use descriptive language that complements the base prompt
- Include specific musical terminology when appropriate
- Keep the scene prompt concise but evocative (1 sentence)
- Consider how this scene contributes to the overall musical journey
- Ensure smooth transitions between scenes for maximum coherence

Return only the scene-specific prompt as a plain text string (do not include the base prompt)."""

        user_prompt = f"""Create a scene-specific prompt for section {current_section} of {num_prompts} that will be combined with this base prompt: "{base_prompt}"{structure_info}

This is scene {current_section} in the sequence.{context_info}

The scene prompt should describe scene-specific elements that complement the base prompt and create a cohesive musical journey."""

        # Store the full prompt sent to AI (including context)
        full_ai_prompt = user_prompt

        # Store the context used for this generation
        sliding_window_contexts.append({
            'section': current_section,
            'previous_scenes': previous_scene_list.copy(),
            'context_text': context_info.strip() if context_info else "No previous scenes (first scene)",
            'full_ai_prompt': full_ai_prompt,
            'base_prompt': base_prompt
        })

        # Make API call to OpenRouter
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 300  # Shorter since we only need scene-specific content
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content'].strip()

            # Clean up the response (remove quotes if present)
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            if content.startswith("'") and content.endswith("'"):
                content = content[1:-1]

            # Ensure we got a reasonable prompt
            if len(content) < 5:
                raise ValueError("AI returned too short scene prompt")

            print(f"[AI] Generated scene {current_section}: {content[:60]}...")
            scene_prompts.append(content)

        except Exception as e:
            print(f"[ERROR] Failed to generate AI scene prompt for section {current_section}: {e}")
            # Fallback: create generic scene prompt for this section
            fallback_scene = f"scene {current_section} continuing the musical development"
            print(f"[AI] Using fallback scene prompt for section {current_section}")
            scene_prompts.append(fallback_scene)

    # Combine base prompt with each scene prompt to create final prompts
    final_prompts = []
    for scene_prompt in scene_prompts:
        # Combine base prompt + scene prompt
        combined_prompt = f"{base_prompt}, {scene_prompt}"
        final_prompts.append(combined_prompt)

    print(f"[AI] Successfully generated {len(final_prompts)} combined prompts using base prompt + sliding window scenes")
    return final_prompts, sliding_window_contexts

def generate_ai_sections(base_prompt, structure_name, seconds_per_section):
    """
    Generate section definitions for AI strategy with creative prompts
    """
    if structure_name not in MUSICAL_STRUCTURES:
        raise ValueError(f"Unknown structure: {structure_name}. Available: {list(MUSICAL_STRUCTURES.keys())}")

    # Calculate number of sections needed
    num_sections = len(MUSICAL_STRUCTURES[structure_name])

    # Generate AI prompts for each section
    ai_prompts, sliding_window_contexts = generate_ai_prompts(base_prompt, num_sections, structure_name=structure_name)

    sections = []
    structure = MUSICAL_STRUCTURES[structure_name]

    for i, (section_id, section_description) in enumerate(structure):
        sections.append({
            'id': section_id,
            'description': section_description,
            'prompt': ai_prompts[i],  # Use AI-generated prompt
            'duration': seconds_per_section
        })

    return sections

def main():
    parser = argparse.ArgumentParser(
        description="Generate long-form music compositions using Strategy 1 (Sequential), Strategy 3 (Hierarchical), or Strategy AI (AI-Generated Prompts)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Strategy 1: Sequential Generation (default)
  python generate_composition.py -p "Contemporary classical piano solo in the style of Nils Frahm" -n 20 -s 30 -o outputs/nils_frahm_suite -f nils_frahm_10_minutes.wav

  # Strategy 3: Hierarchical Generation - Song Structure
  python generate_composition.py --strategy hierarchical --structure song -p "Pop song with piano and vocals" -s 20 -o outputs/pop_song -f pop_song.wav

  # Strategy 3: Hierarchical Generation - Classical Structure
  python generate_composition.py --strategy hierarchical --structure classical -p "Classical symphony movement" -s 45 -o outputs/classical -f symphony_movement.wav

  # Strategy 3: Hierarchical Generation - Simple Structure
  python generate_composition.py --strategy hierarchical --structure simple -p "Ambient electronic music" -s 60 -o outputs/ambient -f ambient_piece.wav

  # Strategy AI: AI-Generated Sequential Prompts
  python generate_composition.py --strategy ai -p "Jazz improvisation with saxophone and piano" -n 5 -s 30 -o outputs/jazz_ai -f jazz_improvisation.wav

  # Strategy AI: AI-Generated Hierarchical Prompts with Song Structure
  python generate_composition.py --strategy ai --structure song -p "Rock ballad with electric guitar and drums" -s 25 -o outputs/rock_ballad -f rock_ballad.wav
"""
    )

    parser.add_argument("-p", "--prompt", required=True,
                       help="Base prompt for music generation")
    parser.add_argument("--strategy", choices=["sequential", "hierarchical", "ai"], default="sequential",
                       help="Generation strategy: sequential (default), hierarchical, or ai")
    parser.add_argument("--structure", choices=list(MUSICAL_STRUCTURES.keys()), default="simple",
                       help="Musical structure for hierarchical strategy (default: simple)")
    parser.add_argument("-n", "--num-clips", type=int,
                       help="Number of clips to generate (ignored for hierarchical strategy)")
    parser.add_argument("-s", "--seconds-per-clip", type=int, default=30,
                       help="Duration of each clip/section in seconds (default: 30)")
    parser.add_argument("-o", "--output-dir", default="outputs/composition",
                       help="Output directory for clips and final composition")
    parser.add_argument("-f", "--final-name", default="composition.wav",
                       help="Name of the final concatenated composition file")

    args = parser.parse_args()

    # Validate arguments based on strategy
    if args.strategy == "sequential":
        if not args.num_clips:
            print("[ERROR] --num-clips is required for sequential strategy")
            sys.exit(1)
        if args.num_clips < 1:
            print("[ERROR] Number of clips must be at least 1")
            sys.exit(1)
        total_duration = args.num_clips * args.seconds_per_clip
        print(f"[INFO] Will generate {total_duration} seconds ({total_duration/60:.1f} minutes) of music")
        print(f"[INFO] Using {args.num_clips} clips of {args.seconds_per_clip} seconds each")
    elif args.strategy == "ai":
        # For AI strategy, determine if it's sequential or hierarchical based on --num-clips
        if args.num_clips:
            # AI sequential mode
            if args.num_clips < 1:
                print("[ERROR] Number of clips must be at least 1")
                sys.exit(1)
            total_duration = args.num_clips * args.seconds_per_clip
            print(f"[INFO] Will generate {total_duration} seconds ({total_duration/60:.1f} minutes) of music")
            print(f"[INFO] Using AI strategy with {args.num_clips} sequential clips of {args.seconds_per_clip} seconds each")
        else:
            # AI hierarchical mode
            sections = generate_hierarchical_sections(args.prompt, args.structure, args.seconds_per_clip)
            num_sections = len(sections)
            total_duration = num_sections * args.seconds_per_clip
            print(f"[INFO] Will generate {total_duration} seconds ({total_duration/60:.1f} minutes) of music")
            print(f"[INFO] Using AI strategy with {args.structure} structure and {num_sections} sections of {args.seconds_per_clip} seconds each")
    else:  # hierarchical
        # For hierarchical, num_clips is determined by the structure
        sections = generate_hierarchical_sections(args.prompt, args.structure, args.seconds_per_clip)
        num_sections = len(sections)
        total_duration = num_sections * args.seconds_per_clip
        print(f"[INFO] Will generate {total_duration} seconds ({total_duration/60:.1f} minutes) of music")
        print(f"[INFO] Using {args.structure} structure with {num_sections} sections of {args.seconds_per_clip} seconds each")

    if args.seconds_per_clip < 5:
        print("[ERROR] Clip/section duration must be at least 5 seconds")
        sys.exit(1)

    # Check if MusicGPT is running
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 8642))
        sock.close()
        print("[OK] MusicGPT WebSocket accessible")
    except:
        print("[ERROR] Cannot connect to MusicGPT WebSocket")
        print("Start MusicGPT first: scripts\\run_musicgpt_cpu.bat")
        sys.exit(1)

    # Check if FFmpeg is available
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            raise FileNotFoundError
        print("[OK] FFmpeg available for concatenation")
    except FileNotFoundError:
        print("[ERROR] FFmpeg not found. Please install FFmpeg for audio concatenation.")
        print("Download from: https://ffmpeg.org/download.html")
        sys.exit(1)

    # Run the composition generation based on strategy
    if args.strategy == "sequential":
        success = asyncio.run(generate_composition_sequential(
            args.prompt,
            args.num_clips,
            args.seconds_per_clip,
            args.output_dir,
            args.final_name
        ))
    elif args.strategy == "ai":
        # Determine AI mode based on --num-clips
        if args.num_clips:
            # AI sequential mode
            success = asyncio.run(generate_composition_ai_sequential(
                args.prompt,
                args.num_clips,
                args.seconds_per_clip,
                args.output_dir,
                args.final_name
            ))
        else:
            # AI hierarchical mode
            success = asyncio.run(generate_composition_ai_hierarchical(
                args.prompt,
                args.structure,
                args.seconds_per_clip,
                args.output_dir,
                args.final_name
            ))
    else:  # hierarchical
        success = asyncio.run(generate_composition_hierarchical(
            args.prompt,
            args.structure,
            args.seconds_per_clip,
            args.output_dir,
            args.final_name
        ))

    if success:
        print("\n✅ COMPOSITION GENERATION COMPLETE!")
        print(f"Check your output directory: {args.output_dir}")
        print(f"Final file: {args.final_name}")
    else:
        print("\n❌ COMPOSITION GENERATION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
