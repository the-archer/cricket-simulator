# main function which runs the match...

# classses:
# team , score, multiple players, lineup, (batting / bowling)

# player
# score, balls faced, skill stats (ave, sr)
# bowls balled, wickets taken

# match state, overs, each over will have balls
# 
from enum import Enum
import pickle
import names
import random
import argparse
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier
import pickle
from collections import deque
import csv
import datetime
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class SimulateMode(Enum):
    MANUAL = 0
    AUTO = 1

class BatterState(Enum):
    DID_NOT_BAT = 0
    CURRENTLY_BATTING = 1
    DISMISSED = 2
    

class Player:
    def __init__(self, player_id, first_name: str, last_name: str, bt_ave: float, bt_sr: float, bowl_ave: float, bowl_sr: float):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.batting_average = bt_ave
        self.batting_sr = bt_sr
        self.bowling_average = bowl_ave
        self.bowling_sr = bowl_sr
        
        self.batting_runs = 0
        self.batting_balls = 0
        self.batting_fours = 0
        self.batting_sixes = 0
        self.batter_state = BatterState.DID_NOT_BAT 
        
        self.bowling_runs = 0
        self.bowling_balls = 0
        self.overs = 0
        self.wickets = 0
    
class Team:
    def __init__(self, batting_line_up: List[Player], bowling_line_up: List[int], team_name):
        self.batting_line_up = batting_line_up
        self.bowling_line_up = bowling_line_up
        self.team_name = team_name
        self.score = 0
        self.wickets = 0
        self.overs = 0
        self.balls = 0
        
 
