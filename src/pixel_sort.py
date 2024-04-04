from PIL import Image, ImageOps
from typing import Tuple
import numpy as np

BoxType = Tuple[int, int, int, int]

def main():
    
    box = (100,100,400,400)
    image: Image = pixel_sort("examples/ex1.png", box)
    
    save_image(image)
    
    
    

def pixel_sort(path: str, box: BoxType) -> Image:
    im = Image.open(path)
    print(im.format, im.size, im.mode)
    
    region = im.crop(box)
    
    region = _sort_region(region)
    
    im.paste(region, box)
    
    return im


def _sort_region(region: Image):
    
    pixel_arr = np.asarray(region)
    
    
    pixel_arr = np.sort(pixel_arr, axis=1)
    
    region = Image.fromarray(pixel_arr)
    
    return region


def save_image(image: Image) -> None:
    out_file_name = 'sorted.png' # change this later
    path = f'out/{out_file_name}'
    image.save(path)


if __name__ == "__main__":
    main()