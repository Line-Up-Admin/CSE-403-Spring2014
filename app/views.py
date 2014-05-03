from app import app

@app.route('/helloworld')
def index():
    return "Hello, World!"
