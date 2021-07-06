import socket
from tkinter import *
from tkinter.ttk import *
import os
from datetime import datetime

def writeAll(folderName, fileName):
    FilesList = [f for f in os.listdir(folderName) if os.path.isfile(os.path.join(folderName, f))]
    with open(fileName, "w") as inp:
        for f in FilesList:
            inp.write(f+"\n")
        inp.close()


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


label.grid(row = 0, column = 1, sticky = W, padx = 2,pady=2)
label.place(x=25, y=25, anchor="center")
Label1.grid(row = 1, column = 1, sticky = W, padx = 2,pady=2)
Label2.grid(row = 1, column = 2, sticky = W, padx = 2,pady=2)
Label3.grid(row = 1, column = 3, sticky = W, padx = 2,pady=2) 
Label4.grid(row = 1, column = 4, sticky = W, padx = 2,pady=2) 

cpt = 2


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

BUFFER_SIZE = 4096
folderName = "./files"
fileName = "files.txt"
writeAll(folderName, fileName)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen()
client_socket, address = s.accept()



received = client_socket.recv(BUFFER_SIZE).decode()

Label1 = Label(root, text=str(datetime.now()))  
Label3 = Label(root, text=str(received).replace("\n","")) 
Label2 = Label(root, text=str(address[0])+":"+str(address[1]))

Label1.grid(row = cpt, column = 1, sticky = W, padx = 2)
Label2.grid(row = cpt, column = 2, sticky = W, padx = 2)
Label3.grid(row = cpt, column = 3, sticky = W, padx = 2) 

h = open("history.txt", "a")
h.write(str(datetime.now())+" : "+str(received).replace("\n","")+" "+str(address)+"\n")

status = "Succes"
try:
    with open(os.path.join(folderName,received.replace("\n","")), "rb") as f:
        while True:
            
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                
                break
            
            client_socket.sendall(bytes_read)
except:
    status = "Failed"
Label4 = Label(root, text=status)
Label4.grid(row = cpt, column = 4, sticky = W, padx = 2) 


cpt+=1
client_socket.close()

s.close()


root.mainloop()


