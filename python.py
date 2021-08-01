from turtle import*
import socket
import select
import _thread
from threading import Thread
import os
conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('127.0.0.1',1234))
count=int(conn.recv(1024).decode('utf-8'))
position=[]
print(count)
lineNumber=int(conn.recv(1024).decode('utf-8'))

line=lineNumber
rangel=80
board =  [["" for x in range(line)] for y in range(line)]
screen=Screen()
width=rangel*line
height=rangel*line
screen.setup(width+20,height+130)
ScoreO=0
ScoreX=0
pen=Turtle()
pen.pencolor("red")
pen.speed(1000)
pen.penup()
pen.pensize(5)
screen.bgcolor("black")
for i in range (line+1):
    pen.penup()
    pen.goto(-width/2+i*rangel,height/2)
    pen.pendown()
    pen.goto(-width/2+i*rangel,-height/2)
    
for i in range (line+1):
    pen.penup()
    pen.goto(-width/2,height/2-i*rangel)
    pen.pendown()
    pen.goto(width/2,height/2-i*rangel)

kalem=Turtle()
kalem.pencolor("white")
kalem.pensize(5)
kalem.hideturtle()
kalem.speed(10)

def circle(x,y):
    kalem.pencolor("white")
    kalem.pensize(5)
    kalem.hideturtle()
    kalem.speed(10)

    kalem.penup()
    kalem.setheading(0)
    kalem.goto(x+rangel/2,y-rangel+5)
    kalem.pendown()
    kalem.circle((rangel-10)/2)

def cross(x,y):
    kalem.penup()
    kalem.pencolor("white")
    kalem.pensize(5)
    kalem.hideturtle()
    kalem.speed(10)
    
    kalem.goto(x+5,y-5)
    kalem.pendown()
    kalem.setheading(-45)
    kalem.forward(rangel*(2**0.5)-15)
    kalem.penup()
    kalem.goto(x+5,y-rangel+5)
    kalem.setheading(45)
    kalem.down()
    kalem.forward(rangel*(2**0.5)-15)
isX=True if count==1 else False
def round (x,y):

    print('heyy')
    global isX,ScoreX,ScoreO,count,gamecount
    column=int((x+width/2)//rangel)
    row=int((-y+height/2)//rangel)
   
    x=rangel*column-width/2
    y=-rangel*row+height/2

    if count==1 and isX:  
        if board[row][column]!="":
            return
       
        print("here")
        conn.send((str(x)+","+str(y)).encode('utf-8'))
        circle(x, y)
        board[row][column]="O"
        isX=False
        isOver("O")  
    
    if count==2 and not isX:
        if board[row][column]!="":
            return
        
        conn.send((str(x)+","+str(y)).encode('utf-8'))
        cross(x, y)
        board[row][column]="X"
        isX=True
        isOver("X")

        
        
   
   
pencil=Turtle()
def winner(player):
    global board,isX
    pencil.clear()
    pencil.penup()
    pencil.goto(0,height/2+20)
    pencil.pendown()
    pencil.color("green")
    
    pencil.write("X: "+str(ScoreX)+" "+"       O: "+str(ScoreO),align="center",font=["Comic Sans MS",20,])
    kalem.clear()
    isX=True
    board=  [["" for x in range(line)] for y in range(line)]
    
def  isOver(player):
    global ScoreX,ScoreO,isX,board
    if board.__str__().count("")==0:
        kalem.clear()
        isX=True
        board=  [["" for x in range(line)] for y in range(line)]
    if  not (checkcol() or checkver() or checkdia() or checkdia2()): return False
    if player is"X":
        ScoreX+=1
    else:
        ScoreO+=1
    winner(player)
    print(f"{player} wins!")
    return True
  
def receive():
    global position
    while True:
        position=conn.recv(1024).decode('utf-8').split(",")
        position=[int(float(x)) for x in position]
        print(receive)

def checkcol():
    isTrue=True 
    for i in range (line):
        isTrue=True

        for j in range (line-1):

            if board[i][j]=="":
                isTrue= False
                break
            if board[i][j+1]!=board[i][j]:
                isTrue= False
                break
        if isTrue:
            return True
    return isTrue
def checkver():
    isTrue=True 
    for i in range (line):
        isTrue=True
        for j in range (line-1): 
           
            if board[j][i]=="":
                isTrue= False
                break

            if board[j+1][i]!=board[j][i]:
                isTrue= False
                break
        if isTrue:
            return isTrue
        
        
    return isTrue

def checkdia():
    for i in range (line-1): 
       
        if board[i][i]=="":
            return False
        if board[i+1][i+1]!=board[i][i]:
            return False
    return True

def checkdia2():
    for i in range (line-1):
        
       
        if board[line-i-1][i]=="":
            return False
        if board[line-i-2][i+1]!=board[line-i-1][i]:
            return False
    return True

receive_thread=Thread(target=receive)
receive_thread.setDaemon(True)
receive_thread.start()

         
screen.onscreenclick(round)
screen.listen()
while True:
    if len(position)!=0:
        if count==2:
            circle(position[0],position[1])
            board[int((-position[1]+height/2)/rangel)][int((position[0]+width/2)/rangel)]="O"
            isOver("O")
            position=[]
            isX=False

        if count==1:
            cross(position[0],position[1])
            board[int((-position[1]+height/2)/rangel)][int((position[0]+width/2)/rangel)]="X"
            position=[]
            isOver("X")
            isX=True
    
    screen.update()
    
   
    
    





