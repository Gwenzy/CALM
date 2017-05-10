﻿# Créé par lcharleu, le 24/03/2017 avec EduPython
import sqlite3, socket, time
IP_SERVER = "127.0.0.1"
PORT_SERVER = 2222



print("Starting server...")
CreateDataBase = sqlite3.connect('CALM.db')
Musics_Directory = "Musics/"

QueryCurs = CreateDataBase.cursor()
print("Creating database")
QueryCurs.execute('''CREATE TABLE IF NOT EXISTS Musiques
(
    id INT PRIMARY KEY NOT NULL,
    Titre TEXT,
    Auteur TEXT,
    Like INT
)''')

CreateDataBase.commit()
print("Database created")
def AddMusic(Titre,Auteur,Categorie,Like):                                                     #A COMPLETER
        QueryCurs.execute('''INSERT INTO Musiques (Titre,Auteur,Like)
        VALUES (?,?,?,?,?)''',(Titre,Auteur,0))

def GetMusics():
    Musics = []
    Resp = QueryCurs.execute('''SELECT Titre FROM Musiques''')
    for row in Resp.fetchall():
        print(row)
        Musics.append(row[0])
    return Musics

def CheminRecherche(Title):
    return Musics_Directory+Title

def AddLike(Title):
    QueryCurs.execute('''SELECT Like FROM Musiques
    WHERE Titre="'''+Title+'''"
    ''')
    
    Like_Number = QueryCurs.fetchone()[0]
    

    QueryCurs.execute('''UPDATE Musiques
    SET Like='''+(Like_Number+1)+'''
     WHERE Titre = "'''+Title+'''"
    ''')
    
    CreateDataBase.commit()

def AddDislike(ID):
    QueryCurs.execute('''SELECT Like FROM Musiques
    WHERE Titre="'''+Title+'''"
    ''')
    
    Like_Number = QueryCurs.fetchone()[0]
    

    QueryCurs.execute('''UPDATE Musiques
    SET Like='''+(Like_Number-1)+'''
     WHERE Titre = "'''+Title+'''"
    ''')
    
    CreateDataBase.commit()
def FormatMusics(musics):
    result = ""
    for music in musics:
        result+=music
        result+="|"
    return result
#-------------------------EMERIC------------------------------



print("Server fully started, ready to listen")
while True:
    try:
        print("Waiting for a new connection")
        Mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Mysocket.bind((IP_SERVER, PORT_SERVER))
        Mysocket.listen(5)
        client, address = Mysocket.accept()
        print("Someone just connected")
        response = client.recv(255).decode()
        print("New message : "+response)
        if response == "musiclist":
            musics = FormatMusics(GetMusics())
                
            time.sleep(2)
            Mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Mysocket.connect((IP_SERVER, PORT_SERVER+1))
            Mysocket.send(musics)
            Mysocket.close()
        elif response.startswith("download"):
            None
        print("Close")
        Mysocket.close()
    except Exception as e: print(str(e))





