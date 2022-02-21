from urllib import robotparser


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
