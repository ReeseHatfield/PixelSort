from PIL import Image, ImageOps
import numpy as np
from out import save_image

def main():
    im = Image.open("examples/ex1.png")
    print(im.format, im.size, im.mode)

    box = (100,100,400,400)
    region = im.crop(box)
    
    pixel_arr = np.asarray(region)
    
    print(pixel_arr)
    
    pixel_arr = np.sort(pixel_arr, axis=1)
    
    region = Image.fromarray(pixel_arr)
    
    im.paste(region, box)
    
    save_image(im)
    
    
    
    


if __name__ == "__main__":
    main()