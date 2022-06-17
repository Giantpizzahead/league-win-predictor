# ONLY WORKS ON MAC

import pygame
import os
import random
import pickle
import ctypes
from ctypes import wintypes
import json
import requests
import re
import time
from predict import predict
from sklearn.linear_model import LogisticRegression

pygame.init()
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
width = 150
height = display_height - 50
offset_x = display_width - width - 4
offset_y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (offset_x, offset_y)

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
done = False
fuchsia = (255, 0, 128)  # Transparency color

# print(pygame.font.get_fonts())
# print(pygame.font.match_font("sfnsrounded"))
font_1 = pygame.font.Font('/System/Library/Fonts/SFNSRounded.ttf', 18)
font_2 = pygame.font.Font('/System/Library/Fonts/SFNSRounded.ttf', 40)
title = font_1.render('Win Prediction', True, (220, 220, 220))
titleRect = title.get_rect()
titleRect.center = (width / 2, height / 2 - 24)

disp_batch = 1000
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
    champ_data = [-1 for _ in range(10)]
    curr_blue = 0
    curr_red = 5
    for i in range(len(player_data)):
        curr_champ = player_data[i]['championName'].lower()
        curr_champ = re.compile('[^a-z]').sub('', curr_champ)
        if curr_champ not in champ_ratings:
            raise Exception(f'{curr_champ} not in champ_ratings!')
        if player_data[i]['team'] == 'ORDER':
            champ_data[curr_blue] = champ_ratings[curr_champ]
            curr_blue += 1
        else:
            champ_data[curr_red] = champ_ratings[curr_champ]
            curr_red += 1
    for i in range(10):
        if champ_data[i] == -1:
            champ_data[i] = champ_ratings['jarvaniv']
    
    # Process players
    active_name = all_data['activePlayer']['summonerName']
    team_names = [[], []]
    players = [-1 for _ in range(10)]
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
        if players[i] == -1:
            players[i] = [1, 0, 0, 0, 0]
    global is_on_blue
    is_on_blue = (active_name in team_names[0])
    print(team_names, active_name, is_on_blue)
    
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
                'R_01_A': 2,
                'C_06_A': 2,
                'C_03_A': 2,
                'L_01_A': 2,
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
    
    # Get new win prediction
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

    screen.fill(fuchsia)  # Transparent background
    breakpoint = height * displayed_pred
    blue = (18, 65, 122)
    red = (122, 18, 18)
    if not is_on_blue:
        displayed_pred = 1 - displayed_pred
        blue, red = red, blue
    
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, width, height))
    pygame.draw.rect(screen, red, pygame.Rect(0, 0, width, height-breakpoint))
    pygame.draw.rect(screen, blue, pygame.Rect(0, height-breakpoint, width, breakpoint))
    
    screen.blit(title, titleRect)
    color = (min((1-displayed_pred) * 400, 255), min(displayed_pred * 400, 255), 0)
    textChance = font_2.render(f'{displayed_pred*100:.1f}%', True, color)
    textChanceRect = textChance.get_rect()
    textChanceRect.center = (width / 2, height / 2 + 11)
    screen.blit(textChance, textChanceRect)
    pygame.display.update()

    clock.tick(60)
