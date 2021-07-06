import socket
from tkinter import *
import os



filename = ""
BUFFER_SIZE = 4096
    
    

def CurSelet(evt):
    global filename
    
    filename = str(listbox.get(listbox.curselection()))
    value = filename.encode()
    Host = "127.0.0.1"
    Port = 5000
    s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host, Port))
    s.send(value)
    
    with open(os.path.join("Client",filename.replace("\n", "")), "wb") as f:
        while True:
           
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:    
                
                break
            
            f.write(bytes_read)
            
            f.close()
            
    s.close()


if __name__ == "__main__":
    
    



    root = Tk()
    root.title("Client")
    sizex = 600
    sizey = 400
    posx  = 40
    posy  = 20
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    label = Label(root, text = "Liste des fichiers")

    label.pack() 



    fileList = []
    file = open("files.txt", "r")
    lines = file.readlines()
    for l in lines:
        fileList.append(l)
    file.close()
    listbox = Listbox(root,width=60,height=60,font=('times',13))
    for f in fileList:
        listbox.insert(END, f)
    listbox.pack()
    listbox.bind('<Double-1>',CurSelet)



    
    
           


    
    
    root.mainloop()
    