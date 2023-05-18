from RPA.Browser.Selenium import Selenium
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, List
import re
import spacy
import os

DEFAULT_SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin",'Ada Lovelace', 'Grace Hopper', 'Lynn Conway']
BASE_URL = "https://en.wikipedia.org/wiki/"

class Robot:

    def __init__(self, name: str, scientists: Optional[List[str]] = None,
                 summary_prediction: bool = False,
                 summary_prediction_model: str = "en_core_web_sm",headless: bool = False):
        """
        Initializes the robot with a name and opens a browser.
        
        Parameters:
        name: str - The name of the robot
        scientists: Optional[List[str]] - A list of scientists to scrape data for. Defaults to a pre-defined list.
        summary_prediction: bool - Whether or not to use a spacy model to predict the field of work from the scientist's introduction.
        summary_prediction_model: str - The name of the spacy model to use for predictions. Defaults to "en_core_web_sm".
        headless: bool - Whether or not to run the browser in headless mode.
        """
        self.name = name
        self.browser = Selenium()
        self.browser.open_available_browser(headless=headless)
        self.summary_prediction = summary_prediction
        self.summary_prediction_model = summary_prediction_model
    
        if scientists is None:
            self.scientists = DEFAULT_SCIENTISTS
        else:
            self.scientists = scientists

        if self.summary_prediction:
            self.model_name = self.summary_prediction_model
            self.ensure_spacy_model_exists()
            self.nlp = spacy.load(self.get_model_path())

    def get_scientists_summary(self) -> List[dict]:
        """
        Returns a list of dictionaries containing the information of the scientists.
        """
        return [self.parse_scientist_data(scientist) for scientist in self.scientists]

    def parse_scientist_data(self, scientist: str) -> dict:
        """
        Returns a dictionary containing the information of the scientist.
        """
        try:
            soup = self.get_scientist_page_soup(scientist)
            born, died = self.find_birth_death_dates(soup)
            age = self.calculate_age(born, died)

            born = born.replace('(', '').replace(')', '')
            died = died.replace('(', '').replace(')', '')

            intro = self.get_first_paragraph(soup)
            field_of_work = self.get_field_of_work(soup)

            if field_of_work == 'Not specified' and intro != 'unknown' and self.summary_prediction:
                field_of_work = self.infer_field_of_work(intro) + " (Predicted)"

            birthplace = self.get_birthplace(soup)

            return {
                'name': scientist,
                'born': born,
                'died': died,
                'age': age,
                'introduction': intro,
                'field_of_work': field_of_work,
                'birthplace': birthplace
            }
        except Exception as e:
            print(f"Error while parsing scientist data: {e}")
            return {}
    
    def infer_field_of_work(self, intro: str) -> str:
        """
        Infers the field of work from the introduction.
        """
        doc = self.nlp(intro)
        field_of_work_entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "EVENT", "LAW", "LANGUAGE", "NORP"]]
        field_of_work = ', '.join(list(set(field_of_work_entities)))  # Remove duplicates and join the keywords

        return field_of_work if field_of_work else 'Not specified'

    def find_birth_death_dates(self, soup: BeautifulSoup) -> tuple:
        """
        Finds the birth and death dates of the scientist from the soup object.
        """
        born = self.find_date(soup, 'Born')
        died = self.find_date(soup, 'Died')

        if born != 'unknown' and died == 'unknown':
            died = 'Present'

        return born, died

    def find_date(self, soup: BeautifulSoup, date_type: str) -> str:
        """
        Finds a date (born or died) of the scientist from the soup object.
        """
        try:
            date_data = soup.find('th', string=date_type)
            date = date_data.find_next_sibling('td').find('span').text.strip() if date_data else 'unknown'
        except Exception as e:
            print(f"Error while finding {date_type} date: {e}")
            date = 'unknown'
        return date

    def calculate_age(self, born: str, died: str) -> str:
        """
        Calculates the age of the scientist.
        """
        try:
            born_date = datetime.strptime(born, "(%Y-%m-%d)")
            died_date = datetime.strptime(died, "(%Y-%m-%d)") if died != 'Present' else datetime.today()
            age = (died_date - born_date).days // 365
        except Exception as e:
            print(f"Error while calculating age: {e}")
            age = 'unknown'
        return age
    
    def get_first_paragraph(self, soup: BeautifulSoup) -> str:
        """
        Gets the first paragraph of the scientist page.
        """
        paragraphs = soup.find_all('p')
        try:
            for paragraph in paragraphs:
                text = paragraph.text.strip()
                # Check if the paragraph has text
                if len(text) > 0:
                    text = self.clean_text(text)
                    return text
            # If no paragraph with text is found
            return 'Information not available.'
        except Exception as e:
            print(f"Error while getting first paragraph: {e}")
            return 'unknown'

    def get_field_of_work(self, soup: BeautifulSoup) -> str:
        """
            Gets the field of work of the scientist.
        """
        infobox = soup.find('table', {'class': 'infobox'})
        if not infobox:
            return 'Not specified'

        field_data = infobox.find('th', string='Fields')
        if not field_data:
            return 'Not specified'

        fields_td = field_data.find_next_sibling('td')
        if not fields_td:
            return 'Not specified'

        fields = fields_td.find_all('a')
        field_of_work = ', '.join([field.text for field in fields])
        return self.clean_text(field_of_work) if field_of_work else 'Not specified'

    def get_birthplace(self, soup: BeautifulSoup) -> str:
        """
        Gets the birthplace of the scientist.
        """
        try:
            infobox = soup.find('table', {'class': 'infobox'})
            if not infobox:
                return 'Not specified'

            birthplace_data = infobox.find('th', string='Born')
            if not birthplace_data:
                return 'Not specified'

            birthplace_td = birthplace_data.find_next_sibling('td')
            if not birthplace_td:
                return 'Not specified'

            birthplace = birthplace_td.find('div', {'class': 'birthplace'})
            if not birthplace:
                return 'Not specified'

            birthplace_text = birthplace.text.strip()
            return self.clean_text(birthplace_text) if birthplace_text else 'Not specified'
        except Exception as e:
            print(f"Error while getting birthplace: {e}")
            return 'unknown'

    def clean_text(self, text: str) -> str:
        """
        Cleans the text.
        """
        text = text.strip()  # Remove whitespace at the beginning and end
        text = re.sub(r'\[\d+\]', '', text)  # Remove reference tags
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace and newline characters
        return text
    
    # Helper Functions
    def ensure_spacy_model_exists(self) -> None:
        """
        Check if the model exists, if not download and store it.
        """
        if not os.path.exists(self.get_model_path()):
            self.download_and_store_spacy_model()

    def get_model_path(self) -> str:
        """
        Returns the path of the spacy model.
        """
        return os.path.join(os.getcwd(), "models", self.model_name)

    def download_and_store_spacy_model(self) -> None:
        """
        Downloads and stores the spacy model.
        """
        if not os.path.exists(os.path.join(os.getcwd(), "models")):
            os.makedirs(os.path.join(os.getcwd(), "models/{self.model_name}}/"), exist_ok=True)
        spacy.cli.download(self.model_name)
        nlp = spacy.load(self.model_name)
        nlp.to_disk(self.get_model_path())

    def get_scientist_page_soup(self, scientist: str) -> BeautifulSoup:
        """
        Fetches the scientist page and returns the parsed BeautifulSoup object.
        """
        scientist_info_url = BASE_URL + scientist.replace(' ', '_')
        self._open_webpage(scientist_info_url)
        return BeautifulSoup(self._get_page_source(), "html.parser")

    def _open_webpage(self, webpage: str) -> None:
        """
        Opens the webpage.
        """
        try:
            self.browser.go_to(webpage)
        except Exception as e:
            print(f"Error while opening webpage: {e}")

    def _get_page_source(self) -> str:
        """
        Returns the page source of the current webpage.
        """
        try:
            return self.browser.get_source()
        except Exception as e:
            print(f"Error while getting page source: {e}")
            return ""

    def close_browser(self) -> None:
        """
        Closes the browser.
        """
        try:
            self.browser.close_all_browsers()
        except Exception as e:
            print(f"Error while closing browser: {e}")


    # Greetings and Console Output

    def say_hello(self) -> None:
        """
        Says hello to the user and explains what the robot does and the steps involved.
        """
        print(f"\nHello, I am {self.name}! I am a robot that can scrape data from Wikipedia for scientists and predict their field of work using their introduction if not available on wikipedia.")
        print("Let's get started!\n")

    def say_goodbye(self) -> None:
        """
        Says goodbye to the user.
        """
        print(f"\nGoodbye! I hope you liked my work.")

    @staticmethod
    def display_info(scientists) -> None:
        """
        Displays the information of the scientist.
        """
        for scientist in scientists:
            print(f"Name: {scientist['name']}\n")
            print(f"Born: {scientist['born']}")
            print(f"Died: {scientist['died']}")
            print(f"Age: {scientist['age']}\n")
            print(f"Introduction: {scientist['introduction']}\n")
            print(f"Field of work: {scientist['field_of_work']}")
            print(f"Birthplace: {scientist['birthplace']}")
            print("----------------------------------------\n")