class Match:
    def __init__(self, team_1, team_2, first_innings_model: RandomForestClassifier, second_innings_model: RandomForestClassifier):
        self.team_1= team_1
        self.team_2 = team_2
        self.first_innings_model = first_innings_model
        self.second_innings_model = second_innings_model
        self.first_innings_score = 0
        self.match_log = []
        
    def simulate_match(self, mode):
        batting_team = self.team_1                
        bowling_team = self.team_2
        end_of_innings_flag = False
        for innings in [1, 2]:
            batter = batting_team.batting_line_up[0]
            non_striker = batting_team.batting_line_up[1]
            ball_score = deque()
            ball_score_cur = 0
            ball_wicket = deque()
            ball_wicket_cur = 0
            # put some dummy runs (3 rr) for start of innings
            for i in range(0, 15):
                ball_score.append(1)
                ball_score_cur += 1
                ball_score.append(0)
                ball_wicket.append(0)
                ball_wicket.append(0)
            for over_no in range(0, 50):
                bowler = bowling_team.batting_line_up[bowling_team.bowling_line_up[over_no]]
                ball = 1
                while ball <= 6:
                    if mode == SimulateMode.MANUAL:
                        input()
                    res = get_bowl_result_model(batter, bowler, batting_team, ball_score_cur, ball_wicket_cur,
                                                self.first_innings_score, self.first_innings_model, self.second_innings_model)
                    log = {"team_1": self.team_1.team_name, "team_2": self.team_2.team_name, "innings": innings, "over": over_no, "ball": ball, 
                           "over_worm": over_no + ball/6, "batter": batter.first_name[0] + " " + batter.last_name, 
                           "bowler": bowler.first_name[0] + " " + bowler.last_name}
                    if innings == 2:
                        log["runs_to_win"] = self.first_innings_score + 1 - batting_team.score
                        log["target"] = self.first_innings_score + 1
                    ball_wicket_cur -= ball_wicket.popleft()
                    ball_score_cur -= ball_score.popleft()
                    if not res.isdigit():
                        batting_team.wickets += 1
                        batter.batting_balls += 1
                        bowler.bowling_balls += 1
                        bowler.wickets += 1
                        print(f"{over_no}.{ball}: {bowler.last_name} to {batter.last_name}: {res} OUT!")
                        print(f"{batter.last_name}: {batter.batting_runs}({batter.batting_balls})")
                        log["wicket"] = res
                        log["runs"] = 0
                        if end_of_innings(batting_team, innings, self.first_innings_score):
                            end_of_innings_flag = True
                            self.match_log.append(log)
                            break
                        batter = batting_team.batting_line_up[batting_team.wickets + 1]
                        ball_wicket.append(1)
                        ball_wicket_cur += 1
                        ball_score.append(0)
                    else:
                        res = int(res)
                        batting_team.score += res
                        batter.batting_runs += res
                        batter.batting_balls += 1
                        if res == 4:
                            batter.batting_fours += 1
                        if res == 6:
                            batter.batting_sixes += 1
                        bowler.bowling_runs += res
                        bowler.bowling_balls += 1
                        print(f"{over_no}.{ball}: {bowler.last_name} to {batter.last_name}: {res} run(s)")
                        log["runs"] = res
                        ball_wicket.append(0)
                        ball_score.append(res)
                        ball_score_cur += res
                        if res%2 == 1:
                            batter, non_striker = non_striker, batter
                    log["score"] = batting_team.score
                    log["wickets_lost"] = batting_team.wickets
                    if innings == 2:
                        log["runs_to_win"] = self.first_innings_score + 1 - batting_team.score
                        log["target"] = self.first_innings_score + 1        
                    self.match_log.append(log)
                    if end_of_innings(batting_team, innings, self.first_innings_score):
                        end_of_innings_flag = True
                        break
                        
                    ball+=1
                    batting_team.balls = ball
                    batting_team.overs = over_no
                if end_of_innings_flag:
                    end_of_innings_flag = False
                    break
                bowler.overs += 1
                print (f"End of over {over_no+1}: Score: {batting_team.score}/{batting_team.wickets} \t" 
                    f"{batter.last_name}: {batter.batting_runs}({batter.batting_balls}) \t" 
                    f"{non_striker.last_name}: {non_striker.batting_runs}({non_striker.batting_balls}) \t" 
                    f"{bowler.last_name}: {bowler.overs}-0-{bowler.wickets}-{bowler.bowling_runs}\n")
                batter, non_striker = non_striker, batter
            if innings == 1:
                print(f"\nEnd of innings 1: Score: {batting_team.score}/{batting_team.wickets} in {over_no}.{ball} overs")
                self.first_innings_score = batting_team.score
                batting_team = self.team_2
                bowling_team = self.team_1
            if innings == 2:
                print(f"\nEnd of innings 2: Score: {batting_team.score}/{batting_team.wickets} in {over_no}.{ball} overs")
                if batting_team.score > self.first_innings_score:
                    print(f"{self.team_2.team_name} won by {10-batting_team.wickets} wickets")
                elif batting_team.score < self.first_innings_score:
                    print(f"{self.team_1.team_name} won by {self.first_innings_score - batting_team.score} runs")
                else:
                    print("Match tied!")

    def save_log(self):
        file_name = "match_logs/"
        if self.team_1.team_name < self.team_2.team_name:
            file_name += self.team_1.team_name.replace(" ", "") + "vs" + self.team_2.team_name.replace(" ", "") + "_"
        else: 
            file_name += self.team_2.team_name.replace(" ", "") + "vs" + self.team_1.team_name.replace(" ", "") + "_"
        file_name += datetime.date.today().strftime("%Y%m%d") + "_"
        
        index = 1
        while os.path.exists(file_name + str(index) + ".csv"):
            index += 1
        file_name += str(index) + ".csv"
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['team_1', 'team_2', 'innings', 'over', 'ball', 'over_worm', 'batter', 'bowler', 'runs', 'wicket', 'score', 'wickets_lost', 'runs_to_win', 'target']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in self.match_log:
                writer.writerow(log)

        
                

def get_bowl_result_model(batter: Player, bowler: Player, team: Team, runs_last_30_balls: int, 
                      wickets_last_30_balls: int, first_innings_score: int, first_innings_model: RandomForestClassifier,
                      second_innings_model: RandomForestClassifier) -> str:
    prob_dist = get_prob_dist_for_ball(batter, bowler, team, runs_last_30_balls, wickets_last_30_balls, 
                             first_innings_score, first_innings_model, second_innings_model) 
    rand = random.random()
    running_sum = 0
    for res, prob in prob_dist.items():
        running_sum += prob
        if rand < running_sum:
            return res
    return '0'
                   
            
