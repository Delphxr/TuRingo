from flask import Blueprint,render_template, request,flash

views = Blueprint('views', __name__)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@views.route('/',methods=['GET','POST'])
def home():
    return "TuRingo home"

@views.route('/editor', methods=['GET','POST'])
def editor():
    return render_template("editor.html")
