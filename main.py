from robotics import Robot
from bs4 import BeautifulSoup
import json

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

robot = Robot("Quandrinaut")

def introduce_yourself():
    robot.say_hello()

def main():
    introduce_yourself()
    scientist_data = []

    for scientist in SCIENTISTS:
        url = f"https://en.wikipedia.org/wiki/{scientist.replace(' ', '_')}"
        robot.open_webpage(url)

        soup = BeautifulSoup(robot.get_page_source(), "html.parser")

        born, died = robot.find_birth_death_dates(soup)
        
        age = robot.calculate_age(born, died)
        
        born = born.replace('(', '').replace(')', '')
        died = died.replace('(', '').replace(')', '')

        intro = robot.get_first_paragraph(soup)
        feild_of_work = robot.get_field_of_work(soup)
        birthplace = robot.get_birthplace(soup)

        robot.display_info(scientist, born, died, age, intro, feild_of_work,birthplace)
        
        scientist_data.append({
                'name': scientist,
                'born': born,
                'died': died,
                'age': age,
                'introduction': intro,
                'field_of_work': feild_of_work,
                'birthplace': birthplace
            })
    with open('scientist_data.json', 'w') as f:
        json.dump(scientist_data, f, indent=4)

    robot.close_browser()

if __name__ == "__main__":
    main()
