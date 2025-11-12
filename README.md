# 🎵 MusicCreator - Advanced AI Music Composition System

**Generate professional-quality music compositions using multiple AI strategies with seamless continuation, musical structures, and intelligent prompt engineering.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://docker.com)

## 🎯 Overview

MusicCreator is a comprehensive AI music generation system featuring three distinct composition strategies:

- **🎼 Strategy 1: Sequential Generation** - Long-form compositions with continuation prompts
- **🏗️ Strategy 2: Hierarchical Generation** - Structured compositions using predefined musical forms
- **🤖 Strategy 3: AI-Generated Prompts** - Intelligent prompt engineering with sliding window coherence

The system produces seamless music pieces of any desired length with automatic prompt documentation and dual-format output.

### ✨ Key Features

- 🎼 **Three Composition Strategies** - Sequential, Hierarchical, and AI-Generated approaches
- 🏗️ **Predefined Musical Structures** - Song, Classical, Simple forms with proper musical architecture
- 🤖 **Base Prompt + Sliding Window Scenes AI** - Fixed base prompt ensures coherence + scene prompts consider previous scenes (max 3 total) for maximum musical continuity
- 📝 **Automatic Prompt Documentation** - Detailed text files documenting all generation prompts
- 🔄 **Seamless Continuation** - AI maintains musical coherence across clips
- 📊 **Modern Progress Bars** - Beautiful CLI interface with Rich library
- 🎵 **Dual Format Output** - Automatic WAV + MP3 generation
- 🚀 **Resume Capability** - Continue from existing clips
- 🎛️ **Flexible Configuration** - Custom prompts, durations, structures, and styles
- 🔧 **Headless Operation** - No web browser required
- ⚡ **WebSocket API Integration** - Direct communication with MusicGPT

## 🏗️ Architecture

### Strategy 1: Sequential Generation with Continuity

```
Base Prompt → Clip 1 → Continuation Prompt → Clip 2 → ... → FFmpeg Concatenation → Final Composition
```

1. **Generate Base Clip** - First clip uses your creative prompt
2. **Continuation Prompts** - Subsequent clips use "continuation part X" prompts
3. **Seamless Concatenation** - FFmpeg combines clips into final composition
4. **Format Conversion** - Automatic MP3 generation for smaller file sizes

### Strategy 2: Hierarchical Generation with Musical Structures

```
Base Prompt + Structure → Section Prompts → Clip Generation → Concatenation → Structured Composition
```

1. **Choose Musical Structure** - Select from predefined forms (Simple, Song, Classical)
2. **Generate Section Prompts** - Each section gets context-specific prompts
3. **Structured Generation** - Clips follow musical architecture
4. **Professional Output** - Complete compositions with proper form

### Strategy 3: AI-Generated Prompts with Base Prompt + Sliding Window Scenes

```
Base Prompt → AI Scene Generation → Sliding Window Context → Combined Prompts → MusicGPT → Composition
```

1. **Base Prompt Setup** - Fixed base prompt defines the overall music concept and ensures coherence
2. **Sliding Window Scenes** - AI generates scene-specific prompts considering ALL previous scenes for maximum continuity
3. **Context-Aware Generation** - Each scene prompt includes the current scene + up to 2 previous scenes (max 3 total)
4. **Combined Prompts** - Final prompts sent to MusicGPT combine base prompt + scene prompt for optimal results
5. **Maximum Coherence** - Base prompt consistency + contextual scene development ensures seamless musical flow
6. **Automatic Documentation** - Saves all prompts, AI generation process, and sliding window context for reproducibility

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Docker Desktop** or **Rancher Desktop**
- **FFmpeg** for audio processing
- **Git** for cloning

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FalkoGuderian/MusicCreator.git
   cd MusicCreator
   ```

2. **Install Python dependencies:**
   ```bash
   pip install websockets requests tqdm rich
   ```

3. **Start MusicGPT:**
   ```bash
   # Windows
   scripts\run_musicgpt_cpu.bat

   # Linux/Mac
   docker run -p 8642:8642 gabotechs/musicgpt
   ```

4. **Verify installation:**
   ```bash
   python scripts/generate_composition.py --help
   ```

## 🎵 Usage Examples

### 🎼 Strategy 1: Sequential Generation

#### Generate a 10-Minute Contemporary Classical Suite

```bash
python scripts/generate_composition.py \
  --strategy sequential \
  -p "Contemporary classical piano solo, introspective and emotional, with ambient reverb and subtle harmonic complexity, slow tempo, minimalist yet deeply expressive" \
  -n 20 \
  -s 30 \
  -o outputs/contemporary_classical_suite \
  -f contemporary_classical_10_minutes.wav
