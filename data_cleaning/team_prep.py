from datetime import datetime
import json
import os
import glob
import pprint
import csv
import pandas as pd
import pickle

from odi_data_explore import (
    process_file,
    get_match_id,
    check_valid_match,
    write_to_csv,
    FILE_PATH
)


def get_bowling_line_up(team_name, file_data):
    over_counts = {}
    bowling_line_up = []
    player_registry = file_data["info"]["registry"]["people"]
    for inning in file_data['innings']:
        if inning['team'] == team_name:
            continue
        for over in inning['overs']:
            bowler_name = over['deliveries'][0]['bowler']
            bowling_line_up.append((player_registry[bowler_name], bowler_name))
            if bowler_name in over_counts:
                over_counts[bowler_name] += 1
            else:
                over_counts[bowler_name] = 1
        
    # handle remaining overs 
    while len(bowling_line_up) < 50:        
        try:
            bowler_name = [x for x in sorted(over_counts.items(), key=lambda item: item[1], reverse=True) if x[1] < 10 and x[0]!=bowling_line_up[-1][1]][0][0]
            bowling_line_up.append((player_registry[bowler_name], bowler_name))
            over_counts[bowler_name] += 1
        except Exception as e:
            print(e)
            print(team_name)
            print(file_data["info"]["dates"][0])
            break
    return bowling_line_up

def main():
    team={}
    if not glob.glob(os.path.join(FILE_PATH, '*.json')):
        raise "Check file path"
    for filename in glob.glob(os.path.join(FILE_PATH, '*.json')): #only process .JSON files in folder.      
        file_data =  process_file(filename)   
        match_id = get_match_id(filename)
        match_date = file_data["info"]["dates"][0]
        if match_date >= '2023-10-05':
            for team_name in file_data["info"]["players"].keys():
                if file_data["info"]["gender"]=="female":
                    continue
                else:
                    team[team_name] = {}
                    team[team_name]['batting_line_up'] = {}
                    # get batting line up
                    for player_name in file_data["info"]["players"][team_name]:
                        team[team_name]['batting_line_up'][file_data["info"]["registry"]["people"][player_name]] = player_name
                    # get bowling line up 
                    team[team_name]['bowling_line_up'] = get_bowling_line_up(team_name, file_data)

    with open('teams.pkl', 'wb') as f:
        pickle.dump(team, f)
    
    print (team.keys())

if __name__ == "__main__":
    main()

