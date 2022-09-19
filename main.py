





from scraper import Scraper


def main():
    scraper = Scraper()
    print('Begin :')
    # url = 'https://www.toppr.com/ask/question-set/the-story-of-village-palampur-410265/hard/'
    # scraper.scrape('https://www.toppr.com/ask/question-set/people-as-resource-410295/hard/', '9', 'Economics', 'The Story of Village Palampur', 'easy')
    scraper.start( [9])
    a = 0


if __name__ == "__main__":
    main()