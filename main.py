





from scraper import Scraper


def main():
    scraper = Scraper()
    print('Begin :')
    # classes = [9]
    # subjects = ['Economics', 'History', 'Biology', 'Civics', 'English', 'Geography', 'Elements of Book Keeping and Accountancy', 'Maths', 'General Knowledge', 'Physics', 'Chemistry', 'Elements of Business']
    skip_urls = ['https://www.toppr.com/ask/question-set/physical-features-of-india-410330/ntse/']
    scraper.scrape('https://www.toppr.com/ask/question-set/motion-411129/medium/', 9, 'alpha', 'topic', 'ntse',skip_urls)
    classes = [9]
    subjects = ['Economics', 'History', 'Biology', 'Civics', 'English', 'Geography', 'Elements of Book Keeping and Accountancy', 'Maths', 'General Knowledge', 'Physics', 'Chemistry', 'Elements of Business']
    scraper.start( classes,subjects, skip_urls )
   


if __name__ == "__main__":
    main()