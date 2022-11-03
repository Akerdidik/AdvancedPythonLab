from io import BytesIO
from flask import Blueprint, send_file
from models import Filer

downloader = Blueprint('downloader',__name__,template_folder='./static')
@downloader.route("/downloader/<int:id>",methods=['GET'])
def geter(id):
    filess = Filer().query.filter_by(id=id).first()
    return send_file(BytesIO(filess.data),mimetype='image.png',as_attachment=True,download_name=filess.file_name)