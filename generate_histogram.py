#!/usr/bin/env python3
import sys
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pillow_heif import register_heif_opener

# Register HEIF opener to handle HEIC files
register_heif_opener()

def generate_histogram(image_path):
    """Generate a histogram for the given image and save it to the histograms folder."""

    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} does not exist")
        sys.exit(1)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Create histograms directory if it doesn't exist
    os.makedirs("histograms", exist_ok=True)

    output_path = os.path.join("histograms", f"{base_name}_histogram.png")

    # Load the image
    print(f"Loading image: {image_path}")
    img = Image.open(image_path)

    # Convert to RGB if necessary (handles HEIC and other formats)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Convert to numpy array
    img_array = np.array(img)

    # Create histogram
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Plot histogram for each color channel
    colors = ['red', 'green', 'blue']
    for i, color in enumerate(colors):
        histogram, bin_edges = np.histogram(img_array[:, :, i], bins=256, range=(0, 256))
        ax.plot(bin_edges[0:-1], histogram, color=color, label=color.upper(), alpha=0.7)

    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Color Histogram - {base_name}')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Save the histogram
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Histogram saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_histogram.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    generate_histogram(image_path)
