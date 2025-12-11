🏆 World Cup National Team Success Prediction

This project builds a machine learning model that predicts how far a national team will progress in a FIFA World Cup based solely on player statistics and team-level features from the years before the tournament.

Instead of making a simple “who wins the World Cup?” binary prediction, this project introduces a success gradient that assigns a numeric value to each team based on the stage they reached.
The closer a team gets to the final, the higher their score.

This approach allows us to:

✅ Use richer labels instead of a shallow 1 winner vs 31 non-winners setup

✅ Capture meaningful performance differences between teams

✅ Train a more stable and informative regression model

✅ Rank teams by predicted tournament success for each World Cup year

🎯 Project Goals

Collect and engineer squad-level features based primarily on player statistics.

Build a success gradient that represents each team’s real tournament outcome.

Train machine learning models to predict this success score.

Evaluate how well the model ranks teams in each tournament.

Forecast which teams are most likely to succeed before a World Cup begins.

📦 Dataset Structure

Each dataset entry represents a team in a specific World Cup year and follows this structure:

year | team | goalkeeper_score | rightback_score | ... | striker_score |
team_age_average | elo_before_wc | previous_wc_success | current_wc_success

📈 Success Score (Target Variable)

The success score represents the actual result of a squad in a given World Cup year.

In a typical classification setting, there is one winner and 31 losers. However, this completely ignores the fact that teams reach very different stages of the tournament, which are qualitatively meaningful.

For example:

A team eliminated in the Group Stage is not comparable to a team that reaches the Semi-Final or Final.

These differences contain valuable information about team quality, consistency, and squad strength.

So instead, tournament placement is mapped to a continuous numeric score:

Tournament Stage	Success Score
Group Stage	0.01
Round of 16	0.20
Quarter-Final	0.50
Semi-Final	0.75
Runner-up	0.90
Champion	1.00

This framing turns the problem into a regression + ranking task rather than a simple classification problem.

🎮 Player Score

For each squad in a given year, every player is represented by a player score derived from their FIFA video game ratings for that season.

FIFA ratings are a practical and effective proxy for real-world player quality because they are built using:

Historical performance data from club and international matches

Expert evaluations from scouts and professional analysts

Detailed player attributes including:

Pace

Shooting

Passing

Defending

Physicality

Overall skill

These player scores are aggregated into position-level and squad-level features.

🛠 Dataset Construction Plan

For each squad in each World Cup year:

Iterate over the 23 selected players and collect:

FIFA rating

Player age

Compute average squad age

Retrieve:

The squad’s Elo rating before the tournament

The squad’s Elo rating from the previous year

Attach:

The squad’s World Cup success score for the current year

The squad’s success score from the previous World Cup

🧩 Data Pipeline
✅ Step 1 — Player Ratings (SoFIFA)

SoFIFA hosts player ratings from FIFA 07 through FC 26.

All player data for World Cup years was scraped and saved into CSV files.

Training years used:

2010, 2014, 2018, 2022

Testing year:

2026

These CSV files form the player-level dataset. They are stored inside PlayerDataset/

✅ Step 2 — World Cup Squads (Wikipedia + ESPN)

Wikipedia pages were scraped to extract:

Which national teams qualified

Which players were selected for each squad

For the following tournaments:

2010, 2014, 2018, 2022

Each tournament’s squads were saved to individual CSV files in the Squads/ folder using scrape_squads_wikipedia.py.

The 2026 draw was just done yesterday, so I know which teams are going to play, but the players haven't been announced yet. So I created scrape_espn.py in which I scraped first the squads going to the tournament, and then went over ESPN's page for each squad scraping the players for that squad in the 2026 world cup. This is obviously not definitive yet but it's the best guess as of this moment.

The squads particpating in the world cup for a given year are stores in Squads/.


✅ Step 3 — Link world cup particpating players to dataset

Using link_squads_to_players.py, I build CSVs that match the players from the squads that have went to the world cup to their index in the fifa rating database inside PlayerDataset/ for a given world cup year. 

For each year in Squads/, I went over each player and created the short version of their name (Lionel Messi would be L. Messi), removed accents, normalized, and looked for the best match in the fifa database for that given year in PlayerDataset/. Once the match was found I append the row for that player to the csv for that year in LinkedSquads/. 

So essentially, LinkedSquads/ contains the players who particpated in the world cup for a given year, what team they player for, and their index in the big FIFA database. That index is going to be used in the next step in collecting the data for the teams to start the regression problem. 

Not all players who played in the world cup where matched to an index in the FIFA ratings database because not all of them were even in it. In that case where a player isn't matched, I will replace his entry in the database with the global rating/age/... feature average. 

The matching rates for the years:

2010: 77.85326086956522 % was matched

2014: 80.70652173913044 % was matched

2018: 79.4836956521739 % was matched

2022: 82.67148014440433 % was matched

2026: 74.74437627811861 % was matched


✅ Step 4: Build unified dataset:

I build the build_team_features.py script, which goes over each year, and calculates the features we want for a given squad that year. The features are:

team,year,team_mean_overall,team_max_overall,team_top3_overall,team_overall_std,team_top3_shooting,team_top3_passing,team_top3_defending,team_top3_physic,team_top3_pace,team_mean_age,team_min_age,team_max_age,success_score

Where each feature is a factor that we are trying to see how important is its impact on the success score for that team for that year. 

Those feature to success score CSVs are stored in TeamFeatures/.


✅ Step 5: Add success score:

Suprisingly it has proven much easier and quicker to add the success score manually. No code needed for this one. 


✅ Step 6: Train regression model:








