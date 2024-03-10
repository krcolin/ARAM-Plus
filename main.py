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
    def __init__(self, root):
        self.root = root
        self.champions_pool = champions
        self.player_champion = {}
        self.names_entries = []
        self.names = []
        self.name_labels = []
        self.current_player_index = 0
        self.current_player = ""
        self.interleaved_players = []
        self.team1 = []
        self.team2 = []

        self.champion_selection_frame = None
        self.submit_button = None

        self.initialize_ui()

    def initialize_ui(self):
        self.root.title("ARAM Custom Generator")
        self.root.configure(padx=50, pady=50)
        self.root.withdraw()
        title = tk.Label(self.root, text="ARAM Custom Generator", font=FONT)
        title.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nswe")

        img = Image.open("tk_logo.png")
        img = img.reduce(5)
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self.root, image=logo)
        logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # Stops garbage collection of the image
        logo_label.image = logo

        self.names_input = tk.Canvas(self.root, width=400, height=300)
        self.names_input.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        PLAYERS = simpledialog.askinteger("Input", "How many players?",
                                          minvalue=2, maxvalue=10, initialvalue=6)
        for index in range(PLAYERS):
            name = tk.Entry(self.names_input)
            name.grid(row=index, column=0, padx=10, pady=10)
            self.names_entries.append(name)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_names)
        self.submit_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        self.root.after(100, self.center_window)
        self.root.bind("<Return>", self.enter_pressed)
        self.root.mainloop()

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
        self.root.geometry(f'+{x}+{y}')
        self.root.deiconify()

    def all_names_filled(self):
        for name_entry in self.names_entries:
            if name_entry.get() == "":
                return False
        return True

    def is_empty_entry(self):
        for name_entry in self.names_entries:
            if name_entry.get() == "":
                return name_entry
        return None

    def create_champion_selection_area(self):
        # Clear the selection area
        for widget in self.champion_selection_frame.winfo_children():
            widget.destroy()
        if self.current_player in self.team1:
            color = "blue"
        else:
            color = "red"
        tk.Label(self.champion_selection_frame, text=f"{self.current_player}'s Turn to Choose a Champion:", fg=color,
                 font=FONT, bg="#f5f0e4").grid(row=0, column=0, padx=10, pady=10)

        champion_choices = random.sample(self.champions_pool, AMT_CHAMPS)
        for idx, champ in enumerate(champion_choices):
            idx = idx + 1
            btn = tk.Button(self.champion_selection_frame, width=10, text=champ,
                            command=lambda c=champ: self.select_champion(c))
            btn.grid(row=idx, column=0, padx=10, pady=5)

    def select_champion(self, champ):
        self.player_champion[self.current_player] = champ  # Map the player to their selected champion.
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
            reroll_button = tk.Button(self.root, text="Reroll", command=self.reroll)
            reroll_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def update_current_player(self):
        self.current_player = self.interleaved_players[self.current_player_index]

    def submit_names(self):
        self.names = [name_entry.get() for name_entry in self.names_entries if name_entry.get() != ""]
        if not self.empty_names_entry():
            messagebox.showerror("Error", "One or more names are empty.")
            return
        else:
            # Destroy the names input canvas and submit button after successful submission
            self.names_input.destroy()
            self.submit_button.destroy()
            self.initialize_champion_selection()

    def initialize_champion_selection(self):
        # Shuffle names and prepare interleaved player list for turn-based selection
        random.shuffle(self.names)
        players_per_team = len(self.names) // 2
        self.team1 = self.names[:players_per_team]
        self.team2 = self.names[players_per_team:]
        self.interleaved_players = [val for pair in zip(self.team1, self.team2) for val in pair]
        self.current_player_index = 0
        self.current_player = self.interleaved_players[self.current_player_index]

        # Initialize the champion selection UI
        self.champion_selection_frame = tk.Frame(self.root)
        teams_frame = tk.Frame(self.root)
        teams_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe", columnspan=2)
        teams_frame.columnconfigure(0, weight=1)
        teams_frame.columnconfigure(1, weight=1)
        for idx, player in enumerate(self.team1):
            player_label = tk.Label(teams_frame, text=player, font=FONT, fg="blue")
            player_label.grid(column=0, row=idx, sticky="we")
            self.name_labels.append(player_label)
        for idx, player in enumerate(self.team2):
            player_label = tk.Label(teams_frame, text=player, font=FONT, fg="red")
            player_label.grid(column=1, row=idx, sticky="we")
            self.name_labels.append(player_label)
        self.champion_selection_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nswe")
        self.champion_selection_frame.configure(highlightbackground="grey", highlightthickness=2, bg="#f5f0e4")
        self.create_champion_selection_area()

    def reroll(self):
        for widget in self.root.winfo_children():
            try:
                widget_text = widget.cget("text")
                if widget_text == "Reroll":
                    widget.destroy()
            except tk.TclError:
                continue
        self.champions_pool = copy.deepcopy(OG_CHAMPS)
        self.initialize_champion_selection()

    def enter_pressed(self, event):
        if self.empty_names_entry():
            self.submit_names()
        else:
            self.empty_entry().focus_set()

    def empty_entry(self):
        for name_entry in self.names_entries:
            if name_entry.get() == "":
                return name_entry
        return None

    def empty_names_entry(self):
        for name_entry in self.names_entries:
            if name_entry.get() == "":
                return False
        return True


def main():
    root = tk.Tk()
    app = AramCustomGenerator(root)


if __name__ == "__main__":
    main()

