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

# ______________________Loading Process Code___________________________
def loading(progressbar, loading_screen):
    if progressbar['value'] == 0:
        start_button['state'] = 'disabled'
    if progressbar['value'] >= progressbar['maximum']:
        root.bell()
        start_button.config(text="Start", command=start_loading)  # Change button text and command
        start_button['state'] = 'normal'
        progressbar['value'] = 0
        winsound.PlaySound(None, winsound.SND_PURGE)
        main()
        loading_screen.destroy()
        return
    progressbar['value'] += 1
    root.after(20, loading, progressbar, loading_screen)
def main():
    root.withdraw()
    game_window = tk.Toplevel()
    game_window.geometry("1920x1080")
    game_window.title('Play Game')

    game_background_img_path = "img/background-game.jpg"  # Specify the path to the game background image
    background_image = Image.open(game_background_img_path)
    resized_image = background_image.resize((1400, 880))
    background_image_tk = ImageTk.PhotoImage(resized_image)
    canvas = tk.Canvas(game_window, width=1920, height=1080)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=background_image_tk)

    def go_back_to_main():
        game_window.destroy()
        root.deiconify()

    back_to_main_button = tk.Button(game_window, text='Back', width=8, font=('BLOODY TYPE PERSONAL USE', 15),
                                    command=go_back_to_main, bg='brown', fg="White", border=5)
    back_to_main_button.place(x=10, y=20)

#_________________img________________


    image1 = Image.open("img/WALL.jpg")
    image1 = image1.resize((300, 100))  # Adjust the size as needed
    image1_jpg = ImageTk.PhotoImage(image1)
    image2 = Image.open("img/WALL.jpg")
    image2 = image2.resize((300, 100))  # Adjust the size as needed
    image2_jpg = ImageTk.PhotoImage(image2)
    image3 = Image.open("img/WALL.jpg")
    image3 = image3.resize((300, 100))  # Adjust the size as needed
    image3_jpg = ImageTk.PhotoImage(image3)


    wall= canvas.create_image(500, 500, image=image1_jpg)
    wall= canvas.create_image(900, 200, image=image2_jpg)
    wall= canvas.create_image(1200, 550, image=image3_jpg)



    img_play_game_path = "img/play-game-image.jpg"  # Specify the path to the image for the game
    img_play_game = ImageTk.PhotoImage(file=img_play_game_path)
    canvas.create_image(500, 200, image=img_play_game)  # Adjust the coordinates as needed


#open the play game window
    game_window.mainloop()
    root.deiconify()

# _________________Play sound_______________________
def play_sound():
    sound_file_path = 'sound/dark-engine-logo-141942.wav'  # Specify the path to the sound file
    winsound.PlaySound(sound_file_path, winsound.SND_FILENAME + winsound.SND_LOOP)

sound_thread = threading.Thread(target=play_sound)
sound_thread.start()

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

# __________________Buttons___________________
help_button = tk.Button(root, text='Help', width=15, font=('BLOODY TYPE PERSONAL USE', 30), command=show_help, bg='#660000', fg="white", border=10)
help_button.place(x=320, y=420)

exit_button = tk.Button(root, text='Exit', width=15, font=('BLOODY TYPE PERSONAL USE', 30), command=exit_program, bg='#660000', fg="white", border=10)
exit_button.place(x=320, y=540)

start_button = tk.Button(root, text='Start', width=15, font=('BLOODY TYPE PERSONAL USE', 30), command=start_loading, bg='#660000', fg="white", border=10)
start_button.place(x=320, y=300)

root.mainloop()