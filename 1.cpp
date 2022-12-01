#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::vector<unsigned int> elves;

    std::ifstream file("1.txt", std::ios::in);
    std::string line;
    unsigned int current_total = 0;

    while (std::getline(file, line)) {
        if (line == "") {
            elves.push_back(current_total);
            current_total = 0;
        }

        std::istringstream ss(line);
        int val;
        if (ss >> val) {
            current_total += val;
        }
    }

    std::sort(elves.begin(), elves.end());

    // highest value
    std::cout << elves[elves.size()-1] << std::endl;

    // sum of top 3 values
    unsigned int part_2 = 0;
    for (int i = 1; i <= 3; i++) {
        part_2 += elves[elves.size()-i];
    }
    std::cout << part_2 << std::endl;

    return 0;
}