```

**Result:** 20 clips × 30 seconds = 10-minute seamless composition

#### Create a 5-Minute Ambient Piece

```bash
python scripts/generate_composition.py \
  --strategy sequential \
  -p "Ambient electronic music with deep pads and subtle textures, evolving slowly with gentle transitions" \
  -n 10 \
  -s 30 \
  -o outputs/ambient_dreams \
  -f ambient_5_minutes.wav
```

### 🏗️ Strategy 2: Hierarchical Generation

#### Create a Song Structure (8 sections)

```bash
python scripts/generate_composition.py \
  --strategy hierarchical \
  --structure song \
  -p "Pop ballad with piano and vocals, emotional and melodic" \
  -s 20 \
  -o outputs/pop_ballad \
  -f pop_ballad.wav
```

**Structure:** Intro → Verse 1 → Chorus 1 → Verse 2 → Chorus 2 → Bridge → Chorus 3 → Outro

#### Classical Sonata Form

```bash
python scripts/generate_composition.py \
  --strategy hierarchical \
  --structure classical \
  -p "Beethoven-style piano sonata" \
  -s 45 \
  -o outputs/classical_sonata \
  -f beethoven_sonata.wav
```

**Structure:** Exposition → Development → Recapitulation → Coda

#### Simple Three-Part Structure

```bash
python scripts/generate_composition.py \
  --strategy hierarchical \
  --structure simple \
  -p "Ambient electronic music" \
  -s 60 \
  -o outputs/ambient_simple \
  -f ambient_piece.wav
```

**Structure:** Intro → Main → Outro

### 🤖 Strategy 3: AI-Generated Prompts

#### AI-Generated Sequential Composition

```bash
python scripts/generate_composition.py \
  --strategy ai \
  -p "Jazz improvisation with saxophone and piano" \
  -n 8 \
  -s 15 \
  -o outputs/jazz_ai \
  -f jazz_improvisation.wav
```

**Features:** Sliding window coherence, automatic prompt generation

#### AI-Generated Song with Structure

```bash
python scripts/generate_composition.py \
  --strategy ai \
  --structure song \
  -p "Rock ballad with electric guitar and drums" \
  -s 25 \
  -o outputs/rock_ballad \
  -f rock_ballad.wav
```

**Features:** AI creates coherent prompts for each song section

### 🎹 Classical Piano Sonata (AI-Generated)

```bash
python scripts/generate_composition.py \
  --strategy ai \
  --structure simple \
  -p "Classical piano sonata" \
  -s 10 \
  -o outputs/classical_sonata \
  -f classical_sonata.wav
```

**Result:** AI generates coherent prompts for intro, main, and outro sections

## 📋 Command Line Options

```
Usage: python scripts/generate_composition.py [OPTIONS]

Required:
  -p, --prompt TEXT          Base prompt for music generation

Strategy Selection:
  --strategy [sequential|hierarchical|ai]
                             Generation strategy (default: sequential)
  --structure [simple|song|classical]
                             Musical structure for hierarchical/ai strategies (default: simple)

Composition Parameters:
  -n, --num-clips INTEGER    Number of clips to generate for sequential/ai strategies (default: 10)
  -s, --seconds-per-clip INTEGER
                             Duration of each clip/section in seconds (default: 30)

