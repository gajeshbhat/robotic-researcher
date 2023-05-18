from RPA.Browser.Selenium import Selenium
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, List
from pathlib import Path
import re
import spacy
import os

DEFAULT_SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]
BASE_URL = "https://en.wikipedia.org/wiki/"

class Robot:

    def __init__(self, name: str, scientists: Optional[List[str]] = None,
                 summary_prediction: bool = False,
                 summary_prediction_model: str = "en_core_web_sm"):
        """
        Initializes the robot with a name and opens a browser.
        """
        self.name = name
        self.browser = Selenium()
        self.browser.open_available_browser()
        self.summary_prediction = summary_prediction
        self.summary_prediction_model = summary_prediction_model
    
        if scientists is None:
            self.scientists = DEFAULT_SCIENTISTS
        else:
            self.scientists = scientists

        if self.summary_prediction:
            # Define the model used for NER
            self.model_name = self.summary_prediction_model

            if not os.path.exists(os.getcwd() + "/models/" + self.model_name + "/" ):
                self.download_and_store_spacy_model()

            # Load the model
            self.nlp = spacy.load(os.getcwd() + "/models/" + self.model_name + "/")
        
    
    def download_and_store_spacy_model(self):
        if not os.path.exists(os.getcwd() + "/models/"+self.model_name):
            os.makedirs(os.getcwd() + "/models/"+ self.model_name, exist_ok=True)

        # Download the model    
        spacy.cli.download(self.model_name)
        
        # Save the model
        nlp = spacy.load(self.model_name)
        nlp.to_disk(os.getcwd() + "/models/"+self.model_name+"/")
        
        
            
    def infer_field_of_work(self, intro: str) -> str:
        # Load the small English model
        field_of_work_entities = []
        doc = self.nlp(intro)

        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "EVENT", "LAW", "LANGUAGE", "NORP"]:
                field_of_work_entities.append(ent.text)

        # Remove duplicates and join the keywords
        field_of_work = list(set(field_of_work_entities))
    
        if field_of_work:
            return ', '.join(field_of_work)
        else:
            return 'Not specified'


    def get_scientists_summary(self) -> List[dict]:
        """
        Returns a list of dictionaries containing the information of the scientists.
        """
        scientist_data = []
        for scientist in self.scientists:
            scientist_details = self.parse_scientist_data(scientist)
            scientist_data.append(scientist_details)
        return scientist_data
    
    def parse_scientist_data(self, scientist: str) -> dict:
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
        
        self.display_info(scientist, born, died, age, intro, field_of_work, birthplace)
        
        return {
        'name': scientist,
        'born': born,
        'died': died,
        'age': age,
        'introduction': intro,
        'field_of_work': field_of_work,
        'birthplace': birthplace
        }

    def say_hello(self):
        "Introduces itself to the user and describes what it does"
        print(f"Hello, my name is {self.name}")

    def _open_webpage(self, webpage: str):
        self.browser.go_to(webpage)

    def get_scientist_page_soup(self, scientist: str) -> str:
        scientist_info_url = BASE_URL + scientist.replace(' ', '_')
        self._open_webpage(scientist_info_url)
        soup = BeautifulSoup(self._get_page_source(), "html.parser")
        return soup
    
    def _get_page_source(self) -> str:
        return self.browser.get_source()

    def say_goodbye(self):
        print(f"Goodbye, my name is {self.name}")
        self._close_browser()

    # Private method to close the browser
    def _close_browser(self):
        self.browser.close_all_browsers()

    def find_birth_death_dates(self, soup: BeautifulSoup) -> tuple:
        born, died = 'unknown', 'unknown'

        born_data = soup.find('th', string='Born')
        if born_data:
            born_date = born_data.find_next_sibling('td').find('span')
            if born_date:
                born = born_date.text.strip()

        died_data = soup.find('th', string='Died')
        if died_data:
            died_date = died_data.find_next_sibling('td').find('span')
            if died_date:
                died = died_date.text.strip()

        if born != 'unknown' and died == 'unknown':
            died = 'Present'
        
        return born, died

    def calculate_age(self, born: str, died: str) -> str:
        if born == 'unknown' and died == 'unknown':
            return 'unknown'
        
        if died == 'Present':
            born_date = datetime.strptime(born, "(%Y-%m-%d)")
            today = datetime.today()
            age = (today - born_date).days // 365

            return age

        born_date = datetime.strptime(born, "(%Y-%m-%d)")
        died_date = datetime.strptime(died, "(%Y-%m-%d)")
        age = (died_date - born_date).days // 365

        return age

    def get_first_paragraph(self, soup: BeautifulSoup) -> str:
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

    def display_info(self, scientist: str, born: str, died: str, age: str, intro: str,
                    field_of_work: str, birthplace: str) -> None:
        print(f"Name: {scientist}")
        print(f"Born: {born}")
        print(f"Died: {died}")
        print(f"Age: {age}")
        print(f"Birthplace: {birthplace}\n")
        print(f"Introduction: {intro}\n")
        print(f"Field of work: {field_of_work}\n")

    def get_field_of_work(self, soup: BeautifulSoup) -> str:
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

        # Remove reference tags
        field_of_work = re.sub(r'\[\d+\]', '', field_of_work)

        # Remove extra whitespace and newline characters
        field_of_work = re.sub(r'\s+', ' ', field_of_work)

        return field_of_work

    def get_birthplace(self, soup: BeautifulSoup) -> str:
        infobox = soup.find('table', {'class': 'infobox'})
        if not infobox:
            return 'unknown'

        birthplace_data = infobox.find('th', string='Born')
        if not birthplace_data:
            return 'unknown'

        birthplace_td = birthplace_data.find_next_sibling('td')
        if not birthplace_td:
            return 'unknown'

        birthplace = birthplace_td.find('div', {'class': 'birthplace'})
        if not birthplace:
            return 'Not specified'

        birthplace_text = birthplace.text.strip()

        # Remove reference tags
        birthplace_text = re.sub(r'\[\d+\]', '', birthplace_text)

        # Remove extra whitespace and newline characters
        birthplace_text = re.sub(r'\s+', ' ', birthplace_text)

        return birthplace_text