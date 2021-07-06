import socket
from tkinter import *
import os


#Definition des varibales globales

filename = ""
BUFFER_SIZE = 4096
Host = "127.0.0.1"
Port = 5000

#connexion au serveur
s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))


#Definition de la fonction de déconnexion (boutton quitter)
    
def quit(root):
    global s
    try:
        s.send("Q".encode())
        s.close()
    except:
        reConnect()
        s.send("Q".encode())
        s.close()

    root.destroy()





#une fonction pour la reconnexion au cas d'erreur
def reConnect():
    global s
    s.close()
    s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host, Port))


#la fonction de selection des fichiers: avecl'envoie du choix et la réception du fichier
def CurSelet(evt):
    global filename
    
    filename = str(listbox.get(listbox.curselection()))
    value = filename.encode()
    try:
        s.sendall(value)
    except:
        reConnect()
        s.sendall(value)
    
    with open(os.path.join("Client",filename.replace("\n", "")), "wb") as f:
        while True:
           
           
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:    
                
                break
            else:
            
                f.write(bytes_read)
        
        f.close()
            


if __name__ == "__main__":
    
    

# definition de la fenêtre 

    root = Tk()
    root.title("Client")
    sizex = 600
    sizey = 400
    posx  = 40
    posy  = 20
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    label = Label(root, text = "Liste des fichiers")

    label.pack() 


#Ajout des fichiers disponibles (dans files.txt) à l'interface
    fileList = []
    file = open("files.txt", "r")
    lines = file.readlines()
    for l in lines:
        fileList.append(l)
    file.close()
    listbox = Listbox(root,width=60,height=10,font=('times',13))
    for f in fileList:
        listbox.insert(END, f)
    listbox.pack()
    listbox.bind('<Double-1>',CurSelet)

#ajouter un boutton de déconnexion
    button = Button(root, text="Quit", command=lambda root=root:quit(root))
    button.pack()



    
    
           


    
    
    root.mainloop()
    