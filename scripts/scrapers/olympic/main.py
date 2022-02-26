from scripts.scrapers.scrape_utils import ScrapingUtils
from country_codes import CountryCodes


class OlympicScraper:

    def __init__(self, url):
        scr_utils = ScrapingUtils(url=url)
        self.can_crawl = scr_utils.check_crawl_allowed()
        self.cc_scraper = CountryCodes(data_path="data", url="https://www.olympedia.org/countries",
                                       scrape_utils=scr_utils)

    def scrape(self):
        if self.can_crawl:
            print("Crawl is possible.")
            self.cc_scraper.run_scrape()
        else:
            print("It is not possible to crawl this page.")


if __name__ == "__main__":
    oly_scr = OlympicScraper(url="https://www.olympedia.org/", )
    oly_scr.scrape()
