from flask import Flask

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return "Happy Coding!"

if __name__ == '__main__':
    app.run(debug=True)