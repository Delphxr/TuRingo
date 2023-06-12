from website import create_app
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()
app.secret_key = 'arroz con pollo doble'

mongo_uri = 'mongodb://10.0.0.17:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.9.1' 
client = MongoClient(mongo_uri)

db = client.turingo

tareas = db.tareas
tareas_usuario = db.tareasusuario
usuarios = db.usuarios
datos_entrada_salida = db.datosentradasalida

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
