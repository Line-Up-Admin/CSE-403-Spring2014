#!/bash/bin



#copy email template
cp testlogs/test_output_template.txt testlogs/test_output.txt

#run python tests and redirect output to file
python flask_tests/test.py 2>> testlogs/test_output.txt


#email results 
ssmtp laplansk@gmail.com < testlogs/test_output.txt
#ssntp cse403group@uw.edu < test_output.txt
