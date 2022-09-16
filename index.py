import os
from urllib.request import Request
from BD.Consultas import Consultas
from flask import Flask, request
import json
from bucket import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER='uploads'
@app.route('/login', methods=['POST'])
def login():
# Hacer login, si devuelve 0 el usuario no existe, de lo contrario devuelve el IdUser
    try:
        if request.method == "POST":
            consulta = Consultas()
            user = request.json['user']
            password = request.json['password']
            resultado = consulta.consultasLogin(user,password)
            return resultado
    except:
        return 'Se generado un error'

@app.route("/upload", methods=['POST'])
# Cargar imagen y devuelve la Url del objeto subido
def upload():
    if request.method == "POST":
        f = request.files['file']
        print(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        enlace = upload_file(f"uploads/{f.filename}", buckeetName)
        respuesta = {"url": enlace}
        return json.dumps((respuesta))

@app.route('/registro', methods=['POST'])
def registro():
    # Registrar usuario, subir primero imagen para obtener URL, devuelve un estado: 1 si es correcto
    if request.method == "POST":
        consulta = Consultas()
        nombre= request.json['nombre']
        usuario= request.json['usuario']
        password= request.json['pass']
        correo= request.json['correo']
        url = request.json['fotografia']
        respuesta=consulta.insertarUsuario(nombre, usuario, password, correo, url )
        resp = {"estado": respuesta}
        return resp

@app.route('/verificarUsuario', methods=['POST'])
def  verificarUsuario():
    # Registrar usuario, subir primero imagen para obtener URL, devuelve un estado: 1 si es correcto
    if request.method == "POST":
        consulta = Consultas()
        usuario= request.json['usuario']
        correo= request.json['correo']
        respuesta=consulta.VerificarUsuario(usuario, correo)
        print(respuesta)
        if respuesta :
            resp = {"estado": 1}
            return resp
        else:
            resp = {"estado": 0}
            return resp
 
# ############################ seccion de archivos ############################
@app.route('/Archivo', methods=['POST'])
def archivo():
    # Recibe el archivo que se desea guardar
    if request.method == "POST":
        NombreArchivo = request.json['archivo']
        DireccionArchivo = request.json['dir']
        Tipo = request.json['tipo']
        IdUsuario = request.json['user']
        consulta = Consultas()
        respuesta = consulta.insertarArchivo(NombreArchivo, DireccionArchivo, Tipo, IdUsuario)
        resp = {"estado": respuesta}
        return resp

@app.route('/listararchivo', methods=['POST'])
def listararchivo():
   # Listar todos los archivos de un usuario especifico, IdArchivo, NombreArchivo
    if request.method== "POST":
        iduser = request.json['iduser']
        consulta = Consultas()
        respuesta = consulta.consultarArchivos(iduser)
        resp = {"archivo": respuesta}
        return json.dumps(resp)

@app.route('/eliminararchivo',methods=['POST'])
def eliminararchivo():
    # Eliminar un archivo por su idArchivo
    if request.method == 'POST':
        IdArchivo = request.json['IdArchivo']
        Consulta = Consultas()
        respuesta = Consulta.eliminarArchivo(IdArchivo)
        resp = {"estado": respuesta}
        return json.dumps(resp)

@app.route('/editarfile',methods=['POST'])
def editararchivo():
    #Edita los campos nombre, tipo de un archivo
    if request.method == 'POST':
        IdArchivo = request.json['IdArchivo']
        nombre = request.json['nombre']
        tipo = request.json['tipo']
        consulta = Consultas()
        respuesta = consulta.ModificarArchivo(nombre,tipo, IdArchivo)
        resp = {"estado": respuesta}
        return json.dumps(resp)


# ############################ seccion AMIGOS ############################

#lista de no amigos
@app.route('/findfriend', methods=['POST'])
def buscaramigo():
    if request.method == 'POST':
        idUser = request.json['IdUser']
        consulta=Consultas()
        respuesta = consulta.ConsultarNoAmigos(idUser)
        resp = {"noamigos": respuesta}
        return json.dumps(resp)

#agregar amigos
@app.route('/newfriend', methods=['POST'])
def AgregarAmigo():
    #Insertar un nuevo amigo, idUsuario, IdAsociadoAmigo
    if request.method == 'POST':
        IdUsuario = request.json['idusuario']
        IdAsociarAmigo= request.json['idamigo']
        consulta = Consultas()
        respuesta = consulta.insertarAmigo(IdUsuario, IdAsociarAmigo)
        resp = {"estado": respuesta}
        return json.dumps(resp)


#obtener lista de archivos de amigos
@app.route('/listararchivoamigo', methods=['POST'])
def listararchivoamigos():
   # Listar todos los archivos de un usuario especifico, IdArchivo, NombreArchivo
    if request.method== "POST":
        iduser = request.json['iduser']
        consulta = Consultas()
        respuesta = consulta.listaArchivosAmigo(iduser)
        resp = {"archivo": respuesta}
        return json.dumps(resp)




########################  SECCION DE PETICIONES QUE NO USE ############################
#######################################################################################
@app.route('/dashboard')
def dashboard():
    # Devuelve un json con todos los usuarios y sus fotografias privadas y publicas
    consulta = Consultas()
    return consulta.ConsultarUsuario()

@app.route('/dashboarduser', methods=['POST'])
def dashboardUsuario():
    # Devuelve un json con un los usuarios y sus fotografias privadas y publicas
    if request.method == "POST":
        iduser = request.form['iduser']
    consulta = Consultas()
    return consulta.ConsultarUsuarioUnico(iduser)

@app.route('/detallefile', methods=['POST'])
def detallefile():
    # Listar los detalles de un archivo en especifico
    if request.method== "POST":
        iduser = request.form['idArchivo']
        consulta = Consultas()
        respuesta = consulta.consultarArchivosId(iduser)
        resp = {"archivo": respuesta}
        return json.dumps(resp)

@app.route('/alldocs', methods=['POST'])
def ArchivoAmigos():
    # Devuelve los archivos publicos de amigos 
    if request.method == 'POST':
        idUser = request.form['iduser']
        consulta=Consultas()
        
        return consulta.ConsultarNoAmigosTodos(idUser)

@app.route('/docsbuscar', methods=['POST'])
def BuscarAmigo():
    # Devuelve los archivos publicos de amigos 
    if request.method == 'POST':
        idUser = request.form['iduser']
        archivo = request.form['archivo']
        consulta=Consultas()
        
        return consulta.BuscarDoc(idUser,archivo)

@app.route('/user', methods=['POST'])
def ObtenerUsuario():
    # Devuelve todos los detalles del actual usuario
    if request.method == 'POST':
        idUser = request.form['iduser']
        consulta=Consultas()
        return consulta.ObtenerUsuario(idUser)
@app.route('/')
def inicio():
    return 'Hola'

if __name__ == '__main__':
    app.run(debug=True)
