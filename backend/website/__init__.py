from flask import Flask,render_template

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    
    from .views import views

    app.register_blueprint(views,url_prefix='/')
    app.register_error_handler(404, page_not_found)

    return app
