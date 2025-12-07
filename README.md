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

These CSV files form the player-level dataset.

✅ Step 2 — World Cup Squads (Wikipedia + 442)

Wikipedia pages were scraped to extract:

Which national teams qualified

Which players were selected for each squad

For the following tournaments:

2010, 2014, 2018, 2022

Each tournament’s squads were saved to individual CSV files in the Squads/ folder using getSquad.py.

Since the 2026 draw was just completed, squad information for qualified teams was scraped from the 442 website.