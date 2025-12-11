import pandas as pd
import os

SUCCESS_SCORE = {
    "Group": 0.01,
    "R16": 0.20,
    "QF": 0.50,
    "SF": 0.75,
    "Runner-up": 0.90,
    "Champion": 1.00
}



def compute_top3(df, col):
    """Return average of top 3 values in df[col]."""
    top3 = df[col].nlargest(3)
    if len(top3) == 0:
        return 0
    return top3.mean()



def build_team_features(year):

    # Load data
    players = pd.read_csv(f"PlayerDataset/{year}players.csv", low_memory=False)
    squads = pd.read_csv(f"LinkedSquads/{year}_linked.csv")


    #calculate global mean for all numeric columns in that year's dataset so we can fill in for players who weren't matched
    numeric_cols = players.select_dtypes(include="number").columns
    global_means = players[numeric_cols].mean()


    #Merge the players in linkedSquads with their linked index.
    merged = squads.merge(players, left_on="fifa_index", right_index=True, how="left")

    unmatched_mask = merged["fifa_index"].isna() | merged["overall"].isna()

    for col in numeric_cols:
        merged.loc[unmatched_mask, col] = global_means[col]

    features = []

    #For each team compute the features
    for team in merged["team"].unique():
        #create a dataset of only that nationality (while dropping players that haven't been matched)
        team_df = merged[merged["team"] == team].dropna(subset=["overall"]).copy()

        if team_df.empty:
            #no players found
            continue
        
        #Calculate features
        team_mean = team_df['overall'].mean()
        team_max_player = team_df['overall'].max()
        team_standard_deviation = team_df['overall'].std()
        team_top_3_players = compute_top3(team_df, 'overall')
        team_top3_shoot = compute_top3(team_df, "shooting")
        team_top3_pass = compute_top3(team_df, "passing")
        team_top3_def = compute_top3(team_df, "defending")
        team_top3_phys = compute_top3(team_df, "physic")
        team_top3_pace = compute_top3(team_df, "pace")
        team_mean_age = team_df["age"].mean()
        team_min_age = team_df["age"].min()
        team_max_age = team_df["age"].max()


        features.append({
            "team": team,
            "year": year,
            "team_mean_overall": team_mean,
            "team_max_overall": team_max_player,
            "team_top3_overall": team_top_3_players,
            "team_overall_std": team_standard_deviation,

            "team_top3_shooting": team_top3_shoot,
            "team_top3_passing": team_top3_pass,
            "team_top3_defending": team_top3_def,
            "team_top3_physic": team_top3_phys,

            "team_top3_pace": team_top3_pace,

            "team_mean_age": team_mean_age,
            "team_min_age": team_min_age,
            "team_max_age": team_max_age,

            # None for now until I get the results
            "success_score": None
        })


    out = pd.DataFrame(features)
    fout = f"TeamFeatures/{year}_features.csv"
    out.to_csv(fout, index=False)
    print(f"Saved {fout}")
    return out
         


if __name__ == "__main__":
    for y in [2010, 2014, 2018, 2022, 2026]:
        build_team_features(y)

        
    