from math import sqrt
from collections import deque
import pygame
pygame.font.init()



WIDTH = 1600
HEIGHT = 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Soccer Game")

BG = pygame.transform.scale(pygame.image.load("Background.png"), (WIDTH, HEIGHT))

PLAYER_RADIUS = 30
PLAYER_VEL = 4
BALL_RADIUS = 25

FONT = pygame.font.SysFont("comicsans", 30)
CHAT_FONT = pygame.font.SysFont("comicsans", 15)
CHAT_HEIGHT = 200
CHAT_WIDTH = 300
CHAT_POSX = WIDTH - CHAT_WIDTH + 40
CHAT_POSY = HEIGHT - CHAT_HEIGHT + 20
chat_box = pygame.Rect(WIDTH-CHAT_WIDTH, HEIGHT-CHAT_HEIGHT, CHAT_WIDTH, CHAT_HEIGHT)

queue = deque()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
    def reset(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.velx = 0
        self.vely = 0

   
def collide(player, ball):
    if (sqrt(((player.x - ball.x)**2) + ((player.y - ball.y) ** 2)) <= (PLAYER_RADIUS + BALL_RADIUS)):
        ball.velx = (ball.x - player.x)
        ball.vely = (ball.y - player.y)

def wallCollision(ball):
    if(ball.x + ball.velx > 1500 - BALL_RADIUS or ball.x + ball.velx < 78 + BALL_RADIUS ):
        ball.velx *= -1
        if(ball.y > 430 and ball.y < 530):
            ball.reset()
    if(ball.y + ball.vely > 935 - BALL_RADIUS or ball.x + ball.velx < 17 + BALL_RADIUS):
        ball.vely *= -1
   

def draw(player, ball, chat):
    WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, "red", chat_box)
    for i in range(0, 3):
        text = CHAT_FONT.render(chat[i], 1, "white")
        WIN.blit(text, (CHAT_POSX, CHAT_POSY + 40 * i))
    pygame.draw.circle(WIN, "black" , (player.x, player.y), PLAYER_RADIUS)
    pygame.draw.circle(WIN, "gray" , (ball.x, ball.y), BALL_RADIUS)

    pygame.display.update()


def main():
    run = True
    
    player = Player(HEIGHT/2, WIDTH/2)
    ball = Ball(WIDTH/2, HEIGHT/2)
    clock = pygame.time.Clock()

    
    queue.append("TEST 1")
    queue.append("TEST 2")
    queue.append("TEST 3")
    while run:
        clock.tick(60)
        ball.velx *= 0.85
        ball.vely *= 0.85

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_RADIUS -  PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if(keys[pygame.K_RIGHT]) and player.x + PLAYER_RADIUS + PLAYER_VEL <= WIDTH:
            player.x += PLAYER_VEL
        if(keys[pygame.K_UP]) and player.y - PLAYER_RADIUS - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if(keys[pygame.K_DOWN]) and player.y + PLAYER_RADIUS + PLAYER_VEL <= HEIGHT:
            player.y += PLAYER_VEL

        collide(player, ball)
        wallCollision(ball)
        ball.x += ball.velx
        ball.y += ball.vely


        # l = [str(player.x), str(player.y)]
        # print(l[0] + " " + l[1])
        draw(player, ball, queue)
    

    
    pygame.quit()


if __name__ == "__main__":
    main()