Output Configuration:
  -o, --output-dir TEXT      Output directory (default: outputs/composition)
  -f, --final-name TEXT      Final composition filename (default: composition.wav)

Information:
  --help                     Show this message and exit
```

## 📁 Project Structure

```
MusicCreator/
├── scripts/
│   ├── generate_composition.py    # Main composition generator
│   └── run_musicgpt_cpu.bat       # MusicGPT startup script
├── outputs/                       # Generated compositions
├── docs/
│   └── MusicGPT.md               # MusicGPT documentation
└── README.md                     # This file
```

## 🎼 How It Works

### Strategy-Specific Prompt Generation

#### Sequential Strategy
The system automatically generates continuation prompts to maintain musical coherence:

- **Clip 1:** `"Your creative prompt"`
- **Clip 2:** `"Your creative prompt, continuation part 2, maintaining the same emotional depth and style"`
- **Clip 3:** `"Your creative prompt, continuation part 3, maintaining the same emotional depth and style"`

#### Hierarchical Strategy
Each musical section gets context-specific prompts based on its role in the structure:

- **Intro:** `"Your prompt, introduction section setting the mood"`
- **Main:** `"Your prompt, main body section developing the theme"`
- **Outro:** `"Your prompt, conclusion section providing resolution"`

#### AI Strategy with Base Prompt + Sliding Window Scenes
The AI uses a sophisticated approach combining fixed base prompts with intelligent sliding window context:

- **Base Prompt:** Fixed prompt defining the overall music concept and ensuring coherence across the entire composition
- **Sliding Window Scenes:** Each scene prompt includes current scene + up to 2 previous scenes (maximum 3 total) for optimal context without prompt bloat
- **Context-Aware Generation:** AI considers musical continuity when generating each scene prompt
- **Combined Prompts:** Final prompts sent to MusicGPT combine base prompt + contextual scene prompt
- **Maximum Coherence:** Base prompt consistency + sliding window context ensures seamless musical flow

### Automatic Prompt Documentation

Every composition generates a detailed prompts file documenting:

- Generation strategy and parameters
- Base prompt and AI-generated variations
- Section-by-section prompt breakdown
- Timing and file information
- Generation timestamp for reproducibility

### Audio Processing Pipeline

1. **Individual Clips** - Each clip is generated as a separate WAV file
2. **Concatenation** - FFmpeg combines clips with perfect synchronization
3. **Compression** - MP3 version created for smaller file sizes
4. **Documentation** - Prompt details saved for future reference
5. **Metadata** - Duration and format information preserved

## 🎨 Supported Music Styles

The system works with any music style description:

- **Classical:** `"Beethoven-style piano sonata"`
- **Electronic:** `"Ambient techno with deep bass"`
- **Jazz:** `"Miles Davis trumpet improvisation"`
- **Rock:** `"Progressive rock guitar solo"`
- **World:** `"African drumming with polyrhythms"`
- **Experimental:** `"Glitchy electronic soundscapes"`

## 🔧 Advanced Configuration

### Custom Clip Durations

- **Short clips (5-15s):** More frequent transitions, experimental feel
- **Medium clips (20-40s):** Balanced continuity and variety
- **Long clips (60s+):** Extended musical development

### Output Directory Structure

```
outputs/your_composition/
├── clip_01.wav              # Individual clips
├── clip_02.wav
├── ...
├── clip_20.wav
├── composition.wav          # Final WAV file
├── composition.mp3          # Compressed MP3
└── composition_prompts.txt  # Detailed prompt documentation
```

## 🐛 Troubleshooting

### Common Issues

**"Cannot connect to MusicGPT WebSocket"**
- Ensure MusicGPT container is running: `docker ps`
- Check port 8642 is accessible: `netstat -an | find "8642"`

**"FFmpeg not found"**
- Install FFmpeg: `choco install ffmpeg` (Windows)
- Or download from: https://ffmpeg.org/download.html

**"Generation timeout"**
- Increase timeout in script or reduce clip duration
- Check MusicGPT container logs: `docker logs <container_id>`

### Performance Tips

- **CPU Mode:** Use for unlimited generation time
- **GPU Mode:** Faster generation with VRAM limits
- **Batch Processing:** Generate multiple compositions in sequence
- **Resume:** Delete failed clips to resume from interruption

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Format code
black scripts/*.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[MusicGPT](https://github.com/gabotechs/MusicGPT)** - The underlying AI music generation model
- **FFmpeg** - Professional audio processing
- **Rich** - Beautiful CLI interfaces
- **WebSockets** - Real-time API communication

Creating 20 clips × 30s = 600s total composition
Base prompt: Contemporary classical piano solo, introspective and emotional...
Output directory: outputs/contemporary_classical_suite
Final composition: contemporary_classical_10_minutes.wav

[SUMMARY] Generated 20/20 clips successfully

[CONCATENATION] SUCCESS!
Final file: contemporary_classical_10_minutes.wav
Size: 72.5 MB
Expected duration: ~600 seconds
Actual duration: 00:09:59.80

[MP3 CONVERSION] SUCCESS! Created contemporary_classical_10_minutes.mp3 (5.2 MB)

🎵 COMPOSITION COMPLETE!
Total clips: 20 | Clip duration: 30s each | Total duration: 600s
```
## 🎵 Sample Output

