from io import BytesIO
from models import db,Users
from flask import Blueprint, render_template, send_file,request, session
from flask_login import login_required
from models import Filer

files_out = Blueprint('download',__name__, template_folder='./static')
@files_out.route('/download',methods=['GET'])
@login_required
def download():
    if request.method=='GET':
        sess=session['user_id']
        new_user = db.session.query(Users).filter(Users.username==sess)
        temp = new_user[0]
        return render_template('templates/uploaded.html',filers=temp.folls)
