/**
 * Print as much banknotes as the amount of "word" found.
 */
#include <iostream>

#include "count_words.hpp"
#include "split_by.hpp"

using namespace std;

int main(int argc, char **argv) {
  if (argc == 2) {
    string text = argv[1];
    vector<string> words = split_by(text, " ");
    cout << count_words(words) << endl;
  } else {
    cout << "Usage: " << argv[0] << " \"text\"" << endl;
  }
}