def get_prob_dist_for_ball(batter: Player, bowler: Player, team: Team, runs_last_30_balls: int, 
                      wickets_last_30_balls: int, first_innings_score: int, first_innings_model: RandomForestClassifier,
                      second_innings_model: RandomForestClassifier) -> Dict:
    total_balls = team.overs * 6 + team.balls
    curr_rr = (team.score*6) / total_balls if total_balls > 0 else 0
    features = [batter.batting_average, batter.batting_sr, bowler.bowling_average, bowler.bowling_sr,
                batter.batting_runs, batter.batting_balls, batter.batting_fours, batter.batting_sixes,
                bowler.bowling_runs, bowler.wickets, bowler.bowling_balls, team.score, curr_rr, 10 - team.wickets, 
                300 - total_balls, runs_last_30_balls, wickets_last_30_balls]
    if first_innings_score:
        runs_to_win = first_innings_score + 1 - team.score
        reqd_rr = (runs_to_win * 6) / (300 - total_balls)
        features += [runs_to_win, reqd_rr]
        prob = second_innings_model.predict_proba([features])[0]
        return dict(zip(second_innings_model.classes_, prob))
    else:
        prob = first_innings_model.predict_proba([features])[0]
        return dict(zip(first_innings_model.classes_, prob))
                       
                                
def end_of_innings(batting_team, innings, first_innings_score) -> bool:
    if batting_team.wickets == 10:
        return True
    if innings == 2 and batting_team.score > first_innings_score:
        return True
    return False
                  

def get_bowling_line_up(team_name:str, batting_line_up: List[Player]) -> List[int]:
    all_teams = get_all_teams()
    bowling_line_up = all_teams[team_name]['bowling_line_up']
    rev_bat_map = {}
    for i in range(0, len(batting_line_up)):
        rev_bat_map[batting_line_up[i].player_id] = i                 
    return [rev_bat_map[x[0]] for x in bowling_line_up]
      
def get_basic_bowling_line_up() -> List[int]:
    line_up = [11, 10] * 5 + [9, 8] * 5 + [7, 8] * 5 + [7, 9] * 5 + [11, 10] * 5
    return line_up 
   
def get_batting_line_up(team:str) -> List[Player]:
    all_teams = get_all_teams()
    players = all_teams[team]['batting_line_up']
    print(players)
    player_lineup = []
    for player in players: 
        player_first_name = players[player].split(" ")[0]
        player_last_name = players[player].split(" ")[1]
        player_object = get_player_stats(player, player_first_name ,player_last_name)
        if not player_object:
            print("Error loading "+ player_first_name + " " + player_last_name)
        player_lineup.append(player_object)

    return  player_lineup 

def get_player_stats(player_id:str,player_first_name, player_last_name )->Player:
    file_path = "data/player_stats.csv"
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if player_id == row["player_id"]:
                return Player(player_id,player_first_name, player_last_name, row['batter_average'], row['batter_strike_rate'], row['baller_average'], row['baller_strike_rate'] )


def get_random_player() -> Player:
    return Player(names.get_first_name(gender='male'), names.get_last_name(), 30, 100, 25, 30)

def load_models() -> Tuple[RandomForestClassifier, RandomForestClassifier]:
    model_pkl_file = "models/cricket_simulator_model.pkl"  
    with open(model_pkl_file, 'rb') as file:  
        models = pickle.load(file)
    print("Successfully loaded models from .pkl file")
    return models   
     
def get_all_teams() -> dict:
    data = {}
    with open('data/teams.pkl', 'rb') as f:
        data = pickle.load(f)
    return data


def select_teams():
    teams = get_all_teams()
    all_team = []
    selected_team = []
    print("Select a default team and line up")
    print("1. Yes")
    print("2. No")
    val = int(input("Enter your value:"))  

    if val ==1:
        return random.choice([("India","Australia"), ("Australia", "India")])  
    else:
        print("Select first team")
        for team_name in teams:
            all_team.append(team_name)

        for i in range(len(all_team)):
            print(str(i+1)+". "+all_team[i])

        val = int(input("Enter your value:"))    
        team1 = all_team[val-1]

        print("Select second team")        
        for i in range(len(all_team)):
            if i+1 != val:
                print(str(i+1)+". "+all_team[i])
        val = int(input("Enter your value:"))    
        team2 = all_team[val-1]
        return (team1,team2)    

