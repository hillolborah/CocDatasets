import os
import re

#Configs
DIR_PATH = r"/mnt/f/CocDatasets/Perception1/h/raw" #path to image directory
PREFIX = "h"          #"h", "d", "s"
EXTENSION = ".png"


def get_next_index(directory, prefix, extension):
    """
    Scans directory for files like h<number>.png
    Returns next available index
    """
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+){re.escape(extension)}$")
    max_index = 0

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            idx = int(match.group(1))
            max_index = max(max_index, idx)

    return max_index + 1


def rename_images(directory, prefix, extension):
    files = sorted(os.listdir(directory))
    next_index = get_next_index(directory, prefix, extension)

    print(f"Starting rename from {prefix}{next_index}{extension}")

    for filename in files:
        if not filename.lower().endswith(extension):
            continue

        if re.match(rf"^{re.escape(prefix)}\d+{re.escape(extension)}$", filename):
            continue

        old_path = os.path.join(directory, filename)
        new_name = f"{prefix}{next_index}{extension}"
        new_path = os.path.join(directory, new_name)

        print(f"{filename}  →  {new_name}")
        os.rename(old_path, new_path)

        next_index += 1


if __name__ == "__main__":
    if not os.path.isdir(DIR_PATH):
        raise ValueError(f"Invalid directory: {DIR_PATH}")

    rename_images(DIR_PATH, PREFIX, EXTENSION)
    print("Renaming complete.")
