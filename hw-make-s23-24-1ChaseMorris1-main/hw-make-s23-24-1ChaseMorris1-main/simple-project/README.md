# A Simple Project

Modify the given Makefile (in the `source/` folder) so that there are rules for the following targets.

- `all`
- `build`
- `sdist`
- `clean`

You may create additional rules. Here are the details for each rule.

## Rule for a target `all`

It is the default goal. When it is invoked, the executable files and the source distribution archive file are created. The recipe of this rule must be empty.

## Rule for a target `build`

Create two executable files `othello-game` and `othello-game-debug`. When this rule is run while the executable files are already exist, the exeuctable files should not be re-created unless any of the source file (`.cpp` or `.hpp`) has a more recent modifcation date/time than the executable file.

## Rule for a target `sdist`

Create a source distribution with a name `othello-sdist.tar.gz` that can be used to build this project again. When this target is run while the source distribution file is already exist, the source distribution file should only be re-created when the other files has a newer modification date/time than the `othello-sdist.tar.gz`.

## Rule for a target `clean`

This target removes all `.o` files and all the executable files. All `.o` files and all of the exeuctable files must be deleted even if some of them are already deleted before this target run.
