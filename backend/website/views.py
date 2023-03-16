from flask import Blueprint,render_template, request,flash

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@views.route('/editor', methods=['GET','POST'])
def editor():
    return render_template("editor.html")

@views.route('/estudiante', methods=['GET','POST'])
def estudiantes():
    return render_template("estudiante.html")

@views.route('/administrador', methods=['GET','POST'])
def administrador():
    return render_template("administrador.html")
