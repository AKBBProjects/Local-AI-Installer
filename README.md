# Local AI Installer
Build by AKBBProjects

A simple CMD-based Windows tool to help install and manage **free local AI models** using **Ollama**.

## What it does
- Checks your PC for RAM, CPU, GPU, and free disk
- Opens Ollama download page
- Can try `winget` install for Ollama on Windows
- Installs one local model at a time
- Installs quick packs for low-end chat, coding, and vision use
- Lets you list and remove installed models
- Starts local AI chat from CMD
- Saves your default chat model

## Important note
This software is for **local open models**. It does **not** install the real ChatGPT or Claude apps/models offline.

## Supported example models
### Chat
- `llama3.2:1b`
- `llama3.2:3b`
- `mistral`
- `gemma2:2b`
- `gemma2:9b`
- `qwen2.5:3b`
- `qwen2.5:7b`
- `phi3:mini`
- `tinyllama`

### Coding
- `qwen2.5-coder:1.5b`
- `qwen2.5-coder:7b`
- `codellama:7b`
- `deepseek-coder:1.3b`
- `deepseek-coder:6.7b`
- `starcoder2:3b`

### Vision
- `llava`
- `llava:7b`
- `llava:13b`
- `moondream`
- `minicpm-v`

### Reasoning / Bigger
- `deepseek-r1:1.5b`
- `deepseek-r1:7b`
- `qwen2.5:14b`
- `llama3.1:8b`

## How to run
### Method 1
Double click:
- `run_local_ai_installer.bat`

### Method 2
Open CMD in the project folder and run:

```bash
python local_ai_installer.py
```

## Before you install models
1. Install **Ollama** first
2. Restart CMD after installing Ollama if commands are not found
3. Start with a small model if your PC is weak

## Build EXE
Run:

```bash
build_exe.bat
```

After build, your EXE will be in:

```text
dist\Local AI Installer.exe
```

## Recommended model sizes
- **4 GB RAM or lower**: `tinyllama`, `phi3:mini`, `llama3.2:1b`
- **8 GB RAM**: `llama3.2:3b`, `gemma2:2b`, `qwen2.5-coder:1.5b`
- **16 GB+ RAM**: `mistral`, `qwen2.5:7b`, `llava`, `gemma2:9b`

## Notes
- Some model names can change in Ollama over time.
- Internet is needed only to download Ollama and pull models.
- After download, models can run locally/offline.
