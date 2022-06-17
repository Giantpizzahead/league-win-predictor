from constants import *


def get_champ_counts(name, at_least=3):
    '''
    Get champion play counts and win rates for the given player.
    '''
    driver.get(f'https://www.leagueofgraphs.com/summoner/champions/na/{name}#championsData-all-queues')
    element = driver.find_element(By.CSS_SELECTOR, 'div[data-tab-id="championsData-all-queues"]')
    rows = element.find_elements(By.XPATH, './div/table/tbody/tr')[1:]
    champ_counts = []
    for row in rows:
        cols = row.find_elements(By.XPATH, './td')
        champ_name = cols[0].find_element(By.XPATH, './a/div/div[2]/span').text
        num_played = cols[1].find_element(By.XPATH, './a/progressbar/div/div[2]').text
        winrate = cols[2].find_element(By.XPATH, './a/progressbar/div/div[2]').text
        if int(num_played) < at_least:
            break
        champ_counts.append([champ_name, int(num_played), float(winrate[:-1]) / 100])
    return champ_counts


# champ_counts = get_champ_counts('ChallengerPogmaw')
# print(champ_counts)
champ_counts = get_champ_counts('krownetic')
print(champ_counts)
'''
Output:
[['Annie', 105, 0.467], ['Ahri', 89, 0.506], ['Jinx', 34, 0.47100000000000003], ['Ashe', 26, 0.5], ['Tristana', 26, 0.5770000000000001], ['Lux', 12, 0.33299999999999996], ['Nunu & Willump', 
10, 0.4], ['Amumu', 9, 0.556], ['Garen', 5, 0.4], ['Lillia', 4, 0.5], ['Sett', 3, 1.0], ['Master Yi', 3, 0.33299999999999996]]
'''

driver.quit()
