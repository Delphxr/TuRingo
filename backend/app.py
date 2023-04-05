from website import create_app
from pymongo import MongoClient

app = create_app()

mongo_uri = "mongodb://10.0.0.17:27017/?directConnection=true&appName=mongosh+1.8.0"
client = MongoClient(mongo_uri)

db = client.flask_db

tareas = db.tareas
tareas_usuario = db.tareas_usuario
usuarios = db.usuarios
datos_entrada_salida = db.datos_entrada_salida

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
