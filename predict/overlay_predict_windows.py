# ONLY WORKS ON WINDOWS

from inspect import trace
from mimetypes import types_map
import pygame
import win32api
import win32con
import win32gui
import os
import re
import ctypes
from ctypes import wintypes
import json
import requests
import pickle
import time
from predict import predict
from sklearn.linear_model import LogisticRegression

# Amount to scale the UI by (Higher values = Bigger size)
scaling_factor = 0.7

user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
SetWindowPos = user32.SetWindowPos

display_width = win32api.GetSystemMetrics(0)
display_height = win32api.GetSystemMetrics(1)
width = round(200*scaling_factor)
height = round(86*scaling_factor)
offset_x = display_width - width - 5
offset_y = 44
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (offset_x, offset_y)

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
done = False
fuchsia = (255, 0, 128)  # Transparency color

# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
SetWindowPos(pygame.display.get_wm_info()['window'], -1, offset_x, offset_y, 0, 0, 0x0001)

# print(pygame.font.match_font("segoeuiblack"))
font_1 = pygame.font.Font('C:\WINDOWS\Fonts\seguisb.ttf', round(20*scaling_factor))
font_2 = pygame.font.Font('C:\WINDOWS\Fonts\seguisb.ttf', round(48*scaling_factor))
title = font_1.render('Win Prediction', True, (200, 200, 200))
titleRect = title.get_rect()
titleRect.center = (width / 2, height / 2 - round(25*scaling_factor))

disp_batch = 1000//100
past_predictions = [0.5 for _ in range(disp_batch)]
win_prediction = 0.5
is_on_blue = True

def gen_input(all_data):
    player_data = all_data['allPlayers']
    game_data = all_data['gameData']
    event_data = all_data['events']
    game_time = game_data['gameTime']
    
    # Process general game data
    with open(f'data/champ_cache/champ_ratings.pkl', 'rb') as fin:
        champ_ratings = pickle.load(fin)
    curr_blue = 0
    curr_red = 5
    champ_data = [None for _ in range(10)]
    for i in range(len(player_data)):
        curr_champ = player_data[i]['championName'].lower()
        curr_champ = re.compile('[^a-z]').sub('', curr_champ)
        if curr_champ not in champ_ratings:
            print(f'Warning: {curr_champ} not in champ_ratings, defaulting to Annie')
            curr_champ = 'annie'
        if player_data[i]['team'] == 'ORDER':
            champ_data[curr_blue] = champ_ratings[curr_champ]
            curr_blue += 1
        else:
            champ_data[curr_red] = champ_ratings[curr_champ]
            curr_red += 1
    for i in range(10):
        if not champ_data[i]:
            champ_data[i] = champ_ratings['jarvaniv']
    
    # Process players
    active_name = all_data['activePlayer']['summonerName']
    team_names = [[], []]
    players = [None for _ in range(10)]
    curr_blue = 0
    curr_red = 5
    for i in range(len(player_data)):
        p = player_data[i]
        name = p['summonerName']
        level = p['level']
        cs = p['scores']['creepScore']
        kills = p['scores']['kills']
        deaths = p['scores']['deaths']
        assists = p['scores']['assists']
        if p['team'] == 'ORDER':
            team_names[0].append(name)
            players[curr_blue] = [level, cs, kills, deaths, assists]
            curr_blue += 1
        else:
            team_names[1].append(name)
            players[curr_red] = [level, cs, kills, deaths, assists]
            curr_red += 1
    for i in range(10):
        if not players[i]:
            players[i] = [1, 0, 0, 0, 0]
    global is_on_blue
    is_on_blue = (active_name in team_names[0])
    # print(team_names, active_name, is_on_blue)
    
    # Process events
    curr_buildings = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    curr_monsters = [[0, 0, 0], [0, 0, 0]]
    for event in event_data['Events']:
        if event['EventName'] == 'TurretKilled':
            type_to_index = {
                'L_03_A': 0,
                'C_05_A': 0,
                'R_03_A': 0,
                'L_02_A': 1,
                'C_04_A': 1,
                'R_02_A': 1,
                'L_01_A': 2,
                'C_06_A': 2,
                'C_03_A': 2,
                'R_01_A': 2,
                'C_07_A': 2,
                'C_02_A': 4,
                'C_01_A': 4
            }
            t = 0 if 'T2' in event['TurretKilled'] else 1
            curr_buildings[t][type_to_index[event['TurretKilled'][-6:]]] += 1
        elif event['EventName'] == 'InhibKilled':
            t = 0 if 'T2' in event['InhibKilled'] else 1
            curr_buildings[t][3] += 1
        elif event['EventName'] == 'HeraldKill':
            t = 0 if event['KillerName'] in team_names[0] else 1
            curr_monsters[t][0] += 1
        elif event['EventName'] == 'DragonKill':
            t = 0 if event['KillerName'] in team_names[0] else 1
            curr_monsters[t][1] += 1
        elif event['EventName'] == 'BaronKill':
            t = 0 if event['KillerName'] in team_names[0] else 1
            curr_monsters[t][2] += 1
    
    # Form final input
    x = [game_time]
    x += curr_buildings[0] + curr_buildings[1]
    x += curr_monsters[0] + curr_monsters[1]
    for i in range(10):
        x += players[i]
    for i in range(len(champ_data[0])):
        blue_v = sum([v[i] for v in champ_data[:5]])
        red_v = sum([v[i] for v in champ_data[5:]])
        x += [blue_v, red_v]
    return x

clock = pygame.time.Clock()
last_update = -1
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # Get current win prediction
    if time.time() - last_update > 3:
        try:
            # TODO: Maybe don't have False for verifying HTTPS connections
            all_data = json.loads(requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False).content)
            x = gen_input(all_data)
            win_prediction = predict(x)
            # print(f'{win_prediction} win prediction at game time {x[0]:.3f}')
            print(f'\n{win_prediction} win prediction with inputs:\n{x}')
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('Connection failed, is the game open?')
        last_update = time.time()
    past_predictions.append(win_prediction)
    
    # Set current win prediction to be the weighted average of the last few predictions
    few_predictions = past_predictions[-disp_batch:]
    weights = [1 + 2 / disp_batch * i for i in range(disp_batch)]
    displayed_pred = sum([few_predictions[i] * weights[i] for i in range(disp_batch)]) / sum(weights)
    displayed_pred = min(max(displayed_pred, 0), 1)
    
    breakpoint = width * displayed_pred
    blue = (18, 65, 122)
    red = (122, 18, 18)
    if not is_on_blue:
        displayed_pred = 1 - displayed_pred
        blue, red = red, blue

    screen.fill(fuchsia)  # Transparent background
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, width, height))
    pygame.draw.rect(screen, blue, pygame.Rect(0, 0, breakpoint, height))
    pygame.draw.rect(screen, red, pygame.Rect(breakpoint, 0, width-breakpoint, height))
    
    screen.blit(title, titleRect)
    color = (min((1-displayed_pred) * 350, 255), min(displayed_pred * 350, 255), 0)
    textChance = font_2.render(f'{displayed_pred*100:.1f}%', True, color)
    textChanceRect = textChance.get_rect()
    textChanceRect.center = (width / 2, height / 2 + round(11*scaling_factor))
    screen.blit(textChance, textChanceRect)
    pygame.display.update()

    clock.tick(60)
