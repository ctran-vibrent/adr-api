from flask import Flask
app = Flask(__name__)
from app import api
from app import utils
from app import database
