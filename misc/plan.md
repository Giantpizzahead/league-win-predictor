# Entry Level

Give the AI enough info to create a very simple win predictor.

Collect game data through either the Riot API (rate limited) or third party sites like League of Graphs.

Third party sites for champion statistics:
League of Graphs - https://www.leagueofgraphs.com/champions/stats/ahri
Mobalytics - https://app.mobalytics.gg/lol/champions/ahri/build
U.gg - https://u.gg/lol/champions/ahri/build

Third party sites for player statistics:
League of Graphs - https://www.leagueofgraphs.com/summoner/na/krownetic
Mobalytics - https://app.mobalytics.gg/lol/profile/na/krownetic/overview
Op.gg - https://na.op.gg/summoners/na/krownetic
U.gg - https://u.gg/lol/profile/na1/krownetic/overview

Pipeline:
create_data.py
data_loader.py
(some model).py

## Inputs

Apply feature scaling for all inputs.

- Game time
    - 1 float
- KDA of each player
    - 30 integers: 3 integers (kills, deaths, assists) for each of the 5 blue and 5 red players in the game

Players should be input in a specific, constant order (Blue top, jungle, mid, adc, supp, followed by the red team)

## Outputs

- Win probability prediction
    - 1 float from 0 to 1 representing chance of winning (0 = blue, 1 = red)
    - Can be converted to % chance probability by plotting predicted values with actual values and manually observing cutoff points

## Evaluation

- The area under the receiver operating characteristic (AUROC)

# Other things to possibly consider

- Number of objectives taken (turrets, inhibs, rift herald, dragons, barons)
- Ranks of players (if currently unranked, use previous season rankings)
- Player win rates on champions
- General win rates on champions (is this champion meta?)
- Specific win rate of current champion matchups and/or synergies
- Mastery points?