from flask import Blueprint,render_template, request,flash
from website import turing
import json

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

views = Blueprint('views', __name__)

def borrar_usuario(usuario_id):
    result = usuarios.delete_one({'_id': ObjectId(usuario_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Usuario borrado con éxito'})
    else:
        return jsonify({'message': 'Usuario no fue encontrado'})

def insertar_usuario():
    username = request.form['username']
    password = request.form['password']
    correo = request.form['correo']
    tipo_usuario = request.form['tipo_usuario']

    usuario = {
        'username': username,
        'password': password,
        'correo': correo,
        'tipo_usuario': tipo_usuario
    }
    result = usuarios.insert_one(usuario)
    return f'Usuario agregado con el id {result.inserted_id}'

def get_usuarios():
    from app import usuarios
    lista_usuarios = usuarios.find()

    return lista_usuarios

@views.route('/',methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@views.route('/editor', methods=['GET','POST'])
def editor():
    return render_template("editor.html")

@views.route('/estudiante', methods=['GET','POST'])
def estudiantes():
    lista = get_usuarios()
    print(lista)
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
