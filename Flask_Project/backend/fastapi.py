from flask import Blueprint, abort, redirect, render_template, request,session
from flask_login import login_required
from werkzeug.security import generate_password_hash
from models import Users,db

creator = Blueprint('create',__name__, template_folder='./static')
@creator.route('/data/create',methods=['GET','POST'])
@login_required
def create():
    checker=session['user_id']
    if checker!="admin":
        abort(403)
    if request.method=='GET':
        return render_template('templates/createpage.html')
    if request.method=='POST':
        id = request.form['id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password,method='sha256')
        new_user = Users(id=id,username=username,email=email,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/data')

take_data = Blueprint('get_info',__name__,template_folder='../frontend')
@take_data.route('/data')
def ShowData():
    all_users = Users.query.all()
    return render_template('templates/datalist.html',all_users=all_users)

take_data_single = Blueprint('get_single_info',__name__,template_folder='../frontend')
@take_data_single.route('/data/<int:id>')
def ShowSingleData(id):
    new_user = Users.query.filter_by(id=id).first()
    if new_user:
        return render_template('templates/data.html',new_user=new_user)
    return f"User with id={id} doesnt exists"

update_data = Blueprint('update',__name__,template_folder='../frontend')
@update_data.route('/data/<int:id>/update',methods=['GET','POST'])
@login_required
def update(id):
    checker = session['user_id']
    if checker!="admin":
        abort(403)
    new_user = Users.query.filter_by(id=id).first()
    if request.method=='POST':
        if new_user:
            db.session.delete(new_user)
            db.session.commit()

            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hashed_password = generate_password_hash(password,method='sha256')
            new_user = Users(id=id,username=username,email=email,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"User with id = {id} doesnt exists"
    return render_template('templates/update.html',new_user=new_user)

delete_data = Blueprint('delete',__name__,template_folder='../frontend')
@delete_data.route('/data/<int:id>/delete',methods=['GET','POST'])
@login_required
def delete(id):
    checker=session['user_id']
    if checker!="admin":
        abort(403)
    new_user = Users.query.filter_by(id=id).first()
    if request.method=='POST':
        if new_user:
            db.session.delete(new_user)
            db.session.commit()
            return redirect('/data')
        abort(404)
    return render_template('delete.html')
