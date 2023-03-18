from flask import Blueprint,render_template, request,flash
from website import turing
import json

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



@views.route('/turing-compiler', methods=['POST'])
def turing_compiler():
    print("llamada recibida!")
    request_data = request.get_json()

    entrada = request_data["entrada"]
    codigo = json.dumps(request_data["codigo"])
    vacio = request_data["vacio"]

    maquina = turing.TuringMachine() 
    maquina.set_blank(vacio)
    maquina.set_code(codigo)
    
    
    if entrada == "":
        resultado = maquina.run(None)
    else:
        resultado = maquina.run(entrada)
    

    resultado = json.dumps(resultado)
    return resultado
