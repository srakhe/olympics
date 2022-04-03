from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import time
import os


class MedalsIndividual:

    def __init__(self, data_path, url):
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/brave-browser"
        self.browser = webdriver.Chrome("utils/chromedriver", options=options)
        self.data_path = data_path
        self.url = url

    def scrape_table(self, html_data):
        bs_parser = BeautifulSoup(html_data, "html.parser")
        medals_table = bs_parser.find("table")
        data = []
        for tr in medals_table.find_all("tr"):
            medals_data = {}
            data_list = tr.find_all("td")
            if data_list:
                medals_data["country"] = data_list[0].text
                medals_data["country_code"] = data_list[1].text.replace(" ", "")
                medals_data["gold"] = data_list[2].text.replace(" ", "")
                medals_data["silver"] = data_list[3].text.replace(" ", "")
                medals_data["bronze"] = data_list[4].text.replace(" ", "")
                medals_data["total"] = data_list[5].text.replace(" ", "")
                data.append(medals_data)
        return data

    def save_file(self, data, game_group, game_year):
        out_dir = f"{self.data_path}/medals/{game_group}"
        if not os.path.exists(out_dir):
            print(f"Directory does not exist, creating a new folder: {game_group}")
            os.mkdir(out_dir)
        df = pandas.DataFrame(data=data, index=None)
        df.to_csv(f"{out_dir}/{game_year}.csv")
        print(f"Data for {game_group} and year {game_year} saved in csv")

    def control_browser(self, run_times):
        i = 0
        self.browser.get(self.url)
        el = self.browser.find_element_by_xpath('//*[@id="edition_select"]')
        for each_group in el.find_elements_by_tag_name('optgroup'):
            group_name = each_group.get_property("label")
            i += 1
            if i > run_times:
                break
            for each_option in each_group.find_elements_by_tag_name('option'):
                each_option.click()
                time.sleep(5)
                option_name = each_option.text
                html = self.browser.page_source
                each_game_data = self.scrape_table(html_data=html)
                self.save_file(data=each_game_data, game_group=group_name, game_year=option_name)

    def run_scrape(self):
        print("Running medals count (per game) data scraper")
        self.control_browser(run_times=2)
        self.browser.quit()
        print("Completed medals count (per game) data scraper")
