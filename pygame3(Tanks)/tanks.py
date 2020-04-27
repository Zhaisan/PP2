
import pygame
from enum import Enum
import sys
# pylint: disable=no-member
pygame.init()

screen = pygame.display.set_mode((821, 550))
pygame.display.set_caption('War of Tanks')

groundImage = pygame.image.load('ground.jpg') 
image_winner1 = pygame.image.load('TANK1.png')
image_winner2 = pygame.image.load('TANK2.png')
fon = pygame.mixer.Sound('background.wav')
shoot1 = pygame.mixer.Sound('shotoftank.wav')
shoot2 = pygame.mixer.Sound('shotoftank.wav')
collision1 = pygame.mixer.Sound('collision.wav')
collision2 = pygame.mixer.Sound('collision.wav')

font = pygame.font.SysFont('book antiqua', 25)

change1 = True
change2 = True
isGameOver1 = False
isGameOver2 = False
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Bullets:

    def __init__(self, x, y, speedx, speedy):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.shot = False

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y),8)

    def move(self):

        if self.shot == True:
            self.x += self.speedx
            self.y += self.speedy

        self.draw()


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tank:

    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = x 
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (
            self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)


    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

#infinite field
        if (self.x < 0):
            self.x = 821
        if (self.x > 821):
            self.x = 0
        if (self.y < 0):
            self.y = 550
        if (self.y > 550):
            self.y = 0
        
        self.draw()

def GameOver1():
    screen.blit(image_winner1, (0, 0))

def GameOver2():
    screen.blit(image_winner2, (0, 0))

score1 = 3
score2 = 3


mainloop = True
tank1 = Tank(300, 300, 1, (220, 20, 60))
tank2 = Tank(100, 100, 1, (0, 255, 127), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

tanks = [tank1, tank2]
bullet1 = Bullets(831, 560, 0, 0)
bullet2 = Bullets(831, 560, 0, 0)

FPS = 100 
clock = pygame.time.Clock ()
fon.play(-1)

while mainloop:
    mill = clock.tick(FPS)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])

            if event.key == pygame.K_RETURN and bullet1.shot == False:
                
                shoot1.play()
                bullet1.shot = True
                if tank1.direction == Direction.LEFT:
                    bullet1.x = tank1.x - 20
                    bullet1.y = tank1.y + 20
                    bullet1.speedx = -10
                    bullet1.speedy = 0
                if tank1.direction == Direction.RIGHT:
                    bullet1.x = tank1.x + 60
                    bullet1.y = tank1.y + 20
                    bullet1.speedx = 10
                    bullet1.speedy = 0
                if tank1.direction == Direction.UP:
                    bullet1.x = tank1.x + 20
                    bullet1.y = tank1.y - 20
                    bullet1.speedx = 0
                    bullet1.speedy = -10
                if tank1.direction == Direction.DOWN:
                    bullet1.x = tank1.x + 20
                    bullet1.y = tank1.y + 60
                    bullet1.speedx = 0
                    bullet1.speedy = 10

            if event.key == pygame.K_SPACE and bullet2.shot == False:
                
                shoot2.play()
                bullet2.shot = True
                bullet2.x = tank2.x
                bullet2.y = tank2.y
                if tank2.direction == Direction.LEFT:
                    bullet2.x = tank2.x - 20
                    bullet2.y = tank2.y + 20
                    bullet2.speedx = -10
                    bullet2.speedy = 0
                if tank2.direction == Direction.RIGHT:
                    bullet2.x = tank2.x + 60
                    bullet2.y = tank2.y + 20
                    bullet2.speedx = 10
                    bullet2.speedy = 0
                if tank2.direction == Direction.UP:
                    bullet2.x = tank2.x + 20
                    bullet2.y = tank2.y - 20
                    bullet2.speedx = 0
                    bullet2.speedy = -10
                if tank2.direction == Direction.DOWN:
                    bullet2.x = tank2.x + 20
                    bullet2.y = tank2.y + 60
                    bullet2.speedx = 0
                    bullet2.speedy = 10
    if bullet1.x < -5 or bullet1.x > 821 or bullet1.y < -5 or bullet1.y > 550:
        bullet1.shot = False
    if bullet2.x < -5 or bullet2.x > 821 or bullet2.y < -5 or bullet2.y > 550:
        bullet2.shot = False

#collision
    if bullet1.x in range(tank2.x, tank2.x + 40) and bullet1.y in range(tank2.y, tank2.y + 40):
        collision1.play()
        bullet1.shot = False
        bullet1.x = 810
        bullet1.y = 610
        score1 -= 1
        change1 = True
    

    if bullet2.x in range(tank1.x, tank1.x + 40) and bullet2.y in range(tank1.y, tank1.y + 40):
        collision2.play()
        bullet2.shot = False
        bullet2.x = 810
        bullet2.y = 610
        score2 -=1 
        change2 = True

    if change1 == True:
        score_1 = font.render("Player1: " + str(score1), True, (0, 0, 0))
        change1 = False
    
    if change2 == True:
        score_2 = font.render("Player2: " + str(score2), True, (0, 0, 0))
        change2 = False
        

    screen.fill((128, 128, 128))
    screen.blit(groundImage, (0,0))
    screen.blit(score_1, (350, 10))
    screen.blit(score_2, (350, 30))
    tank1.move()
    tank2.move()
    bullet1.move()
    bullet2.move()
    
    #PLAY AGAIN

    if score1 == 0 : 
        isGameOver1 = True
        shot = True
    
    if isGameOver1 == True:
        GameOver2()
        fon.stop()

        if event.key == pygame.K_LSHIFT:
            isGameOver1 = False
            score1 = 3
            score2 = 3
            shot = True
            mainloop = True
            
            change1 = True
            score_1 = font.render("Player1: " + str(score1), True, (0, 0, 0))
            score_2 = font.render("Player2: " + str(score2), True, (0, 0, 0))
            fon.play()
            
            tank1 = Tank(300, 300, 1, (220, 20, 60))
            tank2 = Tank(100, 100, 1, (0, 255, 127), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

            tanks = [tank1, tank2]
            bullet1 = Bullets(831, 560, 0, 0)
            bullet2 = Bullets(831, 560, 0, 0)
        
    if score2 == 0 :
        isGameOver2 = True
        shot = True
    
    if isGameOver2 == True:
        GameOver1()
        fon.stop()
    
        if event.key == pygame.K_LSHIFT:
            isGameOver2 = False
            score2 = 3
            score1 = 3
            shot = True
            mainloop = True
            
            change2 = True
            score_1 = font.render("Player1: " + str(score1), True, (0, 0, 0))
            score_2 = font.render("Player2: " + str(score2), True, (0, 0, 0))
            fon.play()
            tank1 = Tank(300, 300, 1, (220, 20, 60))
            tank2 = Tank(100, 100, 1, (0, 255, 127), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

            tanks = [tank1, tank2]
            bullet1 = Bullets(831, 560, 0, 0)
            bullet2 = Bullets(831, 560, 0, 0)

    pygame.display.flip()

    
pygame.quit()