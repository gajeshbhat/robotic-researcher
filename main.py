import argparse
import time
from lib.robotics import Robot, DEFAULT_SCIENTISTS
from lib.helpers import save_to_json

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Web scraper for scientists' data from Wikipedia.")
    parser.add_argument('-s', '--scientists', nargs='+', default=DEFAULT_SCIENTISTS,
                        help='Names of the scientists to scrape data for.')
    parser.add_argument('-m', '--model', default='en_core_web_sm', help='Spacy model for summary prediction.')
    parser.add_argument('-o', '--output', default='data/scientist_data.json', help='Output file for the scraped data.')
    parser.add_argument('-sp', '--summary_prediction', type=bool, default=False, help='Enable or disable summary prediction.')
    return parser.parse_args()


def init_robot(args):
    """
    Initialize the Robot with given arguments and introduces itself.
    """
    robot = Robot("Quandrinaut", scientists=args.scientists, summary_prediction=args.summary_prediction, summary_prediction_model=args.model)
    robot.say_hello()
    return robot


def collect_data(robot):
    """
    Collect scientist data using the robot.
    """
    return robot.get_scientists_summary()


def close_robot(robot):
    """
    Close the robot and print a goodbye message.
    """
    robot.say_goodbye()


def measure_time(func):
    """
    Measure the time taken by a function to execute.
    """
    start_time = time.time()
    result = func()
    end_time = time.time()

    print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
    return result


def save_data(data, output_file):
    """
    Save data to a JSON file.
    """
    save_to_json(data, output_file)


def main():
    """
    Main function to execute the script.
    """
    args = parse_args()
    
    scientist_robo = measure_time(lambda: init_robot(args))
    scientist_data = measure_time(lambda: collect_data(scientist_robo))
    
    print(f"Robo scraped data for {len(scientist_data)} scientist(s).")

    close_robot(scientist_robo)
    save_data(scientist_data, args.output)


if __name__ == "__main__":
    main()
