# This is outdated and does not work

from json import load
from predict import predict, gen_and_predict

game_time = float(input('Game time (minutes): ')) * 60
players = []
for i in range(10):
    level, cs, kills, deaths, assists = map(int, input(f'Player {i+1} stats: ').split())
    # level = 1
    # cs = 0
    # kills = 0
    # deaths = 0
    # assists = 0
    players.append([level, cs, kills, deaths, assists])

# Generate model input
y = gen_and_predict(game_time, players)

print('Blue team:')
for i in range(5):
    p = players[i]
    print(f'Level {p[0]:<2}  {p[1]:>3} CS  {p[2]:^3}/{p[3]:^3}/{p[4]:^3} KDA')
print('Red team:')
for i in range(5):
    p = players[5+i]
    print(f'Level {p[0]:<2}  {p[1]:>3} CS  {p[2]:^3}/{p[3]:^3}/{p[4]:^3} KDA')
print(f'\nChance of blue winning: {y*100:.1f}%')
