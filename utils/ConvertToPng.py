import os
from PIL import Image
import glob

def convert_folder_to_png(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Define a set of common image extensions (Pillow supports many more)
    valid_extensions = ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.tiff', '*.webp')

    files_found = 0
    files_converted = 0

    for ext in valid_extensions:
        # Use glob to find all files matching the extension in the input directory
        for filepath in glob.glob(os.path.join(input_dir, ext)):
            files_found += 1
            try:
                # Open the image using Pillow
                with Image.open(filepath) as img:
                    # Get the base filename without extension
                    filename = os.path.splitext(os.path.basename(filepath))[0]
                    # Define the new file path with .png extension in the output directory
                    output_path = os.path.join(output_dir, f"{filename}.png")

                    # If the image is in RGBA mode (has transparency), it is already suitable for PNG.
                    # If it is in a different mode (e.g., RGB, CMYK), convert it to RGBA to preserve/handle transparency for the PNG format.
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')

                    # Save the image in PNG format
                    img.save(output_path, format="PNG")
                    files_converted += 1
                    print(f"Converted: {filepath} -> {output_path}")

            except OSError:
                print(f"Error: Cannot convert {filepath}. Skipping.")
    
    print(f"\nConversion complete. Found {files_found} files, successfully converted {files_converted}.")

# Specify your input and output folder names (relative to the script location)
INPUT_FOLDER = 'input_images'
OUTPUT_FOLDER = 'output_images_png'

convert_folder_to_png(INPUT_FOLDER, OUTPUT_FOLDER)
#Note: after conversion, verify and delete duplicates 