import pygame
from enum import Enum
import sys
# pylint: disable=no-member
import math
import pika
import uuid
import json
import time
import random
from threading import Thread


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tanks GAME')

#Uploading everything we have

groundImage = pygame.image.load('ground.png') 
fon = pygame.mixer.Sound('background.wav')
shoot1 = pygame.mixer.Sound('shoot.wav')
shoot2 = pygame.mixer.Sound('shoot.wav')
collision1 = pygame.mixer.Sound('collision.wav')
collision2 = pygame.mixer.Sound('collision.wav')
menu_pic = pygame.image.load('var1.png')
star_pic = pygame.image.load('star.png')
tank1_win = pygame.image.load('tank1win.png')
tank2_win = pygame.image.load('tank2win.png')
font_s = pygame.font.SysFont('Berlin Sans FB', 25)

class TankRpcClient:

    def __init__(self):
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='34.254.177.17',           #we create established connection                               
                port=5672,
                virtual_host='dar-tanks',
                credentials=pika.PlainCredentials(
                    username='dar-tanks',
                    password='5orPLExUYnyVYZg48caMpX'
                )
            )
        )
        self.channel = self.connection.channel()       # creating channel              
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)  #creating anonimous queue
        self.callback_queue = queue.method.queue       #queue where we get response           
        self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)   #we bind the queue to the exchange
        self.channel.basic_consume(queue=self.callback_queue,
                                on_message_callback=self.on_response,    #Data from server comes here
                                auto_ack=True)    #Data must be notified.
        
        self.response= None    
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            #print(self.response)

    def call(self, key, message={}):      #function will send our requests to the server
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)   #changing to json format
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self):    #To find out server status
        self.call('tank.request.healthcheck')
        return self.response['status']== '200'    # if the server is active then it will return 200

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turning_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def firing_bullet(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='34.254.177.17',                                                
                port=5672,
                virtual_host='dar-tanks',
                credentials=pika.PlainCredentials(
                    username='dar-tanks',
                    password='5orPLExUYnyVYZg48caMpX'
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',queue=event_listener,routing_key='event.state.'+room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        #print(self.response)

    def run(self):
        self.channel.start_consuming()

############################     Single Mode     ###############################

def Single():


    correct1 = True
    correct2 = True
    BRICK = (139, 69, 19)


    class Bullets:

        def __init__(self, x, y, sx, sy):
            self.x = x
            self.y = y
            self.sx = sx
            self.sy = sy
            self.shot = False
        
        def draw(self):
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y),8)

        def go(self):

            if self.shot == True:
                self.x += self.sx
                self.y += self.sy

            self.draw()

    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    #Creating Bricks

    class Brick:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            
        
        def draw(self):
            pygame.draw.rect(screen, BRICK, (self.x, self.y, self.width, self. height))
            


    class Tank:

        def __init__(self, x, y, s, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
            self.x = x 
            self.y = y
            self.s = s
            self.color = color
            self.width = 40
            self.direction = Direction.RIGHT

            self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                        d_up: Direction.UP, d_down: Direction.DOWN}

        def draw(self):
            center = (self.x + int(self.width / 2), self.y + int(self.width / 2))
            pygame.draw.rect(screen, self.color,
                            (self.x, self.y, self.width, self.width), 2)
            pygame.draw.circle(screen, self.color, center, int(self.width / 2))

            if self.direction == Direction.RIGHT:
                pygame.draw.line(screen, self.color, center, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

            if self.direction == Direction.LEFT:
                pygame.draw.line(screen, self.color, center, (
                self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)

            if self.direction == Direction.UP:
                pygame.draw.line(screen, self.color, center, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)

            if self.direction == Direction.DOWN:
                pygame.draw.line(screen, self.color, center, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)
        

        def change_direction(self, direction):
            self.direction = direction

        def go(self):
            if self.direction == Direction.LEFT:
                self.x -= self.s
            if self.direction == Direction.RIGHT:
                self.x += self.s
            if self.direction == Direction.UP:
                self.y -= self.s
            if self.direction == Direction.DOWN:
                self.y += self.s

    #infinite field

            if (self.x < 0): self.x = 800
                
            if (self.x > 800): self.x = 0
                
            if (self.y < 0): self.y = 600
                
            if (self.y > 600): self.y = 0
                
            
            self.draw()

    singleloop = True

    surprise = random.randint(3,12)

    x = random.randint(5,700)
    y = random.randint(5,570)

    def Star(x, y):
        
        screen.blit(star_pic, (x, y))

    def Tank1win():
        
        screen.blit(tank1_win, (0, 0))

    def Tank2win():

        screen.blit(tank2_win, (0, 0))

    score1 = 3
    score2 = 3

    tank1 = Tank(300, 300, 1, (220, 20, 60))
    tank2 = Tank(100, 100, 1, (0, 255, 127), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

    tanks = [tank1, tank2]
    bull1 = Bullets(810, 610, 0, 0)
    bull2 = Bullets(810, 610, 0, 0)
    bull3 = Bullets(810, 610, 0, 0)
    bull4 = Bullets(810, 610, 0, 0)
    bull5 = Bullets(810, 610, 0, 0)
    bull6 = Bullets(810, 610, 0, 0)
    bull7 = Bullets(810, 610, 0, 0)

    b1 = Brick(400, 400, 20, 50)
    b2 = Brick(422, 430, 50, 20)
    b3 = Brick(550, 175, 50, 20)
    b4 = Brick(650, 450, 50, 20)
    b5 = Brick(702, 450, 50, 20)
    b6 = Brick(200, 420, 20, 50)
    b7 = Brick(200, 368, 20, 50)
    b8 = Brick(200, 472, 20, 50)

    brick = [b1,b2,b3,b4,b5,b6,b7,b8]

    start_ticks=pygame.time.get_ticks()
    k = 0
    FPS = 50
    clock = pygame.time.Clock ()
    fon.play(-1)
    #Menu()
    while singleloop:
        mill = clock.tick(FPS)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                singleloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    singleloop = False
                
                for tank in tanks:
                    if event.key in tank.KEY.keys():
                        tank.change_direction(tank.KEY[event.key])

                if event.key == pygame.K_RETURN and bull1.shot == False:
                    
                    shoot1.play()
                    bull1.shot = True
                    if tank1.direction == Direction.LEFT:
                        bull1.x = tank1.x - 20
                        bull1.y = tank1.y + 20
                        bull1.sx = -10
                        bull1.sy = 0
                    if tank1.direction == Direction.RIGHT:
                        bull1.x = tank1.x + 60
                        bull1.y = tank1.y + 20
                        bull1.sx = 10
                        bull1.sy = 0
                    if tank1.direction == Direction.UP:
                        bull1.x = tank1.x + 20
                        bull1.y = tank1.y - 20
                        bull1.sx = 0
                        bull1.sy = -10
                    if tank1.direction == Direction.DOWN:
                        bull1.x = tank1.x + 20
                        bull1.y = tank1.y + 60
                        bull1.sx = 0
                        bull1.sy = 10

                if event.key == pygame.K_SPACE and bull2.shot == False:
                    
                    shoot2.play()
                    bull2.shot = True
                    bull2.x = tank2.x
                    bull2.y = tank2.y
                    if tank2.direction == Direction.LEFT:
                        bull2.x = tank2.x - 20
                        bull2.y = tank2.y + 20
                        bull2.sx = -10
                        bull2.sy = 0
                    if tank2.direction == Direction.RIGHT:
                        bull2.x = tank2.x + 60
                        bull2.y = tank2.y + 20
                        bull2.sx = 10
                        bull2.sy = 0
                    if tank2.direction == Direction.UP:
                        bull2.x = tank2.x + 20
                        bull2.y = tank2.y - 20
                        bull2.sx = 0
                        bull2.sy = -10
                    if tank2.direction == Direction.DOWN:
                        bull2.x = tank2.x + 20
                        bull2.y = tank2.y + 60
                        bull2.sx = 0
                        bull2.sy = 10

        
        if bull1.x < -5 or bull1.x > 800 or bull1.y < -5 or bull1.y > 600:
            bull1.shot = False
        if bull2.x < -5 or bull2.x > 800 or bull2.y < -5 or bull2.y > 600:
            bull2.shot = False
    
    #collision

        if bull1.x in range(tank2.x, tank2.x + 40) and bull1.y in range(tank2.y, tank2.y + 40):
            collision1.play()
            bull1.shot = False
            bull1.x = 810
            bull1.y = 610
            score1 -= 1
            correct1 = True
        
        if bull2.x in range(tank1.x, tank1.x + 40) and bull2.y in range(tank1.y, tank1.y + 40):
            collision2.play()
            bull2.shot = False
            bull2.x = 1100
            bull2.y = 860
            score2 -= 1 
            correct2 = True

        
        if bull1.x in range(b1.x , b1.x + 20) and bull1.y in range(b1.y, b1.y+50):
            collision1.play()
            bull1.shot = False
            b1.x = 1050
            b1.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b2.x , b2.x + 50) and bull1.y in range(b2.y, b2.y+20):
            collision1.play()
            bull1.shot = False
            b2.x = 1050
            b2.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b3.x , b3.x + 50) and bull1.y in range(b3.y, b3.y+20):
            collision1.play()
            bull1.shot = False
            b3.x = 1050
            b3.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b4.x , b4.x + 50) and bull1.y in range(b4.y, b4.y+20):
            collision1.play()
            bull1.shot = False
            b4.x = 1050
            b4.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b5.x , b5.x + 50) and bull1.y in range(b5.y, b5.y+20):
            collision1.play()
            bull1.shot = False
            b5.x = 1050
            b5.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b6.x , b6.x + 20) and bull1.y in range(b6.y, b6.y+50):
            collision1.play()
            bull1.shot = False
            b6.x = 1050
            b6.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b7.x , b7.x + 20) and bull1.y in range(b7.y, b7.y+50):
            collision1.play()
            bull1.shot = False
            b7.x = 1050
            b7.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull1.x in range(b8.x , b8.x + 20) and bull1.y in range(b8.y, b8.y+50):
            collision1.play()
            bull1.shot = False
            b8.x = 1050
            b8.y = 850
            bull1.x = 990
            bull1.y = 860
        
        if bull2.x in range(b1.x , b1.x + 20) and bull2.y in range(b1.y, b1.y+50):
            collision2.play()
            bull2.shot = False
            b1.x = 1050
            b1.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b2.x , b2.x + 50) and bull2.y in range(b2.y, b2.y+20):
            collision2.play()
            bull2.shot = False
            b2.x = 1050
            b2.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b3.x , b3.x + 50) and bull2.y in range(b3.y, b3.y+20):
            collision2.play()
            bull2.shot = False
            b3.x = 1050
            b3.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b4.x , b4.x + 50) and bull2.y in range(b4.y, b4.y+20):
            collision2.play()
            bull2.shot = False
            b4.x = 1050
            b4.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b5.x , b5.x + 50) and bull2.y in range(b5.y, b5.y+20):
            collision2.play()
            bull2.shot = False
            b5.x = 1050
            b5.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b6.x , b6.x + 20) and bull2.y in range(b6.y, b6.y+50):
            collision2.play()
            bull2.shot = False
            b6.x = 1050
            b6.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b7.x , b7.x + 20) and bull2.y in range(b7.y, b7.y+50):
            collision2.play()
            bull2.shot = False
            b7.x = 1050
            b7.y = 850
            bull2.x = 990
            bull2.y = 860
        
        if bull2.x in range(b8.x , b8.x + 20) and bull2.y in range(b8.y, b8.y+50):
            collision2.play()
            bull2.shot = False
            b8.x = 1050
            b8.y = 850
            bull2.x = 990
            bull2.y = 860

        if tank1.x in range(b1.x, b1.x + 20) and tank1.y in range(b1.y, b1.y + 50):
            collision1.play()
            b1.x = 1050
            b1.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank1.x in range(b2.x, b2.x + 50) and tank1.y in range(b2.y, b2.y + 20):
            collision1.play()
            b2.x = 1050
            b2.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank1.x in range(b3.x, b3.x + 50) and tank1.y in range(b3.y, b3.y + 20):
            collision1.play()
            b3.x = 1050
            b3.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))    
        
        if tank1.x in range(b4.x, b4.x + 50) and tank1.y in range(b4.y, b4.y + 20):
            collision1.play()
            b4.x = 1050
            b4.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank1.x in range(b5.x, b5.x + 50) and tank1.y in range(b5.y, b5.y + 20):
            collision1.play()
            b5.x = 1050
            b5.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank1.x in range(b6.x, b6.x + 20) and tank1.y in range(b6.y, b6.y + 50):
            collision1.play()
            b6.x = 1050
            b6.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank1.x in range(b7.x, b7.x + 20) and tank1.y in range(b7.y, b7.y + 50):
            collision1.play()
            b7.x = 1050
            b7.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank1.x in range(b8.x, b8.x + 20) and tank1.y in range(b8.y, b8.y + 50):
            collision1.play()
            b8.x = 1050
            b8.y = 850
            score1 -= 1
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
        
        if tank2.x in range(b1.x, b1.x + 20) and tank2.y in range(b1.y, b1.y + 50):
            collision2.play()
            b1.x = 1050
            b1.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))

        if tank2.x in range(b2.x, b2.x + 50) and tank2.y in range(b2.y, b2.y + 20):
            collision2.play()
            b2.x = 1050
            b2.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))

        if tank2.x in range(b3.x, b3.x + 50) and tank2.y in range(b3.y, b3.y + 20):
            collision2.play()
            b3.x = 1050
            b3.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))

        if tank2.x in range(b4.x, b4.x + 50) and tank2.y in range(b4.y, b4.y + 20):
            collision2.play()
            b4.x = 1050
            b4.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))

        if tank2.x in range(b5.x, b5.x + 50) and tank2.y in range(b5.y, b5.y + 20):
            collision2.play()
            b5.x = 1050
            b5.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))
        
        if tank2.x in range(b6.x, b6.x + 20) and tank2.y in range(b6.y, b6.y + 50):
            collision2.play()
            b6.x = 1050
            b6.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))
        
        if tank2.x in range(b7.x, b7.x + 20) and tank2.y in range(b7.y, b7.y + 50):
            collision2.play()
            b7.x = 1050
            b7.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))
        
        if tank2.x in range(b8.x, b8.x + 20) and tank2.y in range(b8.y, b8.y + 50):
            collision2.play()
            b8.x = 1050
            b8.y = 850
            score2 -= 1
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))
        
        
        if correct1 == True:
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
            correct1 = False
        
        if correct2 == True:
            score_2 = font_s.render("Tank2: " + str(score2), True, (0, 0, 0))
            correct2 = False

        
        
        screen.fill((128, 128, 128))
        screen.blit(groundImage, (0,0))
        screen.blit(score_1, (345, 18))
        screen.blit(score_2, (345, 38))
        tank1.go()
        tank2.go()
        bull1.go()
        bull2.go()
        for b in brick:
            b.draw()

        #Super Power by eating suprise

        seconds  = (pygame.time.get_ticks()-start_ticks)/1000
        if seconds > surprise:
            Star(x, y)
        start_ticks2 = pygame.time.get_ticks()
        
        col_x = tank1.x - x
        col_y = tank1.y - y
        if -5 <= col_x <= 5 and -5 <= col_y <= 5:
            x = 1010
            y = 810
            FPS = 120
            seconds2 = (pygame.time.get_ticks()-start_ticks2)/1000
            k += seconds2
            if k > 8:
                FPS = 50
        
        col2_x = tank2.x - x
        col2_y = tank2.y - y
        if -5 <= col2_x <= 5 and -5 <= col2_y <= 5:
            x = 1010
            y = 810
            FPS = 120
            
            seconds2 = (pygame.time.get_ticks()-start_ticks2)/1000
            k += seconds2
            if k > 8:
                FPS = 50
        
        if score1 == 0 :
            score_1 = font_s.render("Tank1: " + str(score1), True, (0, 0, 0))
            Tank2win()
            fon.stop()
        
        if score2 == 0 :
            score_2 = font_s.render("Tank2: " + str(score1), True, (0, 0, 0))
            Tank1win()
            fon.stop()
        
        
        pygame.display.flip()

        
