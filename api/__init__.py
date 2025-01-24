"""
    @author Agha Hammad Raza
    @since 29-12-2024
"""

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# Flask application setup
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




# Flask-Restful API and JWT setup
api = Api(app)
