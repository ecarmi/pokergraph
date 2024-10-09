import matplotlib.pyplot as plt
import numpy as np
import csv

stacks = []

# Reading file
with open("Final_Ledger.csv", "r") as file:
    lines = csv.reader(file, delimiter=",")
    for line in lines:
        if "Player stacks" in line[0]:
            stacks.append(line[0])

rev_stacks = stacks[::-1]

real_players = {} # Dict that stores values in id:[aliases] format
round_list = []

for line in rev_stacks:
    sep = line.split("|") # Separates each line in each stack
    round = []

    for player_bio in sep:
        id = player_bio[player_bio.find('@') + 1 : player_bio.find('"', player_bio.find('@') + 1)].strip() # Finds each id
        name = player_bio[player_bio.find('"') + 1 : player_bio.rfind("@") - 1] # Finds the name

        if not id in real_players:
            real_players[id] = [name] # Initializes new entry in players with first alias
        else:
            if name not in real_players[id]:
                real_players[id].append(name) # Adds the new alias to player

        amount = int(player_bio[player_bio.find("(") + 1 : player_bio.rfind(")")]) # Finds amount of chips per round per person
        dict = {id: int(amount)} # Updates temporary dict
        round.append(dict)
    
    round_list.append(round)

plt.figure(figsize=(12, 6))
colors = plt.cm.tab10(np.linspace(0, 1, len(real_players))) # Initializing a pre-set list of colors
x = np.arange(1, len(round_list) + 1) # Creating the x-values array

for index, (player, aliases) in enumerate(real_players.items()): # Ranging through each player's games
    player_values = []

    for round_itr in round_list: # Going through every round
        player_amount = np.nan # Initializing a NaN value for each player

        for dict_values in round_itr:
            if player in dict_values:
                player_amount = dict_values[player] # If the player has a value in chips, the amount is added
                break
        
        player_values.append(player_amount)

    plt.plot(x, player_values, label=" / ".join(aliases), color=colors[index])

plt.legend(fontsize='small',loc="upper left")
plt.title('Fuck GOA Poker Night 1')
plt.xlabel('Round #')
plt.ylabel('Chips')
plt.show()