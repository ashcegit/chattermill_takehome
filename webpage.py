from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/')
def homepage():
    render_template('home.html')
    return

if __name__=='__main__':
    app.debug=True
    app.run()