import os
import subprocess
import argparse
import re

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
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            file_type = identify_file_type(file_path)
            if (file_size < 3 * 1024 and file_type == "application/octet-stream") or (file_size < 2 * 1024 and os.path.splitext(filename)[1] == ""):
                specific_files.append(filename)
    return specific_files

def main(directory):
    marked_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            if file_size % 512 == 0:
                size_mark = "Marked"
            else:
                size_mark = "Not Marked"
            file_type = identify_file_type(file_path)
            entropy = calculate_entropy(file_path)
            if entropy is not None and entropy >= 7.9999:
                entropy_mark = "Marked"
            else:
                entropy_mark = "Not Marked"
            if size_mark == "Marked" and entropy_mark == "Marked" and "Unknown" not in file_type:
                marked_files.append(filename)
            print(f"File: {filename}, Size Mark: {size_mark}, File Type: {file_type}, Entropy: {entropy}, Entropy Mark: {entropy_mark}")
    print("\nFiles Meeting all Criteria:")
    for file in marked_files:
        print(file)
    print("\nSpecific Files (Size < 3ko and Type: application/octet-stream or Size < 2ko and no extension):")
    specific_files = find_specific_files(directory)
    for file in specific_files:
        print(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("--dossier", help="Chemin du dossier à analyser")
    args = parser.parse_args()
    if args.dossier:
        main(args.dossier)
    else:
        print("Veuillez spécifier le chemin du dossier avec l'option --dossier.")
