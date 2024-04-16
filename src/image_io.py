from PIL import Image

def save_image(image: Image) -> None:
    out_file_name = 'sorted.png' # change this later
    path = f'out/{out_file_name}'
    image.save(path)