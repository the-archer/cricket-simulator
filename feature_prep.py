#This file reads the denormalized data from a csv file and generates features and values for each ball
import csv

# file is a csv file: headers are defined in the design doc,  
FILE_PATH = ''

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
# Batting team wickets lost
# Batting team balls faced
# Batting team runs to win (if batting second)
# Score on last X balls for the team (X = 20)
# Wicket Type on last X balls (X = 20) (0/1) (1 is wicket)



# Output : 
# Classification with probabilities: W1, W2, W3, W4,  W5, W6, 0, 1, 2, 3, 4, 6,
# W1 = bowled
# W2 = leg before
# W3 = caught
# W4 = caught and bowled
# W5 = stumped
# W6 = runout 


def get_features_for_match(match_data):
    team_runs = [0, 0]
    team_wickets = [0, 0]
    bat_stat = {}
    bowl_stat = {}
    ball_score = []
    ball_wicket = []
    for ball in match_data:

        

