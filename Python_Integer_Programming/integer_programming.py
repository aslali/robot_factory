import pulp
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


class IP_Solver:
    def __init__(self, waypoints, speed, load_time, pstart, pgoal):
        """
        Initializes the integer programming solver with problem parameters.

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
        for i in range(spoint + 1, gpoint):
            penalty += self.waypoints[i].p
        return penalty

    def solve(self):
        """
        Solves the integer programming problem to find the optimal route.

        Returns:
        The optimal objective value rounded to 3 decimal places if an optimal solution is found, otherwise None.
        """
        self.waypoints.append(self.pgoal)
        self.waypoints.insert(0, self.pstart)
        nwpoints = len(self.waypoints)
        model = pulp.LpProblem("OTTO_Robot", pulp.LpMinimize)

        # Create binary decision variables
        x = pulp.LpVariable.dicts("x", ((i, j) for i in range(1, nwpoints) for j in range(i + 1, nwpoints + 1)),
                                  cat='Binary')

        # Set objective function: minimize the total time including travel, penalties, and loading time
        model += pulp.lpSum(x[i, j] * (self.travel_time(i - 1, j - 1) + self.penalty_sum(i - 1, j - 1) + self.load_time)
                            for i in range(1, nwpoints) for j in range(i + 1, nwpoints + 1))

        # Add constraints
        # Ensure the robot starts from the starting point (0,0)
        model += pulp.lpSum(x[1, j] for j in range(2, nwpoints + 1)) == 1

        # Ensure the robot ends at the goal point (100,100)
        model += pulp.lpSum(x[i, nwpoints] for i in range(1, nwpoints)) == 1

        # Ensure the path is continuous (flow constraints)
        for k in range(2, nwpoints):
            model += pulp.lpSum(x[j, k] for j in range(1, k)) == pulp.lpSum(x[k, j] for j in range(k + 1, nwpoints + 1))

        # Solve the model using the CBC solver with no message
        model.solve(pulp.PULP_CBC_CMD(msg=False))

        # Return the solution if an optimal solution is found
        if pulp.LpStatus[model.status] == 'Optimal':
            return round(pulp.value(model.objective), 3)
        else:
            print('No optimal solution found')
            return None
