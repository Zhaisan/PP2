# pylint: disable=no-member
import pygame 
import random 
import sys
pygame.init() 

#size of window
screen = pygame.display.set_mode((600,600))    

#surface of points
point_surface = pygame.Surface((150,30))     

#font of points
point_font = pygame.font.SysFont("book antiqua", 30)    

#color of font
BLACK = (0, 0, 0)
#color of surface
ORANGE = (255, 150, 100)

isGameOver = False

#loading images
pulyaImage = pygame.image.load("dssd.png")
backgroundImage = pygame.image.load("background.jpg")     
playerImage = pygame.image.load("player.png")
game_overImage = pygame.image.load("gameover5.jpg")

#player
player_x = 200
player_y = 500

#pulya
pulya_x1 = player_x+18
pulya_y1 = player_y-59

#button press
pressed = pygame.key.get_pressed()
border = False

enemyImage = pygame.image.load("enemy.png")

#enemy
enemy_x = random.randint(0, 600)
enemy_y = random.randint(20, 40)
enemy_dx = 3
enemy_dy = 70

#functions
def player(x, y):
    screen.blit(playerImage,(x,y))

def enemy(x, y):
    screen.blit(enemyImage, (x, y))

def pulya(x1, y1):
    screen.blit(pulyaImage, (pulya_x1,pulya_y1))

def GameOver():     
    screen.blit(game_overImage, (0,0))      

points = 0
k = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quit() 
            
#collison of pulya and enemy    
    if (pulya_x1 >= enemy_x and pulya_x1 <= enemy_x + 60 ) and (pulya_y1 <= enemy_y + 60) :
        enemy_x = random.randint(0, 600)
        enemy_y = random.randint(20, 50)
        pulya_x1 = player_x+18
        pulya_y1 = player_y-59
        points += 10
#giving color to the surface   
    point_surface.fill((ORANGE))
#printing scores to the surface
    point_surface.blit(point_font.render("POINTS:"+str(points), 1, (BLACK)), (0,0))    

#the initial position of the bullet when it reaches the border
    if pulya_y1 <= 0:
        pulya_x1 = player_x+18
        pulya_y1 = player_y-59
        border = False
        screen.fill((BLACK))

    if pressed[pygame.K_SPACE]:
        border = True
    
    if border == True:
        pulya_y1 -=5
#player's move
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]: player_x -= 3
    if pressed[pygame.K_RIGHT]: player_x += 3
    if pressed[pygame.K_UP]: player_y -= 3
    if pressed[pygame.K_DOWN]: player_y += 3
    if pressed[pygame.K_UP]: pulya_y1 -= 3
    if pressed[pygame.K_DOWN]: pulya_y1 += 3
    if pressed[pygame.K_LEFT]: pulya_x1 -= 3
    if pressed[pygame.K_RIGHT]: pulya_x1 += 3
#enemy's move
    enemy_x +=enemy_dx
    if enemy_x < 0 or enemy_x > 536:
        enemy_dx = -enemy_dx
        enemy_y += enemy_dy
#coordinates of collision of enemy and player
    collision_x = enemy_x - player_x      
    collision_y = enemy_y - player_y
    if -50 <= collision_x <= 50 and -50 <= collision_y <= 50:      
        isGameOver = True

#GAMEOVER 
    if isGameOver:       
        GameOver()   
        if pressed[pygame.K_LSHIFT]:     
            isGameOver = False       
            enemy_x, enemy_y = random.randint(0, 600), random.randint(20, 40)     
            player_x, player_y = 200, 500 
            points = 0     
        
    
    if not isGameOver: 
        screen.blit(backgroundImage, (0,0))
        player(player_x,player_y)
        enemy(enemy_x,enemy_y)
        pulya(pulya_x1, pulya_y1)
        screen.blit(point_surface,(228,0))

    pygame.display.flip()