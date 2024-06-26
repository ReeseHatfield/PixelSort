from tkinter import *

from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from typing import Tuple
from image_io import load_image, save_image

from pixel_sort import pixel_sort
from alerts import show_failure, show_success

BoxType = Tuple[int, int, int, int]

# Global variables
# (left, upper, right, lower)
box: BoxType = (0, 0, 0, 0)
img: Image = None
canvas_image_id = None 

def handle_sort():
    global img, canvas_image_id, canvas, box
    img = pixel_sort(img, box)

    # update the Tkinter display with the sorted image
    updated_img = ImageTk.PhotoImage(img)
    canvas.itemconfig(canvas_image_id, image=updated_img)
    
    canvas.image = updated_img
    
def handle_save():
    save_successful: bool = save_image(img)
    if not save_successful:
        show_failure()
        return
    
    show_success()
    
def create_gui():
    if not img:
        print("No image file selected.")
        return

    global canvas_image_id, canvas
    root = Tk()

    sort_btn = Button(root, text="Sort Region", command=handle_sort)
    sort_btn.pack(side="top", fill="x")
    
    save_btn = Button(root, text="Save Image", command=handle_save)
    save_btn.pack(side="bottom", fill="x")
    
    


    img_width, img_height = img.size

    min_size = 500
    img_width = max(img_width, min_size)
    img_height = max(img_height, min_size)

    root.geometry(f"{img_width}x{img_height + 100}")  

    canvas = Canvas(root, width=img_width, height=img_height)
    canvas.pack(side="top", fill="both", expand="yes")

    background = ImageTk.PhotoImage(img)
    canvas_image_id = canvas.create_image(0, 0, anchor="nw", image=background)
    canvas.image = background

    
    line_thickness = 5 

    
    global left, right, up, down 
    left = canvas.create_line(100, 0, 100, img_height, width=line_thickness, fill="black")
    right = canvas.create_line(img_width - 100, 0, img_width - 100, img_height, width=line_thickness, fill="black")
    up = canvas.create_line(0, 100, img_width, 100, width=line_thickness, fill="black")
    down = canvas.create_line(0, img_height - 100, img_width, img_height - 100, width=line_thickness, fill="black")

    
    drag_data = {
        "x": 0, 
        "y": 0, 
        "item": None
    }

    def drag_start(event):
        # find the closest item and start dragging
        drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def drag_motion(event):
        global box
        
        item_tags = canvas.gettags(drag_data["item"])
        if "horizontal" in item_tags:
            # horizontal lines -> only update the x-coordinate
            delta_y = event.y - drag_data["y"]
            canvas.move(drag_data["item"], 0, delta_y)
            drag_data["y"] = event.y
        elif "vertical" in item_tags:
            # vertical lines -> only update the y-coordinate
            delta_x = event.x - drag_data["x"]
            canvas.move(drag_data["item"], delta_x, 0)
            drag_data["x"] = event.x
        
        # Update the bounding box after movement
        update_box()

    # Add tags to identify lines as either horizontal or vertical
    canvas.itemconfig(left, tags=("vertical",))
    canvas.itemconfig(right, tags=("vertical",))
    canvas.itemconfig(up, tags=("horizontal",))
    canvas.itemconfig(down, tags=("horizontal",))


    def update_box():
        global box
        
        # hacky way to make a dict
        elements = ['left', 'right', 'up', 'down']
        coords = {e: canvas.coords(eval(e)) for e in elements}
        
        
        left_coord = min(coords['left'][0], coords['right'][0])
        right_coord = max(coords['left'][0], coords['right'][0])
        up_coord = min(coords['up'][1], coords['down'][1])
        down_coord = max(coords['up'][1], coords['down'][1])
        
        box = (int(left_coord), int(up_coord), int(right_coord), int(down_coord))
        print(f"Updated box: {box}")


    canvas.tag_bind(left, "<ButtonPress-1>", drag_start)
    canvas.tag_bind(right, "<ButtonPress-1>", drag_start)
    canvas.tag_bind(up, "<ButtonPress-1>", drag_start)
    canvas.tag_bind(down, "<ButtonPress-1>", drag_start)

    canvas.tag_bind(left, "<B1-Motion>", drag_motion)
    canvas.tag_bind(right, "<B1-Motion>", drag_motion)
    canvas.tag_bind(up, "<B1-Motion>", drag_motion)
    canvas.tag_bind(down, "<B1-Motion>", drag_motion)

    root.mainloop()


def main():
    global img
    img = load_image()
    if not img:
        print("Operation cancelled.")
    create_gui()

if __name__ == "__main__":
    main()
