"""
Collects a list of Normal, Ranked Solo/Duo, and Ranked Flex matches using the match histories of various summoners.
"""

import random
from constants import *

# Load current users
with open(user_filepath, 'r') as user_file:
    names = [line.strip() for line in user_file.readlines()]

# Load current matches
with open(match_filepath, 'r') as match_file:
    matches = [line.strip() for line in match_file.readlines()]

def save_matches():
    print('Saving matches to text file...')
    with open(match_filepath, 'w') as match_file:
        for match in matches:
            match_file.write(match + '\n')
    print('Save complete!')

print(f'Loaded {len(names)} names, {len(matches)} matches')
start_name = int(input('Name to start from (0-indexed): '))
# TODO: Currently has 10 most recent matches
start_match = int(input('Match to start from (0-indexed): '))
num_matches = int(input('# of past matches to process: '))

# Process matches for each name
for name in names[start_name:]:
    print(f'Processing matches for {name}...')

    # Query the Riot API
    summoner = lol_watcher.summoner.by_name(region, name)
    match_history = lol_watcher.match.matchlist_by_puuid(region, summoner['puuid'], count=num_matches, queue=420)
    match_type = 'Ranked Solo/Duo'
    for match in match_history:
        '''
        q = lol_watcher.match.by_id(region, match)['info']['queueId']
        match_type = None
        if q == 400:
            match_type = 'Normal Draft'
        elif q == 420:
            match_type = 'Ranked Solo/Duo'
        elif q == 440:
            match_type = 'Ranked Flex'
        '''
        if match_type and match not in matches:
            print(f"Discovered {match} [{match_type}]")
            matches.append(match)
    save_matches()
    print(f'Current match count: {len(matches)}\n')

print('All users processed!')
