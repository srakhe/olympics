import time
from urllib import robotparser
import requests
import pandas as pd


class ScrapingUtils:

    def __init__(self, url):
        self.site_url = url

    def check_crawl_allowed(self):
        robot_parser = robotparser.RobotFileParser(url=f"{self.site_url}/robots.txt")
        robot_parser.read()
        return robot_parser.can_fetch("*", "/")

    def get_crawl_delay(self):
        robot_parser = robotparser.RobotFileParser(url=f"{self.site_url}/robots.txt")
        robot_parser.read()
        return robot_parser.crawl_delay("*")

    def fetch_webpage(self, page_url, path, name):
        delay = self.get_crawl_delay()
        print(f"Waiting for time: {delay} seconds before doing a fetch.")
        time.sleep(float(delay))
        try:
            html_data = requests.get(page_url)
            with open(path + "/" + name, "w+") as htmlFile:
                htmlFile.write(html_data.text)
        except:
            print("Webpage fetch successful.")
            return False
        else:
            print("Webpage fetch successful.")
            return True

    def get_webpage_data(self, path, name):
        try:
            with open(path + "/" + name, "r+") as htmlFile:
                html_data = htmlFile.read()
        except:
            print("Saved webpage data fetch successful.")
            return False
        else:
            print("Saved webpage data fetch successful.")
            return html_data

    def create_csv(self, data, path, name):
        df = pd.DataFrame(data=data, index=None)
        df.to_csv(f"{path}/{name}")
        print("Data saved in csv.")
