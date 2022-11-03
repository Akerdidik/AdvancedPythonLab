from flask import Blueprint, redirect

index = Blueprint('index', __name__, template_folder='./static')

@index.route('/', methods=['GET'])
def show():
    return redirect('/home')