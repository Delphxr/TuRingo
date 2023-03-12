from flask import Blueprint,render_template, request,flash

views = Blueprint('views', __name__)

@views.route('/404',methods=['GET','POST'])
def error404():
    return render_template('404.html')

@views.route('/',methods=['GET','POST'])
def home():
    return "TuRingo home"

@views.route('/editor', methods=['GET','POST'])
def editor():
    return render_template("editor.html")
