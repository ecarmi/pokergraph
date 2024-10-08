import matplotlib as plt
import numpy as np
import csv

stacks = []

with open ("Final_Ledger.csv", "r") as file:
    lines = csv.reader(file, delimiter=",")
    for line in lines:
        if "Player stacks" in line[0]:
            stacks.append(line[0])

rev_stacks = stacks[::-1]
print(rev_stacks)

players = []
dict_list = []
for line in rev_stacks:
    sep = line.split("#")
    round = []
    for player in sep:
        name =player[player.find('"')+len('"'):player.rfind("@")]
        if name not in players:
            players.append(name)
        amount = player[player.find("(")+len("("):player.rfind(")")]
        dict = {name: amount}
        round.append(dict)
    dict_list.append(round)



print(dict_list)


players.pop(0)
print(players)