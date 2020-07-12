#!/bin/sh
search(){
    echo "Searching for AOE2 GA DM Lobbies";
    python $(dirname $0)/ga_dm_lobbies.py
}

helpInfo(){
    echo "AOE2 GA DM Lobby Finder"
}

if [ "$1" = "search" ]; then
    search
else
    helpInfo
fi