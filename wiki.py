"""url = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
page = requests.get(url)
page.raise_for_status()

if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table")

    if len(tables) >= 2:
        second_table = tables[1]

        rows = second_table.find_all("tr")

        data = []
        for row in rows:
            columns = row.find_all("td")

            if len(columns) >= 3:
                game = columns[0].get_text(strip=True)
                date = columns[1].get_text(strip=True)
                winning_team = columns[2].get_text(strip=True)
                score = columns[2].get_text(strip=True)
                losing_team = columns[2].get_text(strip=True)
                data.append([game, date, winning_team, score, losing_team])

        df = pd.DataFrame(
            data, columns=["Game", "Date", "Winning Team", "Score", "Losing Team"]
        )
        df.set_index(df.columns[0], inplace=True, drop=True)
        print(df)

    else:
        print("Not enough tables found on the page.")

else:
    print("Failed to retrieve the webpage.")