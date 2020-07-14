#!/bin/sh
search(){
    echo "Searching for AOE2 GA DM Lobbies";
    python $(dirname $0)/ga_dm_lobbies.py
}

helpInfo(){
    echo "Welcome to the AOE2 GA DM Lobby Finder"
    echo
    
}

if [ "$1" = "search" ]; then
    search
    echo "Search Results"
else
    helpInfo
fi