<h1>Robot Navigation Challenge</h1>

<h2>Methods</h2>

**C++ Dynamic Programming**

**Python Dynamic Programming**

**Python Integer Programming**



You have been provided with a navigation challenge. A course is set up in a 100m by 100m factory. Certain points within the space are designated as targets to visit to receive goods. These targets are ordered sequentially -- target 1, target 2, and so on. Your robot must start at (0,0). From there, it should navigate to target 1, stop for 10 seconds, proceed to target 2, stop for 10 seconds, and so on. The course concludes at (100,100), where the robot must stop for an additional 10 seconds.

Each target, except (0,0) and (100,100), has a time penalty associated with missing the load. This penalty reflects the time needed for a human to handle the task later. For instance, if your robot moves directly from target 1 to target 3, skipping target 2, it would incur target 2's penalty. Once the robot reaches target 3, it cannot go back to target 2; targets must be visited in order. Since the robot must stop for 10 seconds at each target to be loaded, there is no risk of accidentally hitting a target too early. For example, if target 3 lies directly between targets 1 and 2, your robot can pass over target 3 without stopping and still incur no penalty.

Your final score is the total time (in seconds) your robot takes to complete the course, plus all penalties. Smaller scores are better.

The robot is highly maneuverable but moves at a speed of 2 m/s. During the 10-second stop at each target, it can easily turn to face the next target, allowing it to move in a straight line between targets.

Given the robot's speed, it might be advantageous to skip some targets and incur their penalties rather than manoeuvring to each one. Given a description of the course, determine the robot's best (lowest) possible time.

You may use any programming language you choose, as long as your submission is straightforward to run.

<h2>Input</h2>

There will be several test cases. Each test case begins with a line containing an integer, N (1 <= N <= 1000), which represents the number of targets on the course. Each of the following N lines describes a target with three integers, X, Y, and P, where (X, Y) is the target's location on the course (1 <= X, Y <= 99, X and Y in meters), and P is the penalty incurred if the target is missed (1 <= P <= 100). The targets are given in order -- the first line after N is target 1, the next is target 2, and so forth. All targets on a given course are unique, with at most one target at any given location. The end of input is marked by a line containing a single 0.

<h2>Output</h2>

For each test case, output a single decimal number indicating the smallest possible time for that course. Round the output to three decimal places (not truncated). Each result should be printed on its own line, with no blank lines between the results.

Sample input and output files are provided for reference.  

cat sample_input_small.txt | ./solution_executable | tee output_small.txt
