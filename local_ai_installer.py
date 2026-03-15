import ctypes
import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
import webbrowser
from pathlib import Path

APP_NAME = "Local AI Installer"
APP_CREDITS = "Build by AKBBProjects"
CONFIG_DIR = Path.home() / ".local_ai_installer"
CONFIG_FILE = CONFIG_DIR / "config.json"

MODEL_CATALOG = {
    "Chat / General": [
        ("llama3.2:1b", "Very light chat model for low-end PCs"),
        ("llama3.2:3b", "Balanced everyday chat model"),
        ("mistral", "Fast, strong general chat model"),
        ("gemma2:2b", "Small Google model for light systems"),
        ("gemma2:9b", "Better quality, needs more RAM"),
        ("qwen2.5:3b", "Good multilingual chat model"),
        ("qwen2.5:7b", "Stronger general assistant model"),
        ("phi3:mini", "Tiny fast Microsoft model"),
        ("tinyllama", "Ultra-light model for weak PCs"),
    ],
    "Coding": [
        ("qwen2.5-coder:1.5b", "Small coding model"),
        ("qwen2.5-coder:7b", "Strong local coding model"),
        ("codellama:7b", "Code generation and explanation"),
        ("deepseek-coder:1.3b", "Light coding model"),
        ("deepseek-coder:6.7b", "Better coding quality"),
        ("starcoder2:3b", "Fast code assistant"),
    ],
    "Vision": [
        ("llava", "Chat with images"),
        ("llava:7b", "Common vision model variant"),
        ("llava:13b", "Higher quality, needs more RAM"),
        ("moondream", "Very small image understanding model"),
        ("minicpm-v", "Compact multimodal model"),
    ],
    "Reasoning / Bigger": [
        ("deepseek-r1:1.5b", "Small reasoning model"),
        ("deepseek-r1:7b", "Strong reasoning model"),
        ("qwen2.5:14b", "Large assistant model"),
        ("llama3.1:8b", "Large general-purpose model"),
    ],
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")



def pause(message="\nPress Enter to continue..."):
    input(message)



def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_config({"default_chat_model": "llama3.2:3b"})



def load_config():
    ensure_config()
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"default_chat_model": "llama3.2:3b"}



def save_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")



def header(title=None):
    clear_screen()
    print("=" * 56)
    print(f"{APP_NAME:^56}")
    print(f"{APP_CREDITS:^56}")
    print("=" * 56)
    if title:
        print(title)
        print("-" * 56)



def run_command(command, shell=False, capture=False):
    try:
        if capture:
            result = subprocess.run(
                command,
                shell=shell,
                text=True,
                capture_output=True,
                check=False,
            )
            return result.returncode, (result.stdout or "") + (result.stderr or "")
        result = subprocess.run(command, shell=shell, check=False)
        return result.returncode, ""
    except FileNotFoundError:
        return 127, "Command not found"
    except Exception as exc:
        return 1, str(exc)



def which_ollama():
    return shutil.which("ollama")



def is_windows_admin():
    if os.name != "nt":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False



