# Sandstorm

Now that [Ella Musk](https://genshin-impact.fandom.com/wiki/Ella_Musk) can speak with the Hilichurl fluently, she set
her sight on Mars. However, the sandstorm on Mars is the major problem she is having touble with. She hired you to write a Makefile
(not sure why she picked a Makefile of all things) that can warn her if the sandstorm is active on Mars.

A sandstorm is active when the modification date and time of the file `sandstorm.txt` is greater than
the file `calm.txt`. Sandstorm is not active otherwise.

Write a Makefile that outputs `warning, a sandstorm is active!` when the sandstorm is active. Otherwise, your Makefile should
not output anything. We will run your Makefile with `--silent` option to help with the later case.
