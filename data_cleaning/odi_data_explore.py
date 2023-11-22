import json
import os
import glob
import pprint
import csv

path = '../data/odis_json'
keywordList = []
all_deliveries = []
for filename in glob.glob(os.path.join(path, '*.json')): #only process .JSON files in folder.      
    with open('{filename}'.format(filename=filename)) as f:
        if filename == '../data/odis_json/1126729.json':
            print('hello')
            file_data = json.load(f)
            match_id = filename.split("/")[-1].split(".")[0]
            series_name = file_data["info"]["event"]["name"]
            gender = file_data["info"]["gender"]
            match_type = file_data["info"]["match_type"]
            match_date = file_data["info"]["dates"][0]
            match_city = file_data["info"]["city"]
            balls_per_over = file_data["info"]["balls_per_over"]
            first_innings = file_data["innings"][0]
            second_innings = file_data["innings"][1]
            
            for over in first_innings["overs"]:
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
                    ball['match_id']=match_id
                    ball['over_number']=over_number
                    ball['series_name']=series_name
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

with open('odi_processed_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['match_id', 'series_name', 'gender', 'match_type', 'match_date', 'match_city',
                'balls_per_over', 'over_number', 'ball_number', 'batter_id', 'batter_name', 'bowler_id', 'bowler_name',
                    'non_striker_id', 'non_striker_name', 'batter_runs', 'extras', 'total', 'is_legbye', 'is_noball', 'is_wide_ball',
                    'is_wicket', 'wicket_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(all_deliveries)):
        ##print(all_deliveries[i])
        writer.writerow(all_deliveries[i])          





