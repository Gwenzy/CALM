# Créé par lcharleu, le 24/03/2017 avec EduPython
import sqlite3, socket, time
IP_SERVER = "127.0.0.1"
PORT_SERVER = 2222
PORT_SERVER_DL = 1111



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

def GetMusics():
    Musics = []
    Resp = QueryCurs.execute('''SELECT Titre FROM Musiques ORDER BY Like DESC''')
    for row in Resp.fetchall():
        print(row)
        Musics.append(row[0])
    return Musics

def AddLike(Title):
    QueryCurs.execute('''SELECT Like FROM Musiques
    WHERE Titre="'''+Title+'''"
    ''')
    
    Like_Number = QueryCurs.fetchone()[0]
    

    QueryCurs.execute('''UPDATE Musiques
    SET Like='''+str(Like_Number+1)+'''
     WHERE Titre = "'''+Title+'''"
    ''')
    
    CreateDataBase.commit()

def AddDislike(Title):
    QueryCurs.execute('''SELECT Like FROM Musiques
    WHERE Titre="'''+Title+'''"
    ''')
    
    Like_Number = QueryCurs.fetchone()[0]
    

    QueryCurs.execute('''UPDATE Musiques
    SET Like='''+str(Like_Number-1)+'''
     WHERE Titre = "'''+Title+'''"
    ''')
    
    CreateDataBase.commit()
def FormatMusics(musics):
    result = ""
    for music in musics:
        result+=music
        result+=".mp3"
        result+="|"
    return result




print("Server fully started, ready to listen")
Mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Mysocket.bind((IP_SERVER, PORT_SERVER))

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((IP_SERVER ,PORT_SERVER_DL))

tcpsock.listen(5)
Mysocket.listen(5)


while True:

    #try:
        print("Waiting for a new connection")
        
        client, (ip, port) = Mysocket.accept()
        print("Someone just connected")
        response = client.recv(255).decode()
        print("New message : "+response)
        if response == "musiclist":
            musics = FormatMusics(GetMusics())
                
            time.sleep(2)
            OtherSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Connecting on ", ip, "on port ", PORT_SERVER+1)
            OtherSocket.connect((str(ip), PORT_SERVER+1))
            OtherSocket.send(musics.encode())
            OtherSocket.close()
        elif response.startswith("download"):
            musicName = response[8:]
            print( "En écoute...")
            (clientsocket, (ip, port)) = tcpsock.accept()
            print("Connection de %s %s" % (ip, port, ))

            
            print("Ouverture du fichier: ", musicName , "...")
            fp = open("Musics/"+musicName+".mp3", 'rb')
            clientsocket.send(fp.read())
            clientsocket.close()
            print("Client déconnecté...")
        elif response.startswith("like"):
            musicName = response[4:]
            AddLike(musicName)
        elif response.startswith("dislike"):
            musicName = response[7:]
            AddDislike(musicName)



        
        print("Close")
        client.close()
    #except Exception as e: print(e)