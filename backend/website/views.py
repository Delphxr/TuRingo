from flask import Blueprint,render_template, request,flash

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def home():
    return "TuRingo home"

@views.route('/editor', methods=['GET','POST'])
def editor():
    return render_template("editor.html")
