from app import app

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/helloworld')
def index():
    return "Hello, World!"
