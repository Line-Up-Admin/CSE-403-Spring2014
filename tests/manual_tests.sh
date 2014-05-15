#!/bash/bin

# This simple script is used to run both the flask and angular tests
# using a SINGLE command from the terminal and display the results
# to the console


#run python tests and redirect output to file
python flask_tests/test.py

#run angular tests and redirect output to file
phantomjs angular_tests/auto_jasmine_tests.js


