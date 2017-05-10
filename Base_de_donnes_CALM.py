# Créé par lcharleu, le 24/03/2017 avec EduPython
import sqlite3

CreateDataBase = sqlite3.connect('CALM.db')

QueryCurs = CreateDataBase.cursor()

QueryCurs.execute('''CREATE TABLE IF NOT EXISTS Musiques
(
    id INT PRIMARY KEY NOT NULL,
    Titre TEXT,
    Auteur TEXT,
    Categorie TEXT,
    Like INT,
    Chemin VARCHAR(255)
)''')

def AddMusic(Titre,Auteur,Categorie,Like):
    AutorisationAjout()
    if autorisation==1:
        Chemin='.../'+Categorie                                                          #A COMPLETER
        QueryCurs.execute('''INSERT INTO Musiques (Titre,Auteur,Categorie,Like,Chemin)
        VALUES (?,?,?,?,?)''',(Titre,Auteur,Categorie,Like,Chemin))
    if autorisation==0:
        DeleteRequete()

def IDRecherche(TitreRecherche):
    ID=QueryCurs.execute('''SELECT id FROM Musiques WHERE Titre=Titrerecherche''')

def CheminRecherche(IDRecherche):
    CheminCherche=QueryCurs.execute('''SELECT Chemin FROM Musiques WHERE id=IDRecherche''')

def AutorisationAjout():
    none                                                                                        #A COMPLETER


def DeleteRequete():
    none

                                                                                        #A COMPLETER
def AddRequete():
    none
                                                                                        #A COMPLETER


def AddLike(ID):
    QueryCurs.execute('''UPDATE Musiques
    Like+=1
    WHERE id=ID
    SELECT *
    FROM Musiques
    ORDER BY Like DESC''')

def AddDislike(ID):
    QueryCurs.execute('''UPDATE Musiques
    Like-=1
    WHERE id=ID
    SELECT *
    FROM Musiques
    ORDER BY Like DESC''')







