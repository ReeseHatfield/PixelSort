from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from typing import Tuple

from pixel_sort import pixel_sort
import os

# BoxType = Tuple[int, int, int, int]

# Global variables
abs_img_path: str = None
# (left, upper, right, lower)
box = (0, 0, 0, 0)
img: Image = None
canvas_image_id = None 

def get_path_from_dialog() -> str:
    file = askopenfilename(filetypes=[("Image files", ".jpg .jpeg .png")])
    if not file:
        return None
    full_path = os.path.abspath(file)
    return full_path

def sort_region():
    global img, canvas_image_id, canvas, box
    img = pixel_sort(img, box)
    
    print(f"Box from sort_region: {box}")
    # update the Tkinter display with the sorted image
    updated_img = ImageTk.PhotoImage(img)
    canvas.itemconfig(canvas_image_id, image=updated_img)
    
    # Keep a reference to avoid garbage collection
    canvas.image = updated_img

# def update_box():
#     global box, left, right, up, down, root
#     left_x = left.winfo_x()
#     right_x = right.winfo_x() + right.winfo_width()
#     up_y = up.winfo_y()
#     down_y = down.winfo_y() + down.winfo_height()
#     box = (int(left_x), int(up_y), int(right_x), int(down_y))
    
    
def create_gui(path: str):
    if not path:
        print("No image file selected.")
        return

    global abs_img_path, img, canvas_image_id, canvas, box
    global left, right, up, down  # Variables to hold line IDs
    abs_img_path = path
    root = Tk()

    btn = Button(root, text="Sort Region", command=sort_region)
    btn.pack(side="top", fill="x")

    img = Image.open(path)
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

    # Line thickness
    line_thickness = 5  # Set to 1 or adjust as needed for thinner lines

    # Creating draggable lines on the canvas
    left = canvas.create_line(100, 0, 100, img_height, width=line_thickness, fill="red")
    right = canvas.create_line(img_width - 100, 0, img_width - 100, img_height, width=line_thickness, fill="blue")
    up = canvas.create_line(0, 100, img_width, 100, width=line_thickness, fill="red")
    down = canvas.create_line(0, img_height - 100, img_width, img_height - 100, width=line_thickness, fill="blue")

    # Initial drag data
    drag_data = {"x": 0, "y": 0, "item": None}

    def drag_start(event):
        # Identify the closest item and start dragging
        drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def drag_motion(event):
        global box
        
        # Identify if the item is a horizontal or vertical line
        item_tags = canvas.gettags(drag_data["item"])
        if "horizontal" in item_tags:
            # For horizontal lines, only update the x-coordinate
            delta_y = event.y - drag_data["y"]
            canvas.move(drag_data["item"], 0, delta_y)
            drag_data["y"] = event.y
        elif "vertical" in item_tags:
            # For vertical lines, only update the y-coordinate
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
        coords_left = canvas.coords(left)
        coords_right = canvas.coords(right)
        coords_up = canvas.coords(up)
        coords_down = canvas.coords(down)
        box = (int(coords_left[0]), int(coords_up[1]), int(coords_right[0]), int(coords_down[1]))
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
    path: str = get_path_from_dialog()
    if path:
        img = Image.open(path)
        create_gui(path)
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