#############################                MULTIPLAYER MODE              ###################################
def Multi():
    

    pygame.init()
    screen = pygame.display.set_mode((1000, 600))

    over_pic = pygame.image.load('overmulti.jpg')

    
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    MOVE_KEYS = {
        pygame.K_w: UP,
        pygame.K_a: LEFT,
        pygame.K_s: DOWN,
        pygame.K_d: RIGHT
    }

    iamtank_up = pygame.image.load('sprite1.png')
    iamtank_right = pygame.image.load('sprite1_right.png')
    iamtank_down = pygame.image.load('sprite1_down.png')
    iamtank_left = pygame.image.load('sprite1_left.png')

    enemy_up = pygame.image.load('sprite2.png')
    enemy_right = pygame.image.load('sprite2_right.png')
    enemy_down = pygame.image.load('sprite2_down.png')
    enemy_left = pygame.image.load('sprite2_left.png')


    font3 = pygame.font.SysFont('Arial Black', 18)

    def Over():
            
        screen.blit(over_pic,(0 , 0))
        

    def draw_tanks(x, y, direction, id):
        font = pygame.font.SysFont('Arial Black', 13)
        
        text_id = font.render(id, True, (255, 255, 255))
        screen.blit(text_id,(x-10, y-20))
        if direction == 'UP':
            screen.blit(iamtank_up, (x, y))
        if direction == 'RIGHT':
            screen.blit(iamtank_right, (x, y))
        if direction == 'DOWN':
            screen.blit(iamtank_down, (x, y))
        if direction == 'LEFT':
            screen.blit(iamtank_left, (x, y))
        
    def draw_tanks2(x, y, direction, id):
        font = pygame.font.SysFont('Arial Black', 13)
        text_id2 = font.render(id, True, (255, 255, 255))
        screen.blit(text_id2,(x-10, y-20))
        if direction == 'UP':
            screen.blit(enemy_up, (x, y))
        if direction == 'RIGHT':
            screen.blit(enemy_right, (x, y))
        if direction == 'DOWN':
            screen.blit(enemy_down, (x, y))
        if direction == 'LEFT':
            screen.blit(enemy_left, (x, y))


    def info_table(tank_id, tank_health, tank_score):
        font = pygame.font.SysFont('Arial Black', 13)
        font2 = pygame.font.SysFont('Arial black', 10)
        if tank_id == client.tank_id:
            text_score = font.render('Score:' + str(tank_score), True, (255, 255, 255))
            text_health = font.render('Health:' + str(tank_health), True, (255, 255, 255))
            text_mytank = font.render('MY TANK:', True, (255, 255, 255))
            text_opponents = font.render('OPPONENTS:', True, (255, 255, 255))
            text_oppo_score_health = font2.render('score and health', True, (255,255,255))
            screen.blit(text_score, (860, 65))
            screen.blit(text_health, (860, 85))
            screen.blit(text_mytank, (855, 42))
            screen.blit(text_opponents, (850, 115))
            screen.blit(text_oppo_score_health, (849, 135))

    def info_sort():
        font = pygame.font.SysFont('Arial Black', 12)
        tanks = event_client.response['gameField']['tanks']
        scores = {}
        scores = {tank['id']: [tank['score'],tank['health']] for tank in tanks }
        sorted_scores = reversed(sorted(scores.items(), key=lambda kv: kv[1]))
        i = 151
        for score in sorted_scores:
            if score[0]!=client.tank_id:
                tank_id = font.render(score[0] + ' ' + str(score[1][0]) + '  ' + str(score[1][1]), True, (255, 255, 255))
                screen.blit(tank_id, (854, i))
                i += 22        

    def game_play():
        multiloop = True
        font = pygame.font.SysFont('Arial Black', 12)
        while multiloop:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    multiloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        multiloop = False
                    if event.key in MOVE_KEYS:
                        client.turning_tank(client.token, MOVE_KEYS[event.key])
                    if event.key == pygame.K_SPACE:
                        client.firing_bullet(client.token)

            #tank_id = tank['id']
            
                        
            kicked = event_client.response['kicked']
            winners = event_client.response['winners']
            losers  = event_client.response['losers']
                    
            try:
                remaining_time = event_client.response['remainingTime']
                text_time = font.render("Remaining Time: " + str(remaining_time), True, (220, 20, 60))
                screen.blit(text_time, (840, 10))
                pygame.draw.line(screen, (255,215,0), (825, 0), (825, 600), 3)
                pygame.draw.rect(screen, (255, 255, 255), (850, 39, 80, 23), 2)
                pygame.draw.rect(screen, (255, 255, 255), (843, 111, 108, 25), 2)
                # hits = event_client.response['hits']
                bullets = event_client.response['gameField']['bullets']
                tanks = event_client.response['gameField']['tanks']
                

                for tank in tanks:
                    tank_id = tank['id']
                    tank_score = tank['score']
                    tank_health = tank['health']
                    tank_x = tank['x'] 
                    tank_y = tank['y']
                    tank_direction = tank['direction']
                    if tank_id == client.tank_id: 
                        draw_tanks(tank_x, tank_y, tank_direction, 'Zhaiss')
                    else: 
                        draw_tanks2(tank_x, tank_y, tank_direction, tank_id)
                    info_table(tank_id, tank_health, tank_score)
                    info_sort()
                for bullet in bullets:
                    bullet_x = bullet['x']
                    bullet_y = bullet['y']
                    if bullet['owner'] == client.tank_id:
                        pygame.draw.circle(screen, (255 , 255 ,255), (bullet_x, bullet_y), 4)
                    else:
                        pygame.draw.circle(screen, (0, 128 ,0), (bullet_x, bullet_y), 4)

            except Exception as e:
                # print(str(e))
                pass
            
            
            for tank in kicked:
                if client.tank_id == tank['tankId']:
                    Over()
                    text_kick = font3.render("YOU ARE KICKED", True, (255, 255, 255))
                    screen.blit(text_kick, (402,200))
                    text_kick2 = font3.render("YOUR SCORE IS:" + ' ' +  str(tank['score']),True, (255, 255, 255))
                    screen.blit(text_kick2, (400, 220))
                    text_replay_kick = font3.render("PRESS 'R' TO REPLAY", True, (255, 215, 0))
                    screen.blit(text_replay_kick, (388, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                multiloop = False

                    pygame.display.flip()
                    time.sleep(5)
                    Menu()
                    

            for tank in winners:
                if client.tank_id == tank['tankId']:
                    Over()
                    text_win = font3.render("YOU ARE WINNER,MAN!", True, (255, 255, 255))
                    screen.blit(text_win, (395, 200))
                    text_win2 = font3.render("YOUR SCORE IS:" + ' ' +  str(tank['score']),True, (255, 255, 255))
                    screen.blit(text_win2, (407, 223))
                    text_replay_win = font3.render("PRESS 'R' TO REPLAY", True, (255, 215, 0))
                    screen.blit(text_replay_win, (388, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                multiloop = False

                    pygame.display.flip()
                    time.sleep(5)
                    Menu()

            for tank in losers:
                if client.tank_id == tank['tankId']:
                    Over()
                    text_lose = font3.render("YOU ARE LOSER,MAN!", True, (255, 255, 255))
                    screen.blit(text_lose, (395, 200))
                    text_lose2 = font3.render("YOUR SCORE IS:" + ' ' +  str(tank['score']),True, (255, 255, 255))
                    screen.blit(text_lose2, (407, 223))
                    text_replay_lose = font3.render("PRESS 'R' TO REPLAY", True, (255, 215, 0))
                    screen.blit(text_replay_lose, (388, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                multiloop = False

                    pygame.display.flip()
                    time.sleep(5)
                    Menu()
                
        
            pygame.display.flip() 
        
        client.connection.close()
        event_client.channel.stop_consuming()
        pygame.quit()
        

    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-5')
    event_client = TankConsumerClient('room-5')
    event_client.start()
    game_play()

##########################         AI Mode            #############################

def Autoplay():
    
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))

    over_pic = pygame.image.load('overmulti.jpg')

    iamtank_up = pygame.image.load('sprite1.png')
    iamtank_right = pygame.image.load('sprite1_right.png')
    iamtank_down = pygame.image.load('sprite1_down.png')
    iamtank_left = pygame.image.load('sprite1_left.png')

    enemy_up = pygame.image.load('sprite2.png')
    enemy_right = pygame.image.load('sprite2_right.png')
    enemy_down = pygame.image.load('sprite2_down.png')
    enemy_left = pygame.image.load('sprite2_left.png')

    font3 = pygame.font.SysFont('Arial Black', 18)

    def Over():
            
        screen.blit(over_pic,(0 , 0))
        

    def draw_tank(x, y,  direction, id):
        font = pygame.font.SysFont('Arial Black', 13)
        
        text_id = font.render(id, True, (255, 255, 255))
        screen.blit(text_id,(x-3, y-20))
        if direction == 'UP':
            screen.blit(iamtank_up, (x, y))
        if direction == 'RIGHT':
            screen.blit(iamtank_right, (x, y))
        if direction == 'DOWN':
            screen.blit(iamtank_down, (x, y))
        if direction == 'LEFT':
            screen.blit(iamtank_left, (x, y))

    def draw_tank2(x, y, direction, id):
        font = pygame.font.SysFont('Arial Black', 13)
        text_id2 = font.render(id, True, (255, 255, 255))
        screen.blit(text_id2,(x-3, y-20))
        if direction == 'UP':
            screen.blit(enemy_up, (x, y))
        if direction == 'RIGHT':
            screen.blit(enemy_right, (x, y))
        if direction == 'DOWN':
            screen.blit(enemy_down, (x, y))
        if direction == 'LEFT':
            screen.blit(enemy_left, (x, y))


    def info_table(tank_id, tank_health, tank_score):
        font = pygame.font.SysFont('Arial Black', 13)
        font2 = pygame.font.SysFont('Arial black', 10)
        if tank_id == client.tank_id:
            text_score = font.render('Score:' + str(tank_score), True, (255, 255, 255))
            text_health = font.render('Health:' + str(tank_health), True, (255, 255, 255))
            text_mytank = font.render('MY TANK:', True, (255, 255, 255))
            text_opponents = font.render('OPPONENTS:', True, (255, 255, 255))
            text_oppo_score_health = font2.render('score and health', True, (255,255,255))
            screen.blit(text_score, (860, 65))
            screen.blit(text_health, (860, 85))
            screen.blit(text_mytank, (855, 42))
            screen.blit(text_opponents, (850, 115))
            screen.blit(text_oppo_score_health, (849, 135))

    def info_sort():
        font = pygame.font.SysFont('Arial Black', 12)
        tanks = event_client.response['gameField']['tanks']
        scores = {}
        scores = {tank['id']: [tank['score'],tank['health']] for tank in tanks }
        sorted_scores = reversed(sorted(scores.items(), key=lambda kv: kv[1]))
        i = 151
        for score in sorted_scores:
            if score[0]!=client.tank_id:
                tank_id = font.render(score[0] + ' ' + str(score[1][0]) + '  ' + str(score[1][1]), True, (255, 255, 255))
                screen.blit(tank_id, (854, i))
                i += 22        

    def game_start():

        autoloop = True
        font = pygame.font.SysFont('Arial Black', 12)
        iamtank_x = None
        iamtank_y = None
        distance = 100

        while autoloop:
            screen.fill((0, 0, 0))
            way = ['UP', 'DOWN', 'RIGHT', 'LEFT']
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    autoloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        autoloop = False
                   
            
                        
            kicked = event_client.response['kicked']
            winners = event_client.response['winners']
            losers  = event_client.response['losers']
                    
            try:
                remaining_time = event_client.response['remainingTime']
                text_time = font.render("Remaining Time: " + str(remaining_time), True, (220, 20, 60))
                screen.blit(text_time, (840, 10))
                pygame.draw.line(screen, (255,215,0), (825, 0), (825, 600), 3)
                pygame.draw.rect(screen, (255, 255, 255), (850, 39, 80, 23), 2)
                pygame.draw.rect(screen, (255, 255, 255), (843, 111, 108, 25), 2)
                #hits = event_client.response['hits']
                bullets = event_client.response['gameField']['bullets']
                tanks = event_client.response['gameField']['tanks']
                
                for bullet in bullets:
                    bullet_x = bullet['x']
                    bullet_y = bullet['y']
                    
                    if bullet['owner'] == client.tank_id:
                        pygame.draw.circle(screen, (255 , 255 ,255), (bullet_x, bullet_y), 4)
                    else:
                        pygame.draw.circle(screen, (0, 128 ,0), (bullet_x, bullet_y), 4)

                        if bullet_x in range(iamtank_x-31, iamtank_x+31): # Уклонение от пуль
                            if iamtank_y < bullet_y:
                                if bullet_y - iamtank_y <= distance:
                                    client.turning_tank(client.token, 'RIGHT')
                            elif iamtank_y > bullet_y:
                                if iamtank_y - bullet_y <= distance:
                                    client.turning_tank(client.token, 'RIGHT')
                        if bullet_y in range(iamtank_y-31, iamtank_y+31):
                            if iamtank_x < bullet_x:
                                if bullet_x - iamtank_x <= distance:
                                    client.turning_tank(client.token, 'DOWN')
                            elif iamtank_x > bullet_x:
                                if iamtank_x - bullet_x <= distance:
                                    client.turning_tank(client.token, 'DOWN')
                
                for tank in tanks:
                    tank_id = tank['id']
                    tank_score = tank['score']
                    tank_health = tank['health']
                    tank_x = tank['x'] 
                    tank_y = tank['y']
                    tank_direction = tank['direction']

                    if tank_id == client.tank_id:           
                        iamtank_x = tank_x
                        iamtank_y = tank_y
                        tank_d = tank_direction
                        if tank_d == 'UP':
                            client.turning_tank(client.token, random.choice(way))
                        if remaining_time % 5 == 0:
                            client.turning_tank(client.token, random.choice(way))
                        draw_tank(tank_x, tank_y, tank_direction, 'Zhaiss')

                    else:              

                        draw_tank2(tank_x, tank_y, tank_direction, tank_id)  # Файринг буллет 
                        if iamtank_x in range(tank_x, tank_x + 31) and tank_y > iamtank_y:
                            client.turning_tank(client.token, 'DOWN')
                            client.firing_bullet(client.token)
                            client.turning_tank(client.token, 'RIGHT')
                        elif iamtank_x in range(tank_x, tank_x + 31) and tank_y < iamtank_y:
                            client.turning_tank(client.token, 'UP')
                            client.firing_bullet(client.token)
                            client.turning_tank(client.token, 'LEFT')
                        elif iamtank_y in range(tank_y, tank_y + 31) and tank_x > iamtank_x:
                            client.turning_tank(client.token, 'RIGHT')
                            client.firing_bullet(client.token)
                            client.turning_tank(client.token, 'DOWN')
                        elif iamtank_y in range(tank_y, tank_y + 31) and tank_x < iamtank_x:
                            client.turning_tank(client.token, 'LEFT')
                            client.firing_bullet(client.token)
                            client.turning_tank(client.token, 'UP')


                    info_table(tank_id, tank_health, tank_score)
                    info_sort()
                
            except Exception as e:
                # print(str(e))
                pass
            
            
            for tank in kicked:
                if client.tank_id == tank['tankId']:
                    Over()
                    text_kick = font3.render("YOU ARE KICKED", True, (255, 255, 255))
                    screen.blit(text_kick, (402,200))
                    text_kick2 = font3.render("YOUR SCORE IS:" + ' ' +  str(tank['score']),True, (255, 255, 255))
                    screen.blit(text_kick2, (400, 220))
                    text_replay_lose = font3.render("PRESS 'R' TO REPLAY", True, (255, 215, 0))
                    screen.blit(text_replay_lose, (388, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                autoloop = False

                    pygame.display.flip()
                    time.sleep(5)
                    Menu()

            for tank in winners:
                if client.tank_id == tank['tankId']:
                    Over()
                    text_win = font3.render("YOU ARE WINNER,MAN!", True, (255, 255, 255))
                    screen.blit(text_win, (395, 200))
                    text_win2 = font3.render("YOUR SCORE IS:" + ' ' +  str(tank['score']),True, (255, 255, 255))
                    screen.blit(text_win2, (407, 223))
                    text_replay_lose = font3.render("PRESS 'R' TO REPLAY", True, (255, 215, 0))
                    screen.blit(text_replay_lose, (388, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                autoloop = False

                    pygame.display.flip()
                    time.sleep(5)
                    Menu()

            for tank in losers:
                if client.tank_id == tank['tankId']:
                    Over()
                    text_lose = font3.render("YOU ARE LOSER,MAN!", True, (255, 255, 255))
                    screen.blit(text_lose, (395, 200))
                    text_lose2 = font3.render("YOUR SCORE IS:" + ' ' +  str(tank['score']),True, (255, 255, 255))
                    screen.blit(text_lose2, (407, 223))
                    text_replay_lose = font3.render("PRESS 'R' TO REPLAY", True, (255, 215, 0))
                    screen.blit(text_replay_lose, (388, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                autoloop = False

                    pygame.display.flip()
                    time.sleep(5)
                    Menu()
                
    
            
            pygame.display.flip() 
        
        client.connection.close()
        event_client.channel.stop_consuming()
        pygame.quit()
        

    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-17')
    event_client = TankConsumerClient('room-17')
    event_client.start()
    game_start()


#############################       MENU         ################################
def Menu():
    
    screen = pygame.display.set_mode((800, 600))
    menu = True
    while menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    Single()
                if event.key == pygame.K_m:
                    Multi()
                if event.key == pygame.K_q:
                    Autoplay()
        
        screen.blit(menu_pic, (0, 0))
        pygame.display.update()

Menu()
#pygame.quit()


