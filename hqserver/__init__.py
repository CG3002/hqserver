'''
This is the python init file
'''
from flask import Flask
app = Flask(__name__)

import hqserver.views
