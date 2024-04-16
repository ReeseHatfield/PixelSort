from tkinter import messagebox


def show_success():
    
    title = "Success"
    message = "File Saved Successfully"
    messagebox.showinfo(title=title, message=message)
    
def show_failure():
    title = "Error"
    message = "File could not be saved"
    messagebox.showerror(title=title, message=message)

