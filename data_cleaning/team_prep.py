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

def main():
    team1 = {}
    team={}
    if not glob.glob(os.path.join(FILE_PATH, '*.json')):
        raise "Check file path"
    for filename in glob.glob(os.path.join(FILE_PATH, '*.json')): #only process .JSON files in folder.      
        file_data =  process_file(filename)   
        match_id = get_match_id(filename)
        match_date = file_data["info"]["dates"][0]
        if match_date > '2023-01-01':
            for team_name in file_data["info"]["players"].keys():
                player = {}
                if team_name in team and file_data["info"]["gender"]=="female":
                    continue
                else:
                    team[team_name] = {}
                    for player_name in file_data["info"]["players"][team_name]:
                        team[team_name][file_data["info"]["registry"]["people"][player_name]] = player_name

    with open('teams.pkl', 'wb') as f:
        pickle.dump(team, f)

    print(team["India"])

if __name__ == "__main__":
    main()

