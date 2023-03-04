import csv
import random
import pandas as pd
import numpy as np

game_board = ['green', 'doodads', 'green', 'purple', 'green', 'paycheck', 'green', 'market'] * 3
game_board[3] = 'charity'
game_board[11] = 'baby'
game_board[19] = 'downsized'
income_items = ['']

professions = pd.read_csv('Professions.csv')
professions.set_index('Name', inplace = True)
index_0 = ['Income'] * 3 + ['Expenses'] * 9 + ['Savings'] + ['Liabilities'] * 5
index_1 = list(professions.columns)
index = pd.MultiIndex.from_arrays([index_0, index_1])
professions = professions.T
professions.set_index(index, inplace = True)
professions = professions.to_dict()

professions = []
f = open('Professions.tsv', 'r')
reader = csv.DictReader(f, delimiter = '\t')
for row in reader:
    dicts = [{}, {}, {}, {}]
    new_dict = {}
    j = 0
    for i, item in enumerate(list(row.items())):
        if item[1].isnumeric():
            row[item[0]] = int(item[1])
        if i != 0 and i != 16 and i < 22:
            if i > 0 and i <= 5:
                j = 0
            elif i > 5 and i < 16:
                j = 1
            elif i > 16 and i < 21:
                j = 2
            dicts[j][item[0]] = row[item[0]]
        elif i < 22:
            new_dict[item[0]] = row[item[0]]
    for i, x in enumerate(['Income', 'Expenses', 'Liabilities', 'Assets']):
        new_dict[x] = dicts[i]
    professions.append(new_dict)
f.close()

player_list = []
turn_number = 0

class Player:
    def __init__(self, name, financial_statement):
        self.name = name
        self.financial_statement = financial_statement

class GameTile:
    def __init__(self, type, flavor_text, menu):
        self.type = type
        self.flavor_text = flavor_text
        self.menu = menu

class AssetTile(GameTile):
    def __init__(self, flavor_text, menu):
        super().__init__(self, 'asset', flavor_text, menu)

class DoodadTile(GameTile):
    def __init__(self, flavor_text, menu):
        super().__init__(self, 'doodad', flavor_text, menu)

class CharityTile(GameTile):
    def __init__(self, flavor_text, menu):
        super().__init__(self, 'charity', flavor_text, menu)

class DownsizedTile(GameTile):
    def __init__(self, flavor_text, menu):
        super().__init__(self, 'downsized', flavor_text, menu)

class Menu:
    pass

def change_turn_number():
    if turn_number == len(player_list):
        turn_number = 0
    else:
        turn_number += 1

def InitPlayers():
    print("Welcome to CashFlow!")
    players_confirmed = False
    while not players_confirmed:
        num_players = validateIntInput("How many players will be playing?")
        players_confirmed = confirmYesNo(f"There will be {num_players} players. Are you sure about this? (y/n)\n")
    for i in range(num_players):
        player_name = input("Enter Player Name")
        if player_name == "":
            player_name = f"Player {i + 1}"
        player_list.append(Player(player_name, random.choice(professions)))

def confirmYesNo(prompt):
    confirmed = False
    valid = False
    while not valid:
        yes_no_input = input(prompt)
        if yes_no_input in ['y', 'n']:
            valid = True
    if yes_no_input == 'y':
        confirmed = True   
    return confirmed

def validateIntInput(prompt = "", minNum = 0, maxNum = 999999):
    valid = False
    while not valid:
        int_input = input(prompt + "\n")
        if int_input.isnumeric() and int(int_input) in range(minNum, maxNum + 1):
            valid = True
        else:
            print("Invalid Number!")
    return int_input

def main():
    InitPlayers()


if __name__ == '__main__':
    main()