### Strategy 1: Sequential Generation

After running the 10-minute contemporary classical example:

```
🎵 STRATEGY 1: Sequential Generation with Continuity
Creating 20 clips × 30s = 600s total composition
Base prompt: Contemporary classical piano solo, introspective and emotional...
Output directory: outputs/contemporary_classical_suite
Final composition: contemporary_classical_10_minutes.wav

[SUMMARY] Generated 20/20 clips successfully

[CONCATENATION] SUCCESS!
Final file: contemporary_classical_10_minutes.wav
Size: 72.5 MB
Expected duration: ~600 seconds
Actual duration: 00:09:59.80

[MP3 CONVERSION] SUCCESS! Created contemporary_classical_10_minutes.mp3 (5.2 MB)

[PROMPTS] Successfully saved prompts to contemporary_classical_10_minutes_prompts.txt

🎵 COMPOSITION COMPLETE!
Total clips: 20 | Clip duration: 30s each | Total duration: 600s
```

### Strategy AI: AI-Generated with Base Prompt + Sliding Window Scenes

After running the AI-generated contemporary classical composition:

```
🎵 STRATEGY AI: AI-Generated Sequential Prompts
[AI] Generating 3 scene prompts using x-ai/grok-4-fast with base prompt + sliding window approach...
[AI] Generated scene 1: Begin with a serene and introspective introduction, featuring delicate arpeggios ascending in C major at a moderate tempo of 72 BPM...
[AI] Generated scene 2: Transition into a brooding development section, evolving the introductory arpeggios into intricate contrapuntal textures...
[AI] Generated scene 3: Culminate in a radiant climax and serene resolution, unleashing cascading scalar runs and resonant block chords...
[AI] Successfully generated 3 combined prompts using base prompt + sliding window scenes

Creating 3 clips × 10s = 30s total composition
Base prompt: Contemporary classical piano solo in C major

AI-Generated Prompts:
  1. Contemporary classical piano solo in C major, Begin with a serene and introspective introduction, featuring delicate arpeggios ascending in C major at a moderate tempo of 72 BPM, building subtle tension through gentle dynamic swells to evoke quiet anticipation for the journey ahead.
  2. Contemporary classical piano solo in C major, Transition into a brooding development section, evolving the introductory arpeggios into intricate contrapuntal textures with dissonant suspensions resolving back to C major consonance, gradually accelerating to 80 BPM while introducing rhythmic ostinatos to deepen the emotional undercurrent and bridge toward climactic release.
  3. Contemporary classical piano solo in C major, Culminate in a radiant climax and serene resolution, unleashing cascading scalar runs and resonant block chords in C major that swell to a fervent forte at 92 BPM before decelerating into a tranquil coda with lingering pedal tones, evoking triumphant catharsis and peaceful closure to the introspective odyssey.

[SUMMARY] Generated 3/3 clips successfully

[CONCATENATION] SUCCESS!
Final file: test_base_scene.wav
Size: 3.62 MB
Expected duration: ~30 seconds
Actual duration: 00:00:29.82

[MP3 CONVERSION] SUCCESS! Created test_base_scene.mp3 (0.28 MB)

🎵 COMPOSITION COMPLETE!
Strategy: AI-Generated Sequential | Total sections: 3
```
============================================================
Creating 20 clips × 30s = 600s total composition
Base prompt: Contemporary classical piano solo, introspective and emotional...
Output directory: outputs/contemporary_classical_suite
Final composition: contemporary_classical_10_minutes.wav

