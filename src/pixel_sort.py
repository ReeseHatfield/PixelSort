from PIL import Image, ImageOps
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
    
    pixel_arr = np.sort(pixel_arr, axis=1)
    
    region = Image.fromarray(pixel_arr)
    
    return region


def save_image(image: Image) -> None:
    out_file_name = 'sorted.png' # change this later
    path = f'out/{out_file_name}'
    image.save(path)


# if __name__ == "__main__":
#     main()