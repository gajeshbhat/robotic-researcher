import argparse
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
    parser.add_argument('-o', '--output', default='scientist_data.json', help='Output file for the scraped data.')
    parser.add_argument('-sp', '--summary_prediction', type=bool, default=False, help='Enable or disable summary prediction.')

    return parser.parse_args()


def init_robot(args):
    """
    Initialize the Robot with given arguments and introduces itself.
    """
    robot = Robot("Quandrinaut", scientists=args.scientists, summary_prediction=args.summary_prediction, summary_prediction_model=args.model)
    robot.say_hello()
    return robot


def main():
    """
    Main function to execute the script.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Initialize the robot
    scientist_parser_robot = init_robot(args)
    # Get the data about the scientists
    scientist_data = scientist_parser_robot.get_scientists_summary()
    # Display the data
    scientist_parser_robot.display_info(scientist_data)

    # If output file is specified, save the data to the file
    if args.output:
        save_to_json(scientist_data, args.output)

if __name__ == "__main__":
    main()
