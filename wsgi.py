# wsgi.py
try:
    from dotenv import load_dot_env
    load_dotenv()
except:
    pass
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"
