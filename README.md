<h1>Cricket Simulator<h1>

<h2>Introduction</h2>
<p> This project experiments with creating a cricket simulator using maching learning.
<p>Take a look at https://medium.com/@tejalnarkar/cricket-simulation-engine-using-machine-learning-a2758933b0a7 for the details.

<h2> Source Data Used </h2>
<p> In order to train the random classifier model, we needed match data at each ball level. Additionally we needed player statistics, which we calculated using the match data. All this data was found on the site: https://cricsheet.org/

<h2> Code </h2>
<p> Disclaimer: This is a proof of concept so please excuse the lack of comments and the hacky code. Contributions / improvements welcome.

<h3> Data </h3>
All the data files are in folder "data". Each match is an individual files in json format.

<h3> Data Prep </h3>
<p>All the data processing and feature prep scripts are in the folder data_prep. 
<p>The odi_data_explore.py file processes the data in the data folder and generates a CSV file with all ball-by-ball data.
<p>The odi_data_explore.py also generates the player statistics file which calculates the batting and bowling averages and strike rates for all players.
<p>The team_prep.py generates the player lineups for each country/team.
<p>The feature_prep.py file creates the features that need to feed into the model

<h3> Models </h3>
<p> The models folder has model training script.
<p> The random forest classifier is in the engine training file.

<h3> Match Simulator </h3>
<p> The match_simulator.py has logic for using the stored model to simulate the match. It also has the logic for the match and maintains the state of the match.

<h2> Steps </h2>
<h3> Prepare Data </h3>

```
python data_prep/odi_data_prep.py
python data_prep/feature_prep.py
python data_prep/team_prep.py
```

<h3> Train Model </h3>

```
python models/engine_training.py
```

<h3> Running the Simulator </h3>

```
python match_simulator.py
```

<h2> Example of output</h2>
<p>
India won by 111 runs

![Output Example](image.png?raw=true "Title")







