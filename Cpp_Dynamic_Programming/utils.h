#ifndef UTILS_H
#define UTILS_H

#include <sstream>
#include <string>
#include <vector>

namespace utils {

    // Structure to store waypoint information (x, y coordinates and penalty p)
    struct waypoint {
        double x, y, p;
    };

    // Function to read input from a file or standard input
    // and parse it into a vector of waypoint vectors (problems)
    void read_input_file(std::istream& input, std::vector<std::vector<waypoint>>& problems);

    // Class to implement the Dynamic Programming Solver for the OTTO problem
    class DP_Solver {
    public:
        // Constructor to initialize the solver with waypoints, speed, load time, start, and goal positions
        DP_Solver(std::vector<utils::waypoint> waypoints, double speed, double load_time, const double pstart[2], const double pgoal[2]);

        // Function to solve the problem and return the minimum time required
        double solve();

    private:
        // Function to calculate travel time between two waypoints
        double travel_time(int spoint, int gpoint);

        // Function to calculate the penalty sum for skipping waypoints between two points
        double penalty_sum(int spoint, int gpoint);

        // Vector to store waypoints
        std::vector<utils::waypoint> waypoints;
        const double speed;        // Robot speed
        const double load_time;    // Load time at each waypoint
        waypoint pstart, pgoal;    // Start and goal waypoints
    };

}

#endif // UTILS_H
