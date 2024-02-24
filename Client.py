
    
import pygame
import pygame_gui
import sys
import socket
import pickle

pygame.init()
pygame.font.init()

## GAME CONSTANTS
WIDTH, HEIGHT = 1600, 960
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_RADIUS = 35
PLAYER_VEL = 5
BALL_RADIUS = 25
pygame.display.set_caption("Soccer Game")

BG = pygame.transform.scale(pygame.image.load("CjJCu.png"), (WIDTH, HEIGHT))

clock = pygame.time.Clock()

name = ""


## CONNECTION

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

ball = [WIDTH/2, HEIGHT/2]
players = {}

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



def draw(players, ball):
    SCREEN.blit(BG, (0, 0))
    for player in players:
        pygame.draw.circle(SCREEN, "black", (players[player].x, players[player].y), PLAYER_RADIUS)
    pygame.draw.circle(SCREEN, "grey", (ball[0], ball[1]), BALL_RADIUS)
    pygame.display.update()



def connect(msg):
    print("CONNECTING")
    print(ADDR)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("CONNECTED")


    run = True
    

    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Keys
        keys = pygame.key.get_pressed()
        data = ""
        if keys[pygame.K_LEFT]:
            data += "1"
        else:
            data += "0"
        if(keys[pygame.K_RIGHT]):
            data += "1"
        else:
            data += "0"
        if(keys[pygame.K_UP]):
            data += "1"
        else:
            data += "0"
        if(keys[pygame.K_DOWN]):
            data += "1"
        else:
            data += "0"

        # Send Data
        try:
            client.send(data.encode(FORMAT))
        except socket.error as e:
            print(e)
        print(data)
        

        #Get Game Data
         
        players, ball = pickle.loads(client.recv(2048))
        draw(players, ball)
        clock.tick(60)

    

connect("hi")

