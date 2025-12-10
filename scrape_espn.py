import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re


BASE = "https://www.espn.com"
YEAR = 2026

# Standard browser header to reduce blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}



def scrape_team_ids(index_url):
    """
    Given the ESPN tournament index page,
    this function extracts:
        - Team names
        - Their internal ESPN team IDs
        - Builds direct squad URLs for each team
    """

    r = requests.get(index_url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    teams = {}

    # Every team link contains "/soccer/team/_/id/"
    for a in soup.select("a[href*='/soccer/team/_/id/']"):
        href = a.get("href")
        name_tag = a.select_one("h2")

        # Skip malformed entries
        if not href or not name_tag:
            continue

        team_name = name_tag.get_text(strip=True)

        # Extract numeric team ID from URL
        match = re.search(r'/id/(\d+)/', href)
        if not match:
            continue

        team_id = match.group(1)

        # Build the team squad page for the World Cup league
        squad_url = f"{BASE}/soccer/team/squad/_/id/{team_id}/league/FIFA.WORLD"

        teams[team_name] = squad_url

    return teams



def scrape_espn_squad(url, team):
    """
    Given a team squad URL and team name,
    returns a list of all players in the squad.

    Each row contains:
        - year
        - team
        - player_name
    """

    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    rows = []

    # All player profile links contain "/soccer/player/"
    for link in soup.select("a.AnchorLink[href*='/soccer/player/']"):
        name = link.get_text(strip=True)

        if name:
            rows.append({
                "year": YEAR,
                "team": team,
                "player_name": name
            })

    return rows



def build_all_squads(index_url):
    """
    Steps:
        1. Get all teams from tournament index
        2. Visit each team squad page
        3. Extract all players
        4. Save final dataset to CSV
    """

    team_urls = scrape_team_ids(index_url)
    all_rows = []

    for team, squad_url in team_urls.items():
        print(f"Scraping squad: {team}")
        rows = scrape_espn_squad(squad_url, team)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    os.makedirs("Squads", exist_ok=True)
    output = f"Squads/{YEAR}_espn_squads.csv"
    df.to_csv(output, index=False)

    print(f"\nSaved {len(df)} players to {output}")
    print(df.head())


if __name__ == "__main__":
    TOURNAMENT_INDEX_URL = "https://www.espn.com/soccer/teams/_/league/fifa.world"
    build_all_squads(TOURNAMENT_INDEX_URL)
