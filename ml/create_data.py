"""
Creates the ML inputs and outputs using the cached match info and timeline.
"""

import pickle
from constants import *

def load_match(name):
    with open(f'{match_cache_folder}/{name}.pkl', 'rb') as fin:
        info = pickle.load(fin)
    with open(f'{timeline_cache_folder}/{name}.pkl', 'rb') as fin:
        timeline = pickle.load(fin)
    return info, timeline

def gen_data(name, info, timeline):
    # Only process non-remade games
    if info['info']['gameDuration'] < 600:
        print(f'Skipping {name} (remade)...')
        return
    
    # Swap roles around if they aren't in the right order
    # This is so the ML model consistently gets the same roles in the same spots
    role_perm = [-1 for _ in range(10)]
    expected_role = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
    unknown_roles = []
    for i in range(5):
        role = info['info']['participants'][i]['teamPosition']
        if not role:
            unknown_roles.append(i)
        else:
            role_perm[i] = expected_role.index(role)
    for v in unknown_roles:
        for i in range(5):
            if i not in role_perm[:5]:
                role_perm[v] = i
                break
    unknown_roles = []
    for i in range(5):
        role = info['info']['participants'][5+i]['teamPosition']
        if not role:
            unknown_roles.append(5+i)
        else:
            role_perm[5+i] = 5+expected_role.index(role)
    for v in unknown_roles:
        for i in range(5, 10):
            if i not in role_perm[5:]:
                role_perm[v] = i
                break
    assert(-1 not in role_perm)
    
    # Process general game data
    with open(f'{champ_cache_folder}/champ_ratings.pkl', 'rb') as fin:
        champ_ratings = pickle.load(fin)
    champ_data = []
    
    for i in range(10):
        curr_champ = info['info']['participants'][i]['championName'].lower()
        if curr_champ not in champ_ratings:
            raise Exception(f'{curr_champ} not in champ_ratings!')
        champ_data.append(champ_ratings[curr_champ])
    
    # Create one input for every snapshot
    frames = timeline['info']['frames']
    curr_kills = [0 for _ in range(11)]
    curr_deaths = [0 for _ in range(11)]
    curr_assists = [0 for _ in range(11)]
    curr_buildings = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    curr_monsters = [[0, 0, 0], [0, 0, 0]]
    all_inputs = []
    all_outputs = []
    for frame in frames:
        game_time = frame['timestamp'] / 1000
        # Process events
        for event in frame['events']:
            if event['type'] == 'CHAMPION_KILL':
                curr_deaths[event['victimId']] += 1
                if event['killerId'] != 0:
                    curr_kills[event['killerId']] += 1
                if 'assistingParticipantIds' in event:
                    for id in event['assistingParticipantIds']:
                        curr_assists[id] += 1
            elif event['type'] == 'BUILDING_KILL':
                t = 1 - (event['teamId'] // 100 - 1)
                if event['buildingType'] == 'INHIBITOR_BUILDING':
                    curr_buildings[t][3] += 1
                elif event['buildingType'] == 'TOWER_BUILDING':
                    type_to_index = {'OUTER_TURRET': 0, 'INNER_TURRET': 1, 'BASE_TURRET': 2, 'NEXUS_TURRET': 4}
                    curr_buildings[t][type_to_index[event['towerType']]] += 1
            elif event['type'] == 'ELITE_MONSTER_KILL':
                t = event['killerTeamId'] // 100 - 1
                if t == 2:
                    continue
                type_to_index = {'RIFTHERALD': 0, 'DRAGON': 1, 'BARON_NASHOR': 2}
                curr_monsters[t][type_to_index[event['monsterType']]] += 1
                
        # Process player snapshots
        players = frame['participantFrames']
        player_data = []
        for i in range(1, 11):
            p = players[str(i)]
            # champ_id = info['info']['participants'][i-1]['championId']
            level = p['level']
            cs = p['jungleMinionsKilled'] + p['minionsKilled']
            player_data.append([level, cs, curr_kills[i], curr_deaths[i], curr_assists[i]])
        blue_won = info['info']['participants'][0]['win']
        
        # Generate ML input and output
        inputs = [game_time]
        inputs += curr_buildings[0] + curr_buildings[1]
        inputs += curr_monsters[0] + curr_monsters[1]
        for v in role_perm:
            inputs += player_data[v]
        for i in range(len(champ_data[0])):
            blue_v = sum([v[i] for v in champ_data[:5]])
            red_v = sum([v[i] for v in champ_data[5:]])
            inputs += [blue_v, red_v]
        outputs = [blue_won]
        all_inputs.append(inputs)
        all_outputs.append(outputs)
    save_data(name, all_inputs, all_outputs)

def save_data(name, inputs, outputs):
    print(f'Saving data for {name}...')
    with open(f'{input_folder}/{name}.pkl', 'wb') as fout:
        pickle.dump(inputs, fout)
    with open(f'{output_folder}/{name}.pkl', 'wb') as fout:
        pickle.dump(outputs, fout)
    print('Save complete!')

# Load current matches
with open(match_filepath, 'r') as match_file:
    matches = [line.strip() for line in match_file.readlines()]

print(f'Loaded {len(matches)} matches')
start_name = int(input('Name to start from (0-indexed): '))
print('Generating data...')

matches = matches[start_name:]
to_process = len(matches)
for match in matches:
    info, timeline = load_match(match)
    gen_data(match, info, timeline)
    to_process -= 1
    print(f'To process: {to_process}\n')

print('Data generation complete!')