def get_total_ram_gb():
    try:
        if os.name == "nt":
            output = subprocess.check_output(
                ["wmic", "computersystem", "get", "TotalPhysicalMemory"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            lines = [line.strip() for line in output.splitlines() if line.strip().isdigit()]
            if lines:
                return round(int(lines[0]) / (1024 ** 3), 1)
    except Exception:
        pass

    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return round(pages * page_size / (1024 ** 3), 1)
    except Exception:
        return None



def get_disk_free_gb(path="."):
    try:
        return round(shutil.disk_usage(path).free / (1024 ** 3), 1)
    except Exception:
        return None



def detect_gpu_name():
    candidates = []
    if os.name == "nt":
        commands = [
            ["wmic", "path", "win32_VideoController", "get", "name"],
            ["powershell", "-Command", "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"],
        ]
        for cmd in commands:
            try:
                output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
                for line in output.splitlines():
                    name = line.strip()
                    if name and "Name" not in name:
                        candidates.append(name)
                if candidates:
                    break
            except Exception:
                continue
    return ", ".join(dict.fromkeys(candidates)) if candidates else "Not detected"



def recommendation_from_ram(ram_gb):
    if ram_gb is None:
        return "Could not detect RAM. Start with tinyllama or phi3:mini."
    if ram_gb < 4:
        return "Use very small models: tinyllama, phi3:mini, llama3.2:1b"
    if ram_gb < 8:
        return "Use small models: llama3.2:1b, gemma2:2b, qwen2.5-coder:1.5b"
    if ram_gb < 16:
        return "Use medium models: llama3.2:3b, mistral, qwen2.5:7b"
    return "You can try bigger models: gemma2:9b, llava:13b, qwen2.5:14b"



def show_system_check():
    header("System Check")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"CPU: {platform.processor() or 'Not detected'}")
    print(f"Admin Mode: {'Yes' if is_windows_admin() else 'No'}")
    ram = get_total_ram_gb()
    disk = get_disk_free_gb()
    print(f"RAM: {ram if ram is not None else 'Unknown'} GB")
    print(f"Free Disk: {disk if disk is not None else 'Unknown'} GB")
    print(f"GPU: {detect_gpu_name()}")
    print(f"Ollama Installed: {'Yes' if which_ollama() else 'No'}")
    print("\nRecommendation:")
    print(f"- {recommendation_from_ram(ram)}")
    pause()



def open_ollama_download():
    header("Install Ollama")
    print("Opening Ollama download page in your browser...")
    webbrowser.open("https://ollama.com/download")
    print("\nAfter installing Ollama, re-open this tool and choose model install.")
    pause()



def install_ollama_winget():
    header("Install Ollama with winget")
    if os.name != "nt":
        print("This quick installer is made for Windows.")
        pause()
        return
    if shutil.which("winget") is None:
        print("winget not found. Opening Ollama download page instead.")
        webbrowser.open("https://ollama.com/download")
        pause()
        return
    print("Trying to install Ollama using winget...\n")
    code, _ = run_command([
        "winget", "install", "-e", "--id", "Ollama.Ollama",
        "--accept-package-agreements", "--accept-source-agreements"
    ])
    if code == 0:
        print("\nOllama install command completed.")
    else:
        print("\nInstall command failed. Opening browser download page.")
        webbrowser.open("https://ollama.com/download")
    pause()



def ensure_ollama_ready():
    if which_ollama() is None:
        print("Ollama is not installed yet.")
        return False
    return True



def flatten_models():
    for category, items in MODEL_CATALOG.items():
        for model_name, description in items:
            yield category, model_name, description



def choose_model(prompt_text="Select a model number: "):
    header("Model Catalog")
    index = 1
    lookup = {}
    for category, items in MODEL_CATALOG.items():
        print(f"\n[{category}]")
        for model_name, description in items:
            print(f" {index:>2}. {model_name:<22} - {description}")
            lookup[str(index)] = model_name
            index += 1
    print("\n 0. Cancel")
    choice = input(f"\n{prompt_text}").strip()
    if choice == "0":
        return None
    return lookup.get(choice)



def install_model():
    header("Install Model")
    if not ensure_ollama_ready():
        pause()
        return
    model_name = choose_model()
    if not model_name:
        return
    header(f"Installing {model_name}")
    print("This may take time depending on your internet speed and model size.\n")
    run_command(["ollama", "pull", model_name])
    pause()



def quick_packs_menu():
    packs = {
        "1": ("Low-End Pack", ["tinyllama", "phi3:mini", "llama3.2:1b"]),
        "2": ("Everyday Chat Pack", ["llama3.2:3b", "mistral", "gemma2:2b"]),
        "3": ("Coding Pack", ["qwen2.5-coder:1.5b", "codellama:7b"]),
        "4": ("Vision Pack", ["moondream", "llava"]),
    }
    header("Quick Model Packs")
    for key, (name, models) in packs.items():
        print(f"{key}. {name} -> {', '.join(models)}")
    print("0. Cancel")
    choice = input("\nSelect pack: ").strip()
    if choice == "0" or choice not in packs:
        return
    if not ensure_ollama_ready():
        pause()
        return
    pack_name, models = packs[choice]
    header(f"Installing {pack_name}")
    for model in models:
        print(f"\n>>> Pulling {model}")
        run_command(["ollama", "pull", model])
    pause("\nPack install complete. Press Enter to continue...")



def list_installed_models(return_only=False):
    if not ensure_ollama_ready():
        return [] if return_only else None
    code, output = run_command(["ollama", "list"], capture=True)
    if code != 0:
        if not return_only:
            header("Installed Models")
            print(output or "Could not read installed models.")
            pause()
        return []
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]
    if return_only:
        models = []
        for line in lines[1:]:
            name = line.split()[0] if line.split() else ""
            if name:
                models.append(name)
        return models
    header("Installed Models")
    print(output if output.strip() else "No models found.")
    pause()



