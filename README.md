This project builds a machine learning model that predicts how far a national team will progress in a FIFA World Cup based solely on player statistics and team-level features from the years before the tournament.

Instead of making a simple “who wins the World Cup?” binary prediction, this project introduces a success gradient that assigns a numeric value to each team based on the stage they reached.
The closer a team gets to the final, the higher their score.

This allows us to:

1-Use richer labels instead of 1 winner vs 31 non-winners

2-Capture meaningful differences between teams

3-Train a more stable, informative model

4-Rank teams by predicted tournament success for each World Cup year


Goals of the Project:

1- Collect and engineer squad-level features, mostly player stats.

2-Build a success gradient representing each team’s real tournament outcome from previous world cups.

3-Train machine learning models to predict this gradient.

4-Evaluate how well the model ranks teams in each tournament.

5-Forecast which teams are most likely to succeed in a given World Cup before it starts.




Part 1: Getting and classifying data

