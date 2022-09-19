





from scraper import Scraper


def main():
    scraper = Scraper()
    print('Begin :')
    # classes = [9]
    # subjects = ['Economics', 'History', 'Biology', 'Civics', 'English', 'Geography', 'Elements of Book Keeping and Accountancy', 'Maths', 'General Knowledge', 'Physics', 'Chemistry', 'Elements of Business']
    classes = [9]
    subjects = ['Economics', 'History', 'Biology', 'Civics', 'English', 'Geography', 'Elements of Book Keeping and Accountancy', 'Maths', 'General Knowledge', 'Physics', 'Chemistry', 'Elements of Business']
    scraper.start( classes,subjects )
    a = 0


if __name__ == "__main__":
    main()