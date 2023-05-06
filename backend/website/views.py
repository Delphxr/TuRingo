from flask import Blueprint,render_template, request,flash
from website import turing
from bson import json_util
import json
from flask import jsonify
import bcrypt
from bson.objectid import ObjectId
from datetime import datetime
import re
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

def insertar_usuario(nombre,apellidos,password,correo,carne,tipo_usuario):
    # Encrypt the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    usuario = {
        'nombre': nombre,
        'apellidos': apellidos,
        'password': hashed_password.decode('utf-8'),
        'correo': correo,
        'carne': carne,
        'tipo_usuario': tipo_usuario
    }
    result = usuarios.insert_one(usuario)
    return f'Usuario agregado con el id {result.inserted_id}'

def check_existing_user(correo):
    existing_user = usuarios.find_one({'correo': correo})
    return existing_user is not None

@views.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']

        password = request.form['password']

        correo = request.form['correo']
        carne = request.form['carne']

        tipo_usuario = 'Estudiante'

        print(request.form)
        if nombre == None or nombre == "" or nombre == " ":
            flash("El nombre no puede estar vacío.",category='error')
        elif(bool(re.match('[a-zA-Z\s]+$', nombre))==False):
            flash("Solo puede usar caracteres de A-Z en el nombre.",category='error')
        elif password == None or password == "" or password == " ":
            flash("El password no puede estar vacío.",category='error')
        elif apellidos == None or apellidos == "" or apellidos == " ":
            flash("Los apellidos no pueden estar vacíos.",category='error')
        elif(bool(re.match('[a-zA-Z\s]+$', apellidos))==False):
            flash("Solo puede usar caracteres de A-Z en los apellidos.",category='error')
        elif carne == None or carne == "" or carne == " ":
            flash("El carne no puede estar vacío.",category='error')
        elif not carne.isnumeric():
            flash("Solo puede usar números en el carne.",category='error')
        else:
            if check_existing_user(correo):
                flash("El usuario ya está registrado en la base de datos.", category='error')
                return render_template("signup.html")
            
            else:
                insertar_usuario(nombre, apellidos, password, correo, carne, tipo_usuario)
                flash('Se ha creado una cuenta correctamente!', category='success')
                return render_template("homepage.html")

    return render_template("signup.html")

def get_usuarios():
    from app import usuarios
    lista_usuarios = list(usuarios.find())

    return lista_usuarios

def get_tareas():
    from app import usuarios
    lista_tareas = list(tareas.find())

    return lista_tareas

def get_tareas_usuario(usuario_id):
    from app import tareas_usuario

    try:
        document = tareas_usuario.find({'idusuario': usuario_id})
        
        if document:
            return document  # Return the document as a string representation
        else:
            return 'Usuario no encontrado'
    except Exception as e:
        return str(e)

def get_tareas_creador(creador_id):
    from app import tareas

    try:
        document = tareas.find({'idcreador': creador_id})
        
        if document:
            return document  # Return the document as a string representation
        else:
            return 'Creador no encontrado'
    except Exception as e:
        return str(e)

def get_tarea_busqueda(busqueda):
    from app import tareas

    tareas_encontradas = tareas.find({"nombre": {"$regex": busqueda, "$options": "i"}})

    return tareas_encontradas

def get_tarea(tarea_id):
    from app import usuarios

    try:
        document = tareas.find_one({'_id': ObjectId(tarea_id)})
        if document:
            return document  # Return the document as a string representation
        else:
            return 'Tarea no encontrada'
    except Exception as e:
        return str(e)

def get_usuario(usuario_id):
    from app import usuarios

    try:
        document = usuarios.find_one({'_id': ObjectId(usuario_id)})
        if document:
            return document  # Return the document as a string representation
        else:
            return 'Usuario no encontrado'
    except Exception as e:
        return str(e)

def cambiar_permiso_usuario(usuario_id, tipo_usuario):
    from app import usuarios

    usuarios.update_one(
        {'_id': usuario_id},
        {'$set': {'tipousuario': tipo_usuario}}
    )

    return 'Permisos de usuario cambiados con exito'

def insertar_tarea(nombre,descripcion,fechacreacion,idcreador,entradasalida,ejemplo):
    from app import tareas
    from app import datos_entrada_salida

    tarea = {
        'nombre': nombre,
        'descripcion': descripcion,
        'fechacreacion': fechacreacion,
        'idcreador': idcreador
    }

    result = tareas.insert_one(tarea)

    datos = {
        'idtarea': result.inserted_id,
        'entradasalida': entradasalida,
        'ejemplo':ejemplo
    }

    result2 = datos_entrada_salida.insert_one(datos)

    return f'Datos entrada salida agregados con el id {result2.inserted_id}'

