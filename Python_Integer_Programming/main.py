import sys
import select
from integer_programming import *  # Import integer programming solver 
# import time  # Import time module for calculating calculation time

# OTTO robot's speed in meters per second
otto_speed = 2.0

# Time in seconds to load at each waypoint
load_time = 10.0

# Starting position (0, 0)
pstart = [0, 0]

# Goal position (100, 100)
pgoal = [100, 100]

# Determine whether to use standard input
use_stdin = not select.select([sys.stdin], [], [], 0)[0]

# List to store the problems (test cases)
problems = []

# If not using standard input, prompt user to select a test case
if use_stdin:
    print("Select the test case. Press:")
    print("s : for sample_input_small")
    print("m : for sample_input_medium")
    print("l : for sample_input_large")
    print("Or press Esc to stop the program")

    # Get user input for selecting the test case
    test_case = input().strip()
    fileName = ""

    # Determine the file name based on user input
    if test_case in ['s', 'S']:
        fileName = "sample_input_small.txt"
        use_stdin = False
    elif test_case in ['m', 'M']:
        fileName = "sample_input_medium.txt"
        use_stdin = False
    elif test_case in ['l', 'L']:
        fileName = "sample_input_large.txt"
        use_stdin = False
    else:
        # Invalid input, exit the program
        print("Invalid input.")
        sys.exit(0)

    # Try to open the selected file and read the problems
    try:
        with open(fileName, 'r') as textfile:
            problems = read_input_file(textfile)
    except IOError:
        # Handle file opening errors
        print(f"Unable to open file: {fileName}", file=sys.stderr)
        sys.exit(1)
else:
    # If using standard input, read problems from stdin
    problems = read_input_file(sys.stdin)

# Uncomment the following lines to measure the execution time
# start_t = time.time()

# Solve each problem using the integer programming solver
for problem in problems:
    solver = IP_Solver(problem, otto_speed, load_time, pstart, pgoal)
    print(solver.solve())

# Uncomment the following lines to measure the execution time
# end_t = time.time()
# print(end_t - start_t)
