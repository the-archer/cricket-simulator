# main function which runs the match...

# classses:
# team , score, multiple players, lineup, (batting / bowling)

# player
# score, balls faced, skill stats (ave, sr)
# bowls balled, wickets taken

# mathc state, overs, each over will have balls
# 
from enum import Enum
import names
from random import random

class SimulateMode(Enum):
    MANUAL = 0
    AUTO = 1

class BatterState(Enum):
    DID_NOT_BAT = 0
    CURRENTLY_BATTING = 1
    DISMISSED = 2
    

class Player:
    def __init__(self, first_name, last_name, bt_ave, bt_sr, bowl_ave, bowl_sr):
        self.first_name = first_name
        self.last_name = last_name
        self.batting_average = bt_ave
        self.batting_sr = bt_sr
        self.bowling_average = bowl_ave
        self.bowling_sr = bowl_sr
        
        self.batting_runs = 0
        self.batting_balls = 0
        self.batter_state = BatterState.DID_NOT_BAT 
        
        self.bowling_runs = 0
        self.bowling_balls = 0
        self.overs = 0
        self.wickets = 0
    
class Team:
    def __init__(self, batting_line_up, bowling_line_up):
        self.batting_line_up = batting_line_up
        self.bowling_line_up = bowling_line_up
        self.score = 0
        self.wickets = 0
        self.overs = 0
        self.balls = 0
        
 
class Match:
    def __init__(self, team_1, team_2):
        self.team_1= team_1
        self.team_2 = team_2
        self.first_innings_score = 0
        self.current_innings = 1
        
    def simulate_match(self, mode):
        batter = self.team_1.batting_line_up[0]
        non_striker = self.team_1.batting_line_up[1]
        bowler = self.team_2.batting_line_up[self.team_2.bowling_line_up[0]-1]
        batting_team = self.team_1
        for over_no in range(0, 50):
            ball = 1
            while ball <= 6:
                input()
                res = get_bowl_result()
                if res == -1:
                    batting_team.wickets += 1
                    batter.batting_balls += 1
                    bowler.bowling_balls += 1
                    bowler.wickets += 1
                    print(f"{over_no}.{ball}: {bowler.last_name} to {batter.last_name}: OUT!")
                    print(f"{batter.last_name}: {batter.batting_runs}({batter.batting_balls})")
                    batter = batting_team.batting_line_up[batting_team.wickets + 1]
                else:
                    batting_team.score += res
                    batter.batting_runs += res
                    batter.batting_balls += 1
                    bowler.bowling_runs += res
                    bowler.bowling_balls += 1
                    print(f"{over_no}.{ball}: {bowler.last_name} to {batter.last_name}: {res} run(s)")
                if res%2 == 1 and res > 0:
                    batter, non_striker = non_striker, batter
                ball+=1
            bowler.overs += 1
            print (f"End of over {over_no+1}: Score: {batting_team.score}/{batting_team.wickets} \t" 
                   f"{batter.last_name}: {batter.batting_runs}({batter.batting_balls}) \t" 
                   f"{non_striker.last_name}: {non_striker.batting_runs}({non_striker.batting_balls}) \t" 
                   f"{bowler.last_name}: {bowler.overs}-0-{bowler.wickets}-{bowler.bowling_runs}\n")
            batter, non_striker = non_striker, batter
            bowler = self.team_2.batting_line_up[self.team_2.bowling_line_up[over_no+1]-1]    
                    
                
                
            
        
def get_bowl_result():
    rand = random()
    if rand < 0.3:
        return 0
    if rand < 0.5:
        return 1
    if rand < 0.55:
        return 2  
    if rand < 0.6:
        return 3
    if rand < 0.75:
        return 4
    if rand < 0.85:
        return 6
    return -1
      
def get_basic_bowling_line_up():
    line_up = [11, 10] * 5 + [9, 8] * 5 + [7, 8] * 5 + [7, 9] * 5 + [11, 10] * 5
    return line_up 
   
def get_basic_batting_line_up():
    return [get_random_player() for x in range(0, 11)]

def get_random_player():
    return Player(names.get_first_name(gender='male'), names.get_last_name(), 30, 100, 25, 30)



def main():
    team_1 = Team(get_basic_batting_line_up(), get_basic_bowling_line_up())
    team_2 = Team(get_basic_batting_line_up(), get_basic_bowling_line_up())
    match = Match(team_1, team_2)
    match.simulate_match(mode = SimulateMode.MANUAL)
    
    
    

if __name__ == "__main__":
    main()   