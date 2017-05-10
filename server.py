#Imports
import socket, sqlite3, time
IP_SERVER = "127.0.0.1"
PORT_SERVER_MSCLIST = 2222
PORT_SERVER_DL = 1111


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 1234))

while True:
        socket.listen(5)
        client, address = socket.accept()
        response = client.recv(255)
        if response != "musiclist":
            conn = sqlite3.connect("calm.db")
			cursor = conn.cursor()
			cursor.execute("CREATE TABLE IF NOT EXISTS 'musics' (id INTEGER PRIMARY KEY AUTOINCREMENT, music VARCHAR NOT NULL);")
			cursor.execute("SELECT * FROM musics")
			resp = cursor.fetchall()
			musics=""
			for row in resp:
				musics+=row[1]
				
			time.sleep(2)
			socket.connect((IP_SERVER, PORT_SERVER_MSCLIST+1))
			socket.send(musics)
			socket.close()
print "Close"
client.close()
stock.close()