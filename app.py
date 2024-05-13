from flask import Flask
from calculator import run

app = Flask(__name__)

@app.route('/')
def home():
   return run()

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)