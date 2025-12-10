"""Run the main function in this file to scrape the squads for the years 
2010, 2014, 2018, 2022  world cups of all countries particpating"""


import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_wc_squad_from_wikipedia(year: int) -> pd.DataFrame:
    url = f"https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup_squads"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")

    # Limit to main article content just to be safe
    content = soup.find("div", id="mw-content-text") or soup

    all_rows = []
    current_team = None

    # Go through headings and tables in document order
    for tag in content.find_all(["h3", "table"]):
        # 1) When we hit an <h3>, update the current team name
        if tag.name == "h3":
            # First non-empty text inside the h3 is the team name
            heading_text = next(tag.stripped_strings, "")
            current_team = heading_text.strip() if heading_text else None

        # 2) When we hit a <table>, see if it looks like a squad and, if so, use the current_team
        elif tag.name == "table":
            try:
                df = pd.read_html(str(tag))[0]
            except ValueError:
                continue

            # We only care about tables with a "Player" column
            if "Player" not in df.columns:
                continue

            for _, row in df.iterrows():
                name = row.get("Player")
                if isinstance(name, str) and name.strip():
                    all_rows.append(
                        {
                            "year": year,
                            "team": current_team,
                            "player_name": name.strip(),
                        }
                    )

    output = pd.DataFrame(all_rows)
    output.to_csv(f"{year}.csv", index=False)


if __name__ == "__main__":
    for year in [2010, 2014, 2018, 2022]:
        get_wc_squad_from_wikipedia(year)
