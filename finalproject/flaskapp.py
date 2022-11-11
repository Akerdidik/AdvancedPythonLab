import os

from models.db import db
from flask import Flask

app = Flask(__name__)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.secret_key="123"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///finalproject.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


with app.app_context():
    db.init_app(app)
