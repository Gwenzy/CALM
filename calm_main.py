#Imports
import pygame, os, sys, tkinter, socket, time
from tkinter import *
#Const
IP_SERVER = "127.0.0.1"
PORT_SERVER = 2222
PORT_SERVER_DL = 1111
MUSIC_DIRECTORY_WIN = os.getenv('APPDATA')+"\\CALM\\"
MUSIC_DIRECTORY = ""
currentMusic=""
currentMusicID=0
isPaused = False
DEBUG = True

localMusics = []
connectionState = False

#Init
pygame.init()
fenetre = pygame.display.set_mode((10, 10), pygame.NOFRAME )
music = pygame.mixer.music

if sys.platform=="win32":
    MUSIC_DIRECTORY = MUSIC_DIRECTORY_WIN
    
if not os.path.isdir(MUSIC_DIRECTORY):
    os.makedirs(MUSIC_DIRECTORY)


#Méthodes utiles

def playPath(path):
    global music
    #On vérifie si la musique est déjà téléchargée
    music.load(path)
    music.play()


  
def play(musicA, newID):
    
    global isPaused
    global currentMusic
    global currentMusicID
    currentMusicID = newID
    if(musicA==currentMusic and isPaused):
        music.unpause()
    else:
        music.stop()
        print("Executed command with "+musicA)
        if isMusicDownloaded(musicA)==False:
            downloadMusic(musicA)
        music.load(MUSIC_DIRECTORY+musicA+".mp3")
        music.play()
        currentMusic = musicA
    isPaused = True
def pause():
    global isPaused
    music.pause()
    isPaused = True

def stop():
    music.stop()

def volume(vol):
    music.set_volume(vol)
    
def getOfflineMusics():
    for file in os.listdir(MUSIC_DIRECTORY):
        if file.endswith(".mp3"):
            localMusics.append(os.path.join(MUSIC_DIRECTORY, file))
def isServerOnline():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((IP_SERVER, PORT_SERVER))
        s.close()
        time.sleep(1)
        return True
    except: 
        return False
    #Emeric
def downloadMusic(musicName):


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_SERVER, PORT_SERVER))
    s.send(("download"+musicName).encode())
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_SERVER, PORT_SERVER_DL))
    r = s.recv(9999999)
    with open(MUSIC_DIRECTORY+musicName+".mp3",'wb') as _file:
        _file.write(r)
    print("Le fichier a été correctement téléchargé")
    
    s.close()
    
    
def isMusicDownloaded(musicID):
    getOfflineMusics()
    global localMusics
    for i in localMusics:
        if(musicID in i):
            return True
    return False     
def getFileNameByID(musicID):
    None
    #Emeric
    
def updateVolume():
    global w
    global music
    music.set_volume(float(w.get())/float(100))
def getMusics():
    musics = []
    
    if(isServerOnline()):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP_SERVER, PORT_SERVER))
        print("Debug")
        
        
        s.send("musiclist".encode())
        s.close()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP_SERVER, PORT_SERVER+1))
        s.listen(5)
        client, address = s.accept()
        response = client.recv(9999999).decode()
        print(response)
        for music in response.split("|"):
            musics.append(music)
        s.close()
        return musics    

        
    else:
       getOfflineMusics()
       return localMusics
continuer = 1

def like():
    if(currentMusic!="" and isServerOnline()):
        print("You just liked "+currentMusic)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP_SERVER, PORT_SERVER))
        s.send(("like"+currentMusic).encode())
        s.close()
    
def dislike():
    if(currentMusic!="" and isServerOnline()):
        print("You just disliked "+currentMusic)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP_SERVER, PORT_SERVER))
        s.send(("dislike"+currentMusic).encode())
        s.close()



def function(button):
    print("Le boutton "+button+" a été poussé")

master = Tk()

bottomframe=Frame(master)
bottomframe.pack(side= BOTTOM)

previousbutton = Button(bottomframe, text='previous', fg='blue',command= lambda: play(listbox.get(currentMusicID-1), currentMusicID-1))
previousbutton.pack(side = LEFT)

green2button = Button(bottomframe, text="Play", fg="green", command= lambda: play(listbox.get(listbox.curselection()), listbox.curselection()[0]))
green2button.pack( side = LEFT)

greenbutton = Button(bottomframe, text="Pause", fg="green",command= lambda: pause())
greenbutton.pack( side = LEFT )

bluebutton = Button(bottomframe, text="Like", fg="red",command= lambda: like())
bluebutton.pack( side = LEFT )

redbutton = Button(bottomframe, text="Dislike", fg="red",command= lambda: dislike())
redbutton.pack( side = LEFT )

nextbutton = Button(bottomframe, text='next', fg='blue',command= lambda: play(listbox.get(currentMusicID+1), currentMusicID+1))
nextbutton.pack(side = RIGHT)

w = Scale(master, from_=0, to=100)
w.pack(side = LEFT)
w.config(command= lambda x: updateVolume())

scrollbar = Scrollbar(master)


listbox = Listbox(master, yscrollcommand=scrollbar.set, width=50)
for i in getMusics():
    print("Adding "+i)
    listbox.insert(END, str(i.split("\\")[len(i.split("\\"))-1])[:len(i.split("\\")[len(i.split("\\"))-1])-4])
listbox.pack(side=LEFT, fill=BOTH)
scrollbar.pack(side=LEFT, fill=Y)
scrollbar.config(command=listbox.yview)

master.mainloop()


while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         continuer=0
pygame.quit()#Ici!