## Scrapers:

### [Olympic Data Scraper](../scripts/scrapers/olympic):

- This directory contains all the scripts that scrape [this](https://www.olympedia.org/) website for data related to the
  olympics.
- Various information such as countries list, olympic games list as well as sports and games list were scraped.
- Some of this information was crucial to the prediction model.

### [Olympic Economic Data Scraper](../scripts/scrapers/olympics-economy):

- This directory contains the script that scrapes [this](https://moneynation.com/olympics-money-facts/) webpage for
  economical data related to the olympics.
- Various information such as the cost of hosting the olympics and profit/loss observed after hosting is obtained.
- This information was very crucial to the prediction model.

### [Twitter Data Scraper](../scripts/sentiment_analysis/twitter_scraper.py):

- This script scrapes Twitter data pertaining to the olympics.
- This data can be scraped by specifying start and end dates.
- These dates would be the start and end dates of a particular olympic game to perform analysis on.
- This scraper enables us to extract relevant data to perform sentiment analysis on.