# Importing module 
import mysql.connector
  
# Creating connection object
mydb = mysql.connector.connect(
    host = "semi1.cs8mmo4tj6mf.us-east-1.rds.amazonaws.com",
    user = "root",
    passwd = "root_BD2S2022",
    database = "Proyecto1"
)

  
def consultas():
    cur = mydb.cursor()
    cur.execute("SELECT IdUser,Usuario,Pass,Correo,Fotografia,Fecha FROM Usuario;")  
    datos= cur.fetchall()
    cur.close()
    return datos

def insertar(Usuario,Pass,Correo,Fotografia):
    cur = mydb.cursor()
    cur.execute('''INSERT INTO Usuario(Usuario,Pass,Correo,Fotografia) VALUES('{}','{}','{}', '{}');'''.format(Usuario,Pass,Correo,Fotografia))  
    n = cur.rowcount()
    mydb.commit()
    cur.close()
    return n


def eliminar(IdUser):
    cur = mydb.cursor()
    cur.execute('''DELETE FROM Usuario WHERE IdUser = ('{}');'''.format(IdUser))  
    n = cur.rowcount()
    mydb.commit()
    cur.close()
    return n

def Modificar(IdUser, Usuario,Pass,Correo,Fotografia):
    cur = mydb.cursor()
    cur.execute('''UPDATE Usuario SET Usuario='{}',Pass='{}',Correo='{}',Fotografia ='{}' WHERE IdUser={}};'''.format(Usuario,Pass,Correo,Fotografia,IdUser))  
    n = cur.rowcount()
    mydb.commit()
    cur.close()
    return n


dat = consultas()

for fila in dat:
    print(fila)
# print(mydb)