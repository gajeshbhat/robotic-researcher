# Robotic Researcher

Welcome to the Robotic Researcher project. This project is a software robot designed to retrieve and display key information about a list of renowned scientists.

The robot accomplishes this by navigating to each scientist's Wikipedia page, extracting important information, and displaying it in a user-friendly format. It leverages the `rpaframework` library for browser automation and the `bs4` library for web scraping.

## Installation
You can create a virtual environment and install the dependencies using the following commands:

```
python3 -m venv venv
source venv/bin/activate
```

Before you run the robot, make sure you have the necessary Python libraries installed:
```
pip install -r requirements.txt
```
**Note:** This may take a while as it will install the spacy model as well which can be used to add a lot of features to the robot and work on parsed data. I have included the venv folder as well which has all the dependencies installed. In that case you can just go ahead and enable it using ```source venv/bin/activate``` and run the robot.

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
1. I have added a profiling file profile_robot.py to profile the Robot class.
2. I used the `line profiler` package to profile the two different implementations for S-expression evaluation. You can install it by running `pip install line_profiler` or by running pip install -r requirements.txt
3. Below are the results from the test runs I did. This further helps us pin point the performance bottleneck in the code.

```
Total time: 14.3133 s
File: /Users/gajesh/git/robotic_researcher/profile_robot.py
Function: profile_small_input at line 59

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    59                                           def profile_small_input():
    60         1 2639477000.0 2639477000.0     18.4      robot = Robot("Quandrinaut", scientists=scientist_small, summary_prediction=False, summary_prediction_model='en_core_web_sm')
    61         1 11673784000.0 11673784000.0     81.6      scientist_data = robot.get_scientists_summary()
    62         1      43000.0  43000.0      0.0      print(len(scientist_data))

Total time: 81.1858 s
File: /Users/gajesh/git/robotic_researcher/profile_robot.py
Function: profile_medium_input at line 65

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    65                                           def profile_medium_input():
    66         1 2546859000.0 2546859000.0      3.1      robot = Robot("Quandrinaut", scientists=scientist_large, summary_prediction=False, summary_prediction_model='en_core_web_sm')
    67         1 78638934000.0 78638934000.0     96.9      scientist_data = robot.get_scientists_summary()
    68         1      30000.0  30000.0      0.0      print(len(scientist_data))
```

Run `python profile_robot.py` to run the profiling script.

## Future Enhancements

There are numerous potential enhancements to this project, such as:

- Enhancing the Spacy model training for more accurate predictions of a scientist's field of work.
- Adding multi-threading to scrape data for multiple scientists concurrently.
- Including more details about scientists, such as their significant contributions or awards received.
- Using spacy model to extract more information from the summary text and creating a knwoledge graph of the scientist.

