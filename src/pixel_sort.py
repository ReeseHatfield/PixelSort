from PIL import Image
from typing import Tuple
import numpy as np

BoxType = Tuple[int, int, int, int]


def pixel_sort(im: Image, box: BoxType) -> Image:

    print(f"Box is {box}")
    
    region = im.crop(box)
    
    region = _sort_region(region)
    
    im.paste(region, box)
    
    return im


def _sort_region(region: Image):
    
    pixel_arr = np.asarray(region) 
    
    pixel_arr = np.sort(pixel_arr, axis=0)
    
    region = Image.fromarray(pixel_arr)
    
    return region
