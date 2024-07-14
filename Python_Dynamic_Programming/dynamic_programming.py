import math


def read_input_file(input):
    """
    Reads the input file and parses the waypoints for multiple problems.

    Args:
    input: A file-like object containing the input data.

    Returns:
    A list of problems, where each problem is a list of Waypoint objects.
    """
    first_line = True
    single_problem = []
    all_problems = []
    for newline in input:
        vnum = list(map(float, newline.strip().split()))
        if len(vnum) == 1 and first_line:
            first_line = False
        elif len(vnum) == 1:
            all_problems.append(single_problem)
            single_problem = []
        else:
            wp = Waypoint(x=vnum[0], y=vnum[1], p=vnum[2])
            single_problem.append(wp)
    return all_problems


class Waypoint:
    def __init__(self, x: float, y: float, p: float):
        """
        Initializes a Waypoint object.

        Args:
        x: The x-coordinate of the waypoint.
        y: The y-coordinate of the waypoint.
        p: The penalty associated with skipping this waypoint.
        """
        self.x = x
        self.y = y
        self.p = p


class DP_Solver:
    def __init__(self, waypoints, speed, load_time, pstart, pgoal):
        """
        Initializes the dynamic programming solver with problem parameters.

        Args:
        waypoints: A list of Waypoint objects representing the waypoints.
        speed: The speed of the robot in meters per second.
        load_time: The loading time at each waypoint in seconds.
        pstart: The starting position as a list [x, y].
        pgoal: The goal position as a list [x, y].
        """
        self.waypoints = waypoints
        self.speed = speed
        self.load_time = load_time
        self.pstart = Waypoint(pstart[0], pstart[1], 0.0)
        self.pgoal = Waypoint(pgoal[0], pgoal[1], 0.0)

    def travel_time(self, spoint, gpoint):
        """
        Calculates the travel time between two waypoints.

        Args:
        spoint: The starting waypoint index.
        gpoint: The goal waypoint index.

        Returns:
        The travel time in seconds.
        """
        x1 = self.waypoints[spoint].x
        x2 = self.waypoints[gpoint].x
        y1 = self.waypoints[spoint].y
        y2 = self.waypoints[gpoint].y
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance / self.speed

    def penalty_sum(self, spoint, gpoint):
        """
        Calculates the total penalty for skipping waypoints between two points.

        Args:
        spoint: The starting waypoint index.
        gpoint: The goal waypoint index.

        Returns:
        The total penalty for skipping waypoints.
        """
        penalty = 0
        for k in range(spoint + 1, gpoint):
            penalty += self.waypoints[k].p
        return penalty

    def solve(self):
        """
        Solves the problem using dynamic programming to find the optimal route.

        Returns:
        The optimal objective value rounded to 3 decimal places.
        """
        self.waypoints.append(self.pgoal)
        self.waypoints.insert(0, self.pstart)
        nwpoints = len(self.waypoints)

        # Initialize the dp array with infinity values
        dp = [float('inf')] * nwpoints
        dp[0] = 0  # Starting point has zero cost

        # Fill the dp array using the dynamic programming approach
        for i in range(1, nwpoints):
            for j in range(0, i):
                tji = self.travel_time(j, i)
                pji = self.penalty_sum(j, i)
                dp[i] = min(dp[i], dp[j] + tji + pji + self.load_time)

        return round(dp[-1], 3)  # Return the optimal cost to reach the goal
