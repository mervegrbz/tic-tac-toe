import socket 
import _thread
from threading import Thread
import sys
import select
import random
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1",1234))
server.listen(2)        
count=0
connections=[]
linenum= input("how many line: ")

def threaded(client,player):
    global count
    while True:
        if(count==2):
            break
        
    client.send(str(player).encode('utf-8'))
    client.send(str(linenum).encode('utf-8'))
    while True:
        try:
            
            message=client.recv(1024) 
            broadcast(client,message)
            

            
            
        
        except Exception as e:
            print(e)
            break
            
def broadcast(client,message):
    for connection in connections:
        if(connection!=client):
            connection.send(message)
           

def remove(connection):
    if(connection in connections):
        connections.remove(connection)
        


while True:

    client,address=server.accept()
    connections.append(client)
    count+=1
    
    if(count%2==1):
        print("new game")
    else:
        print("okay")
        

    print("Connected"+str(address[0]) + str(address[1]))

    Thread(target=threaded,args=(client,count)).start()
    
