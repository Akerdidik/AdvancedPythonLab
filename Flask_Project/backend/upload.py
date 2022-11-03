from io import BytesIO
from flask import Blueprint, render_template,request, send_file,session
from flask_login import login_required
from models import db,Users,Filer
from werkzeug.utils import secure_filename

files_in = Blueprint('upload',__name__, template_folder='./static')
@files_in.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    if request.method=='POST':
        file_name = request.files['files']
        user_name = session['user_id']
        new_user = db.session.query(Users).filter(Users.username == user_name)
        user = new_user[0]
        new_file = db.session.query(Filer).all()
        files = []
        for i in new_file:
            files.append(i.file_name)
        
        if file_name not in files:
            uploader = Filer(
            file_name=file_name.filename,
            data = file_name.read()
            )
            db.session.add(uploader)
            db.session.commit()
        
        file_to_append = db.session.query(Filer).filter(Filer.file_name==file_name.filename)
        x = file_to_append[0]
        user.folls.append(x)
        db.session.commit()
        return render_template('templates/subscribe.html')
    else:
        user_name = session['user_id']
        new_user=db.session.query(Users).filter(Users.username == user_name)
        user=new_user[0]
        return render_template('templates/subscribe.html')

''' def download(id):
        item = Item().query.filter_by(id=id).first()
        return send_file(BytesIO(item.data),mimetype='image.png', as_attachment=True, download_name=item.name)'''



