from flask import Blueprint, render_template, request, flash
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
from flask import Flask, session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def borrar_usuario(usuario_id):
    from app import usuarios

    result = usuarios.delete_one({'_id': ObjectId(usuario_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Usuario borrado con éxito'})
    else:
        return jsonify({'message': 'Usuario no fue encontrado'})


def insertar_usuario(nombre, apellidos, password, correo, carne, tipo_usuario):
    from app import usuarios

    # Encrypt the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    tipo_usuario = "Estudiante"

    usuario = {
        'nombre': nombre,
        'apellidos': apellidos,
        'password': hashed_password,
        'correo': correo,
        'carne': carne,
        'tipo_usuario': tipo_usuario
    }
    result = usuarios.insert_one(usuario)
    return f'Usuario agregado con el id {result.inserted_id}'


def check_existing_user(correo):
    from app import usuarios

    existing_user = usuarios.find_one({'correo': correo})
    return existing_user


def get_user_password(correo):
    from app import usuarios

    user = usuarios.find_one({'correo': correo})
    if user:
        return user.get('password')
    else:
        return None

def get_usuarios():
    from app import usuarios
    lista_usuarios = list(usuarios.find())

    return lista_usuarios


def get_tareas():
    from app import usuarios
    from app import tareas
    from app import datos_entrada_salida

    lista_tareas = list(tareas.find().sort('_id', -1))

    # Obtener los datos de entrada y salida para cada tarea
    for tarea in lista_tareas:
        id_tarea = tarea['_id']
        datos = list(datos_entrada_salida.find({'idtarea': id_tarea}))
        if datos:
            tarea['datos_entrada_salida'] = datos[0]

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
    from app import datos_entrada_salida

    try:
        tareas_encontradas = tareas.find({'idcreador': creador_id})
        resultado = []

        for tarea in tareas_encontradas:
            tarea_actual = tarea.copy()
            entradasalida = datos_entrada_salida.find(
                {"idtarea": tarea["_id"]})
            tarea_actual["datos_entrada_salida"] = list(entradasalida)
            resultado.append(tarea_actual)

        return resultado

    except Exception as e:
        return str(e)


def get_tarea_busqueda(busqueda):
    from app import tareas
    from app import datos_entrada_salida

    lista_tareas = list(tareas.find(
        {"nombre": {"$regex": busqueda, "$options": "i"}}))

    for tarea in lista_tareas:
        id_tarea = tarea['_id']
        datos = list(datos_entrada_salida.find({'idtarea': id_tarea}))
        if datos:
            tarea['datos_entrada_salida'] = datos[0]

    return lista_tareas


def get_usuario_busqueda(busqueda):
    from app import usuarios

    usuarios_encontrados = usuarios.find({
        "$or": [
            {"nombre": {"$regex": busqueda, "$options": "i"}},
            {"apellidos": {"$regex": busqueda, "$options": "i"}}
        ]
    })

    return usuarios_encontrados


def get_tarea(tarea_id):
    from app import usuarios
    from app import tareas

    try:
        document = tareas.find_one({'_id': ObjectId(tarea_id)})
        if document:
            return document
        else:
            print('Tarea no encontrada')
            return None
    except Exception as e:
        return str(e)


def get_datos_entrada_salida(id_tarea):
    from app import datos_entrada_salida
    from app import tareas

    try:
        document = datos_entrada_salida.find_one(
            {'idtarea': ObjectId(id_tarea)})
        if document:
            return document
        else:
            print('Datos de entrada y salida no encontrados')
            return None
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

    tipo_usuario = tipo_usuario.upper()
    print(tipo_usuario)

    nuevo_tipo = ""

    if tipo_usuario == "ESTUDIANTE":
        nuevo_tipo = "Administrador"
    elif tipo_usuario == "ADMINISTRADOR":
        nuevo_tipo = "Estudiante"

    administrador_count = usuarios.count_documents(
        {'tipo_usuario': 'Administrador'})

    if administrador_count == 1 and nuevo_tipo == 'Estudiante':
        flash("No se puede cambiar el tipo de usuario. Debe haber al menos un usuario con tipo 'Administrador'.", category='error')
    else:
        usuarios.update_one(
            {'_id': ObjectId(usuario_id)},
            {'$set': {'tipo_usuario': nuevo_tipo}}
        )
        flash("Tipo de cuenta del usuario cambiado con éxito a " +
              nuevo_tipo, category='success')

    return


def insertar_tarea(nombre, descripcion, vacio, fechacreacion, idcreador, entradasalida, ejemplo):
    from app import tareas
    from app import datos_entrada_salida

    tarea = {
        'nombre': nombre,
        'descripcion': descripcion,
        'parametro_vacio': vacio,
        'fechacreacion': fechacreacion,
        'idcreador': idcreador,
        'visible': True
    }

    result = tareas.insert_one(tarea)

    datos = {
        'idtarea': result.inserted_id,
        'entradasalida': entradasalida,
        'ejemplo': ejemplo
    }

    result2 = datos_entrada_salida.insert_one(datos)

    return f'Datos entrada salida agregados con el id {result2.inserted_id}'


def actualizar_tarea(idtarea, nombre, descripcion, vacio, fechacreacion, entradasalida):
    from app import tareas
    from app import datos_entrada_salida

    tareas.update_one(
        {'_id': ObjectId(idtarea)},
        {'$set': {
            'nombre': nombre,
            'descripcion': descripcion,
            'parametro_vacio': vacio,
            'fechacreacion': fechacreacion
        }}
    )

    datos_entrada_salida.update_one(
        {'idtarea': ObjectId(idtarea)},
        {'$set': {
            'entradasalida': entradasalida
        }}
    )

    return


def subir_tarea(idusuario, idtarea, fechaentrega, nota, codigodiagrama, entradasalida):
    from app import tareas_usuario
    from app import datos_entrada_salida

    tarea_usuario = {
        'idusuario': idusuario,
        'idtarea': idtarea,
        'fechaentrega': fechaentrega,
        'nota': nota,
        'codigodiagrama': codigodiagrama
    }

    result = tareas_usuario.insert_one(tarea_usuario)

    return f'Tarea de usuario entregada con el id {result.inserted_id}'

def set_tarea_no_visible(id_tarea):
    from app import tareas

    tareas.update_one(
        {'_id': ObjectId(id_tarea)},
        {'$set': {'visible': False}}
    )
    flash("Tarea borrada con éxito.", category='success')