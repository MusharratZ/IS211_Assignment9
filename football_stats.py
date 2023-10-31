"""
       url = "https://www.cbssports.com/nfl/stats/player/passing/nfl/regular/qualifiers/"
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
url = "https://www.cbssports.com/nfl/stats/player/passing/nfl/regular/qualifiers/"
page = requests.get(url, headers=headers)
# print(page.raise_for_status)

if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.find("table", {"class": "TableBase-table"})

    rows = table.find_all("tr")

    data = []
    for row in rows:
        columns = row.find_all("td")

        # Ensure that there are at least 3 columns in each row
        if len(columns) >= 3:
            player_name = columns[0].find("a").get_text(strip=True)
            position = (
                columns[0]
                .find("span", class_="CellPlayerName-position")
                .get_text(strip=True)
            )
            team = (
                columns[0]
                .find("span", class_="CellPlayerName-team")
                .get_text(strip=True)
            )
            touchdown = columns[8].get_text(strip=True)

            data.append([player_name, position, team, touchdown])

    df = pd.DataFrame(data, columns=["Player Name", "Position", "Team", "Touchdowns"])
    df.set_index(df.columns[0], inplace=True, drop=True)
    # Print the top 20 players
    top_20_players = df.head(20)
    print(top_20_players)


else:
    print("Failed to retrieve the webpage.")