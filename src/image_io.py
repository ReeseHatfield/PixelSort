from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfile

import os


def save_image(image: Image) -> bool:
    try:
        file = asksaveasfile(mode='w', defaultextension='png')
        if not file:
            print("No file to save")
            return False
            
        abs_path = os.path.abspath(file.name)
        image.save(abs_path) 
        return True
    except Exception as e:
        return False


def load_image() -> Image:
    
    file = askopenfilename(filetypes=[("Image files", ".jpg .jpeg .png")])
    if not file:
        return None
    
    path = os.path.abspath(file)
    image = Image.open(path)
    
    return image
