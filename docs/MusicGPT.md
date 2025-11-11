# MusicGPT Setup and Usage

## Overview
[MusicGPT](https://github.com/gabotechs/MusicGPT) is a user-friendly wrapper around Meta's MusicGen model, ideal for generating piano and instrumental music from text prompts. It provides a web-based UI and supports both GPU and CPU execution.

## Prerequisites
- Docker Desktop or Rancher Desktop installed
- For GPU mode: NVIDIA drivers and CUDA toolkit
- For CPU mode: No additional requirements (slower performance)

## Installation
The wrapper scripts handle Docker image pulling automatically.

## Usage

### GPU Mode (Recommended)
Run `scripts/run_musicgpt.bat` to start MusicGPT with GPU acceleration.

### CPU Mode (Fallback)
Run `scripts/run_musicgpt_cpu.bat` for CPU-only execution.

### Web Interface
1. After starting the container, open http://localhost:8642 in your browser
2. Enter a text prompt like "melancholic piano solo in C major"
3. Click Generate to create music
4. Download the generated WAV file

## Prompt Examples
- "Classical piano sonata, slow and emotional"
- "Jazz piano improvisation, upbeat tempo"
- "Ambient piano with reverb, minimalist"

## Output
- Format: WAV audio files
- Duration: Configurable (default ~10-30 seconds)
- Location: Stored in container volume, accessible via mounted directory

## Troubleshooting
- **GPU not detected**: Use CPU mode script
- **Port conflict**: Change port mapping in script if 8642 is in use
- **Slow generation**: Reduce model size or use CPU mode

## Technical Details
- Docker Image: gabotechs/musicgpt
- Port: 8642
- Volume Mount: %USERPROFILE%\.musicgpt for model persistence
- GPU Flags: --gpus all for GPU mode
