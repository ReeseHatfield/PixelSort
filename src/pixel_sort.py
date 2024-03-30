from PIL import Image, ImageOps
import numpy as np

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
    
    im.save('out/sorted.png')
    

    
    # region = ImageOps.grayscale(region)
    
    # im.paste(region, box)
    
    # im.save('out/grayscale_box_example1.png')
    
    
    


if __name__ == "__main__":
    main()