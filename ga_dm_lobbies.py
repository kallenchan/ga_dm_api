import requests
import json
import pandas as pd

ga_dm_players = ['JAbill',
                'TROJN',
                'huskserk']

def get_lobbies():
    response=requests.get("https://aoe2.net/api/lobbies?game=aoe2hd&language=en")
    lobbies=pd.json_normalize(response.json())
    ga_dm_lobbies=lobbies[['lobby_id','name','game_type','num_players','players','num_slots']][
        (lobbies.game_type==2) &
                              (lobbies.name.str.contains(r"\bis\b|\bGA\b",case=False)|
                               lobbies.name.str.contains(r"\bis\b|\bGADM\b",case=False)|
                               lobbies.name.str.contains(r"green",case=False)|
                               lobbies.name.str.contains(r"arabia",case=False)|
                              lobbies.name.str.contains("jabill",case=False))]
    return ga_dm_lobbies


lobbies_df=get_lobbies()
for index,lobby in lobbies_df.iterrows():
    data=pd.DataFrame(lobby.players)
    print("              ")
    print("Game Number {}".format(index))
    print("              ")
    print(data[pd.notnull(data.name)][['name','rating']])
    print("Lobby Name: {}".format(lobby.name))
    print("Players: {} / {}".format(lobby.num_players,lobby.num_slots))
    # filt =  pd.DataFrame(lobby.players)['name'].str.lower().isin(ga_dm_players)
    # print(pd.DataFrame(lobby.players)[['name','rating']][filt])

print({"{} {} Found".format(len(lobbies_df),"Results")})

lobby_ids=lobbies_df.loc[:,'lobby_id']
def join_game(lobby_ids):
    selected_game=input("Please select a game")
    # webbrowser.open_new(steam_protocol)
    if float(selected_game) in lobby_ids.index:
        steam_protocol="steam://joinlobby/221380/{}".format(lobby_ids.to_dict()[float(selected_game)])
        print("Joining Game"+" "+steam_protocol)
    else:
        print("Invalid Game Number")
        join_game(lobby_ids)

if (len(lobbies_df)>0):
    join_game(lobby_ids)

