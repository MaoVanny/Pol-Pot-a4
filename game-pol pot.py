from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
import winsound
import threading
import sys

root = tk.Tk()

# Variable
SPEED = 7
TIME = 10
GRAVITY_FORCE = 9
bullet_color = "red"
# Set up a list to store player bullets
scroll_offset = 0
jump_count = 0
action = 0
score = 0
SHOOTING_DISTANCE = 300
enemy_ation = 10
direction = 1
player_bullets = []
keyPressed = []
obstacles = []
pol_pots = []
target = None
is_jumping = False
# Create the bullet
bullet = None

max_blood = 3
current_lives = max_blood
max_lives = 3
life = max_lives


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
        main(loading_screen)
        return
    progressbar['value'] += 1
    root.after(20, loading, progressbar, loading_screen)



def main(loading_screen):
    WIN_WIDTH = 1920
    WIN_HEIGHT = 1080
    root.withdraw()
    loading_screen.withdraw()
    game_window = tk.Toplevel()
    game_window.geometry(root.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT)))
    game_window.title('Play Game')
    
    canvas.pack()
    background  = tk.PhotoImage(file="img/loadingscreen.png")
    background_img1 = canvas.create_image(0, 0, image=background)
    background_img2 = canvas.create_image(WIN_WIDTH, 0, image=background)
   
    #__________game__________________
    # Images player and land
    image1 = tk.PhotoImage(file="img/Characters/player/Run/0.png")
    player = canvas.create_image(100, 100, image=image1)
    land = canvas.create_rectangle(0, 500, 1536, 800, fill="Brown", tags="wall")

  

    # Main of function
    def game():
        canvas.pack()
        canvas.bind_all("<KeyPress>",handle_key_press)
        canvas.bind_all("<KeyRelease>",handle_key_release)
        canvas.bind_all("<space>",shoot)
        canvas.focus_set()
        create_obstacles()
        enemies()
        
    # Create wall of game
    def create_obstacles():
        walls = [
            canvas.create_rectangle(230, 240, 400, 280, fill="white", tags="wall"),
            canvas.create_rectangle(480, 100, 650, 130, fill="white", tags="wall"),
            canvas.create_rectangle(780, 200, 950, 230, fill="white", tags="wall"),
            canvas.create_rectangle(450, 300, 650, 330, fill="Red", tags="wall"),
            canvas.create_rectangle(850, 360, 900, 390, fill="Red", tags="wall"),
            canvas.create_rectangle(480, 400, 950, 430, fill="white", tags="wall"),
            canvas.create_rectangle(1050, 380, 1150, 410, fill="white", tags="wall"),
            canvas.create_rectangle(240, 480, 330, 510, fill="white", tags="wall")
            ]
        for obstacle in walls:
            obstacles.append(obstacle)


    #create all enemies
    imageTk_1 = tk.PhotoImage(file="img/Reverse characters/enemy/Run/0.png")
    enemys = [
            canvas.create_image(500,200, image= imageTk_1, anchor="center",tags ="enemy"),
            canvas.create_image(500,240, image= imageTk_1, anchor="center",tags ="enemy"),
            canvas.create_image(500,280, image= imageTk_1, anchor="center",tags ="enemy"),
            canvas.create_image(500,340, image= imageTk_1, anchor="center",tags ="enemy"),
            canvas.create_image(500,380, image= imageTk_1, anchor="center",tags ="enemy"),
            canvas.create_image(500,420, image= imageTk_1, anchor="center",tags ="enemy")
        ]
    for enemy in enemys:
            pol_pots.append(enemy)
            
    # Call action of animies
    def enemies():
        for pol_pot in pol_pots:
            create_bullet(pol_pot)
            move_enemy(pol_pot)
            
    #Create enimies bullet
    def create_bullet(pol_pot):
        global bullet, update_id
        hx1, hy1 = canvas.coords(pol_pot)
        px1, py1  = canvas.coords(player)
        if hx1 - px1 <= SHOOTING_DISTANCE and bullet is None:
            # Enemy is within shooting distance and bullet is not present, shoot
            bullet = canvas.create_rectangle(hx1, (hy1) + 5 , hx1 - 10, (hy1) + 10, fill="orange")
        # Move the bullet
        if bullet is not None:
            canvas.move(bullet, -2, 0)
            bx1, by1, bx2, by2 = canvas.coords(bullet)
            overlap = canvas.find_overlapping(bx1,by1,bx2,by2)
            # Check for bullet-player collision
            if bx2 < 0 :
                # Bullet reached the end, remove it
                canvas.delete(bullet)
                bullet = None
            if player in overlap:
                # Bullet collided with the player, end the game
                got_hit()
                canvas.delete(bullet)
                bullet = None
            
        # window.after_cancel(update_id)
        update_id = game_window.after(20,create_bullet, pol_pot)

    # enimies ation
    def move_enemy(pol_pot):
        global enemy_ation, direction
        canvas.move(pol_pot, direction, 0)
        enemy_ation += direction
        if enemy_ation >= 120:
            direction = -1
        elif enemy_ation <= 10:
            direction = 1
        canvas.after(100, move_enemy,pol_pot)

    # study of key that has enter by player
    def handle_key_press(event):
        global is_jumping, jump_count
        if event.keysym == "Left" and "Left" not in keyPressed:
            keyPressed.append("Left")
        elif event.keysym == "Right" and "Right" not in keyPressed:
            keyPressed.append("Right")
        elif event.keysym == "Up" and not is_jumping:
            is_jumping = True
            jump_count = 20
        
        # function for release key of player
    def handle_key_release(event):
        if event.keysym == "Left" and "Left" in keyPressed:
            keyPressed.remove("Left")
        elif event.keysym == "Right" and "Right" in keyPressed:
            keyPressed.remove("Right")
        
    # function for shooing of charcter
    def shoot(event):
        x1, y1 = canvas.coords(player)
        bullet = canvas.create_rectangle(x1 + 30, y1 - 5 , x1 + 40, y1 - 10, fill=bullet_color)
        player_bullets.append(bullet)

    # function for move character
    def move_player():
        global action
        global is_jumping, jump_count
        x, y = 0, 0
        if "Left" in keyPressed:
            x = -10
            action = 0
            canvas.move(background_img1, +2, 0)
            canvas.move(background_img2, +2, 0)
        elif "Right" in keyPressed:
            action += 10
            x = 10
            canvas.move(background_img1, -2, 0)
            canvas.move(background_img2, -2, 0)
            walk_animation()
        if is_jumping:
            y = -GRAVITY_FORCE
            jump_count -= 1
            if jump_count == 0:
                is_jumping = False
        if check_movement(player, x, y):
                canvas.move(player, x, y)
        scroll_screen(x)

        if not is_jumping:
            apply_gravity()
        # add functions
        move_bullets()
        check_bullet_collision()
        game_window.after(20,move_player)
            

    # # Load your action images of player
    image_walk1 = tk.PhotoImage(file="img/Characters/player/Run/0.png")
    image_walk2 = tk.PhotoImage(file="img/Characters/player/Run/1.png")
    image_walk3 = tk.PhotoImage(file="img/Characters/player/Run/2.png")
    image_walk4 = tk.PhotoImage(file="img/Characters/player/Run/3.png")
    image_walk5 = tk.PhotoImage(file="img/Characters/player/Run/4.png")
    image_walk6 = tk.PhotoImage(file="img/Characters/player/Run/5.png")

    # player's action
    def walk_animation():
        global action
        if action == 10:
            canvas.itemconfig(player, image = image_walk1)
        elif action == 20:
            canvas.itemconfig(player, image = image_walk2)
        elif action == 30:
            canvas.itemconfig(player, image = image_walk3)
        elif action == 40:
            canvas.itemconfig(player, image = image_walk4)
        elif action == 50:
            canvas.itemconfig(player, image = image_walk5)
        elif action == 60:
            canvas.itemconfig(player, image = image_walk6)
        elif action == 70:
            canvas.itemconfig(player, image = image_walk1)
        if action == 70:
            action = 0
        return
        
    # Check condition of wall 
    def check_movement(item, dx=0, dy=0):
        item_coords = canvas.coords(item)
        new_x1 = item_coords[0] + dx + 50
        new_y1 = item_coords[1] + dy + 50
        new_x2 = item_coords[0] + dx - 40
        new_y2 = item_coords[1] + dy - 40
        overlapping_objects = canvas.find_overlapping(new_x1, new_y1, new_x2, new_y2)
        for wall_id in canvas.find_withtag("wall"):
            if wall_id in overlapping_objects:
                return False

        return True

    # Gravity for character
    def apply_gravity():
        if not check_movement(player, 0, GRAVITY_FORCE):
            return

        canvas.move(player, 0, GRAVITY_FORCE)
        scroll_screen(0)

    # Scroll screen
    def scroll_screen(x_direction):
        global scroll_offset
        player_coords = canvas.coords(player)
        x1, x2  = player_coords
        
        if x_direction > 0 and x2 >= 300 -scroll_offset:
            scroll_offset += 40
            canvas.move(player, -10, 0)
            for obstacle in obstacles:
                    canvas.move(obstacle, -10, 0)
            for enemy in pol_pots:
                    canvas.move(enemy, -10, 0)
        elif x_direction < 0 and x1 <=scroll_offset:
            scroll_offset -= 40
            canvas.move(player, 10, 0)
            for obstacle in obstacles:
                canvas.move(obstacle, 10, 0)
         
            for enemy in pol_pots:
                canvas.move(enemy, 10, 0)

    # Move bullets of player
    def move_bullets():
        for bullet in player_bullets:
            canvas.move(bullet, 10, 0)

    # Check bullet collision
    def check_bullet_collision():
        for bullet in player_bullets:
            bullet_coords = canvas.coords(bullet)
            overlapping_objects = canvas.find_overlapping(*bullet_coords)

            # delect bulet when it thouch someting
            for obstacle in obstacles:
                if obstacle in overlapping_objects:
                    canvas.delete(bullet)
                    player_bullets.remove(bullet)

    # check condition player's bullet
    def check_bullet_collision():
        for bullet in player_bullets:
            bullet_coords = canvas.coords(bullet)
            overlapping_objects = canvas.find_overlapping(*bullet_coords)
            all_enemies = pol_pots
            # delect bulet when it thouch someting
            for obstacle in obstacles:
                if obstacle in overlapping_objects:
                    canvas.delete(bullet)
                    player_bullets.remove(bullet)
                
            for pol_pot in all_enemies:   
                if pol_pot in overlapping_objects:
                        canvas.delete(pol_pot)
                        canvas.delete(bullet)
                        pol_pots.remove(pol_pot)
                        player_bullets.remove(bullet)
                        increase_score()

                            
                    
    # blood of hero 
    def lose_blood():
        global current_lives
        current_lives -= 1

    def gain_life():
        global current_lives
        if current_lives < max_blood:
            current_lives += 1

    def hit_player():
        lose_blood()
        if current_lives <= 0:
            lose_all_blood()
    def got_hit():
        hit_player()
        update_blood()

    def get_more_blood():
        gain_life()
        update_blood()

    def update_blood():
        progress_bar["value"] = current_lives
        progress_bar["style"] = "Blood.Horizontal.TProgressbar" if current_lives > 0 else "Empty.Horizontal.TProgressbar"

    style = tk.ttk.Style()
    style.theme_use('default')
    style.configure("Blood.Horizontal.TProgressbar", troughcolor='white', background='red')
    style.configure("Empty.Horizontal.TProgressbar", troughcolor='white', background='gray')

    progress_bar = Progressbar(game_window, length=200, mode="determinate", maximum=max_blood, style="Blood.Horizontal.TProgressbar")
    progress_bar.place(x=80,y=30)


    # player life


    def lose_life():
        global life
        life -= 1

    def gain_life():
        global life
        if life < max_lives:
            life += 1

    def kill_player():
        lose_life()
        if life <= 0:
            print("Game Over", "You have lost all your lives!")

    def lose_all_blood():
        global current_lives
        kill_player()
        update_lives()
        current_lives = 3

    def update_lives():
        global lives_frame

        if life > 0:
            last_heart_index = life - 1
            heart_labels = lives_frame.grid_slaves()

            if heart_labels and len(heart_labels) > 1:
                last_heart_label = heart_labels[last_heart_index]
                last_heart_label.destroy()

                for i, heart_label in enumerate(heart_labels[:last_heart_index]):
                    heart_label.configure(image=heart_empty_image)

        else:
            lives_frame.destroy()


    heart_full_image = Image.open("img/heart_full.png")
    heart_full_image = heart_full_image.resize((40, 40))
    heart_full_image = ImageTk.PhotoImage(heart_full_image)

    heart_empty_image = Image.open("img/heart_empty.png")
    heart_empty_image = heart_empty_image.resize((40, 40))
    heart_empty_image = ImageTk.PhotoImage(heart_empty_image)
    global lives_frame
    lives_frame = tk.Canvas(game_window)
    lives_frame.place(x=80,y=70)

    for i in range(max_lives):
        heart_label = tk.Label(lives_frame, image=heart_full_image)
        heart_label.grid(row=0, column=i)


    # player score
    def increase_score():
        global score
        score += 1
        score_label.config(text="Score: " + str(score))

    score_label = tk.Label(game_window, text="Score: 0", font=("Arial", 16))
    score_label.place(x=1200,y=20)


    # Time of player 
    timer_label = tk.Label(game_window, text="", font=("Arial", 24))
    timer_label.place(x=500,y=20)

    # Define the countdown function
    def countdown(seconds):
        if seconds >= 0:
            timer_label.config(text=f"Time life: {seconds} seconds")
            seconds -= 1
            timer_label.after(1000, countdown, seconds)
        else:
            timer_label.config(text="Time's up!")

    # Start the countdown with 60 seconds
    countdown(30)


    update_blood()
    walk_animation()       
    game()
    move_player()
    game_window.mainloop()

    def go_back_to_main():
        game_window.destroy()
        root.deiconify()

    back_to_main_button = tk.Button(game_window, text='Back', width=8, font=('BLOODY TYPE PERSONAL USE', 15),
                                    command=go_back_to_main, bg='brown', fg="White", border=5)
    back_to_main_button.place(x=10, y=20)

#_________________img________________

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

    help_background_img_path = "img/help-background.png"  # Specify the path to the help window background image
    background_image = Image.open(help_background_img_path)
    width = 1400
    height = 720

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