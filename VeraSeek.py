import os
import subprocess
import argparse
import re
from rich.progress import Progress, BarColumn
import time
import datetime
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

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def main(directory):
    console = Console()
    Taggué_files = []
    High_entropy_files = []
    
    with Progress("[progress.description]{task.description}", BarColumn(), transient=True) as progress:
        task = progress.add_task("[cyan]🔍 Analyse des fichiers...", total=None)
        start_time = time.time()
        total_files = sum(len(files) for _, _, files in os.walk(directory))
        completed_files = 0
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
                    High_entropy_files.append(file_path)
                else:
                    entropy_mark = "Non taggué"
                if size_mark == "Taggué" and entropy_mark == "Taggué" and "Unknown" not in file_type:
                    Taggué_files.append(file_path)
                completed_files += 1
                progress.update(task, advance=1, description=f"⌛ ETA: {format_time((time.time() - start_time) * (total_files - completed_files) / completed_files)} - {completed_files}/{total_files} ({completed_files * 100 / total_files:.2f}%) 🦄🦄🦄🦄 ")
        progress.console.print("\n\n[cyan]✅ Analyse des fichiers [bold]finie !")
    
    console.print("\n[b] ➡️ Fichiers remplissant tous les critères :[/b]")
    for file in Taggué_files:
        console.print(f"[yellow]➔ {file}\n\n")

    console.print("\n[b] ➡️ Fichiers avec une entropie de 7.9999 ou plus :[/b]")
    for file in High_entropy_files:
        console.print(f"[yellow]➔ {file}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("--dossier", help="Chemin du dossier à analyser")
    args = parser.parse_args()
    if args.dossier:
        main(args.dossier)
    else:
        print("Veuillez spécifier le chemin du dossier avec l'option --dossier 'chemin'.")
