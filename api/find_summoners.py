"""
Collects a list of summoner names by branching out from the match history of those already in the list.
"""

import random
from constants import *

# Base names that cover all ranks
starting_names = ['Civilians', 'deltaromega', 'Twck8', 'boomdadoom', 'lizzlebizzle',
                  'OiSkunk', 'Xcipe', 'Legacy', 'Haxorr', 'Geiger', 'Bmfx']

# Load current users
with open(user_filepath, 'r') as user_file:
    names = [line.strip() for line in user_file.readlines()]
    if not names:
        print('No summoners in text file, starting with default names...')
        names = starting_names

def save_users():
    print('Saving users to text file...')
    with open(user_filepath, 'w') as user_file:
        for name in names:
            user_file.write(name + '\n')
    print('Save complete!')

# Get target # of names
print(f'Starting with {len(names)} names')
target = int(input('Target # of names: '))


# Branch out from known names to get more
while len(names) < target:
    # Branch out from a random summoner
    # TODO: Should change this to all summoners in names at some point
    name = names[random.randint(0, 12)]
    recent_num = random.randint(0, 19)
    print(f'Branching using recent match {recent_num+1} of {name}...')

    # Query the Riot API
    summoner = lol_watcher.summoner.by_name(region, name)
    match_history = lol_watcher.match.matchlist_by_puuid(region, summoner['puuid'])
    if len(match_history) <= recent_num:
        print('Not enough matches in history, skipping')
        continue
    match = lol_watcher.match.by_id(region, match_history[recent_num])
    new_puuids = match['metadata']['participants']
    for puuid in new_puuids:
        new_summoner = lol_watcher.summoner.by_puuid(region, puuid)
        new_name = new_summoner['name']
        if new_name not in names and new_name.isascii():
            # Get this summoner's rank
            rank = lol_watcher.league.by_summoner(region, new_summoner['id'])
            for r in rank:
                if r['queueType'] == 'RANKED_SOLO_5x5':
                    print(f"Discovered {new_name} [{r['tier'].title()} {r['rank']}]")
                    break
            else:
                rank = {'tier': 'Unranked', 'rank': ':('}
                print(f"Discovered {new_name} [Unranked]")
            names.append(new_name)
            if len(names) == target:
                break
    save_users()
    print(f'Current name count: {len(names)}\n')

print('Target met!')
