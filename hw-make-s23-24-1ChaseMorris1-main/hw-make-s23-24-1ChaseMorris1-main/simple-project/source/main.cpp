// Brock Ferrell
// CS2401
// November 23, 2015
// Project7
#include <string>
#include <iostream>

#include "game.hpp"
#include "othello.hpp"

using namespace std;
using namespace main_savitch_14;

int main(int argc, char* argv[])
{
    if (argc == 2) {
        if (string(argv[1]) == "--version") {
            cout << "2024.1" << endl;
        }
    } else {
        Othello theGame;
        theGame.restart();
        theGame.play();
    }
}
