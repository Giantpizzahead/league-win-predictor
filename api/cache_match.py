"""
Caches the match info and timeline for each match in the text file.
"""

import os
import pickle
from tracemalloc import start
from constants import *

# Load current matches
with open(match_filepath, 'r') as match_file:
    matches = [line.strip() for line in match_file.readlines()]

def save_match(name, info, timeline):
    print(f'Caching match data for {name}...')
    with open(f'{match_cache_folder}/{name}.pkl', 'wb') as fout:
        pickle.dump(info, fout)
    with open(f'{timeline_cache_folder}/{name}.pkl', 'wb') as fout:
        pickle.dump(timeline, fout)
    print('Save complete!')

print(f'Loaded {len(matches)} matches')
start_match = int(input('Match to start from (0-indexed): '))

# Process matches for each name
matches = matches[start_match:]
to_process = len(matches)
for match in matches:
    if os.path.isfile(f'{match_cache_folder}/{match}.pkl') and os.path.isfile(f'{timeline_cache_folder}/{match}.pkl'):
        print(f'Skipping match {match} (already processed)')
        to_process -= 1
        continue
    print(f'Processing match {match}...')

    # Query the Riot API
    info = lol_watcher.match.by_id(region, match)
    timeline = lol_watcher.match.timeline_by_match(region, match)

    save_match(match, info, timeline)
    to_process -= 1
    print(f'To process: {to_process}\n')

print('All matches processed!')
