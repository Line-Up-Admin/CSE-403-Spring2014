# This is the file that contains all the route handlers.
from app import app

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
    return app.send_static_file('index.html')

# Takes the '/helloworld' route and returns "Hello, World!"
@app.route('/helloworld')
def index():
    return "Hello, World!"
