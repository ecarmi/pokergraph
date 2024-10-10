import matplotlib.pyplot as plt
import numpy as np
import csv

def get_file_stacks(file_path):
    """
    Gets the poker stacks from the file specified.

    Args:
        param1 str: Path to the CSV with the poker logs.

    Returns:
        list: Every index of stacks from the poker CSV.
    """
    stacks_lines = []
    buy_in_lines = []

    # Reading file
    with open(file_path, "r") as file:
        lines = csv.reader(file, delimiter=",")
        for line in lines:
            if "Player stacks" in line[0]:
                stacks_lines.append(line[0])
            elif "joined the game with a stack" in line[0]:
                buy_in_lines.append(line[0])

    return stacks_lines[::-1], buy_in_lines

def init_poker_table(rev_stacks, buy_lines):
    """
    Initializes the poker table for further manipulation.

    Args:
        param1 list: Every index of stacks from the poker CSV.
    
    Returns:
        dict: Key value pair of unique user ID to alias of each user.
        list: Every index of played games within this poker instance.
    """
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
            round.append({id: int(amount)})

        round_list.append(round)

    buy_in_amounts_id = {}
    buy_in_amounts_name = {}
    
    for line in buy_lines:
        
        id = line[line.find('@') + 1 : line.find('"', line.find('@') + 1)].strip() # Finds each id
        buy_in_amounts_id[id] = 1 if not id in buy_in_amounts_id else buy_in_amounts_id[id] + 1
        buy_in_amounts_name[" / ".join(real_players[id])] = 1 if not " / ".join(real_players[id]) in buy_in_amounts_name else buy_in_amounts_name[" / ".join(real_players[id])] + 1

    print(buy_in_amounts_id,buy_in_amounts_name)
        
    return real_players, round_list

def create_plot_fig(player_list, rounds, night_num):
    """
    Creates the figure for the poker night with specified players and with round information.

    Args:
        param1 dict: Dictionary containing unique ID keys of each player, with an array of aliases as its values.
        param2 list: Array containing every round, with a nested array with dicts for every player per round.
        param3 str: The count of which poker night it is in string format.
    
    Returns:
        Nothing, void function.
    """
    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, len(player_list))) # Initializing a pre-set list of colors
    x = np.arange(1, len(rounds) + 1) # Creating the x-values array

    for index, (player, aliases) in enumerate(player_list.items()): # Ranging through each player's games
        player_values = []

        for round_itr in rounds: # Going through every round
            player_amount = np.nan # Initializing a NaN value for each player

            for dict_values in round_itr:
                if player in dict_values:
                    player_amount = dict_values[player] # If the player has a value in chips, the amount is added
                    break
            
            player_values.append(player_amount)

        plt.plot(x, player_values, label=" / ".join(aliases), color=colors[index])

    plt.legend(fontsize='small',loc="upper left")
    plt.title('Fuck GOA Poker Night ' + night_num)
    plt.xlabel('Round #')
    plt.ylabel('Chips')
    plt.show()

def main():
    """
    Main function for this program, ran at the start.
    """
    print("Welcome to the Poker Graph Creator.")

    file_name = input("Ledger CSV file path: ")
    el_stackos = []

    while True:
        try:
            stackos, buy_inos = get_file_stacks(file_name)
            break
        except Exception as e:
            print(e)
            file_name = input("Ledger CSV file path: ")

    night = input("Ledger night #: ")
    ps, rds = init_poker_table(stackos, buy_inos)
    create_plot_fig(ps, rds, night)

    print("Figure presented successfully.")

main()