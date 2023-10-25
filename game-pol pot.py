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