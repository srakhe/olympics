from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

olympics_year_bid_data = {'Host_Year': None, 'Bid_Year': None, 'Bid_City': None, 'Bid_Country': None}
country_bid_data = {'Country': None, 'City': None, 'Failed_Bids': None, 'Success_Bids': None}


#  Downloading Web page
def download_page(web_url, name):
    downloaded_page = requests.get(web_url)

    # Saving the webpage as .html file
    file_obj = open(name, 'wb')
    file_obj.write(downloaded_page.content)
    file_obj.close()


# Common Utils Function
def check_dash_cell(cellvalue):
    if cellvalue == "—":
        return True
    return False


# Returns the year from string date
def extract_years(cellvalue):
    if not check_dash_cell(cellvalue):
        years_list = [int(s) for s in re.findall(r'-?\d+\.?\d*', cellvalue.text.strip())]
        return years_list if len(years_list) > 0 else list()
    return list()


def populate_data(row_data, index_list):
    if row_data[index_list[0]].a is None:
        country_bid_data['City'] = row_data[index_list[0]].text
    else:
        country_bid_data['City'] = row_data[index_list[0]].a.text
    country_bid_data['Failed_Bids'] = extract_years(row_data[index_list[1]])
    country_bid_data['Success_Bids'] = extract_years(row_data[index_list[2]])


def extract_location(row_data, index_list):
    # Bidding City
    if row_data[index_list[0]].a is None:
        olympics_year_bid_data['Bid_City'] = row_data[index_list[0]].text
    else:
        olympics_year_bid_data['Bid_City'] = row_data[index_list[0]].a.text

        # Bidding Country
    a_list = row_data[index_list[1]].find_all("a")
    if len(a_list) > 1:
        olympics_year_bid_data['Bid_Country'] = a_list[1].text
    else:
        olympics_year_bid_data['Bid_Country'] = a_list[0].text


def get_bid_year(input_value):
    return input_value.split(" ")[-1] if not check_dash_cell(input_value) else ""


def scrape_data(url, file_name, title, start_index):
    # Additional Variables
    bid_by_year_df = pd.DataFrame(columns=['Host_Year', 'Bid_Year', 'Bid_City', 'Bid_Country'])
    bid_by_country_df = pd.DataFrame(columns=['Country', 'City', 'Failed_Bids', 'Success_Bids'])

    download_page(url, file_name)

    # Scrapes the data and saves it as .csv file
    with open(file_name, 'rb') as page:
        content = page.read()
        soup = BeautifulSoup(content, 'html.parser')

        tables_list = soup.find_all('table', attrs={'class': 'wikitable'})

        # Bids by Year
        tab_one_rows = tables_list[0].find_all("tr")
        for rowvalue in tab_one_rows[start_index:]:

            row_data = rowvalue.find_all("td")
            no_cols = len(row_data)

            first_column = row_data[0].a.text if row_data[0].a is not None else row_data[0].text

            if no_cols >= 2 and re.match(r'^([\s\d]+)$', first_column):
                # Host Year
                olympics_year_bid_data['Host_Year'] = first_column

                # Bidding Year
                if row_data[1].a is None:
                    olympics_year_bid_data['Bid_Year'] = get_bid_year(row_data[1].text)
                else:
                    olympics_year_bid_data['Bid_Year'] = get_bid_year(row_data[1].a.text)

                # Bidding City and Country
                if row_data[2].a is None and row_data[3].a is None:
                    olympics_year_bid_data['Bid_City'] = row_data[2].text if not check_dash_cell(row_data[2]) else ""
                    olympics_year_bid_data['Bid_Country'] = row_data[3].text if not check_dash_cell(row_data[3]) else ""

                else:
                    extract_location(row_data, [2, 3])

                bid_by_year_df = bid_by_year_df.append(olympics_year_bid_data, ignore_index=True)

            elif no_cols >= 3:
                extract_location(row_data, [0, 1])
                if row_data[2].i is None or (row_data[2].i is not None and not row_data[2].i.text == 'Withdrew'):
                    bid_by_year_df = bid_by_year_df.append(olympics_year_bid_data, ignore_index=True)

            elif no_cols >= 2:
                extract_location(row_data, [0, 1])
                bid_by_year_df = bid_by_year_df.append(olympics_year_bid_data, ignore_index=True)

        # Bids by Country
        tab_two_rows = tables_list[1].find_all("tr")
        for rowvalue in tab_two_rows[1:]:
            row_data = rowvalue.find_all("td")
            no_cols = len(row_data)
            if no_cols == 3:
                populate_data(row_data, [0, 1, 2])

            if no_cols == 4:
                country_bid_data['Country'] = row_data[0].a['title']
                populate_data(row_data, [1, 2, 3])

            bid_by_country_df = bid_by_country_df.append(country_bid_data, ignore_index=True)

    # Writing the Structured data to csv format
    bid_by_year_df.to_csv('Datasets/' + title + 'bidbyyear.csv', index=False)
    bid_by_country_df.to_csv('Datasets/' + title + 'bidbycountry.csv', index=False)


# Main method
if __name__ == '__main__':
    scrape_data("https://en.wikipedia.org/wiki/List_of_bids_for_the_Summer_Olympics", "summer_bids.html", 'summer', 4)
    scrape_data("https://en.wikipedia.org/wiki/List_of_bids_for_the_Winter_Olympics", "winter_bids.html", 'winter', 3)
