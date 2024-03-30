import os
import subprocess
import argparse
import re
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.console import Console

def calculate_entropy(file_path):
    command = ["ent", "-c", file_path]
    result = subprocess.run(command, capture_output=True)
    if result.returncode == 0:
        entropy = re.search(rb'Entropy\s*=\s*(\d+\.\d+)', result.stdout)
        if entropy:
            entropy_value = float(entropy.group(1).decode('utf-8'))
            return entropy_value
    return None

def identify_file_type(file_path):
    command = ["file", "--mime-type", file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return "Unknown"

def find_specific_files(directory):
    specific_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            file_type = identify_file_type(file_path)
            if (file_size < 3 * 1024 and file_type == "application/octet-stream") or (file_size < 2 * 1024 and os.path.splitext(filename)[1] == ""):
                specific_files.append(file_path)
    return specific_files

def main(directory):
    console = Console()
    Taggué_files = []
    file_count = sum(len(files) for _, _, files in os.walk(directory))

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Processing...", total=file_count)
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_size = os.path.getsize(file_path)
                if file_size % 512 == 0:
                    size_mark = "Taggué"
                else:
                    size_mark = "Non taggué"
                file_type = identify_file_type(file_path)
                entropy = calculate_entropy(file_path)
                if entropy is not None and entropy >= 7.9999:
                    entropy_mark = "Taggué"
                else:
                    entropy_mark = "Non taggué"
                if size_mark == "Taggué" and entropy_mark == "Taggué" and "Unknown" not in file_type:
                    Taggué_files.append(file_path)
                console.print(f"File: {file_path}, Size Mark: [green]{size_mark}[/green], File Type: [green]{file_type}[/green], Entropy: {entropy}, Entropy Mark: [green]{entropy_mark}[/green]")
                progress.update(task, advance=1)
    
    console.print("\nFichiers remplissant tous les critères :")
    for file in Taggué_files:
        console.print(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("--dossier", help="Chemin du dossier à analyser")
    args = parser.parse_args()
    if args.dossier:
        main(args.dossier)
    else:
        print("Veuillez spécifier le chemin du dossier avec l'option --dossier 'chemin'.")
