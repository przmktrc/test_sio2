# The test_sio2 script
test_sio2 is a simple script to test if a program gives correct answers for some given input.
Originally used with the [sio2 project](https://github.com/sio2project/oioioi). \
\
It runs the specified program giving it as input files from _test_dir_/in/ with a .in extension, redirectiong its output to _test_dir_/temp/ with the same name as the input file but with a .out extension (though it can be turned off), and then comparing it with a file from _test_dir_/out/ with the same name as the temp file.
## Environment
The script has been tested only on Linux with Python 3.9
## Running
To run, simply execute `python test_sio2.py <args>`.
## Installation
You can't really install test_sio2, but you can create a script in your ~/bin folder looking somewhat like this
> #!/bin/bash \
> python _path/to/test_sio2.py_ "$@"
