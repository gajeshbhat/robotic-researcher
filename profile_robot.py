# You need to install line_profiler package to run this script:
from lib.robotics import Robot
from line_profiler import LineProfiler

scientist_small = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin",'Ada Lovelace', 'Grace Hopper', 'Lynn Conway']
scientist_large = [
    "Albert Einstein", 
    "Isaac Newton", 
    "Marie Curie", 
    "Charles Darwin",
    "Ada Lovelace", 
    "Grace Hopper", 
    "Lynn Conway",
    "Nikola Tesla",
    "Max Planck",
    "Erwin Schrödinger",
    "Niels Bohr",
    "Werner Heisenberg",
    "Stephen Hawking",
    "Richard Feynman",
    "Galileo Galilei",
    "Johannes Kepler",
    "Michael Faraday",
    "James Clerk Maxwell",
    "Marie Skłodowska-Curie",
    "Heinrich Hertz",
    "Louis Pasteur",
    "Georg Ohm",
    "Alexander Fleming",
    "Enrico Fermi",
    "Ernest Rutherford",
    "Francis Crick",
    "James Watson",
    "Rosalind Franklin",
    "Barbara McClintock",
    "Jane Goodall",
    "Rachel Carson",
    "Carl Sagan",
    "Neil deGrasse Tyson",
    "Frederick Sanger",
    "Linus Pauling",
    "Kary Mullis",
    "Francis Collins",
    "Sally Ride",
    "Rita Levi-Montalcini",
    "Robert Hooke",
    "Edwin Hubble",
    "Antonie van Leeuwenhoek",
    "Alessandro Volta",
    "Hans Christian Oersted",
    "Andre-Marie Ampere",
    "Claude Bernard",
    "Paul Dirac",
    "Hans Bethe",
    "Murray Gell-Mann",
    "Chen Ning Yang"
]

def profile_small_input():
    robot = Robot("Quandrinaut", scientists=scientist_small, summary_prediction=False, summary_prediction_model='en_core_web_sm')
    scientist_data = robot.get_scientists_summary()
    print(len(scientist_data))
    robot.close_browser()


def profile_medium_input():
    robot = Robot("Quandrinaut", scientists=scientist_large, summary_prediction=False, summary_prediction_model='en_core_web_sm')
    scientist_data = robot.get_scientists_summary()
    print(len(scientist_data))
    robot.close_browser()

# Initialize the profiler and add the functions to be profiled:
profiler = LineProfiler()
profiler.add_function(profile_small_input)
profiler.add_function(profile_medium_input)

# Run the profiler and print the results for recursive and memoized functions:
profiler.run('profile_small_input()')
profiler.print_stats()

profiler.run('profile_medium_input()')
profiler.print_stats()
