from website import create_app
from pymongo import MongoClient

app = create_app()
app.secret_key = "secret key"

mongo_uri = "mongodb://localhost:27017/?directConnection=true&appName=mongosh+1.8.0"
client = MongoClient(mongo_uri)

db = client.turingo

tareas = db.tareas
tareas_usuario = db.tareasusuario
usuarios = db.usuarios
datos_entrada_salida = db.datosentradasalida

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
