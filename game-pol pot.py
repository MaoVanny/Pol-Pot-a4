from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import winsound
import threading
import sys

root = tk.Tk()

# ___________________Main screen____________________

root.geometry("1920x1080")
frame = tk.Frame(root, width=1920, height=1080)
frame.pack()
canvas = tk.Canvas(frame, width=1920, height=1080)
canvas.pack()

# Load an image in the script
main_screen_img_path = "img/main-screen.png"  # Specify the path to the main screen image
img = Image.open(main_screen_img_path)
resized_image = img.resize((1450, 720))
imageTk_1 = ImageTk.PhotoImage(resized_image)
canvas.create_image(0, 0, anchor="nw", image=imageTk_1)

# _________________Loading screen_____________
def start_loading():
    loading_screen = tk.Toplevel(root)
    loading_screen.geometry("1920x1080")
    loading_screen.title("Loading Screen")
    frame = tk.Frame(loading_screen, width=1920, height=1080)
    frame.pack()
    canvas = tk.Canvas(frame, width=1920, height=1080)
    canvas.pack()

    # Specify the path to the loading screen image
    loading_screen_img_path = "img/loadingscreen.png"  
    img1 = Image.open(loading_screen_img_path)
    resized_image1 = img1.resize((1370, 850))
    imageTk = ImageTk.PhotoImage(resized_image1)
    canvas.create_image(0, 0, anchor="nw", image=imageTk)

    progressbar = ttk.Progressbar(loading_screen, orient="horizontal", length=300, mode="determinate")
    progressbar.place(x=500, y=550)
    loading(progressbar, loading_screen)
    imageTk()


# _________________Button functions____________
def show_help():
    root.withdraw()
    help_window = Toplevel(root)
    help_window.title("Help")
    help_window.geometry("1920x1080")

    help_background_img_path = "img/help-background.jpg"  # Specify the path to the help window background image
    background_image = Image.open(help_background_img_path)
    width = 1400
    height = 750
    background_image = background_image.resize((width, height))
    background_image = ImageTk.PhotoImage(background_image)

    canvas = Canvas(help_window, width=width, height=height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=background_image)

    def close_help():
        help_window.destroy()
        root.deiconify()

    # Button Back in player screen
    back_button= tk.Button(help_window, text='Back', width=8, font=('BLOODY TYPE PERSONAL USE', 30), command=close_help, bg='#660000',fg="white",border=10)
    back_button.place(x=30, y=30)
    back_button.lift()
    help_window.focus_set()
    help_window.mainloop()

def exit_program():
    sys.exit()
