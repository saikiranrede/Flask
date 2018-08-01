from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Homepage !!!"

@app.route('/about/')
def about():
    return "WebSite exercises starts here !!!"

if __name__=="__main__":
    app.run(debug=True)
