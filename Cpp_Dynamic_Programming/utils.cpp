#include "utils.h"
#include <iostream>
#include <string>
#include <vector>
#include <limits>
#include <cmath>
using namespace std;

namespace utils {

    // Function to read input from a file or standard input
    // and parse it into a vector of waypoint vectors (problems)
    void read_input_file(istream& input, vector<vector<waypoint>>& all_problems) {
        string newline;
        double num;
        bool first_line = true;

        vector<waypoint> single_problem;

        // Read each line from the input
        while (getline(input, newline)) {
            stringstream ss(newline);
            vector<double> vnum;

            // Parse numbers from the line
            while (ss >> num) {
                vnum.push_back(num);
            }

            // First line indicates the number of waypoints
            if (vnum.size() == 1 && first_line) {
                first_line = false;
            } else if (vnum.size() == 1) {
                // A single number indicates the end of a problem set
                all_problems.push_back(single_problem);
                single_problem.clear();
            } else {
                // Parse waypoint details and add to the current problem
                waypoint wp;
                wp.x = vnum[0];
                wp.y = vnum[1];
                wp.p = vnum[2];
                single_problem.push_back(wp);
            }
        }
    }

    // Constructor to initialize the solver with waypoints, speed, load time, start, and goal positions
    DP_Solver::DP_Solver(vector<waypoint> waypoints, double speed, double load_time, const double pstart[2], const double pgoal[2]) :
        waypoints(waypoints), speed(speed), load_time(load_time) {

        this->pstart.x = pstart[0];
        this->pstart.y = pstart[1];
        this->pstart.p = 0.0;

        this->pgoal.x = pgoal[0];
        this->pgoal.y = pgoal[1];
        this->pgoal.p = 0.0;
    }

    // Function to calculate travel time between two waypoints
    double DP_Solver::travel_time(int spoint, int gpoint) {
        double x1 = waypoints[spoint].x;
        double x2 = waypoints[gpoint].x;
        double y1 = waypoints[spoint].y;
        double y2 = waypoints[gpoint].y;
        double distance = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2));
        return distance / speed;
    }

    // Function to calculate the penalty sum for skipping waypoints between two points
    double DP_Solver::penalty_sum(int spoint, int gpoint) {
        double penalty = 0;
        for (int k = spoint + 1; k < gpoint; ++k) {
            penalty += waypoints[k].p;
        }
        return penalty;
    }

    // Function to solve the problem and return the minimum time required
    double DP_Solver::solve() {
        waypoints.push_back(pgoal);  // Add goal to waypoints
        waypoints.insert(waypoints.begin(), pstart);  // Add start to waypoints
        int nwpoints = waypoints.size();
        vector<double> dp(nwpoints, numeric_limits<double>::max());
        dp[0] = 0;  // Starting point has zero cost

        // Dynamic programming to compute minimum time to reach each waypoint
        for (int i = 1; i < nwpoints; ++i) {
            for (int j = 0; j < i; ++j) {
                double tji = travel_time(j, i);
                double pji = penalty_sum(j, i);
                dp[i] = min(dp[i], dp[j] + tji + pji + load_time);
            }
        }

        return round(dp.back() * 1000) / 1000;  // Return rounded result to 3 decimal places
    }

} // namespace utils
