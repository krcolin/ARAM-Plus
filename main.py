# -*- coding: utf-8 -*-
import random
from data.data import champions, logo
import os
import ctypes

# CHAT-GPT Generated code to change cmd prompt design
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
STD_OUTPUT_HANDLE = -11
handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
mode = ctypes.c_ulong()
ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
ctypes.windll.kernel32.SetConsoleMode(handle, mode)
systeem = os.system('color F0')

# Colors for cmd
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[30m"

print(logo)


# Function to get 6 names from input
def get_names():
    """
    A function that prompts the user to enter 6 names separated by commas, then returns the names as a list if there are exactly 6 names entered. Otherwise, it prints an error message and continues prompting for input.

    :return: list: The list of names entered by the user.
    """
    while True:
        input_names = input(f"Enter 6 namen met een , er tussen: ")
        namen = [name.strip() for name in input_names.split(',')]
        if len(namen) == 6:
            return namen
        else:
            print("Error: Vul 6 namen in.")


namen = get_names()


def main():
    random.shuffle(namen)

    team1 = namen[0:3]
    team2 = namen[3:]
    f_team1 = ", ".join(team1).title()
    f_team2 = ", ".join(team2).title()
    print(f"\n{BLUE}Team Blue: {f_team1}\n{RED}Team Red: {f_team2}")

    champions_per_player = assign_champions_interactively(team1, team2, champions)

    print_teams_with_champions(team1, team2, champions_per_player)


def assign_champions_interactively(team1: list, team2: list, champions: list):
    """
    Assigns champions interactively to two teams of players from a pool of available champions.

    :param team1: List of players in team 1.
    :param team2: List of players in team 2.
    :param champions: List of available champions.
    :return: A dictionary containing the allocation of champions to each player in the format {player: "Champion 1, Champion 2, ..."}.
    :rtype: dict
    """
    global count
    champions_pool = champions[:]
    champion_allocation = {player: [] for player in team1 + team2}
    count = 0

    def player_select_champion(player: str, champions_pool: list):
        """
        Selects a champion for the player from the given champions pool.

        :param player: The player for whom the champion is being selected.
        :param champions_pool: The pool of champions to select from.
        :return: The chosen champion selected from the pool.
        :rtype: str
        """
        global count
        if count % 2 == 0:
            kleur = BLUE
        else:
            kleur = RED
        available_choices = random.sample(champions_pool, 3)
        print(f"\n{kleur}{player.title()}'s keuzes:")
        for idx, champ in enumerate(available_choices, start=1):
            print(f"\t{idx}. {champ}")
        while True:
            try:
                choice = int(input(f"{GREEN}Welk nummer: ")) - 1
                if 0 <= choice < 3:
                    chosen_champion = available_choices[choice]
                    champions_pool.remove(chosen_champion)
                    break
                else:
                    print("Kies een nummer tussen 1 en 3.")
            except ValueError:
                print("Voer a.u.b. een geldig nummer in.")
        count += 1
        return chosen_champion

    players_order = []
    for player1, player2 in zip(team1, team2):
        players_order.append(player1)
        players_order.append(player2)

    for _ in range(1):
        for player in players_order:
            chosen_champion = player_select_champion(player, champions_pool)
            champion_allocation[player].append(chosen_champion)

    for player in champion_allocation:
        champion_allocation[player] = ', '.join(champion_allocation[player]).title()

    return champion_allocation


def print_teams_with_champions(team1: list, team2: list, champion_allocation: dict):
    """
    Print teams with champions and their allocations.

    :param team1: list of strings representing the players in the blue team
    :param team2: list of strings representing the players in the red team
    :param champion_allocation: dictionary mapping player names to their allocated champions

    """
    print(f"\n{BLUE}Blue:")
    for player in team1:
        print(f"\t{player.title()}: {champion_allocation[player]}")

    print(f"\n{RED}Red:")
    for player in team2:
        print(f"\t{player.title()}: {champion_allocation[player]}")


if __name__ == "__main__":
    while True:
        main()
        prompt = input(f"\n{RESET}Enter voor reroll, 'namen' om nieuwe "
                       f"namen toe te voegen of 'exit' om te stoppen... ").lower()
        if prompt == 'exit':
            break
        if prompt == 'namen':
            namen = get_names()
