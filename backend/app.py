from website import create_app
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()
app.secret_key = os.getenv('SECRET_KEY')

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)

db = client.turingo

tareas = db.tareas
tareas_usuario = db.tareasusuario
usuarios = db.usuarios
datos_entrada_salida = db.datosentradasalida

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
