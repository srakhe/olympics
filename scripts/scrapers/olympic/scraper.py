from scripts.scrapers.utils import ScrapingUtils
from country_codes_scraper import CountryCodesScraper


class OlympicScraper:

    def __init__(self, url):
        scr_utils = ScrapingUtils(url=url)
        self.can_crawl = scr_utils.check_crawl_allowed()
        self.crawl_delay = scr_utils.get_crawl_delay()
        self.cc_scraper = CountryCodesScraper(data_path="data", url="https://www.olympedia.org/countries")

    def scrape(self):
        if self.can_crawl:
            print("Crawl is possible.")
            self.cc_scraper.run_scrape()
        else:
            print("It is not possible to crawl this page.")


if __name__ == "__main__":
    oly_scr = OlympicScraper(url="https://www.olympedia.org/")
    oly_scr.scrape()
