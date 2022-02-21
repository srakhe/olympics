from scripts.scrapers.utils import ScrapingUtils


class OlympicScraper:

    def __init__(self, url):
        scr_utils = ScrapingUtils(url=url)
        self.can_crawl = scr_utils.check_crawl_allowed()
        self.crawl_delay = scr_utils.get_crawl_delay()

    def scrape(self):
        if self.can_crawl:
            print("Crawl is possible.")
        else:
            print("It is not possible to crawl this page.")


if __name__ == "__main__":
    oly_scr = OlympicScraper(url="https://www.olympedia.org/")
    oly_scr.scrape()