def print_scorecard(team_1:Team, team_2:Team):
    print("\n")
    print(color.BOLD+team_1.team_name+" Innings Score Card"+ color.END+"\n")
    print('{:<20s}'.format("BATTING")+ "\t Runs \t Balls \t 4s \t 6s \t SR")
    print("=============================================================")
    for player in team_1.batting_line_up:
        if player.batting_balls == 0:
            continue
        print('{:<20s}'.format(player.first_name+" "+player.last_name)+" \t "+str(player.batting_runs)+" \t "
              +str(player.batting_balls) + " \t "+str(player.batting_fours)+" \t "+str(player.batting_sixes)+" \t "+str(round(player.batting_runs*100/player.batting_balls,2)))
    print("\n")
    print(f"Total Score \t {team_1.overs}.{team_1.balls} Overs (RR: {round((team_1.score*6)/(team_1.overs*6+team_1.balls), 2)}) \t {team_1.score}/{team_1.wickets}")
    print("\n")
    print('{:<20s}'.format("BOWLING")+ "\t Overs \t Runs \t Wickets \t Econ ")
    print("=============================================================")
    for player in team_2.batting_line_up:
        if player.overs>0:
            print('{:<20s}'.format(player.first_name+" "+player.last_name)+" \t "+str(player.overs)+" \t "
              +str(player.bowling_runs) + " \t "+str(player.wickets)+" \t "+str(round(player.bowling_runs/player.overs,2)))
    print("\n")
    print(color.BOLD+team_2.team_name+" Innings Score Card"+ color.END+"\n")
    print('{:<20s}'.format("BATTING")+ "\t Runs \t Balls \t 4s \t 6s \t SR")
    print("=============================================================")
    for player in team_2.batting_line_up:
        if player.batting_balls == 0:
            continue
        print('{:<20s}'.format(player.first_name+" "+player.last_name)+" \t "+str(player.batting_runs)+" \t "
              +str(player.batting_balls) + " \t "+str(player.batting_fours)+" \t "+str(player.batting_sixes)+" \t "+str(round(player.batting_runs*100/player.batting_balls,2)))
        
    print("\n") 
    print(f"Total Score \t {team_2.overs}.{team_2.balls} Overs (RR: {round((team_2.score*6)/(team_2.overs*6+team_2.balls), 2)}) \t {team_2.score}/{team_2.wickets}")
    print("\n")   
    print('{:<20s}'.format("BOWLING")+ "\t Overs \t Runs \t Wickets \t Econ ")
    print("=============================================================")
    for player in team_1.batting_line_up:
        if player.overs>0:
            print('{:<20s}'.format(player.first_name+" "+player.last_name)+" \t "+str(player.overs)+" \t "
              +str(player.bowling_runs) + " \t "+str(player.wickets)+" \t "+str(round(player.bowling_runs/player.overs,2)))
        

    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Simulation mode: auto/manual")
    args = parser.parse_args()
    mode = SimulateMode.AUTO
    if args.mode == 'manual':
        mode = SimulateMode.MANUAL
    team_1_name,team_2_name = select_teams()
    team_1_batting_line_up = get_batting_line_up(team_1_name)
    team_2_batting_line_up = get_batting_line_up(team_2_name)
    if len(team_1_batting_line_up) != 11 or len(team_2_batting_line_up) != 11:
        print("Couldn't load all players. Exiting.")
        return

    team_1 = Team(team_1_batting_line_up, get_bowling_line_up(team_1_name, team_1_batting_line_up), team_1_name)
    team_2 = Team(team_2_batting_line_up, get_bowling_line_up(team_2_name, team_2_batting_line_up),team_2_name)
    first_innings_model, second_innings_model = load_models()
    if mode == SimulateMode.MANUAL:
        print ("Press enter to start the match:")
    match = Match(team_1, team_2, first_innings_model, second_innings_model)
    match.simulate_match(mode)
    match.save_log()
    print_scorecard(team_1,team_2)
    
    
    

if __name__ == "__main__":
    main()   