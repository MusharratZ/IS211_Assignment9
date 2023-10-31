"""url = "https://finance.yahoo.com/quote/AAPL/history?p=AAPL"
"""
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
url = "https://finance.yahoo.com/quote/AAPL/history?p=AAPL"
page = requests.get(url, headers=headers)
page.raise_for_status()
if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table", {"data-test": "historical-prices"})
    if table:
        rows = table.find_all("tr")

        if len(rows) >= 2:
            print("Date           Close")

            for row in rows[1:]:
                columns = row.find_all("td")

                if len(columns) >= 5:
                    date = columns[0].get_text()
                    close_price = columns[4].get_text()
                    print(f"{date}  {close_price}")
                else:
                    print("Data is not in the expected format.")
        else:
            print("No data rows found in the table.")
    else:
        print("Table not found on the page.")
else:
    print("Failed to retrieve the webpage.")