Useful source for relatively complete in game events documentation: https://github-com.translate.goog/XHXIAIEIN/LeagueCustomLobby/wiki/client%3A--game-client?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp
Gives mappings for all the towers / inhibs

Killing an Elder Dragon while you are alive grants Aspect of the Dragon to all living teammates for 150 seconds.
By being alive while your team lands the killing blow on Baron Nashor, you get a 180 second buff.
So if you want to track when this buff is active, you'll need to record who is alive and dead at the time, along with when each person dies. Seems like a lot of work, but could be worth it maybe.

- Let's start with just tracking the # of each objective killed though.

4 dragons is a soul.

Inhibs can respawn, the events are clearly marked though.

For timeline events:
BUILDING_KILL is for towers and inhibs
ELITE_MONSTER_KILL is for dragons, heralds, barons, and elders

Tensorflow has RNNs and more complex deep learning stuff, Scikit Learn has many classic machine learning algos

For player skill:
If a player is unranked, you can use their most recent rank from a past season as well.
The overall win rate of a player is useful info.
In addition to champion win rates, it might help to give a number for KDA like (K+A)/D, or just K+A if D=0, for more accurate carry analysis.
Patterns may help make things slightly more accurate (win chance after a lost game, blue vs red side, etc).
Maybe give the results of the last few games played by that player to the model?
This would all take a lot of time per match...

- For now, just pass in their rank as one numeric variable (combine rank and division). You might need another boolean variable to mark whether or not they are unranked.
- Afterwards, try including champion win rate, KDA, and number of games played on that champion.

For team compositions:
The win rate of each champion in a specific elo bracket is very useful (it shows what's in the "meta" at each elo).
https://lolalytics.com/lol/ahri/build/?tier=silver - Use this site for every champion's win rates / predicted win rates after taking certain objectives.
https://leagueoflegends.fandom.com/wiki/List_of_champions/Ratings - Use to get basic statistics about champions and their damage types.

- For now, pass in the overall win rate of each champion in a specific elo bracket (average of players in the lobby).
- Afterwards, try including the 5 categorical ratings given by Riot, along with the style (AP/AD) of the champ and their mechanical difficulty.

OH ALSO WE NEED TO REMOVE REMADE GAMES FROM THE DATASET CAUSE THEY WILL CONFUSE THE AI A LOT OK THANKS
Also todo, display correct win prediction when you're on the red side