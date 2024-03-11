# -*- coding: utf-8 -*-
import copy
import random
from data.data import champions
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

FONT = ("Helvetica", 18)
AMT_CHAMPS = 3
OG_CHAMPS = champions


class AramCustomGenerator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.champions_pool = copy.deepcopy(OG_CHAMPS)
        self.player_champion = {}
        self.names_entries = []
        self.names = []
        self.old_names = []
        self.names_input = None
        self.name_labels = []
        self.current_player_index = 0
        self.current_player = ""
        self.interleaved_players = []
        self.team1 = []
        self.team2 = []
        self.entered_names = False
        self.champion_selection_frame = None
        self.submit_button = None
        self.amount_players = 6
        self.teams_frame = None
        self.champion_buttons = []
        self.initialize_ui()

    def initialize_ui(self):
        self.root.title("ARAM Custom Generator")

        icon = Image.open("logo.ico")
        icon_image = ImageTk.PhotoImage(icon)
        self.root.wm_iconphoto(True, icon_image)
        self.root.configure(padx=50, pady=50)

        title = tk.Label(self.root, text="ARAM Custom Generator", font=FONT)
        title.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nswe")
        img = Image.open("tk_logo.png")
        img = img.reduce(5)
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self.root, image=logo)
        logo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        # Stops garbage collection of the image
        logo_label.image = logo

        self.create_names_input()

        menu_bar = tk.Menu(self.root)
        reroll_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Reroll", menu=reroll_menu)
        reroll_menu.add_command(label="New names", command=self.reroll_names)
        reroll_menu.add_separator()
        reroll_menu.add_cascade(label="Same names", command=self.reroll_champions_only)
        menu_bar.add_separator()
        menu_bar.add_command(label="Exit", command=self.quit)

        self.root.config(menu=menu_bar)
        self.root.bind("<Return>", self.enter_pressed)
        self.root.bind("<Key-1>", lambda x: self.button_pressed(0))
        self.root.bind("<Key-2>", lambda x: self.button_pressed(1))
        self.root.bind("<Key-3>", lambda x: self.button_pressed(2))

        self.center_window()
        self.root.update()
        self.root.mainloop()

    def create_names_input(self):
        self.root.withdraw()

        self.amount_players = simpledialog.askinteger(
            "Input",
            "How many players?",
            minvalue=2,
            maxvalue=10,
            initialvalue=self.amount_players,
        )
        self.names_input = tk.Canvas(self.root, width=400, height=300)
        self.names_input.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        for index in range(self.amount_players):
            row = index // 2
            column = index % 2
            name = tk.Entry(self.names_input)
            if index < len(self.old_names):
                name.insert(0, self.old_names[index])
            name.grid(row=row, column=column, padx=10, pady=10)
            self.names_entries.append(name)

        if self.names_entries:
            self.names_entries[0].focus_set()
        self.submit_button = tk.Button(
            self.root, text="Submit", width=20, command=self.submit_names
        )
        self.submit_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        self.root.update()
        self.names_input.update()
        self.root.deiconify()
        self.names_entries[0].focus_set()

    def submit_names(self):
        self.names = [
            name_entry.get()
            for name_entry in self.names_entries
            if name_entry.get() != ""
        ]
        if not self.all_entries_filled():
            messagebox.showerror("Error", "One or more names are empty.")
            return
        else:
            # Destroy the names input canvas and submit button after successful submission
            self.names_input.destroy()
            self.submit_button.destroy()
            self.initialize_champion_selection()

    def enter_pressed(self, event):
        if not self.entered_names:
            if self.all_entries_filled():
                self.submit_names()
                self.entered_names = True
            else:
                self.empty_entry().focus_set()

    def empty_entry(self):
        for name_entry in self.names_entries:
            if name_entry.get() == "":
                return name_entry
        return None

    def all_entries_filled(self):
        for name_entry in self.names_entries:
            if name_entry.get() == "":
                return False
        return True

    def center_window(self):
        # Update the window to make sure we have the latest dimensions
        self.root.update_idletasks()

        # Get the window dimensions
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates based on the screen dimensions
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the position of the window at the center of the screen
        self.root.geometry(f"+{x}+{y}")
        self.root.update()

    def initialize_champion_selection(self):
        # Shuffle names and prepare interleaved player list for turn-based selection
        random.shuffle(self.names)
        players_per_team = len(self.names) // 2
        self.team1 = self.names[:players_per_team]
        self.team2 = self.names[players_per_team:]
        self.interleaved_players = [
            val for pair in zip(self.team1, self.team2) for val in pair
        ]
        self.current_player_index = 0
        self.current_player = self.interleaved_players[self.current_player_index]

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=0, minsize=150)
        # Initialize the champion selection UI
        self.champion_selection_frame = tk.Frame(self.root)
        self.teams_frame = tk.Frame(self.root)
        self.teams_frame.grid(
            row=2, column=0, padx=10, pady=10, sticky="nswe", columnspan=4
        )
        self.teams_frame.columnconfigure(0, weight=1)
        self.teams_frame.columnconfigure(1, weight=1)
        for idx, player in enumerate(self.team1):
            player_label = tk.Label(self.teams_frame, text=player, font=FONT, fg="blue")
            player_label.grid(column=0, row=idx, sticky="we", columnspan=1)
            self.name_labels.append(player_label)
        for idx, player in enumerate(self.team2):
            player_label = tk.Label(self.teams_frame, text=player, font=FONT, fg="red")
            player_label.grid(column=1, row=idx, sticky="we", columnspan=1)
            self.name_labels.append(player_label)
        self.champion_selection_frame.grid(
            row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nswe"
        )
        self.champion_selection_frame.configure(
            highlightbackground="grey", highlightthickness=2, bg="#f5f0e4"
        )
        self.create_champion_selection_area()
        self.center_window()

    def create_champion_selection_area(self):
        # Clear the selection area
        for widget in self.champion_selection_frame.winfo_children():
            widget.destroy()
        if self.current_player in self.team1:
            color = "blue"
        else:
            color = "red"
        tk.Label(
            self.champion_selection_frame,
            text=f"{self.current_player}'s Turn to Choose a Champion:",
            fg=color,
            font=FONT,
            bg="#f5f0e4",
        ).grid(row=0, column=0, pady=10, columnspan=2)
        self.champion_buttons = []
        champion_choices = random.sample(self.champions_pool, AMT_CHAMPS)
        for idx, champ in enumerate(champion_choices):
            idx = idx + 1
            btn = tk.Button(
                self.champion_selection_frame,
                width=20,
                text=champ,
                command=lambda c=champ: self.select_champion(c),
            )
            btn.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            (tk.Label(self.champion_selection_frame, text=f"{idx}.", font=("Helvetica", 8), bg="#f5f0e4").
             grid(row=idx, column=0, sticky="e"))
            self.champion_buttons.append(btn)

    def select_champion(self, champ):
        self.player_champion[self.current_player] = (
            champ  # Map the player to their selected champion.
        )
        self.champions_pool.remove(champ)  # Remove the selected champion from the pool.

        # Update the corresponding label for the current player.
        for name_label in self.name_labels:
            cur_name = name_label.cget("text")
            if self.current_player == cur_name:
                name_label.config(text=f"{cur_name}: {champ}")

        self.current_player_index += 1
        if self.current_player_index < len(self.interleaved_players):
            self.update_current_player()
            self.create_champion_selection_area()
        else:
            self.champion_selection_frame.destroy()
            self.root.update()

    def update_current_player(self):
        self.current_player = self.interleaved_players[self.current_player_index]

    def quit(self):
        self.root.destroy()

    def reroll_names(self):
        if self.champion_selection_frame:
            self.champion_selection_frame.destroy()
            self.champion_selection_frame = None
        if self.names_input:
            self.names_input.destroy()
            self.names_input = None
        if self.teams_frame:
            self.teams_frame.destroy()
            self.teams_frame = None
        # Clear existing names and reset state as needed
        self.reset_state()

        self.root.rowconfigure(3, weight=0, minsize=0)

        # Re-initialize the names input area for new input
        self.create_names_input()

    def reroll_champions_only(self):
        # Functionality to reroll champions while keeping the names
        if self.champion_selection_frame:
            self.champion_selection_frame.destroy()
        if self.names_input:
            self.names_input.destroy()
            self.names_input = None
        if self.teams_frame:
            self.teams_frame.destroy()
            self.teams_frame = None

        # No need to reset names, but reset other states as needed
        self.reset_state(keep_names=True)
        self.initialize_champion_selection()

    def button_pressed(self, number):
        try:
            self.champion_buttons[number].invoke()
        except (IndexError, tk.TclError):
            pass

    def reset_state(self, keep_names=False):
        if not keep_names:
            self.old_names = self.names
            self.names = []
        # Reset the rest of the state
        self.names_entries = []
        self.name_labels = []
        self.entered_names = False if not keep_names else True
        self.player_champion = {}
        self.champions_pool = copy.deepcopy(OG_CHAMPS)  # Reset champion pool
        self.current_player_index = 0
        self.current_player = ""
        self.interleaved_players = []
        self.team1 = []
        self.team2 = []


def main():
    root = tk.Tk()
    app = AramCustomGenerator(root)


if __name__ == "__main__":
    main()
