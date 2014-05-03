#!/bash/bin

#clean up
cd /var/www
rm -rf lineup_test

#copy email template
#cp testlogs/test_output_template.txt testlogs/test_output.txt
git clone https://github.com/Line-Up-Admin/CSE-403-Spring2014.git /var/www/lineup_test


cd /var/www/lineup_test/tests

#run python tests and redirect output to file
python flask_tests/test.py 2> test_output.txt

#run angular tests and redirect output to file
phantomjs angular_tests/auto_jasmine_tests.js 1>> test_output.txt


#email results 
ssmtp cse403group@uw.edu < test_output.txt



