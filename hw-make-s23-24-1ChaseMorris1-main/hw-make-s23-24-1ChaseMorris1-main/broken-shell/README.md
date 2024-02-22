# A Broken Shell

You are an intern in a small software company. You are tasked to create a Makefile that compiles one of their
projects written in C++17. Unfoutunately, due to the global pandemic, the company do not have enough
money to license out a high-end shell program. Thus, you are stuck with a broken shell program that can only run a command
with only one `.cpp` file as an argument to a command. The shell will also refuse to run any command containg an asterisk (`*`; ASCII code 42).

Write a Makefile, in the `source/` folder, that compiles this project using the shell with said limitations. Your Makefile must produce
an executable file with a name `money-printer`. You are not allowed to make any modification to the
codebase (e.g. renaming the file, changing the file content, etc.)
