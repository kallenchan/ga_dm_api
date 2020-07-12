import requests
import json
import pandas as pd

def get_lobbies():
    response=requests.get("https://aoe2.net/api/lobbies?game=aoe2hd&language=en")
    lobbies=pd.json_normalize(response.json())
    ga_dm_lobbies=lobbies[['name','game_type','num_players','players','num_slots']][
        (lobbies.game_type==2) &
                              (lobbies.name.str.contains(r"\bis\b|\bGA\b",case=False)|
                               lobbies.name.str.contains(r"\bis\b|\bGADM\b",case=False)|
                               lobbies.name.str.contains(r"green",case=False)|
                               lobbies.name.str.contains(r"arabia",case=False)|
                              lobbies.name.str.contains("jabill",case=False))]
    return ga_dm_lobbies


df=get_lobbies()
for index,lobby in df.iterrows():
    data=pd.DataFrame(lobby.players)
    print(data[pd.notnull(data.name)][['name','rating']])
    print("Lobby Name: {}".format(lobby.name))
    print("Players: {} / {}".format(lobby.num_players,lobby.num_slots))
