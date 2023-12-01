import json
import os
import glob
import pprint
import csv
import pandas as pd

FILE_PATH = '../data/odis_json'

def process_file(filename: str) -> json:
    with open('{filename}'.format(filename=filename)) as f:
        file_data = json.load(f)
    return file_data        

def get_match_id(filename):
    return filename.split("/")[-1].split(".")[0]

def check_valid_match(file_data:json) -> bool:
    return len(file_data["innings"])!=2

def get_batter_stats(df):
    batter_sums = df.groupby('batter_id', as_index=False)[['batter_runs','is_wicket']].sum()
    batter_count = df.groupby('batter_id').size().reset_index(name='Count')
    batter_count['Count'] = batter_count['Count'].astype(int)
    batter_stats = pd.merge(batter_sums, batter_count, on='batter_id')
    batter_stats['batter_average'] = batter_stats['batter_runs'] / batter_stats['is_wicket'] 
    batter_stats['batter_strike_rate'] = batter_stats['batter_runs'] / batter_stats['Count'] *100
    return batter_stats

def get_baller_stats(df):
    baller_sums = df.groupby('bowler_id', as_index=False)[['batter_runs','is_wicket']].sum()
    baller_count = df.groupby('bowler_id').size().reset_index(name='Count')
    baller_count['Count'] = baller_count['Count'].astype(int)
    baller_stats = pd.merge(baller_sums, baller_count, on='bowler_id')
    baller_stats['baller_average'] = baller_stats['batter_runs']/ baller_stats['is_wicket'] 
    baller_stats['baller_strike_rate'] = baller_stats['Count'] / baller_stats['is_wicket']  
    return    baller_stats

def write_to_csv(fieldnames: list, filename:str, data:dict):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction = 'ignore')
        writer.writeheader()
        for i in range(len(data)):
            ##print(all_deliveries[i])
            writer.writerow(data[i])  
    print("File {} written successfully".format(filename))

def print_player_stats(df):
    batter_stats = get_batter_stats(df)
    baller_stats = get_baller_stats(df)
    player_stats = pd.merge(batter_stats,baller_stats,left_on='batter_id', right_on='bowler_id')
    print(player_stats['batter_id'])
    player_stats.rename(columns={"batter_id":"player_id"},inplace = True)
    print(player_stats['player_id'])
    player_stats.drop('bowler_id',axis=1, inplace=True)
    fieldnames = ['player_id','baller_average','baller_strike_rate','batter_average','batter_strike_rate']
    data = player_stats.to_dict('records') 
    write_to_csv(fieldnames, 'player_stats.csv', data)

def main():
    keywordList = []
    all_deliveries = []
    if not glob.glob(os.path.join(FILE_PATH, '*.json')):
        raise "Check file path"
    
    for filename in glob.glob(os.path.join(FILE_PATH, '*.json')): #only process .JSON files in folder.      
        file_data =  process_file(filename)   
        match_id = get_match_id(filename)
        gender = file_data["info"]["gender"]
        match_type = file_data["info"]["match_type"]
        match_date = file_data["info"]["dates"][0]
        match_city = file_data["info"]["city"] if 'city' in file_data["info"] else "NA"
        balls_per_over = file_data["info"]["balls_per_over"]
        if check_valid_match(file_data):
            continue
        first_innings = file_data["innings"][0]
        second_innings = file_data["innings"][1]
        all_innings = [first_innings,second_innings]
        innings_number =0
        
        for innings in all_innings:
            innings_number += 1 
            for over in innings["overs"]:
                over_number = over["over"]
                count = 0
                for delivery in over["deliveries"]:
                    ball_number = count
                    batter_id = file_data["info"]["registry"]["people"][delivery["batter"]]
                    batter_name = delivery["batter"]
                    bowler_id = file_data["info"]["registry"]["people"][delivery["bowler"]]
                    bowler_name = delivery["bowler"]
                    non_striker_id = file_data["info"]["registry"]["people"][delivery["non_striker"]]
                    non_striker_name = delivery["non_striker"]
                    batter_runs = delivery["runs"]["batter"]
                    extras = delivery["runs"]["extras"]
                    total = delivery["runs"]["total"]
                    is_noball = int()
                    wicket_type = int()
                    if 'extras' in delivery:
                        if 'legbyes' in delivery["extras"]:
                            is_legbye = 1
                        else:
                            is_legbye = 0   
                        if 'noballs' in delivery["extras"]:
                            is_noball = 1
                        else:
                            is_noball = 0
                        if 'wides' in delivery["extras"]:
                            is_wide_ball = 1
                        else:
                            is_wide_ball = 0   
                    else:
                        is_legbye = 0
                        is_wide_ball = 0
                        s_noball = 0         
                    
                    if 'wickets' in delivery:
                        is_wicket = 1
                        wicket_type = delivery["wickets"][0]["kind"]
                    else:
                        is_wicket = 0    
                    count += 1
                    ball = {}
                    ball['innings_number'] = innings_number
                    ball['match_id']=match_id
                    ball['over_number']=over_number
                    ball['gender']=gender
                    ball['match_type']=match_type
                    ball['match_date']=match_date
                    ball['match_city']=match_city
                    ball['balls_per_over']=balls_per_over

                    ball['ball_number']=ball_number
                    ball['batter_id']=batter_id
                    ball['batter_name']=batter_name
                    ball['bowler_id']=bowler_id
                    ball['bowler_name']=bowler_name
                    ball['non_striker_id']=non_striker_id
                    ball['non_striker_name']=non_striker_name
                    ball['batter_runs']=batter_runs
                    ball['extras']=extras
                    ball['total']=total
                    ball['is_legbye']=is_legbye
                    ball['is_noball']=is_noball
                    ball['is_wide_ball']=is_wide_ball
                    ball['is_wicket']=is_wicket
                    ball['wicket_type']=wicket_type
                    all_deliveries.append(ball)

    df = pd.DataFrame(all_deliveries)
    batter_stats = get_batter_stats(df)
    baller_stats = get_baller_stats(df)
    print_player_stats(df)
    final_data_frame = pd.merge(pd.merge(df,batter_stats[['batter_average','batter_strike_rate','batter_id']],on='batter_id'),baller_stats[['baller_average','baller_strike_rate', 'bowler_id']],on='bowler_id')
    final_data_frame = final_data_frame.sort_values(['match_id', 'innings_number', 'over_number', 'ball_number'], ascending=[True, True, True, True])


    all_deliveries_stats = final_data_frame.to_dict('records')              
    fieldnames = ['innings_number','match_id', 'gender', 'match_type', 'match_date', 'match_city',
                    'balls_per_over', 'over_number', 'ball_number', 'batter_id', 'batter_name', 'bowler_id', 'bowler_name',
                        'non_striker_id', 'non_striker_name', 'batter_runs', 'extras', 'total', 'is_legbye', 'is_noball', 'is_wide_ball',
                        'is_wicket', 'wicket_type','baller_average','baller_strike_rate','batter_average','batter_strike_rate']

    write_to_csv(fieldnames,'odi_processed_data.csv',all_deliveries_stats )      
    

if __name__ == "__main__":
    main() 

## Create a file function to read file and return something
## Create main function