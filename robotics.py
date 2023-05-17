from RPA.Browser import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Robot:
    def __init__(self, name):
        self.name = name
        self.browser = Browser()
        self.browser.open_available_browser()

    def say_hello(self):
        print("Hello, my name is " + self.name)

    def say_goodbye(self):
        print("Goodbye, my name is " + self.name)

    def open_webpage(self, webpage):
        self.browser.go_to(webpage)

    def get_page_source(self):
        return self.browser.get_source()

    def close_browser(self):
        self.browser.close_all_browsers()

    def find_birth_death_dates(self, soup):
        born_data = soup.find('th', text='Born')
        if born_data:
            born_date = born_data.find_next_sibling('td').find('span')
            born = born_date.text.strip() if born_date else 'unknown'
        else:
            born = 'unknown'

        died_data = soup.find('th', text='Died')
        
        if died_data:
            died_date = died_data.find_next_sibling('td').find('span')
            died = died_date.text.strip() if died_date else 'unknown'
        else:
            died = 'unknown'
        return born, died


    def calculate_age(self, born, died):
        if born == 'unknown' or died == 'unknown':
            return 'unknown'

        born_date = datetime.strptime(born, "(%Y-%m-%d)")
        died_date = datetime.strptime(died, "(%Y-%m-%d)")
        age = (died_date - born_date).days // 365

        return age

    def get_first_paragraph(self, soup):
        paragraphs = soup.find_all('p')

        for paragraph in paragraphs:
            text = paragraph.text.strip()

            # Check if the paragraph has text
            if len(text) > 0:
                # Remove reference tags
                text = re.sub(r'\[\d+\]', '', text)
                # Remove extra whitespace and newline characters
                text = re.sub(r'\s+', ' ', text)
                return text

        # If no paragraph with text is found
        return 'Information not available.'

    def display_info(self, scientist, born, died, age, intro):
        print(f"Name: {scientist}")
        print(f"Born: {born}")
        print(f"Died: {died}")
        print(f"Age: {age}")
        print(f"Introduction: {intro}\n")
