# Robotic Researcher

Welcome to the Robotic Researcher project. This project is a software robot designed to retrieve and display key information about a list of renowned scientists.

The robot accomplishes this by navigating to each scientist's Wikipedia page, extracting important information, and displaying it in a user-friendly format. It leverages the `rpaframework` library for browser automation and the `bs4` library for web scraping.

## Installation

Before you run the robot, make sure you have the necessary Python libraries installed:

```bash
pip install rpaframework bs4 spacy
```

## Execution

Run the robot using the following command:

```bash
python robotics_researcher.py
```

## Example commands
Below are some examples of different ways you can run the script `robotics_researcher.py` Assume SCIENTISTS is a list of scientists names.

Run the robot without any command line arguments:
```
python robotics_researcher.py
```
This will use default values for all parameters and start scraping information for the scientists specified in the script itself.

Specify a list of scientists as a command line argument:
```
python robotics_researcher.py --scientists "Albert Einstein" "Isaac Newton" "Marie Curie"
```

This will override the default scientists list and start scraping information for Albert Einstein, Isaac Newton, and Marie Curie.

Specify an output file:
```
python robotics_researcher.py --output_file scientists_data.json
```
This will save the scraped data in a file named scientists_data.json.

Combine the above options:
``` 
python robotics_researcher.py --scientists "Albert Einstein" "Isaac Newton" "Marie Curie" --output_file scientists_data.json
```
This will scrape information for Albert Einstein, Isaac Newton, and Marie Curie and save the results in a file named scientists_data.json.

You can optionally add command line arguments to customize the operation.

## Code Structure

### 1. robotics_researcher.py

This script orchestrates the entire web scraping operation. It provides command line argument parsing to customize the operation as required. 

If you run the script, it uses the given arguments (or defaults) to scrape Wikipedia for information on specific scientists, display it, and optionally save it to a file.

### 2. lib/robotics.py

This Python module contains the `Robot` class, which is responsible for scraping data from Wikipedia for specific scientists. 

The `Robot` class provides functionalities to:

- Open a browser and navigate to each scientist's Wikipedia page.
- Retrieve and calculate key information such as date of birth, date of death, age, the first paragraph of their Wikipedia page, and more.
- Display the retrieved information in an easily readable manner.
- Optionally predict the scientist's field of work using a Spacy model, if this information isn't directly available on their Wikipedia page.
- Save and load the Spacy model for the prediction.
- Gracefully handle exceptions, including when the browser fails to open or close.

### 3. lib/helpers.py

This Python module includes helper functions, such as `save_to_json()`, to aid in certain operations like saving data to a JSON file.

### 4. tests/test_robotics.py

This Python module contains unit tests for the `Robot` class. It uses the `unittest` library to test the functionalities of the `Robot` class.

## Bonus Features

This robot has the ability to infer the field of work of a scientist from the first paragraph of their Wikipedia page using a Spacy model.

## Error Handling

The robot is equipped to handle common errors that may occur during web scraping. For example, if the robot fails to retrieve a piece of information, it will handle the exception gracefully and continue with the operation.

## Profiling and Benchmarking


## Future Enhancements

There are numerous potential enhancements to this project, such as:

- Enhancing the Spacy model training for more accurate predictions of a scientist's field of work.
- Adding multi-threading to scrape data for multiple scientists concurrently.
- Including more details about scientists, such as their significant contributions or awards received.

## Submission

