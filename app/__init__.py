from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# app is this folder './app/' ... 'import app' is a packege
from app import routes