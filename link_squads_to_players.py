import os
import re
import unicodedata
import pandas as pd



def normalize_short_key(text):

    text = text.lower().strip()

    # Strip accents
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    # Remove everything except letters and numbers
    text = re.sub(r"[^a-z0-9]", "", text)

    return text


def make_short_from_full(full_name):
    # Strip accents FIRST
    name = unicodedata.normalize("NFKD", full_name)
    name = "".join(c for c in name if not unicodedata.combining(c))

    # Replace punctuation with spaces
    name = re.sub(r"[,'’\-]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    parts = name.split()

    if len(parts) == 1:
        return parts[0]

    first_initial = parts[0][0]
    surname = " ".join(parts[1:])

    return f"{first_initial}. {surname}"



def find_short_name_column(players_df):
    for col in ["short_name", "name"]:
        if col in players_df.columns:
            return col


def find_rating_column(players_df):
    for col in ["overall", "ova", "rating"]:
        if col in players_df.columns:
            return col


def find_player_index_by_short_only(player_name, players_df):
    """
    If multiple matches:
        → pick highest rated
    If still ambiguous:
        → return None
    """

    full_key = normalize_short_key(player_name)
    derived_short = make_short_from_full(player_name)
    short_key = normalize_short_key(derived_short)

    matches = players_df[
        (players_df["short_key"] == short_key) |
        (players_df["short_key"] == full_key)
    ]

    if matches.empty:
        return None

    # Highest rating tie-break
    rating_col = find_rating_column(players_df)

    if rating_col and rating_col in matches.columns:
        matches = matches.sort_values(by=rating_col, ascending=False)

    # If top 2 have same rating → ambiguous → return None
    if len(matches) > 1 and rating_col:
        if matches.iloc[0][rating_col] == matches.iloc[1][rating_col]:
            return None

    return matches.iloc[0].name




def link_year(year):
    print(f"Linking year {year}...")

    players_path = f"PlayerDataset/{year}players.csv"
    squads_path = f"Squads/{year}.csv"

    players_df = pd.read_csv(players_path, low_memory=False)
    squads_df = pd.read_csv(squads_path)

    short_col = find_short_name_column(players_df)
    players_df["short_key"] = players_df[short_col].astype(str).apply(normalize_short_key)

    results = []
    playersMatched = totalPlayers = 0
    for _, row in squads_df.iterrows():
        player_name = row["player_name"]
        team = row["team"]
        y = row["year"]

        totalPlayers += 1

        idx = find_player_index_by_short_only(player_name, players_df)
        
        if idx is not None:
            playersMatched += 1

        results.append({
            "year": y,
            "team": team,
            "player_name": player_name,
            "derived_short_name": make_short_from_full(player_name),
            "fifa_index": idx
        })

    print(f"{(playersMatched/totalPlayers) * 100} % was matched")
    os.makedirs("LinkedSquads", exist_ok=True)
    out_path = f"LinkedSquads/{year}_linked.csv"
    pd.DataFrame(results).to_csv(out_path, index=False)

    print(f"Saved → {out_path}")



if __name__ == "__main__":
    for year in [2010, 2014, 2018, 2022, 2026]:
        link_year(year)
    

    