[SUMMARY] Generated 20/20 clips successfully

[CONCATENATION] SUCCESS!
Final file: contemporary_classical_10_minutes.wav
Size: 72.5 MB
Expected duration: ~600 seconds
Actual duration: 00:09:59.80

[MP3 CONVERSION] SUCCESS! Created contemporary_classical_10_minutes.mp3 (5.2 MB)

🎵 COMPOSITION COMPLETE!
Total clips: 20 | Clip duration: 30s each | Total duration: 600s
```

---

## 🎵 TODO: Lyrics and Vocals Integration

Based on research into open-source vocal music generation tools, implement the following features to add lyrics and vocals support to MusicCreator:

### 🎤 **Lyrics Generation**
- [ ] **Ollama Integration**: Set up Ollama Docker container for local AI lyrics generation
  - Pull `ollama/ollama` image and run with persistent volume
  - Pull Llama 3.1 model for creative text generation
  - Create API endpoint for lyrics generation from prompts
  - Support structured lyrics output ([Verse], [Chorus], etc.)
- [ ] **OpenRouter LLM Integration**: Leverage existing OpenRouter setup for lyrics generation
  - Use available LLM models for creative text generation
  - Integrate with existing open-notebook-setup infrastructure
  - API endpoint: `https://openrouter.ai/api/v1` (already configured)

### 🗣️ **Spoken Vocals (Kokoro-TTS)**
- [ ] **Kokoro-TTS Integration**: Leverage existing kokoro-tts from open-notebook-setup
  - **Current Status**: Already running in Docker at `http://kokoro-tts:8880/v1`
  - **Capabilities**: OpenAI-compatible TTS for spoken voice synthesis
  - **Use Case**: Convert generated lyrics to spoken vocals (not sung/melody)
  - **Integration**: Combine with MusicGPT instrumentals for spoken-word tracks
- [ ] **Lyrics-to-Speech Pipeline**: Create workflow for spoken vocal tracks
  - Generate lyrics → Convert to speech → Mix with instrumental music
  - Voice selection and emotion parameters
  - Audio synchronization and timing

### 🎼 **Vocal Music Tools Integration**

