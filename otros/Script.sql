CREATE DATABASE IF NOT EXISTS Proyecto1;
USE Proyecto1;

CREATE TABLE Usuario(
    IdUser INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Usuario VARCHAR(100) NOT NULL,
    Pass VARCHAR(250) NOT NULL,
    Correo VARCHAR(100) NOT NULL,
    Fotografia VARCHAR(250) NOT NULL,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Archivo(
    IdArchivo INT PRIMARY KEY AUTO_INCREMENT,
    NombreArchivo VARCHAR(100) NOT NULL,
    DireccionArchivo VARCHAR(250) NOT NULL,
    Tipo BIT,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Amigo(
    IdAmigo INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT NOT NULL,
    IdAsociarAmigo INT NOT NULL,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUser) ON DELETE CASCADE ON UPDATE CASCADE ,
    FOREIGN KEY (IdAsociarAmigo) REFERENCES Usuario(IdUser) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Usuario_archivo(
    IdAsociado INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT NOT NULL,
    IdArchivo INT NOT NULL,
    FOREIGN KEY(IdUsuario) REFERENCES Usuario(IdUser) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(IdArchivo) REFERENCES Archivo(IdArchivo) ON DELETE CASCADE ON UPDATE CASCADE
);

/*
DROP TABLE Usuario_archivo;
DROP TABLE Amigo;
DROP TABLE Archivo;
DROP TABLE Usuario;

SELECT IdUser,Nombre,Usuario,Pass,Correo,Fotografia,Fecha FROM Usuario;
SELECT IdArchivo, NombreArchivo, DireccionArchivo, Tipo, Fecha FROM Archivo;
SELECT IdAmigo,IdUsuario,IdAsociarAmigo FROM Amigo;
SELECT IdAsociado, IdUsuario, IdArchivo FROM Usuario_archivo;

INSERT INTO Usuario(Nombre,Usuario,Pass,Correo,Fotografia) VALUES('Prueba 1 apellido','Prueba1','Prueba1','prueba1@pruba', 'prueba');
INSERT INTO Usuario(Nombre,Usuario,Pass,Correo,Fotografia) VALUES('Prueba 2 apellido','Prueba2','Prueba2','prueba2@pruba', 'prueba');
INSERT INTO Archivo(NombreArchivo, DireccionArchivo, Tipo) VALUES('Primer Archivo','Direccion archivo',1);
INSERT INTO Archivo(NombreArchivo, DireccionArchivo, Tipo) VALUES('Segundo Archivo 2','Direccion archivo',1);
INSERT INTO Amigo(IdUsuario,IdAsociarAmigo) VALUES(1,2);
INSERT INTO Usuario_archivo(IdUsuario, IdArchivo) VALUES(1,1);
INSERT INTO Usuario_archivo(IdUsuario, IdArchivo) VALUES(1,2);

UPDATE Usuario SET Nombre='Archivo uno apellido', Usuario='Prueba_1',Pass='Prueba_1',Correo='Prueba_1@pruba',Fotografia ='prueba_1' WHERE IdUser=1;
UPDATE Archivo SET NombreArchivo='Primer_archivo', DireccionArchivo='Direccion primer archivo', Tipo=1 WHERE IdArchivo=1;
UPDATE Amigo SET IdUsuario=1,IdAsociarAmigo=2 WHERE IdAmigo=1;
UPDATE Usuario_archivo SET IdUsuario=1, IdArchivo=1 WHERE IdAsociado=1;


//Lista de amigos
SELECT Us.Usuario FROM AMIGO as Am
INNER JOIN Usuario AS Us
ON Am.IdAsociarAmigo = Us.IdUser
WHERE IdAmigo=1;

//Lista de archivos de un usuario en particular
SELECT Us.Nombre, Us.IdUser, if(Ar.Tipo=1,"público","privado") as Tipo, Ar.NombreArchivo, Ar.Fecha, Ar.DireccionArchivo FROM Usuario_archivo AS Ua
INNER JOIN Usuario AS Us
ON Ua.IdUsuario = Us.IdUser
INNER JOIN Archivo AS Ar
ON Ua.IdArchivo = Ar.IdArchivo
WHERE IdUsuario=1 AND Ar.Tipo=1;

//Contidad de archivos publicos

SELECT COUNT(*) AS Cantidad FROM Usuario_archivo AS Us
INNER JOIN Archivo AS Ar
ON Us.IdUsuario=Ar.IdArchivo
WHERE Us.IdUsuario=1 AND Ar.Tipo=1;

//Busqueda por nombre de archivo

SELECT Ar.NombreArchivo, Us.Usuario ,Ar.Fecha FROM Usuario_archivo AS Ua
INNER JOIN Archivo AS Ar
ON Ua.IdArchivo= Ar.IdArchivo
INNER JOIN Usuario as Us
ON Ua.IdUsuario = Us.IdUser
WHERE Ar.NombreArchivo LIKE "S%" AND Ua.IdUsuario IN (SELECT Am.IdAsociarAmigo FROM AMIGO as Am
INNER JOIN Usuario AS Us
ON Am.IdAsociarAmigo = Us.IdUser
WHERE idUsuario=1);

*/
