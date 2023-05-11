import os
from PIL import Image

# List all files in the directory
directory = 'data/icons/'
files = os.listdir(directory)

# Iterate over the files and perform operations
for file in files:
    fname = os.path.join(directory, file)
    # Open the image
    image = Image.open(fname)
    # Convert to RGB color mode
    image = image.convert("RGB")

    # Resize the image while maintaining aspect ratio
    width, height = image.size
    new_width = 16  # Specify the desired width
    new_height = new_width
    resized_image = image.resize((new_width, new_height))

    new_name = f"data/mini_icons/{fname.split('/')[-1].split('.')[0]}.png"
    print(new_name)
    # Save the resized image as a JPEG with compression
    resized_image.save(new_name, "JPEG", optimize=True, quality=1000)
