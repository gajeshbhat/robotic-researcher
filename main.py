from robotics import Robot
from bs4 import BeautifulSoup
import json

def main() -> None:
    # Initialize the robot and Introduce itself
    scientist_robo = Robot("Quandrinaut",scientists=['Ada Lovelace', 'Grace Hopper', 'Lynn Conway'],summary_prediction=True,summary_prediction_model="en_core_web_lg")
    scientist_robo.say_hello()

    scientist_data = scientist_robo.get_scientists_summary()

    with open('data/scientist_data.json', 'w') as f:
        json.dump(scientist_data, f, indent=4)

    # Say goodbye and close the browser
    scientist_robo.say_goodbye()

if __name__ == "__main__":
    main()
