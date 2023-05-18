import argparse
import time
import json
from robotics import Robot, DEFAULT_SCIENTISTS


def save_to_json(data, output_path):
    """
    Save the data to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Web scraper for scientists' data from Wikipedia.")
    parser.add_argument('-s', '--scientists', nargs='+', default=DEFAULT_SCIENTISTS,
                        help='Names of the scientists to scrape data for.')
    parser.add_argument('-m', '--model', default='en_core_web_sm', help='Spacy model for summary prediction.')
    parser.add_argument('-o', '--output', default='scientist_data.json', help='Output file for the scraped data.')
    return parser.parse_args()


def main():
    """
    Main function to execute the script.
    """
    args = parse_args()

    # Start Measuring Robo's time
    start_time = time.time()

    # Initialize the robot and introduce itself
    scientist_robo = Robot("Quandrinaut", scientists=args.scientists, summary_prediction=False, summary_prediction_model=args.model)
    scientist_robo.say_hello()

    scientist_data = scientist_robo.get_scientists_summary()

    # Say goodbye and close the browser
    scientist_robo.say_goodbye()
    
    # End Measuring Robo's time
    end_time = time.time()

    # Print the time taken by Robo and other details
    print(f"Robo took {end_time - start_time} seconds to scrape data for {len(scientist_data)} scientist(s).")

    # Save the data to a JSON file
    save_to_json(scientist_data, args.output)

if __name__ == "__main__":
    main()
