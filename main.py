# -*- coding: utf-8 -*-
import random
from data.data import champions
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

PLAYERS = simpledialog.askinteger("Input", "How many players?", minvalue=2, maxvalue=10)
FONT = ("Helvetica", 18)
AMT_CHMPS = 3

img = Image.open("tk_logo.png")
img = img.reduce(5)


def center_window(root):
    # Update the window to make sure we have the latest dimensions
    root.update_idletasks()

    # Get the window dimensions
    width = root.winfo_width()
    height = root.winfo_height()

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates based on the screen dimensions
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the position of the window at the center of the screen
    root.geometry(f'+{x}+{y}')
    root.deiconify()


root = tk.Tk()
root.title("ARAM 3v3 Custom Generator")
root.configure(padx=50, pady=50)

logo = ImageTk.PhotoImage(img)

title = tk.Label(root, text="ARAM 3v3 Custom Generator", font=FONT)
logo_label = tk.Label(root, image=logo)

logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

title.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nswe")
names_input = tk.Canvas(root, width=400, height=300)
names_input.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
champions_pool = champions
names_entries = []
names = []
player_champion = {}

for index, _ in enumerate(range(PLAYERS)):
    name = tk.Entry(names_input)
    name.grid(row=index, column=0, padx=10, pady=10)
    names_entries.append(name)


def create_champion_selection_area():
    for widget in champion_selection_frame.winfo_children():
        widget.destroy()
    if current_player in team1:
        color = "blue"
    else:
        color = "red"


    tk.Label(champion_selection_frame, text=f"{current_player}'s Turn to Choose a Champion:", fg=color,
             font=FONT).grid(row=0, column=0, padx=10, pady=10)

    champion_choices = random.sample(champions_pool, AMT_CHMPS)
    for idx, champ in enumerate(champion_choices):
        idx = idx + 1
        btn = tk.Button(champion_selection_frame, width=10, text=champ, command=lambda c=champ: select_champion(c))
        btn.grid(row=idx, column=0, padx=10, pady=5)


def select_champion(champ):
    global current_player_index, interleaved_players
    player_champion[current_player] = champ  # Map the player to their selected champion.
    champions_pool.remove(champ)  # Remove the selected champion from the pool.

    # Update the corresponding label for the current player.
    for name_label in name_labels:
        cur_name = name_label.cget("text")
        if current_player == cur_name:
            name_label.config(text=f"{cur_name}: {champ}")

    current_player_index += 1
    if current_player_index < len(interleaved_players):
        update_current_player()
        create_champion_selection_area()
    else:
        champion_selection_frame.destroy()


def update_current_player():
    global current_player
    current_player = interleaved_players[current_player_index]


def submit_names():
    global names, current_player, interleaved_players, current_player_index
    names = [name_entry.get() for name_entry in names_entries if name_entry.get() != ""]
    if len(names) < PLAYERS:
        messagebox.showerror("Error", "One or more names are empty.")
        return
    else:
        # Destroy the names input canvas and submit button after successful submission
        names_input.destroy()
        submit_button.destroy()
        initialize_champion_selection()


submit_button = tk.Button(names_input, text="Submit", command=submit_names)
submit_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
root.withdraw()
root.after(100, center_window, root)

name_labels = []


def initialize_champion_selection():
    global champions_pool, player_champion, interleaved_players, current_player, current_player_index,\
        champion_selection_frame, team1 ,team2
    # Shuffle names and prepare interleaved player list for turn-based selection
    random.shuffle(names)
    players_per_team = len(names) // 2
    team1 = names[:players_per_team]
    team2 = names[players_per_team:]
    interleaved_players = [val for pair in zip(team1, team2) for val in pair]
    current_player_index = 0
    current_player = interleaved_players[current_player_index]

    # Initialize the champion selection UI
    champion_selection_frame = tk.Frame(root)
    teams_frame = tk.Frame(root)
    teams_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe", columnspan=2)
    teams_frame.columnconfigure(0, weight=1)
    teams_frame.columnconfigure(1, weight=1)
    for idx, player in enumerate(team1):
        player_label = tk.Label(teams_frame, text=player, font=FONT, fg="blue")
        player_label.grid(column=0, row=idx, sticky="ew")
        name_labels.append(player_label)
    for idx, player in enumerate(team2):
        player_label = tk.Label(teams_frame, text=player, font=FONT, fg="red")
        player_label.grid(column=1, row=idx, sticky="ew")
        name_labels.append(player_label)
    champion_selection_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nswe")
    champion_selection_frame.configure(highlightbackground="grey", highlightthickness=1, relief="raised")
    create_champion_selection_area()


root.mainloop()
