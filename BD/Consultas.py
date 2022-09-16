import mysql.connector
import json
from BD.NodoJson import NodoJson
import datetime

class Consultas:
    # def __init__(self):
    #     self.mydb = mysql.connector.connect(
    #     host = "dbproyecto1.c9p3lkjwyslq.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     passwd = "Marco.201122934",
    #     database = "Proyecto1"
    #     )
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host = "semi1.cs8mmo4tj6mf.us-east-1.rds.amazonaws.com",
        user = "root",
        passwd = "root_BD2S2022",
        database = "Proyecto1"
        )

    def consultasLogin(self, user, password):
        # Consultar si el usuario y la contraseña son validos
        # Consultar si el usuario y la contraseña son validos
        cur = self.mydb.cursor()
        cur.execute('''SELECT IdUser , Nombre ,Usuario, cast( aes_decrypt(Pass, "semi12022")  as char), Correo, Fotografia, Fecha FROM Usuario WHERE  (Usuario='{}' OR Correo='{}')  AND  aes_decrypt(Pass, "semi12022")  = '{}';'''.format(user,user,password))
        #cur.execute('''SELECT * FROM Usuario WHERE  (Usuario='{}' OR Correo='{}')  AND  aes_decrypt(Pass, "semi12022")  = '{}';'''.format(user,user,password))
        datos= cur.fetchall()
        cur.close()
        uno=''
        for row in datos:
            uno= ({"idUser":row[0],"Nombre":row[1], "Usuario":row[2], "Pass":row[3],  "Correo":row[4],"Fotografia":row[5],"Fecha":row[6].strftime('%d/%m/%Y')})
        
        if len(uno)>0:
            stud_json = json.dumps(uno, indent=2, sort_keys=False)
        else:
            stud_json='{"idUser":0}'

        cur.close()
        return stud_json
        
    def insertarUsuario(self,Nombre,Usuario,Pass,Correo,Fotografia):
        # Inserta un usuario, antes debe estar subida la fotografia
        cur = self.mydb.cursor()
        cur.execute('''INSERT INTO Usuario(Nombre,Usuario,Pass,Correo,Fotografia) VALUES('{}','{}',aes_encrypt('{}', "semi12022"),'{}','{}');'''.format(Nombre,Usuario,Pass,Correo,Fotografia))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n 

    def VerificarUsuario(self, Usuario,Correo):
        # Todos los dato del usuario actual
        cur = self.mydb.cursor()
        cur.execute('''SELECT Correo FROM Usuario WHERE (Usuario='{}' OR Correo='{}') ;'''.format(Usuario,Correo))  
        datos= cur.fetchall()
        cur.close()
        if len(datos)>0:
            return True
        else:
            return False

    ################# seccion de archivos ################
    def insertarArchivo(self,NombreArchivo, DireccionArchivo, Tipo, IdUsuario):
        # Guardar un archivo
        cur = self.mydb.cursor()
        cur.execute('''INSERT INTO Archivo(NombreArchivo, DireccionArchivo, Tipo, IdUsuario) VALUES('{}','{}',{},{});'''.format(NombreArchivo, DireccionArchivo, Tipo, IdUsuario))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n

    def consultarArchivos(self, idUser):
        # Listar solo los archivos de un usuario especifico idArchivo, NombreArchivo, combobox
        cur = self.mydb.cursor()
        cur.execute("SELECT *  FROM Archivo WHERE IdUsuario ={};".format(idUser))  
        datos= cur.fetchall()
        cur.close()
        uno=[]
        for row in datos:
            uno.append({"IdArchivo":row[0],"NombreArchivo":row[1], "Direccion":row[2], "Tipo":row[3],  "IdUsuario":row[4],"Fecha":row[5].strftime('%d/%m/%Y')})
        return uno

    def eliminarArchivo(self,IdArchivo):
        # Eliminar un archivo en especifico
        cur = self.mydb.cursor()
        cur.execute('''DELETE FROM Archivo WHERE idArchivo={};'''.format(IdArchivo))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n

    def ModificarArchivo(self,NombreArchivo, Tipo,IdArchivo):
        cur = self.mydb.cursor()
        cur.execute('''UPDATE Archivo SET NombreArchivo = ('{}'),Tipo =  {} WHERE IdArchivo = ('{}') ;'''.format(NombreArchivo, Tipo,IdArchivo))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n

     # ############################ seccion AMIGOS ############################
    
    def ConsultarNoAmigos(self, idUser):
        # Consultar usuario no amigos y obtener el listado de archivos publicos o privados de todo los usuarios
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('''select Archivos.Publicos , Archivos.Users , Archivos.nombre,Archivos.username,Archivos.foto from  
        (
        select count(Archivo.IdArchivo) as Publicos , Archivo.IdUsuario as Users , Usuario.Nombre as nombre,Usuario.Usuario as username , Usuario.Fotografia as foto from Archivo 
        INNER JOIN Usuario ON Archivo.IdUsuario = Usuario.IdUser
        where Tipo = 1
        group by IdUsuario
        ) as Archivos 
        Where Archivos.Users In (
        select IdUser  as noAmigo  from   Usuario where IdUser NOT IN (
        SELECT * FROM 
        (
        (select IdAsociarAmigo   from Amigo  where IdUsuario = ('{}'))
            union 
            (select IdUsuario  from Amigo  where IdAsociarAmigo = ('{}'))
        ) as amigos
        ) and   IdUser <> ('{}')
        );'''.format(idUser,idUser,idUser))  
        datos= cur.fetchall()
        # 1 = publico
        # 0 = privado
        uno=[]
        for row in datos:
            uno.append({"cantidad":row[0],"id_usuario":row[1], "nombre":row[2], "user":row[3],  "foto":row[4]})
        return uno

    def insertarAmigo(self,IdUsuario,IdAsociarAmigo):
        # Guardar un nuevo amigo
        cur = self.mydb.cursor()
        cur.execute('''INSERT INTO Amigo(IdUsuario,IdAsociarAmigo) VALUES('{}','{}');'''.format(IdUsuario,IdAsociarAmigo))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n
    
    def listaArchivosAmigo(self, idUser):
        cur = self.mydb.cursor()
        cur.execute('''select Archivo.IdArchivo, Archivo.NombreArchivo ,Archivo.DireccionArchivo, Archivo.Fecha, Usuario.IdUser , Usuario.Usuario from Archivo  
        INNER JOIN Usuario ON Archivo.IdUsuario = Usuario.IdUser
        where  IdUsuario  in (
            SELECT *  FROM 
            (
            (select IdAsociarAmigo as idAmigos  from Amigo  where IdUsuario = ('{}'))
                union 
                (select IdUsuario as idAmigos  from Amigo  where IdAsociarAmigo = ('{}'))
            )   AS amigos
            ) and Tipo = 1 ;'''.format(idUser,idUser))  
        datos= cur.fetchall()
        uno=[]
        for row in datos:
            uno.append({"idArchivo":row[0],"nombreArchivo":row[1], "urlArchivo":row[2], "fechaArchivo":row[3].strftime('%d/%m/%Y'), "is_user" :row[4],"user":row[5]})
        return uno
    
    ############################ SECCION DE CONSULTAS QUE NO USE #################
    def consultas(self):
        cur = self.mydb.cursor()
        cur.execute("SELECT IdUser,Usuario,Pass,Correo,Fotografia,Fecha FROM Usuario;")  
        datos= cur.fetchall()
        cur.close()
        return datos

    def consultaArchivoUser(self):
        # Lista todos los usuarios
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('SELECT Ar.IdArchivo,Us.Usuario, Us.IdUser, if(Ar.Tipo=1,"público","privado") as Tipo, Ar.NombreArchivo, Ar.Fecha, Ar.DireccionArchivo FROM Usuario_archivo AS Ua INNER JOIN Usuario AS Us ON Ua.IdUsuario = Us.IdUser INNER JOIN Archivo AS Ar ON Ua.IdArchivo = Ar.IdArchivo WHERE IdUsuario=1 AND Ar.Tipo=1')  
        datos= cur.fetchall()
        for row in datos:
            mydict.add(row[0],({"Usuario":row[1],"IdUser":row[2],"Tipo":row[3],"NombreArchivo":row[4],"Fecha":row[5].strftime('%d/%m/%Y'),"DireccionArchivo":row[6]}))
        stud_json = json.dumps(mydict, indent=2, sort_keys=False)
        cur.close()
        return stud_json

    def Unir(self):

        return

    def ConsultarUsuario(self):
        # Consultar usuario y obtener el listado de archivos publicos o privados de todo los usuarios
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('SELECT idUser, Nombre, idUser FROM Usuario')  
        datos= cur.fetchall()
        # 1 = publico
        # 0 = privado
        for row in datos:
            mydict.add(row[0],({"Usuario":row[1],"_id":row[2],"privados":Consultas.SubConsultaArchivoUser(self,0,row[0]), "publicos":Consultas.SubConsultaArchivoUser(self,1,row[0])}))
        stud_json = json.dumps({"Archivos":list(mydict.values())}, indent=2, sort_keys=False)
        cur.close()
        return stud_json

    def ConsultarUsuarioUnico(self,idUser):
        # Consultar usuario y obtener el listado de archivos publicos o privados de todo los usuarios
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('SELECT idUser, Nombre, idUser FROM Usuario WHERE idUser={}'.format(idUser))  
        datos= cur.fetchall()
        # 1 = publico
        # 0 = privado
        for row in datos:
            mydict.add(row[0],({"Usuario":row[1],"_id":row[2],"privados":Consultas.SubConsultaArchivoUser(self,0,row[0]), "publicos":Consultas.SubConsultaArchivoUser(self,1,row[0])}))
        stud_json = json.dumps({"Archivos":list(mydict.values())}, indent=2, sort_keys=False)
        cur.close()
        return stud_json

    def SubConsultaArchivoUser(self,tipo,idUsuario):
        # SubConsulta los archivos, filtrados por publicos o privado y por el idUsuario
        mydict1 = NodoJson()
        cur1 = self.mydb.cursor()
        cur1.execute('SELECT Ar.IdArchivo,Ar.NombreArchivo,Us.Usuario,Ar.Fecha, Ar.DireccionArchivo,if(Ar.Tipo=1,"público","privado") as Tipo FROM Archivo AS Ar INNER JOIN Usuario AS Us ON Ar.IdUsuario = Us.IdUser WHERE IdUsuario={} AND Ar.Tipo={};'.format(idUsuario,tipo))  
        datos1= cur1.fetchall()
        for row1 in datos1:
            mydict1.add(row1[0],({"Nombre":row1[1],"Propietario":row1[2],"Fecha":row1[3].strftime('%d/%m/%Y'),"Ruta":row1[4]}))
        cur1.close()
        return list(mydict1.values())

    

   

    
    

   





    
    def buscarUsuario(self, idUser, user):
        # Buscar usuario
        cur = self.mydb.cursor()
        cur.execute("   select IdUser  as noAmigo  from   Usuario where IdUser NOT IN ( SELECT * FROM ( (select IdAsociarAmigo   from Amigo  where IdUsuario = ({}))  union (select IdUsuario  from Amigo  where IdAsociarAmigo = ({}))	) as amigos ) and   IdUser <> ({}) and Usuario LIKE'{}%''';".format(idUser, user)) 
        datos= cur.fetchall() 
        cur.close()
        return datos

    def eliminar(self,IdUser):
        cur = self.mydb.cursor()
        cur.execute('''DELETE FROM Usuario WHERE IdUser = ('{}');'''.format(IdUser))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n

    def Modificar(self,IdUser, Usuario,Pass,Correo,Fotografia):
        cur = self.mydb.cursor()
        cur.execute('''UPDATE Usuario SET Usuario='{}',Pass='{}',Correo='{}',Fotografia ='{}' WHERE IdUser={}};'''.format(Usuario,Pass,Correo,Fotografia,IdUser))  
        n = cur.rowcount
        self.mydb.commit()
        cur.close()
        return n

    
    """
        def ConsultarNoAmigos(self, idUser,Usuario):
            # Consultar usuario no amigos y obtener el listado de archivos publicos o privados de todo los usuarios
            mydict = NodoJson()
            cur = self.mydb.cursor()
            cur.execute('''SELECT Ar.IdUsuario, Us.Usuario, count(Ar.Tipo) AS Conteo, Fotografia 
    FROM Archivo as Ar
    INNER JOIN Usuario AS Us
    ON Ar.IdUsuario = Us.IdUser
    WHERE Ar.Tipo=1 AND Ar.IdUsuario IN (
    select IdUser from   Usuario where IdUser NOT IN (
    SELECT * FROM 
    (
    (select IdAsociarAmigo   from Amigo  where IdUsuario = ({}))
    union 
    (select IdUsuario  from Amigo  where IdAsociarAmigo = ({}))
    ) as amigos
    ) and   IdUser <> ({}) and Usuario LIKE'{}%'

    ) group by Ar.IdUsuario,Us.Nombre
    '''.format(idUser,idUser,idUser,Usuario))  
            datos= cur.fetchall()
            # 1 = publico
            # 0 = privado
            for row in datos:
                mydict.add(row[0],({"Usuario":row[1],"_id":row[0], "publicos":row[2],"imagen":row[3]}))
            stud_json = json.dumps({"Archivos":list(mydict.values())}, indent=2, sort_keys=False)
            cur.close()
            return stud_json
    """
    def ConsultarNoAmigosTodos(self, idUser):
        # Consultar usuario amigos y obtener el listado de archivos publicos o privados de todo los usuarios
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('''SELECT IdArchivo, NombreArchivo, Us.Usuario, Ar.Fecha, Ar.DireccionArchivo FROM Archivo AS Ar
    INNER JOIN Usuario AS Us
    ON Us.IdUser = Ar.IdUsuario
    WHERE Ar.Tipo=1 AND IdUsuario in(
    SELECT *  FROM 
	(
	   (select IdAsociarAmigo as idAmigos  from Amigo  where IdUsuario = ({}))
		union 
		(select IdUsuario as idAmigos  from Amigo  where IdAsociarAmigo = ({}))
	)   AS amigos );'''.format(idUser,idUser))  
        datos= cur.fetchall()
        for row in datos:
            mydict.add(row[0],({"Archivo":row[1],"Propietario":row[2], "Fecha":row[3].strftime('%d/%m/%Y'),"URL":row[4]}))
        stud_json = json.dumps({"Archivos":list(mydict.values())}, indent=2, sort_keys=False)
        cur.close()
        return stud_json

    def BuscarDoc(self, idUser, archivo):
        # Consultar usuario amigos por medio de nombre y obtener el listado de archivos publicos o privados de todo los usuarios
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('''
        SELECT IdArchivo, NombreArchivo, Us.Usuario, Ar.Fecha, Ar.DireccionArchivo FROM Archivo AS Ar
    INNER JOIN Usuario AS Us
    ON Us.IdUser = Ar.IdUsuario
    WHERE Ar.Tipo=1 AND NombreArchivo LIKE('{}%') AND IdUsuario in(
    SELECT *  FROM 
	(
	   (select IdAsociarAmigo as idAmigos  from Amigo  where IdUsuario = ({}))
		union 
		(select IdUsuario as idAmigos  from Amigo  where IdAsociarAmigo = ({}))
	)   AS amigos);
        '''.format(archivo, idUser,idUser))  
        datos= cur.fetchall()
        for row in datos:
            mydict.add(row[0],({"Archivo":row[1],"Propietario":row[2], "Fecha":row[3].strftime('%d/%m/%Y'),"URL":row[4]}))
        stud_json = json.dumps({"Archivos":list(mydict.values())}, indent=2, sort_keys=False)
        cur.close()
        return stud_json

    def ObtenerUsuario(self, idUser):
        # Todos los dato del usuario actual
        mydict = NodoJson()
        cur = self.mydb.cursor()
        cur.execute('''SELECT idUser,Nombre,Usuario,Pass,Correo,Fotografia,Fecha from Usuario where idUser={};'''.format(idUser))  
        datos= cur.fetchall()
        uno=''
        for row in datos:
            uno= ({"idUser":row[0],"Nombre":row[1], "Usuario":row[2], "Pass":row[2], "Correo":row[4],"Fotografia":row[5],"Fecha":row[6].strftime('%d/%m/%Y')})
        stud_json = json.dumps(uno, indent=2, sort_keys=False)
        cur.close()
        return stud_json
    
    