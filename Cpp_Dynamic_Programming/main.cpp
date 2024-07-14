#include "utils.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unistd.h>
#include <iomanip>
//#include <chrono>

using namespace std;

int main() {
    // Constants for the problem setup
    const double pgoal[2] = {100, 100};
    const double pstart[2] = {0, 0};
    const double otto_speed = 2.0;
    const double load_time = 10.0;

    // Determine if input is from standard input
    bool use_stdin = !isatty(fileno(stdin));
    vector<vector<utils::waypoint>> problems;

    if (!use_stdin) {
        // If not using standard input, prompt the user for the test case
        cout << "Select the test case. Press:" << endl;
        cout << "s : for sample_input_small" << endl;
        cout << "m : for sample_input_medium" << endl;
        cout << "l : for sample_input_large" << endl;
        cout << "Or press Esc to stop the program" << endl;

        char test_case;
        string fileName;
        cin >> test_case;

        // Determine which file to open based on user input
        switch (test_case) {
            case 's':
            case 'S':
                fileName = "sample_input_small.txt";
                use_stdin = false;
                break;
            case 'm':
            case 'M':
                fileName = "sample_input_medium.txt";
                use_stdin = false;
                break;
            case 'l':
            case 'L':
                fileName = "sample_input_large.txt";
                use_stdin = false;
                break;
            default:
                // Handle invalid input
                cout << "Invalid input." << endl;
                return 0;
        }

        // Open the selected input file
        ifstream textfile(fileName);
        if (!textfile.is_open()) {
            cerr << "Unable to open file: " << fileName << endl;
            return 1;
        }

        // Read the input file and parse the waypoints
        utils::read_input_file(textfile, problems);
    } else {
        // Read input from standard input and parse the waypoints
        utils::read_input_file(cin, problems);
    }

    // Uncomment the following lines to measure execution time
    // auto t_start = chrono::high_resolution_clock::now();

    // Iterate over each problem and solve it using the dynamic programming solver
    for (auto problem : problems) {
        utils::DP_Solver solver = utils::DP_Solver(problem, otto_speed, load_time, pstart, pgoal);
        // Output the result with three decimal places
        cout << fixed << setprecision(3) << solver.solve() << endl;
    }

    // Uncomment the following lines to measure execution time
    // auto t_end = chrono::high_resolution_clock::now();
    // double elapsed_time_ms = chrono::duration<double> (t_end-t_start).count();
    // cout<<"elapsed time is: " << elapsed_time_ms << endl;

    return 0;
}
