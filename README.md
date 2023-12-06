<h1>Cricket Simulator<h1>

<h2>Context</h2>
<p>As a part of our thanksgiving break Simrat and I worked on creating a cricket simulator using Machine Learning. We used Random Forest Classifier for predicting the probability distribution of each ball. 

<h2> Source Data Used </h2>
<p> In order to train the model, we needed match data at each ball level. Additionally we needed player statistics, which we calculated using the match data. All this data was found on site: https://cricsheet.org/

<h2> Coding details </h2>
<h3> Data </h3>
All the data files are in folder "data". Each match is in individual files in json format.

<h3> Data Cleaning </h3>
<p>All the data precessing and feature prep scripts are in this folder. 
<p>The odi_data_explore.py file processes the data in the data folder and generates a CSV file with all ball-by-ball data.
<p>The odi_data_explore.py also generates the player statistics file which calculates the batting and bowling averages and strike rates for all players.
<p>The team_prep.py generates the player lineups for each country/team.
<p>The feature_prep.py file creates the features that need to feed into the model

<h3> Models </h3>
<p> The models folder has model training scripts
<p> The random forest classifier is in the engine training file.

<h3> Match Simulator </h3>
<p> The match_simulator.py has logic for using the stored model to simulate the match. It also has the logic for the match and maintains the state of the match.

<h2> Example of output</h2>
<p>
India won by 111 runs

![Output Example](image.jpg?raw=true "Title")
