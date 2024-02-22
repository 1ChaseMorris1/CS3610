/**
 * @file debug_main.cpp
 * @author Krerkkiat Chusap
 * @brief For debugging purposes
 *
 * This file exist solely to prevent student from passing
 * *.cpp as an input to the compiler.
 *
 * Its effectiveness is questionable, but hopefully error message
 * in the compilation step guides the student to a more suitable compilation
 * comamnds.
 *
 * And if you are a student reading this, `g++ *.cpp` is not the correct
 * answer for the compilation command nor does `g++ main.cpp game.cpp
 * othello.cpp`
 */
#include "game.hpp"
#include "othello.hpp"

using namespace main_savitch_14;

int main(int argc, char* argv[]) {
  if (argc == 2) {
    if (string(argv[1]) == "--version") {
      cout << "2024.1d" << endl;
    }
  } else {
    Othello game;
    game.restart();
    // Only make one move and display the board.
    game.make_move("C3");
    game.display_status();
  }
  
}
