#!/bash/bin

# clean up any repos from previous tests
rm -rf ~/LineUpTestSpace/CSE-403-Spring2014

#copy email template
#cp testlogs/test_output_template.txt testlogs/test_output.txt
git clone https://github.com/Line-Up-Admin/CSE-403-Spring2014.git ~/LineUpTestSpace


cd ~/LineUpTestSpace/CSE-403-Spring2014/tests/

# run python tests and redirect output to file
python flask_tests/test.py 2> test_output.txt

# run angular tests and redirect output to file
phantomjs angular_tests/auto_jasmine_tests.js 1>> test_output.txt

# email results 
ssmtp cse403group@uw.edu < test_output.txt
