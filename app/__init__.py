from flask import Flask

app = Flask(__name__)

# app is this folder './app/' ... 'import app' is a packege
from app import routes