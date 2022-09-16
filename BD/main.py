from Consultas import Consultas
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mydb = mysql.connector.connect(
    host = "semi1.cs8mmo4tj6mf.us-east-1.rds.amazonaws.com",
    user = "root",
    passwd = "root_BD2S2022",
    database = "Proyecto1"
)

@app.route('/')
def home():
    return "Hello, world!"

@app.route('/verificarUsuario', methods=['POST'])
def verificarUsuario():
    Usuario = request.json['Usuario']
    Correo = request.json['Correo']
    consulta = Consultas()
    return consulta.verificarUsuario(Usuario,Correo)
   


if __name__ == '__main__':
    app.run(debug=True)
    consulta = Consultas()
    print(consulta)