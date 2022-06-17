from ctypes import util
from constants import *
import pickle
import re


def get_champ_ratings():
    '''
    Get Riot's official champion ratings.
    '''
    manual_mapping = {'nunuwillump': 'nunu', 'wukong': 'monkeyking'}
    
    driver.get(f'https://leagueoflegends.fandom.com/wiki/List_of_champions/Ratings')
    element = driver.find_element(By.CSS_SELECTOR, '.table-wide-inner')
    rows = element.find_elements(By.XPATH, './table/tbody/tr')
    champ_ratings = {}
    for row in rows:
        cols = row.find_elements(By.XPATH, './td')
        champ_name = cols[0].get_attribute('data-sort-value').lower()
        champ_name = re.compile('[^a-z]').sub('', champ_name)
        if champ_name in manual_mapping:
            champ_name = manual_mapping[champ_name]
        damage = int(cols[3].text)
        toughness = int(cols[4].text)
        control = int(cols[5].text)
        mobility = int(cols[6].text)
        utility = int(cols[7].text)
        damage_style = int(cols[8].get_attribute('data-sort-value'))
        damage_rating = 0 if cols[9].text == 'Physical' else 1
        difficulty = int(cols[10].text)
        champ_ratings[champ_name] = [damage, toughness, control, mobility, utility, damage_style, damage_rating, difficulty]
        print(f'Processed {champ_name}')
    return champ_ratings

champ_ratings = get_champ_ratings()
print(champ_ratings)
with open(f'{champ_cache_folder}/champ_ratings.pkl', 'wb') as fout:
    pickle.dump(champ_ratings, fout)

driver.quit()
