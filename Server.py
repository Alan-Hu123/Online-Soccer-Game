import socket
from _thread import *
import pickle
import threading
import time
import random
import math
import pygame
pygame.init()
clock = pygame.time.Clock()
SERVER_IP = socket.gethostbyname(socket.gethostname())

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 5050

WIDTH = 1600
HEIGHT = 960

PLAYER_RADIUS = 35
PLAYER_VEL = 5
BALL_RADIUS = 25

DISCONNECT = "!Disconnect"

class Player:
    def __init__(self, x):
        if(x % 2 == 0):
            self.x = WIDTH/4
            self.y = HEIGHT/2
        else:
            self.x = WIDTH*0.75
            self.y = HEIGHT/2
class Ball:
    def __init__(self, x, y):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.velx = 0
        self.vely = 0

def collide(player, ball):
    if (math.sqrt(((player.x - ball.x)**2) + ((player.y - ball.y) ** 2)) <= (PLAYER_RADIUS + BALL_RADIUS)):
        ball.velx = (ball.x - player.x)
        ball.vely = (ball.y - player.y)

def wallCollision(ball):
    if(ball.x + ball.velx > 1500 - BALL_RADIUS or ball.x + ball.velx < 78 + BALL_RADIUS ):
        if(ball.y > 430 and ball.y < 530):
            ball.reset()
        ball.velx *= -1
    if(ball.y + ball.vely > 935 - BALL_RADIUS or ball.y + ball.vely < 17 + BALL_RADIUS):
        ball.vely *= -1
    
    ball.x += ball.velx
    ball.y += ball.vely
    ball.velx *= 0.8
    ball.vely *= 0.8

   
def move(player, input):
    if(input[0] == "1") and player.x - PLAYER_RADIUS -  PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL
    if(input[1] == "1") and player.x + PLAYER_RADIUS +  PLAYER_VEL <= WIDTH:
        player.x += PLAYER_VEL
    if(input[2] == "1") and player.y - PLAYER_RADIUS - PLAYER_VEL >= 0:
        player.y -= PLAYER_VEL
    if(input[3] == "1") and player.y + PLAYER_RADIUS + PLAYER_VEL <= HEIGHT:
        player.y += PLAYER_VEL


try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print(f"{SERVER_IP} Could not Start")
    quit()

S.listen()

print("SERVER STARTED")


def moveBall(ball):
    global ball_pos
    while True:
        wallCollision(ball)
        ball_pos = [ball.x, ball.y]
        clock.tick(60)
        

def handle_client(conn, id):
    global connections, players, ball_pos
    current_id = id
    print(current_id, " Connected")

    players[current_id] = Player(current_id)
    connected = True
    while connected:
        try: 
            data =  conn.recv(20)
            if not data:
                connected = False
                print("false")
            data = data.decode("utf-8")
            # print(data)
            players[current_id]
        except Exception as e:
            print(e)
            break
        if len(data) != 0:
            move(players[current_id], data)
        collide(players[current_id], ball)
        
        send_data = pickle.dumps((players, ball_pos))
        conn.send(send_data)
             

    print("Disconnect")
    connections -= 1
    print("closed")
    del players[current_id]
    conn.close()

    



print("Setting Up Level")
print("waiting for connetions")
print((SERVER_IP, PORT))

players = {}
ball = Ball(WIDTH/2, HEIGHT/2)
ball_pos = []
connections = 0
_id = 0

start_new_thread(moveBall, (ball, ))
while True:
    host, addr = S.accept()
    print("[Connection] Connected to : ", addr)

    connections += 1
    start_new_thread(handle_client, (host, _id))
    _id += 1

print("Server offline")