from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup


class OlympicCostScraper:

    def __init__(self, url):
        self.url = url
        self.data_path = "data/olympic_cost"
        self.olympic_cost_table_columns = None
        self.olympic_cost_df = None

    def fetch_html(self):
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        return webpage

    def save_html(self, webpage):
        filename = self.data_path + '.html'
        with open(filename, 'wb') as file:
            file.write(webpage)

    def create_df(self):
        filename = self.data_path + '.html'
        file = open(filename)
        soup = BeautifulSoup(file.read(), "html.parser")
        olympic_medal_table = soup.findAll("table", {"class": "igsv-table no-datatables"})
        column_headers = []
        self.olympic_cost_table_columns = olympic_medal_table[1].findAll("tr")
        olympic_table_column_headers = self.olympic_cost_table_columns[1]
        for row in olympic_table_column_headers:
            column_headers.append(row.text)
        column_headers.append('Year')
        column_headers.append('Type')
        column_headers.append('City')
        column_headers.append('Country')
        self.olympic_cost_df = pd.DataFrame(columns=column_headers)

    def extract_features(self):
        k = 0
        for row in self.olympic_cost_df.iterrows():
            olympic_info = row[1][0].split(',')
            if len(olympic_info) < 3:
                self.olympic_cost_df['Country'].loc[k] = olympic_info[1]
                self.olympic_cost_df['City'].loc[k] = olympic_info[0].split(' ')[3]
                self.olympic_cost_df['Year'].loc[k] = olympic_info[0].split(' ')[0]
                self.olympic_cost_df['Type'].loc[k] = olympic_info[0].split(' ')[1]
            else:
                self.olympic_cost_df['City'].loc[k] = olympic_info[1]
                self.olympic_cost_df['Country'].loc[k] = olympic_info[2]
                olympic_year_and_type = olympic_info[0]
                olympic_year_and_type = olympic_year_and_type.split(' ')
                self.olympic_cost_df['Year'].loc[k] = olympic_year_and_type[0]
                self.olympic_cost_df['Type'].loc[k] = olympic_year_and_type[1]
            k = k + 1

    def save_dataframe_to_csv(self):
        filename = self.data_path + '.csv'
        self.olympic_cost_df.to_csv(filename)

    def scrape(self):
        html_data = self.fetch_html()
        self.save_html(html_data)
        self.create_df()
        olympic_cost_table_column_demo = self.olympic_cost_table_columns[2:]
        k = 0
        for row in olympic_cost_table_column_demo:
            individual_row_data = row.find_all("td")
            field_value = [field.text.split('\n')[0] for field in individual_row_data]
            field_value.append('NA')
            field_value.append('NA')
            field_value.append('NA')
            field_value.append('NA')
            self.olympic_cost_df.loc[k] = field_value
            k = k + 1
        self.extract_features()
        self.save_dataframe_to_csv()


if __name__ == "__main__":
    oly_cost_scraper = OlympicCostScraper(url="https://moneynation.com/olympics-money-facts/")
    oly_cost_scraper.scrape()
