# This is the file that contains all the route handlers.
from app import app
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from q_classes import QueueServer
from user_module import UserModule
app = Flask(__name__)
app.config.from_object(__name__)
server = QueueServer()
module = UserModule()

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/join', methods=['POST'])
def add_to_queue():
    userID = request.form['userID']
    queueID = request.form['queueID']
    queue_result = server.add(userID, queueID)
    #return JSON version of queue

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = module.login(username, password)
        # EVAN: is result the userID?
    else:
        # THOMAS: so I shouldn't redirect to static login page? 
        #what if method is GET?
        pass

@app.route('/dequeue', methods=['POST'])
def dequeue():
    queueID = request.form['queueID']
    employeeID = request.form['userID']
    member = server.dequeue(employeeID, queueID)
    # return JSON QueueMember

@app.route('/searchResults')

@app.route('/search')

@app.route('/memberQueue')

@app.route('/employeeQueue')

@app.route('/adminQueue')

@app.route('/queueStatus')

@app.route('/myQueues')

@app.route('/remove')

@app.route('/qtracks')

@app.route('/qtracksData')

@app.route('/createUser')

@app.route('/createQueue')

@app.route('/logout')

# Takes the '/helloworld' route and returns "Hello, World!"
@app.route('/helloworld')
def index():
    return "Hello, World!"