def remove_model():
    header("Remove Model")
    if not ensure_ollama_ready():
        pause()
        return
    models = list_installed_models(return_only=True)
    if not models:
        print("No installed models found.")
        pause()
        return
    for i, model in enumerate(models, start=1):
        print(f"{i}. {model}")
    print("0. Cancel")
    choice = input("\nSelect model to remove: ").strip()
    if choice == "0":
        return
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(models):
        print("Invalid choice.")
        pause()
        return
    target = models[int(choice) - 1]
    header(f"Removing {target}")
    run_command(["ollama", "rm", target])
    pause()



def set_default_model():
    config = load_config()
    model_name = choose_model("Choose default chat model number: ")
    if not model_name:
        return
    config["default_chat_model"] = model_name
    save_config(config)
    header("Default Model Saved")
    print(f"Default chat model set to: {model_name}")
    pause()



def start_chat():
    header("Start AI Chat")
    if not ensure_ollama_ready():
        pause()
        return
    config = load_config()
    default_model = config.get("default_chat_model", "llama3.2:3b")
    print(f"Current default model: {default_model}")
    print("1. Use default model")
    print("2. Choose installed model")
    print("0. Cancel")
    choice = input("\nSelect option: ").strip()
    if choice == "0":
        return
    model_name = default_model
    if choice == "2":
        models = list_installed_models(return_only=True)
        if not models:
            print("No installed models found.")
            pause()
            return
        header("Choose Installed Model")
        for i, model in enumerate(models, start=1):
            print(f"{i}. {model}")
        pick = input("\nModel number: ").strip()
        if not pick.isdigit() or int(pick) < 1 or int(pick) > len(models):
            print("Invalid choice.")
            pause()
            return
        model_name = models[int(pick) - 1]
    header(f"Running chat with {model_name}")
    print("Type /bye inside Ollama chat to exit back to this app.\n")
    subprocess.run(["ollama", "run", model_name], check=False)
    pause()



def save_project_info():
    header("Project Info")
    text = f"""
    App data folder:
      {CONFIG_DIR}

    Default model config file:
      {CONFIG_FILE}

    Tips:
    - Install Ollama first.
    - Start with a small model if your PC has less than 8 GB RAM.
    - Vision models need more storage.
    - ChatGPT / Claude themselves are not local models; this installer is for free local models.
    """
    print(textwrap.dedent(text).strip())
    pause()



def main_menu():
    ensure_config()
    while True:
        config = load_config()
        header()
        print(f"Default Chat Model: {config.get('default_chat_model', 'llama3.2:3b')}")
        print("\n1. System Check")
        print("2. Install Ollama (Browser)")
        print("3. Install Ollama (winget)")
        print("4. Install Single Model")
        print("5. Install Quick Model Pack")
        print("6. Start AI Chat")
        print("7. Show Installed Models")
        print("8. Remove Model")
        print("9. Set Default Chat Model")
        print("10. Project Info")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()
        if choice == "1":
            show_system_check()
        elif choice == "2":
            open_ollama_download()
        elif choice == "3":
            install_ollama_winget()
        elif choice == "4":
            install_model()
        elif choice == "5":
            quick_packs_menu()
        elif choice == "6":
            start_chat()
        elif choice == "7":
            list_installed_models()
        elif choice == "8":
            remove_model()
        elif choice == "9":
            set_default_model()
        elif choice == "10":
            save_project_info()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
            pause()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
