import os

players = os.listdir("player")

for player in players:
    os.makedirs(f"match/{player[:-4]}", exist_ok = True)