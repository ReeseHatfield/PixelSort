from PIL import Image
from tkinter.filedialog import askopenfilename

import os


def save_image(image: Image) -> None:
    out_file_name = 'sorted.png'  # change this later
    path = f'out/{out_file_name}'
    image.save(path)


def load_image() -> Image:
    file = askopenfilename(filetypes=[("Image files", ".jpg .jpeg .png")])
    if not file:
        return None
    
    path = os.path.abspath(file)
    image = Image.open(path)
    
    return image
