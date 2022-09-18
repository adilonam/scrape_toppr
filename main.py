





from scraper import Scraper


def main():
    scraper = Scraper()
    print('Url to scrape :')
    url = 'https://www.toppr.com/ask/question-set/the-story-of-village-palampur-410265/hard/'
    scraper.scrape(url, '9', 'Economics', 'The Story of Village Palampur', 'easy')
    a = 0


if __name__ == "__main__":
    main()