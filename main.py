from robotics import Robot
from bs4 import BeautifulSoup

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

robot = Robot("Quandrinaut")

def introduce_yourself():
    robot.say_hello()

def main():
    introduce_yourself()

    for scientist in SCIENTISTS:
        url = f"https://en.wikipedia.org/wiki/{scientist.replace(' ', '_')}"
        robot.open_webpage(url)

        soup = BeautifulSoup(robot.get_page_source(), "html.parser")

        born, died = robot.find_birth_death_dates(soup)
        
        age = robot.calculate_age(born, died)
        
        born = born.replace('(', '').replace(')', '')
        died = died.replace('(', '').replace(')', '')

        intro = robot.get_first_paragraph(soup)

        robot.display_info(scientist, born, died, age, intro)

    robot.close_browser()

if __name__ == "__main__":
    main()
