import matplotlib.pyplot as plt
import numpy as np
import csv
import re

set_buy_in_amount = 500

def get_file_stacks(file_path):
    """
    Gets the poker stacks from the file specified.

    Args:
        param1 str: Path to the CSV with the poker logs.

    Returns:
        list: Every index of stacks from the poker CSV.
    """
    stacks_lines = []

    # Reading file
    with open(file_path, "r") as file:
        lines = csv.reader(file, delimiter=",")
        for line in lines:
            if "Player stacks" in line[0] or "joined the game with a stack" in line[0] or "sit back with the"  in line[0] or "quits" in line[0] or "stand up" in line[0]:
                stacks_lines.append(line[0])

    return stacks_lines[::-1]

def init_poker_table(rev_stacks):
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
    global buy_in_value
    buy_in_value = {} # total value of all buy ins
    quit_val = {}
    global final_vals # last chip value player has
    final_vals = {}
    

    for line in rev_stacks:
        ## search lines that contain stood up or quit, take last one in list, set that equal to player final chip value
        match1 = re.search(r"The player \".*@\s(.*)\" (quits|stand up) (?:the game with a|with the) stack of (\d+)", line)

        if match1:  # if line is quits/stand up
            id = match1.group(1)
            final_value = int(match1.group(3))
            final_vals [id] = final_value
            continue

        match = re.search(r"The player \".*@\s(.*)\" (joined|sit back) (?:the game with a|with the) stack of (\d+)", line)

        if match:  # if line is joined/sit back
            id = match.group(1)
            buy_in_amount = int(match.group(3))
            if id == "sDvCEJwYSa":
                    print(line+str(buy_in_amount))
            
            if match.group(2) == "sit back":
                #quit_val[id] = buy_in_amount
                None
                            
            elif buy_in_amount == set_buy_in_amount:
                buy_in_value[id] = buy_in_amount if (not id in buy_in_value) else buy_in_value[id] + buy_in_amount
                if id == "sDvCEJwYSa":
                    #print(buy_in_amount)
                    None
                continue
            continue
        
        sep = line.split("|") # Separates each line in each stack
        round = []

        for player_bio in sep:  # else for lines that are player stack values
            id = player_bio[player_bio.find('@') + 1 : player_bio.find('"', player_bio.find('@') + 1)].strip() # Finds each id
            name = player_bio[player_bio.find('"') + 1 : player_bio.rfind("@") - 1] # Finds the name

            if not id in real_players:
                real_players[id] = [name] # Initializes new entry in players with first alias
            else:
                if name not in real_players[id]:
                    real_players[id].append(name) # Adds the new alias to player

            amount = int(player_bio[player_bio.find("(") + 1 : player_bio.rfind(")")]) # Finds amount of chips per round per person
            round.append({id: [amount, (amount - (0 if id not in buy_in_value else buy_in_value[id])) / 100]})

        round_list.append(round)
       
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
    fig, (p1, p2, p3) = plt.subplots(3, 1, figsize=(12, 8))

    colors = plt.cm.tab10(np.linspace(0, 1, len(player_list))) # Initializing a pre-set list of colors
    x = np.arange(1, len(rounds) + 1) # Creating the x-values array

    table = []

    for index, (player, aliases) in enumerate(player_list.items()): # Ranging through each player's games
        player_values = []
        cash_values = []

        for round_itr in rounds: # Going through every round
            player_amount = np.nan # Initializing a NaN value for each player
            cash_amount = np.nan

            for dict_values in round_itr:
                if player in dict_values:
                    player_amount = dict_values[player][0] # If the player has a value in chips, the amount is added
                    cash_amount = dict_values[player][1]
                    break
            
            player_values.append(player_amount)
            cash_values.append(cash_amount)

        p1.plot(x, player_values, label=" / ".join(aliases), color=colors[index])
        p2.plot(x, cash_values, label=" / ".join(aliases), color=colors[index])
    
    #loop thorugh final append to cash 
    table = []
    for player in final_vals:
        final_vals[player] = (final_vals[player] - buy_in_value[player]) /100
        table.append([player_list[player][0], final_vals[player]])        
    
    p1.set_title('Fuck GOA Poker Night ' + night_num)
    p1.set_xlabel('Round #')
    p1.set_ylabel('Chips')

    p2.set_xlabel('Round #')
    p2.set_ylabel('Money')

    p2.legend(fontsize='small', loc="upper left")

    table.insert(0, ["Name", "Results"])

    p3.axis('tight')
    p3.axis('off')
    vis_table = p3.table(cellText=table, colLabels=None, cellLoc = 'center', loc='center')
    vis_table.auto_set_font_size(False)
    vis_table.set_fontsize(10)

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
            stackos = get_file_stacks(file_name)
            break
        except Exception as e:
            print(e)
            file_name = input("Ledger CSV file path: ")

    night = input("Ledger night #: ")
    ps, rds = init_poker_table(stackos)
    create_plot_fig(ps, rds, night)

    print("Figure presented successfully.")

main()