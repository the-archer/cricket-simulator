#This file reads the denormalized data from a csv file and generates features and values for each ball
import csv
from collections import deque

# file is a csv file: headers are defined in the design doc,  
FILE_PATH = 'data_cleaning/odi_processed_data.csv'

# dictionary : key  - match_id, 
# value:list each ball, sorted in order of the ball , each list item is a dictionary containing all the items in the csv 

# after that will do more processing

def process_csv_file(file_path):
    data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            match_id = row['match_id']
            if match_id not in data:
                data[match_id] = []
            ball = row.copy()
            data[match_id].append(ball)
    return data

# Batsman average
# Batsman Strike rate
# Bowler average
# Bowler strike rate
# ------------------

# Batsman score
# Batsman bowls faced
# Batsman 4s scored
# Batsman 6s scored
# Bowler runs given 
# Bowler wickets taken
# Bowler balls bowled
# Batting team score
# Current run rate
# Batting team wickets remaining
# Batting team balls remaining
# Runs in last 30 balls
# Wickets in last 30 balls
# Batting team runs to win (if batting second)
# Required run rate (if batting second)


# Output : 
# Classification with probabilities: W1, W2, W3, W4,  W5, W6, 0, 1, 2, 3, 4, 6,
# W1 = bowled
# W2 = leg before
# W3 = caught
# W4 = caught and bowled
# W5 = stumped
# W6 = runout 

# feature is a list of list
# values is a list
def get_features_for_match(match_data):
    team_runs = 0
    team_wickets_rem = 10
    first_innings_target = 0
    second_innings = False
    bat_stat = {}
    bowl_stat = {}
    ball_score = deque()
    ball_score_cur = 0
    ball_wicket = deque()

    # put some dummy runs (3 rr) for start of innings
    for i in range(0, 15):
        ball_score.append(1)
        ball_score_cur += 1
        ball_score.append(0)
        ball_wicket.append(0)
        ball_wicket.append(0)
    ball_wicket_cur = 0
    features = [[], []]
    values = [[], []]
    ball_count = 0
    for ball in match_data:
        if not second_innings and ball['innings_number'] == '2':
            second_innings = True
            first_innings_target = team_runs + 1
            team_runs = 0
            team_wickets_rem = 10
            ball_count = 0
            ball_score = deque()
            ball_score_cur = 0
            ball_wicket = deque()
            # put some dummy runs (3 rr) for start of innings
            for i in range(0, 15):
                ball_score.append(1)
                ball_score_cur += 1
                ball_score.append(0)
                ball_wicket.append(0)
                ball_wicket.append(0)
            ball_wicket_cur = 0
        batsman = ball['batter_id']
        bowler = ball['bowler_id']
        if batsman not in bat_stat:
            bat_stat[batsman] = {'runs': 0, 'balls':0, 'fours': 0, 'sixes': 0}
        if bowler not in bowl_stat:
            bowl_stat[bowler] = {'runs': 0, 'balls':0, 'wickets': 0}

        runs_to_win = 0
        balls_remaining = 300 - ball_count
        reqd_rr = 0


        if ball['innings_number'] == '2':
            runs_to_win = first_innings_target - team_runs
            reqd_rr = (runs_to_win *6 ) / balls_remaining
        
        curr_rr =  (team_runs * 6) / ball_count if ball_count > 0 else 0
        
        bat_ave = ball['batter_average']
        bat_sr = ball['batter_strike_rate']
        bowl_ave = ball['baller_average']
        bowl_sr = ball['baller_strike_rate']
        if ball['innings_number'] == '1':
            features[0].append([bat_ave, bat_sr, bowl_ave, bowl_sr, bat_stat[batsman]['runs'], bat_stat[batsman]['balls'], bat_stat[batsman]['fours'],  
            bat_stat[batsman]['sixes'],bowl_stat[bowler]['runs'], bowl_stat[bowler]['wickets'], bowl_stat[bowler]['balls'],
            team_runs, curr_rr, team_wickets_rem, balls_remaining, ball_score_cur, ball_wicket_cur])
        elif ball['innings_number'] == '2':
            features[1].append([bat_ave, bat_sr, bowl_ave, bowl_sr, bat_stat[batsman]['runs'], bat_stat[batsman]['balls'], bat_stat[batsman]['fours'],  
            bat_stat[batsman]['sixes'],bowl_stat[bowler]['runs'], bowl_stat[bowler]['wickets'], bowl_stat[bowler]['balls'],
            team_runs, curr_rr, team_wickets_rem, balls_remaining, ball_score_cur, ball_wicket_cur, runs_to_win, reqd_rr])
            
        team_runs += int(ball['total'])
        team_wickets_rem -= int(ball['is_wicket'])
        ball_score_cur -= ball_score.popleft()
        ball_score.append(int(ball['total']))
        ball_score_cur += int(ball['total'])
        ball_wicket_cur -= ball_wicket.popleft()
        ball_wicket.append(int(ball['is_wicket']))
        ball_wicket_cur += int(ball['is_wicket'])
        if ball['is_noball'] != '1' and ball['is_wide_ball'] != '1':
            ball_count += 1
        bat_stat[batsman]['runs'] += int(ball['batter_runs'])
        if ball['is_wide_ball'] != '1':
            bat_stat[batsman]['balls'] += 1
        if ball['batter_runs'] == '4':
            bat_stat[batsman]['fours'] += 1
        if ball['batter_runs'] == '6':
            bat_stat[batsman]['sixes'] += 1
        bowl_stat[bowler]['runs'] += int(ball['total'])
        if ball['is_noball'] != '1' and ball['is_wide_ball'] != '1':
            bowl_stat[bowler]['balls'] += 1
        if ball['wicket_type'] != 'run out':
            bowl_stat[bowler]['wickets'] += int(ball['is_wicket'])
            
        value = ''
        if ball['is_wicket'] == '1':
            if ball['wicket_type'] in ['bowled', 'caught', 'caught and bowled', 
                                       'lbw', 'stumped', 'run out']:
                value = ball['wicket_type']
            else: 
                value = 0
        else:
            value = ball['batter_runs']
        
        values[int(ball['innings_number'])-1].append(value)
        
    return (features, values)


        
    
                
                
def write_features_to_file(features):
    with open('data_cleaning/features.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Batsman average', 'Batsman strike rate','Bowler average', 'Bowler strike rate',  'Batsman score','Batsman bowls faced', 'Batsman 4s scored','Batsman 6s scored', 'Bowler runs given', 
                     'Bowler wickets taken','Bowler balls bowled','Batting team score','Current run rate','Batting team wickets remaining',
                     'Batting team balls remaining','Runs in last 30 balls','Wickets in last 30 ball',
                     'Batting team runs to win (if batting second)','Required run rate (if batting second)'])
        writer.writerows(features[0])
        writer.writerows(features[1])      
              
def write_values_to_file(values):
    with open('data_cleaning/values.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for val in values[0]:
            writer.writerow([val])
        for val in values[1]:
            writer.writerow([val])    
        
            
        
            

def main():
    data = process_csv_file(FILE_PATH)
    first_innings_features = []
    second_innings_features = []
    first_innings_values = []
    second_innings_values = []
    print (len(data))
    features, values = get_features_for_match(data['1000887'])
    #print (features)
    for match_id in data:
        features, values = get_features_for_match(data[match_id])
        first_innings_features.append(features[0])
        second_innings_features.append(features[1])
        first_innings_values.append(values[0])
        second_innings_values.append(values[1])
    # write_features_to_file(features)
    # write_values_to_file(values)
      

if __name__ == "__main__":
  main()

        

