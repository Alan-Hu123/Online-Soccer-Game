from math import sqrt
import pygame
pygame.font.init()



WIDTH = 1600
HEIGHT = 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Soccer Game")

BG = pygame.transform.scale(pygame.image.load("CjJCu.png"), (WIDTH, HEIGHT))

PLAYER_RADIUS = 35
PLAYER_VEL = 5
BALL_RADIUS = 25

FONT = pygame.font.SysFont("comicsans", 30)

ball = [0, 0]
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

        
def collide(player, ball):
    if (sqrt(((player.x - ball.x)**2) + ((player.y - ball.y) ** 2)) <= (PLAYER_RADIUS + BALL_RADIUS)):
        ball.velx = (ball.x - player.x)
        ball.vely = (ball.y - player.y)

def wallCollision(ball):
    if(ball.x + ball.velx > 1500 - BALL_RADIUS or ball.x + ball.velx < 78 + BALL_RADIUS ):
        ball.velx *= -1
    if(ball.y + ball.vely > 935 - BALL_RADIUS or ball.x + ball.velx < 17 + BALL_RADIUS):
        ball.vely *= -1
   

def draw(player, ball):
    WIN.blit(BG, (0, 0))


    pygame.draw.circle(WIN, "black" , (player.x, player.y), PLAYER_RADIUS)
    pygame.draw.circle(WIN, "gray" , (ball.x, ball.y), BALL_RADIUS)
    pygame.display.update()


def main():
    run = True
    
    player = Player(HEIGHT/2, WIDTH/2)
    ball = Ball(WIDTH/2, HEIGHT/2)
    clock = pygame.time.Clock()

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

        draw(player, ball)
    

    
    pygame.quit()


if __name__ == "__main__":
    main()