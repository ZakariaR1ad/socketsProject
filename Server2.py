import threading
from tkinter import *
import socket
from datetime import datetime
import os

#Définition des variables
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

BUFFER_SIZE = 4096
folderName = "./files"
fileName = "files.txt"


#Ecriture des noms des fichiers (dispo dans le dossier files) dans le fichier files.txt
def writeAll(folderName, fileName):
    FilesList = [f for f in os.listdir(folderName) if os.path.isfile(os.path.join(folderName, f))]
    with open(fileName, "w") as inp:
        for f in FilesList:
            inp.write(f+"\n")
        inp.close()


#L'application principale (Main thread)
class MyApp():
   
   def __init__(self, mywin):
        self.mywin = mywin
        
        writeAll(folderName, fileName)
        
            
#Définition de la fenêtre
root = Tk()
root.title("Server")
sizex = 600
sizey = 400
posx  = 40
posy  = 20
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
label = Label(root, text = "Liste des requêtes")



Label1 = Label(root, text="Date et Heure")  
Label2 = Label(root, text="Source") 
Label3 = Label(root, text="Nom de Fichier")
Label4 = Label(root, text="Status")


label.grid(row = 0, column = 1, sticky = W, padx = 2)

Label1.grid(row = 1, column = 1, sticky = W, padx = 2,pady=2)
Label2.grid(row = 1, column = 2, sticky = W, padx = 2,pady=2)
Label3.grid(row = 1, column = 3, sticky = W, padx = 2,pady=2) 
Label4.grid(row = 1, column = 4, sticky = W, padx = 2,pady=2) 

cpt = 2
myapp = MyApp(root)


#Le coté socket qui comprend :connexion, réception et envoie
def mainloop():
    global cpt
    
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen()
        client_socket, address = s.accept()
        received = client_socket.recv(BUFFER_SIZE).decode()
        if(received == "Q"):
            break
        else:
            h = open("history.txt", "a")
            h.write(str(datetime.now())+" : "+str(received).replace("\n","")+" "+str(address)+"\n")
            h.close()
            
            Label1 = Label(root, text=str(datetime.now()))  
            Label3 = Label(root, text=str(received).replace("\n","")) 
            Label2 = Label(root, text=str(address[0])+":"+str(address[1]))

            Label1.grid(row = cpt, column = 1, sticky = W, padx = 2)
            Label2.grid(row = cpt, column = 2, sticky = W, padx = 2)
            Label3.grid(row = cpt, column = 3, sticky = W, padx = 2) 

            status = "Succes"
            try:
                with open(os.path.join(folderName,received.replace("\n","")), "rb") as f:
                    
                    while True:
                        
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            
                            break
                        
                        client_socket.sendall(bytes_read)
                    f.close()
                    
            except:
                status = "Failed"
            Label4 = Label(root, text=status)
            Label4.grid(row = cpt, column = 4, sticky = W, padx = 2) 


            cpt+=1
            
        client_socket.close()

    s.close()

threading.Thread(target=mainloop).start()
root.mainloop()