#### **YuE Implementation**
- [ ] **Docker Setup**: Create Docker configuration for YuE full-song generation
  - Base image: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04`
  - Install Python 3.8, flash-attn, and dependencies
  - Auto-download models from Hugging Face
- [ ] **Web Interface**: Add YuE controls to React app
  - Genre selection (pop, rock, classical, etc.)
  - Structured lyrics input with [verse]/[chorus] tags
  - Voice style selection (male/female, emotional, energetic)
  - Multi-language support (English, Chinese, etc.)
- [ ] **API Integration**: Connect to YuE inference pipeline
  - Stage 1 model: `m-a-p/YuE-s1-7B-anneal-en-cot`
  - Stage 2 model: `m-a-p/YuE-s2-1B-general`
  - Support for 30s segments with concatenation

#### **ACE-Step Implementation**
- [ ] **Docker Containerization**: Manual Docker setup for ACE-Step
  - Python 3.10 environment with required dependencies
  - GUI interface integration via web proxy
- [ ] **Lyrics Editor**: Implement in-browser lyrics editing
  - Text2Music tab functionality
  - Support for custom lyrics with [verse] tags
  - Real-time preview and editing
- [ ] **Generation Controls**: Add ACE-Step parameters to UI
  - Vocal LoRA selection for different voice styles
  - Song length up to 4 minutes
  - Hardware optimization for 8GB VRAM

#### **DiffRhythm Implementation**
- [ ] **Native Docker Support**: Use existing docker-compose.yml
  - Container entry and script execution
  - Volume mounting for persistent storage
- [ ] **Lyrics File Support**: .lrc file upload/creation interface
  - Timestamp-based lyrics input
  - Style prompt integration
- [ ] **Fast Generation**: Implement DiffRhythm's quick inference
  - 4m45s maximum song length
  - Song continuation features

#### **Riffusion Integration**
- [ ] **Docker Deployment**: Set up Riffusion hobby version
  - Local inference server
  - API endpoint creation
- [ ] **Prompt-Based Vocals**: Embed lyrics in generation prompts
  - "Piano song with lyrics about [theme]"
  - Real-time clip generation
- [ ] **Remixing Interface**: Add riffusion controls for vocal remixing

### 🔄 **Audio Processing Pipeline**
- [ ] **FFmpeg Integration**: Add MP3 conversion to all containers
  - Dockerfile updates: `RUN apt-get install -y ffmpeg`
  - Automatic WAV to MP3 conversion
  - Quality settings and optimization
- [ ] **File Management**: Implement output handling
  - Volume mounting for file persistence
  - Automatic organization of vocal tracks
  - Download functionality for generated files

### 🎛️ **UI/UX Enhancements**
- [ ] **Lyrics Interface**: Create dedicated lyrics input section
  - AI generation button (Ollama integration)
  - Manual editing with syntax highlighting
  - Template system for song structures
- [ ] **Vocal Controls**: Add voice and style parameters
  - Gender selection, emotional range, language
  - Instrument accompaniment options
  - Preview generation for short clips
- [ ] **Progress Tracking**: Enhanced progress bars for vocal generation
  - Multi-stage progress (lyrics → music → conversion)
  - Real-time status updates

### 🔧 **Backend Integration**
- [ ] **API Endpoints**: Create RESTful APIs for all tools
  - Unified interface for different vocal tools
  - Status monitoring and error handling
  - File upload/download capabilities
- [ ] **Container Orchestration**: Rancher Desktop integration
  - Automatic container startup/shutdown
  - Resource allocation and GPU management
  - Network configuration for tool communication

### 🧪 **Testing & Validation**
- [ ] **Quality Testing**: Test vocal quality across different tools
  - Compare YuE vs ACE-Step vs DiffRhythm output
  - Hardware performance benchmarking
  - Prompt optimization and iteration
- [ ] **Integration Testing**: End-to-end lyrics-to-song pipeline
  - Ollama → Vocal Tool → FFmpeg conversion
  - Error handling and fallback mechanisms
  - User experience validation

### 📚 **Documentation Updates**
- [ ] **User Guide**: Update main README with vocal features
  - Setup instructions for each tool
  - Usage examples with lyrics
  - Troubleshooting vocal-specific issues
- [ ] **API Documentation**: Document new endpoints and parameters
- [ ] **Example Prompts**: Create vocal music prompt library

### 🎯 **Priority Implementation Order**
1. **Kokoro-TTS Integration** (Already available - quick win for spoken vocals)
2. **OpenRouter Lyrics Generation** (Leverage existing infrastructure)
3. **Lyrics-to-Speech Pipeline** (Combine kokoro-tts with MusicGPT instrumentals)
4. **Ollama Lyrics Generation** (Alternative local lyrics generation)
5. **ACE-Step Integration** (Beginner-friendly, good balance of features)
6. **FFmpeg Pipeline** (Essential for MP3 output)
7. **YuE Implementation** (Most advanced vocal quality)
8. **UI Polish** (Unified interface for all vocal tools)
9. **DiffRhythm & Riffusion** (Additional options and fast generation)

---

**🎼 Create your masterpiece with AI-powered music composition! 🎹✨**
