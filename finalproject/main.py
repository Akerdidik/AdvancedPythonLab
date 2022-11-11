import os
import pathlib
import requests
from flask import Flask, render_template, url_for, redirect, request, session, abort, url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models.models import User,Post
from flaskapp import app, db
from fastapi import Depends, FastAPI, HTTPException
from flask_login import login_required
from notificator import Notification

def add_user(user: User) -> None:
    db.session.add(user)
    db.session.commit()
def add_post(post:Post)->None:
    db.session.add(post)
    db.session.commit()

fapp = FastAPI()

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.post_id).all()
    return render_template('index.html',data = posts )

@login_required
@app.route('/<int:post_owner>/update/<int:post_id>', methods=('GET', 'POST'))
def edit(post_owner,post_id):
    try:
        ids = session['id']
    except:
        abort(401)
    if ids != post_owner:
        abort(403)
    if ids != post_id:
        abort(403)
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        titlename = request.form['titlename']
        fundraising = request.form['fundraising']
        additional = request.form['additional']
        fromfund =int (request.form['fromfund'])
        tofund = int( request.form['tofund'])
        post_owner = request.form['post_owner']
        post.titlename = titlename
        post.fundraising = fundraising
        post.additional = additional
        post.fromfund = fromfund
        post.tofund = tofund
        post.post_owner = post_owner
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('user_page',id=post.post_owner))
    return render_template('updatepost.html', post=post)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/causesingle')
def causesingle():
    return render_template('cause-single.html')


@app.route('/causes')
def causes():
    return render_template('causes.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':

        try:
            ids = session['id']
        except:
            abort(401)
        name = request.form['name']
        email_to = request.form['email']
        try:
            amount = int(request.form['amount'])
            if amount <=0:
                return render_template('donate.html', mesage='Only valid amount!')
        except:
            return render_template('donate.html', mesage='Only numbers!')
        message = request.form['message']
        user = db.session.query(User).filter_by(id=ids).first()
        defaulter = user.balance - amount
        if defaulter < 0:
            return render_template('donate.html',mesage='Not enough balance')

        user.balance = defaulter
        new_user = db.session.query(User).filter_by(email=email_to).first()

        if new_user == None:
            return render_template('donate.html', mesage='Unregistered user email!')

        new_user.balance += amount
        db.session.add(user)
        db.session.add(new_user)
        db.session.commit()
        notificator = Notification()
        notificator.notificator(f"Donation {amount}$ for '{name}' project has been recieved from '{user.email}'",
            message, email_to
        )
        session['amount'] = defaulter
    return render_template('donate.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/login', methods =['GET', 'POST'])
def login(context=None):
    mesage = ''
    if request.method == "POST":
        user = db.session.query(User).filter_by(email=request.form['email'], password=request.form['password']).first()
        print(user)
        if user:
            session['loggedin'] = True
            session['id'] = user.id
            session['email'] = user.email
            session['amount'] = user.balance
            mesage = 'Logged in successfully !'
            if user.google_name == None:
                session['h_id'] = False
            else:
                print("imba")
                session['h_id'] = True
            return redirect(url_for("user_page",id=user.id))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html',mesage=mesage)

@login_required
@app.route('/<int:post_owner>/delete/<int:post_id>')
def delete(post_owner,post_id):
    try:
        ids = session['id']
    except:
        abort(401)
    if ids != post_owner:
        abort(403)
    if ids != post_id:
        abort(403)
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_page',id=post_owner))

@login_required
@app.route("/user/<int:id>")
def user_page(id,context=None):
    try:
        ids = session['id']
    except:
        abort(401)
    if ids != id:
        abort(403)
    query = db.session.query(User).join(Post).filter(Post.post_owner == id).first()
    if query:
        return render_template("user.html", context=query)
    else:
        query = db.session.query(User).filter(User.id == id).first()
        return render_template("user.html", context=query)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message=''
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        data = db.session.query(User).filter_by(email=request.form['email']).first()
        if data:
            return redirect(url_for('error'))
        else:
            add_user(User(name=name, 
                        email=email,
                        password=password,
                        balance=10000))
            message="You succesfully registered!"
        return render_template('login.html',message='Succesfully registered!')

    return render_template('register.html',message=message)


@app.route('/error', methods=["GET"])
def error():
    return render_template('register.html', mesage='User already exists')

@login_required
@app.route('/post',methods = ['GET','POST'])
def post():
    try:
        ids = session['id']
    except:
        abort(401)
    mesage=''
    if request.method =="POST":
        titlename = request.form['titlename']
        fundraising = request.form['fundraising']
        additional = request.form['additional']
        fromfund =int (request.form['fromfund'])
        tofund = int( request.form['tofund'])
        post_owner = request.form['post_owner']
        add_post(Post(titlename=titlename,fundraising=fundraising,additional=additional,fromfund=fromfund,tofund=tofund,post_owner=post_owner))
        mesage="Post added!"
        return render_template('post.html',mesage=mesage)
    return render_template("post.html")

@login_required
@app.route("/logout")
def logout():
    try:
        ids = session['id']
    except:
        abort(401)
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))

GOOGLE_CLIENT_ID = "69054447754-7vklvapi0aufibe87paag7l7csdqcn1l.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "imba.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback",
)

@app.route('/glogin')
def glogin():

    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["h_id"] = True
    all_users = User.query.order_by(User.id).all()
    name = session["name"]
    for i in all_users:

        if i.google_name == name:
            try:
                kk = session['id']
            except:
                session['loggedin'] = True
                session['id'] = i.id
                session['email'] = i.email
                session['amount'] = i.balance
                return redirect(url_for("user_page", id = i.id))
            if i.id == kk:
                print(i.google_name)
                session['loggedin'] = True
                session['id'] = i.id
                session['email'] = i.email
                session['amount'] = i.balance
                return redirect(url_for("user_page", id = i.id))
    try:
        ids = session['id']
    except:
        session["h_id"] = False
        abort(401)
    try:
        user = db.session.query(User).filter_by(id=ids).first()
        user.google_name = name
        db.session.add(user)
        db.session.commit()
    except:
        abort(401)
    session['amount'] = user.balance
    return redirect(url_for("user_page", id =ids))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
