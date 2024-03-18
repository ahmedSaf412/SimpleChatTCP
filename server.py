import threading
import socket

#host address

host= '127.0.0.1'
port = 43282


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

#----handling client connection
def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index= clients.index(client)#get the index in the clients list
            clients.remove(client)#remove the element from list
            client.close()#close the terminal

            nickname=nicknames[index]#now brodcast the incident
            broadcast(f"{nickname} left the chat".encode('ascii'))
            break



def recieve():
    while True:
        #accept clients all the time when it tries to connect
        client,address=server.accept()
        print(f"connected with {str(address)}")

        #send the nickname
        client.send("NICK".encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        nicknames.append(nickname)#modify list of nicknames
        clients.append(client)

        print(f"Nickname of the client {nickname}!")
        broadcast(f"{nickname} hopped the the chat".encode('ascii'))
        client.send("connected to the server!".encode('ascii'))
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()


print("server is on")
recieve()