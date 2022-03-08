import urllib.request
import pandas as pd
from bs4 import BeautifulSoup


def scrape(page_url):
    urllib.request.urlretrieve(page_url, "data/olympic_cost.html")
    page = open("data/olympic_cost.html")
    soup = BeautifulSoup(page.read(), "html.parser")
    olympic_cost_table = soup.findAll("table", {"class": "wikitable"})
    olympic_cost_table_columns = olympic_cost_table[0].findAll("th")
    column_headers = []
    for col in olympic_cost_table_columns:
        column_headers.append(col.text.split('\n')[0])
    olympic_table = pd.DataFrame(columns=column_headers)
    olympic_cost_table_values = olympic_cost_table[0].findAll("tr")
    k = 0
    for row in olympic_cost_table_values[1:]:
        individual_row_data = row.find_all("td")
        field_value = [field.text.split('\n')[0] for field in individual_row_data]
        olympic_table.loc[k] = field_value
        k = k + 1
    olympic_table.to_csv("data/olympic_cost.csv")


if __name__ == "__main__":
    scrape(page_url="https://en.wikipedia.org/wiki/Cost_of_the_Olympic_Games")
