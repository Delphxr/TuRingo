from flask import Blueprint, render_template, request, flash
from website import turing
from website import db_functions
from bson import json_util
import json
from flask import jsonify
import bcrypt
from bson.objectid import ObjectId
from datetime import datetime
import re
import os
import sys
from flask import Flask, session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

views = Blueprint('views', __name__)

@views.route('/login', methods=['POST'])
def login():
    usuario_exists = 'usuario' in session
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        tareas = db_functions.get_tareas()
        usuario = None
        _id = None
        tipo_usuario = None

        if db_functions.check_existing_user(email):
            hashed_password = db_functions.get_user_password(email)

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                usuario = db_functions.check_existing_user(email)
                # --------------------Guardar el usuario actual en la sesion----------------------------------
                usuario = json_util.dumps(usuario)
                # --------------------------------------------------------------------------------------------
                print(usuario)
                session['usuario'] = usuario
                print(session)
                usuario_exists = 'usuario' in session
                print(usuario_exists)
                
                # --------------------Cargar el usuario actual de la sesion de flask----------------------------
                session_json = json.loads(session['usuario'])
                sesion = session_json
                _id = session_json['_id']['$oid']
                tipo_usuario = session_json['tipo_usuario']
                # ----------------------------------------------------------------------------------------------

                flash('Se ha iniciado sesión correctamente!', category='success')
                return render_template("homepage.html", usuario=usuario, usuario_exists=usuario_exists, tareas=tareas, _id=_id, tipo_usuario=tipo_usuario)
            else:
                flash('Password incorrecta, por favor intente de nuevo.',
                      category='error')
                return render_template("homepage.html", tareas=tareas, usuario_exists=usuario_exists, id=_id, tipo_usuario=tipo_usuario)

        else:
            flash(
                'El correo no está registrado, por favor intente de nuevo.', category='error')
            return render_template("homepage.html", tareas=tareas, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)

    return render_template("homepage.html", tareas=tareas, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('logout', methods=['GET', 'POST'])
def logout():
    # --------------------------Retirar el usuario actual de la sesión de flask para cerrar sesión---------------------
    session.pop('usuario', None)
    # -----------------------------------------------------------------------------------------------------------------
    tareas = db_functions.get_tareas()
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None
    print(usuario_exists)

    return render_template("homepage.html", tareas=tareas, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/signup', methods=['GET', 'POST'])
def signup():
    from app import usuarios
    usuario_exists = 'usuario' in session

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']

        password = request.form['password']
        password2 = request.form['password2']

        correo = request.form['email']
        carne = request.form['carne']

        tipo_usuario = 'Estudiante'

        tareas = db_functions.get_tareas()
        usuario = None
        _id = None

        print(request.form)
        if (password != password2):
            flash("Las passwords deben ser iguales.",category='error')
        elif nombre == None or nombre == "" or nombre == " ":
            flash("El nombre no puede estar vacío.", category='error')
        elif not re.match(r'^[0-9a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$', nombre):
            flash(
                "Solo puede usar caracteres de A-Z, números y tildes en el nombre.", category='error')
        elif password == None or password == "" or password == " ":
            flash("El password no puede estar vacío.", category='error')
        elif apellidos == None or apellidos == "" or apellidos == " ":
            flash("Los apellidos no pueden estar vacíos.", category='error')
        elif not re.match(r'^[0-9a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ.,;:¡!¿?(){}[\]<>«»"\'«»]+$', apellidos):
            flash("Solo puede usar caracteres de A-Z, números, tildes y signos de puntuación en los apellidos.", category='error')
        elif carne == None or carne == "" or carne == " ":
            flash("El carne no puede estar vacío.", category='error')
        elif not carne.isnumeric():
            flash("Solo puede usar números en el carne.", category='error')
        else:
            if db_functions.check_existing_user(correo):
                flash("El usuario ya está registrado en la base de datos.",
                      category='error')
                return render_template("homepage.html", usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)

            else:
                db_functions.insertar_usuario(nombre, apellidos, password,
                                 correo, carne, tipo_usuario)
                flash('Se ha creado una cuenta correctamente!', category='success')

                return render_template("homepage.html", usuario=usuario, tareas=tareas, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)

    return render_template("homepage.html", usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)

@views.route('/', methods=['GET', 'POST'])
def home():
    from app import tareas

    tareas = db_functions.get_tareas()
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']

    return render_template("homepage.html", tareas=tareas, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/editor', methods=['GET', 'POST'])
def editor():
    id_tarea = request.args.get('id_tarea')
    tarea = db_functions.get_tarea(id_tarea)

    datos_entrada_salida = db_functions.get_datos_entrada_salida(id_tarea)

    usuario_exists = 'usuario' in session
    id_usuario = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        id_usuario = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    
    # --------------------Guardar la tarea actual en la sesion----------------------------------
    tarea_json = json_util.dumps(tarea) # Se convierte a json la tarea para guardar en la sesion
    session['current_tarea'] = tarea_json # Se guarda la tarea actual en la sesion de flask
    # ------------------------------------------------------------------------------------------

    # --------------------Cargar la tarea actual de la sesion para obtener sus parametros--------------------------
    tarea_json = json.loads(session['current_tarea']) # Se carga la tarea actual de la sesión de flask
    id_tarea = tarea_json['_id']['$oid'] # Se obtiene el id de la tarea actual de la sesion
    parametro_vacio = tarea_json['parametro_vacio'] # Se obtiene el parametro vacio de la tarea actual de la sesion
    # -------------------------------------------------------------------------------------------------------------

    # --------------------Guardar los datos de E/S de la tarea actual en la sesion-----------------------------------------------------------
    datos_es_json = json_util.dumps(datos_entrada_salida) # Se convierte a json los datos de e/s de la tarea actual para guardar en la sesion
    session['current_entrada_salida'] = datos_es_json # Se guarda los datos de entrada y salida actual en la sesion de flask
    # ---------------------------------------------------------------------------------------------------------------------------------------

    # --------------------Cargar los datos de E/S de la tarea actual de la sesion para obtener sus parametros-------------------------
    datos_es_json = json.loads(session['current_entrada_salida']) # Se carga los datos de e/s de la tarea actual de la sesion de flask
    # --------------------------------------------------------------------------------------------------------------------------------

    print(id_tarea) # El id de la tarea
    print(parametro_vacio) # El parametro vacio de la tarea
    print(datos_es_json) # Los datos de entrada y salida de la tarea
    print(id_usuario) # El id del usuario

    return render_template("editor.html", tarea=tarea, datos_entrada_salida=datos_entrada_salida,usuario_exists=usuario_exists,id_usuario=id_usuario,tipo_usuario=tipo_usuario,id_tarea=id_tarea,parametro_vacio=parametro_vacio,datos_es_json=datos_es_json)


@views.route('/gameditor', methods=['GET', 'POST'])
def gameditor():
    usuario_exists = 'usuario' in session
    id_usuario = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        id_usuario = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']

    return render_template("gameditor.html", usuario_exists=usuario_exists, id_usuario=id_usuario, tipo_usuario=tipo_usuario)


@views.route('/estudiante', methods=['GET', 'POST'])
def estudiantes():
    from app import usuarios
    from app import tareas
    from app import datos_entrada_salida

    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']

    id_usuario = request.args.get('id')

    student_view = True
    if request.args.get('adminview'):
        student_view = False

    estudiante = db_functions.get_usuario(id_usuario)

    tareas_usuario = db_functions.get_tareas_usuario(id_usuario)
    backup_tareas_usuario = tareas_usuario.clone()

    tareas_id = [ObjectId(tarea['idtarea']) for tarea in backup_tareas_usuario]

    tareas_info = tareas.find({'_id': {'$in': tareas_id}})

    result = []

    for tarea_usuario in tareas_usuario:
        tarea_id = ObjectId(tarea_usuario['idtarea'])
        tarea_info = tareas.find_one({'_id': tarea_id})
        if tarea_info:
            tarea_usuario['nombre'] = tarea_info['nombre']
        else:
            tarea_usuario['nombre'] = None
        result.append(tarea_usuario)

    tareas_usuario = result
    print(tareas_usuario)

    return render_template("estudiante.html", estudiante=estudiante, tareas_usuario=tareas_usuario, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/busqueda_tarea', methods=['GET', 'POST'])
def busqueda_tarea():
    busqueda = request.args.get('busqueda', default='*', type=str)
    busqueda = busqueda.upper()
    print(busqueda)

    lista_tareas = db_functions.get_tarea_busqueda(busqueda)
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']

    return render_template("ver_tareas.html", lista_tareas=lista_tareas, busqueda=busqueda, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/busqueda_usuario', methods=['GET', 'POST'])
def busqueda_usuario():
    busqueda = request.args.get('busqueda', default='*', type=str)
    busqueda = busqueda.upper()
    print(busqueda)

    lista_estudiantes = db_functions.get_usuario_busqueda(busqueda)
    print(lista_estudiantes)
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    return render_template("ver_estudiantes.html", lista_estudiantes=lista_estudiantes, busqueda=busqueda, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/administrador', methods=['GET', 'POST'])
def administrador():
    # from app import usuarios

    id_creador = request.args.get('id')

    administrador = db_functions.get_usuario(id_creador)

    tareas_administrador = db_functions.get_tareas_creador(id_creador)
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']

    return render_template("administrador.html", administrador=administrador, tareas_administrador=tareas_administrador, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/crear_tarea', methods=['GET', 'POST'])
def crear_tarea():
    from app import usuarios
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    id_creador = request.args.get('id')

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        vacio = request.form.get('vacio')
        fechacreacion = datetime.now().strftime("%d-%m-%Y")
        entradas = request.form.getlist('entrada')
        salidas = request.form.getlist('salida')

        if nombre == None or nombre == "" or nombre == " ":
            flash("El nombre no puede estar vacío.", category='error')
        elif not re.match(r'^[0-9a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$', nombre):
            flash(
                "Solo puede usar caracteres de A-Z, números y tildes en el nombre.", category='error')
        elif descripcion == None or descripcion == "" or descripcion == " ":
            flash("La descripcion no puede estar vacía.", category='error')
        elif not re.match(r'^[0-9a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ.,;:¡!¿?(){}[\]<>«»"\'«»]+$', descripcion):
            flash("Solo puede usar caracteres de A-Z, números, tildes y signos de puntuación en la descripcion.", category='error')
        elif (id_creador == None or id_creador == "" or id_creador == " "):
            flash("El ID del creador de la tarea no puede estar vacío.",
                  category='error')
        else:
            entradasalida = []

            for entrada, salida in zip(entradas, salidas):
                entradasalida.append({'entrada': entrada, 'salida': salida})

            result = {'entradasalida': entradasalida}

            try:
                db_functions.insertar_tarea(nombre, descripcion, vacio, fechacreacion,
                               id_creador, entradasalida, True)
                flash('Se ha creado una tarea correctamente!', category='success')
                administrador = db_functions.get_usuario(id_creador)
                tareas_administrador = db_functions.get_tareas_creador(id_creador)
                return render_template("administrador.html", administrador=administrador, tareas_administrador=tareas_administrador, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)
            except Exception as e:
                flash("Error: No se dio un administrador valido.", category='error')
                return render_template("administrador.html", administrador=None, tareas_administrador=None, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)

    administrador = db_functions.get_usuario(id_creador)

    tareas_administrador = db_functions.get_tareas_creador(id_creador)

    return render_template("administrador.html", administrador=administrador, tareas_administrador=tareas_administrador, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/editar_tarea', methods=['GET', 'POST'])
def editar_tarea():
    from app import usuarios
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    id_creador = request.args.get('id')

    id_creador = request.args.get('id')
    id_tarea = request.args.get('id_tarea')
    _id = id_creador

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        vacio = request.form.get('vacio')
        fechacreacion = datetime.now().strftime("%d-%m-%Y")
        entradas = request.form.getlist('entrada')
        salidas = request.form.getlist('salida')

        if nombre is None or nombre.strip() == "":
            flash("El nombre no puede estar vacío.", category='error')
        elif not re.match(r'^[0-9a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$', nombre):
            flash(
                "Solo puede usar caracteres de A-Z, números y tildes en el nombre.", category='error')
        elif descripcion is None or descripcion.strip() == "":
            flash("La descripción no puede estar vacía.", category='error')
        elif not re.match(r'^[0-9a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ.,;:¡!¿?(){}[\]<>«»"\'«»]+$', descripcion):
            flash("Solo puede usar caracteres de A-Z, números, tildes y signos de puntuación en la descripción.", category='error')
        elif (id_creador == None or id_creador == "" or id_creador == " "):
            flash("El ID del creador de la tarea no puede estar vacío.",
                  category='error')
        else:
            entradasalida = []

            for entrada, salida in zip(entradas, salidas):
                entradasalida.append({'entrada': entrada, 'salida': salida})

            result = {'entradasalida': entradasalida}

            try:
                db_functions.actualizar_tarea(id_tarea, nombre, descripcion,
                                 vacio, fechacreacion, entradasalida)
                flash('Se ha editado la tarea correctamente!', category='success')
                administrador = db_functions.get_usuario(id_creador)
                tareas_administrador = db_functions.get_tareas_creador(id_creador)
                return render_template("administrador.html", administrador=administrador, tareas_administrador=tareas_administrador, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)
            except Exception as e:
                print(e)
                flash("Error: No se dio un administrador valido.", category='error')
                return render_template("administrador.html", administrador=None, tareas_administrador=None, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)

    administrador = db_functions.get_usuario(id_creador)

    tareas_administrador = db_functions.get_tareas_creador(id_creador)

    return render_template("administrador.html", administrador=administrador, tareas_administrador=tareas_administrador, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/ver_tareas', methods=['GET', 'POST'])
def ver_tareas():
    lista_tareas = db_functions.get_tareas()
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    id_creador = request.args.get('id')

    return render_template("ver_tareas.html", lista_tareas=lista_tareas, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/ver_estudiantes', methods=['GET', 'POST'])
def ver_estudiantes():
    lista_estudiantes = db_functions.get_usuarios()
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    id_creador = request.args.get('id')

    return render_template("ver_estudiantes.html", lista_estudiantes=lista_estudiantes, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/cambiar_permisos', methods=['GET', 'POST'])
def cambiar_permisos():
    id_usuario = request.args.get('id')
    tipo_usuario = request.args.get('tipo')
    print(id_usuario)
    print(tipo_usuario)

    db_functions.cambiar_permiso_usuario(id_usuario, tipo_usuario)
    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    id_creador = request.args.get('id')

    lista_estudiantes = db_functions.get_usuarios()
    return render_template("ver_estudiantes.html", lista_estudiantes=lista_estudiantes, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


@views.route('/borrar_tarea', methods=['GET', 'POST'])
def borrar_tarea():
    from app import usuarios

    usuario_exists = 'usuario' in session
    _id = None
    tipo_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        _id = session_json['_id']['$oid']
        tipo_usuario = session_json['tipo_usuario']
    id_creador = request.args.get('id')

    id_tarea = request.args.get('id_tarea')
    print(id_tarea)

    db_functions.set_tarea_no_visible(id_tarea)

    id_creador = request.args.get('id')

    administrador = db_functions.get_usuario(id_creador)

    tareas_administrador = db_functions.get_tareas_creador(id_creador)

    return render_template("administrador.html", administrador=administrador, tareas_administrador=tareas_administrador, usuario_exists=usuario_exists, _id=_id, tipo_usuario=tipo_usuario)


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


# hay que ver la forma de recibir parametros tambien el id de tarea para manejar parametros de prueba
# y tambien el id de usuario
@views.route('/entregar-tarea', methods=['POST'])
def entregar_tarea():
    print("llamada recibida!")
    request_data = request.get_json()

    usuario_exists = 'usuario' in session
    id_usuario = None

    if usuario_exists:
        session_json = json.loads(session['usuario'])
        sesion = session_json
        # El id del usuario que envia la tarea
        id_usuario = session_json['_id']['$oid']


    # --------------------Cargar la tarea actual de la sesion para obtener sus parametros--------------------------
    tarea_json = json.loads(session['current_tarea']) # Se carga la tarea actual de la sesión de flask
    id_tarea = tarea_json['_id']['$oid'] # Se obtiene el id de la tarea actual de la sesion
    parametro_vacio = tarea_json['parametro_vacio'] # Se obtiene el parametro vacio de la tarea actual de la sesion
    # -------------------------------------------------------------------------------------------------------------


    # --------------------Cargar los datos de E/S de la tarea actual de la sesion para obtener sus parametros-------------------------
    datos_es_json = json.loads(session['current_entrada_salida']) # Se carga los datos de e/s de la tarea actual de la sesion de flask
    # --------------------------------------------------------------------------------------------------------------------------------


    ejemplos = datos_es_json["entradasalida"]
    vacio_test = parametro_vacio

    codigo = json.dumps(request_data["codigo"])

    maquina = turing.TuringMachine()
    maquina.set_blank(vacio_test)
    maquina.set_code(codigo)

    calificacion = maquina.get_nota(ejemplos)

    resultado = {"calificacion": calificacion}

    import datetime
    today = datetime.datetime.today()

    print(id_usuario)
    print(id_tarea)
    print(calificacion)
    print(codigo)
    print(ejemplos)
    db_functions.subir_tarea(id_usuario, id_tarea,today,calificacion,codigo,ejemplos )

    return resultado
