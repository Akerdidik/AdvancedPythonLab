from flask import Flask, abort, redirect, render_template,request
import sqlalchemy
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash
from models import db, Users,Stacks
from index import index
from login import login
from logout import logout
from register import register
import scheduler as sch
from home import home
from stacks import stacker
from upload import files_in
from download import files_out
from geters import downloader
from fastapi import creator,take_data,take_data_single,update_data,delete_data
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, static_folder='./static')

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://aker:reka@localhost/cve'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()
app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(stacker)
app.register_blueprint(files_in)
app.register_blueprint(files_out)
app.register_blueprint(downloader)
app.register_blueprint(creator)
app.register_blueprint(take_data)
app.register_blueprint(take_data_single)
app.register_blueprint(delete_data)
app.register_blueprint(update_data)
with app.app_context():
    db.create_all()

def starter():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sch.start_scheduling,trigger="interval",seconds=600)
    scheduler.start()
    return scheduler

with app.app_context():
    scheduler = starter()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