def entregar_tarea(idusuario,idtarea,fechaentrega,nota,codigodiagrama):
    from app import tareas_usuario

    tarea_usuario = {
        'idusuario': nombre,
        'idtarea': descripcion,
        'fechaentrega': fechacreacion,
        'nota': idcreador,
        'codigodiagrama': codigodiagrama
    }

    result = tareas_usuario.insert_one(tarea_usuario)
    return f'Tarea de usuario entregada con el id {result.inserted_id}'

@views.route('/',methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@views.route('/editor', methods=['GET','POST'])
def editor():
    return render_template("editor.html")

@views.route('/estudiante', methods=['GET','POST'])
def estudiantes():
    from app import usuarios
    from app import tareas

    id_usuario = request.args.get('id')

    estudiante = get_usuario(id_usuario)

    tareas_usuario = get_tareas_usuario(id_usuario)
    backup_tareas_usuario = tareas_usuario.clone()

    tareas_id = [ObjectId(tarea['idtarea']) for tarea in backup_tareas_usuario]

    tareas_info = tareas.find({'_id': {'$in': tareas_id}})
    
    result = []
    for tarea in tareas_usuario:
        tarea_informacion = [info_tarea for info_tarea in tareas_info if info_tarea['_id'] == ObjectId(tarea['idtarea'])]
        tarea['informacion'] = tarea_informacion
        result.append(tarea)
        
    tareas_usuario = result

    return render_template("estudiante.html",estudiante=estudiante,tareas_usuario=tareas_usuario)

@views.route('/busqueda_tarea',methods=['GET','POST'])
def busqueda_tarea():
    busqueda = request.args.get('busqueda', default = '*', type = str)
    busqueda=busqueda.upper()
    if (len(busqueda)<3):
        return render_template("busqueda_tarea.html",tareas=None,busqueda=busqueda)
    else:
        tareas = get_tarea_busqueda(busqueda)
        return render_template("busqueda_tarea.html",tareas=tareas,busqueda=busqueda)

@views.route('/administrador', methods=['GET','POST'])
def administrador():
    from app import usuarios

    id_creador = request.args.get('id')

    administrador = get_usuario(id_creador)

    tareas_administrador = get_tareas_creador(id_creador)

    return render_template("administrador.html",administrador=administrador,tareas_administrador=tareas_administrador)

@views.route('/crear_tarea', methods=['GET','POST'])
def crear_tarea():
    from app import usuarios

    id_creador = request.args.get('id')

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        fechacreacion = datetime.now().strftime("%d-%m-%Y")
        entradas = request.form.getlist('entrada')
        salidas = request.form.getlist('salida')

        if nombre == None or nombre == "" or nombre == " ":
            flash("El nombre no puede estar vacío.",category='error')
        elif(bool(re.match('[0-9a-zA-Z\s]+$', nombre))==False):
            flash("Solo puede usar caracteres de A-Z y números en el nombre.",category='error')
        elif descripcion == None or descripcion == "" or descripcion == " ":
            flash("La descripcion no puede estar vacía.",category='error')
        elif(bool(re.match('[0-9a-zA-Z\s]+$', descripcion))==False):
            flash("Solo puede usar caracteres de A-Z  y números en la descripcion.",category='error')
        elif(id_creador == None or id_creador == "" or id_creador == " "):
            flash("El ID del creador de la tarea no puede estar vacío.",category='error')
        else:
            valid = True

            for entrada in entradas:
                if entrada.strip() == "":
                    valid = False
                    break

            for salida in salidas:
                if salida.strip() == "":
                    valid = False
                    break
            
            print(valid)
            if valid:
                entradasalida = []

                for entrada, salida in zip(entradas, salidas):
                    entradasalida.append({'entrada': entrada, 'salida': salida})

                result = {'entradasalida': entradasalida}

                try:
                    insertar_tarea(nombre, descripcion, fechacreacion, id_creador, entradasalida, True)
                    flash('Se ha creado una tarea correctamente!', category='success')
                    administrador = get_usuario(id_creador)
                    tareas_administrador = get_tareas_creador(id_creador)
                    return render_template("administrador.html",administrador=administrador,tareas_administrador=tareas_administrador)
                except Exception as e:
                    flash("Error: No se dio un administrador valido.",category='error')
                    return render_template("administrador.html",administrador=None,tareas_administrador=None)
            elif not valid:
                flash("Todas las entradas y salidas deben estar llenas.",category='error')
                administrador = get_usuario(id_creador)
                tareas_administrador = get_tareas_creador(id_creador)
                return render_template("administrador.html",administrador=administrador,tareas_administrador=tareas_administrador)

    administrador = get_usuario(id_creador)

    tareas_administrador = get_tareas_creador(id_creador)

    return render_template("administrador.html",administrador=administrador,tareas_administrador=tareas_administrador)

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
