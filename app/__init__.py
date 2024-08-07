from flask import Flask
app = Flask(__name__)
from app import routes
from app.dash import apl
from app.dashheatmap import apl
from app.dashvisu import apl
