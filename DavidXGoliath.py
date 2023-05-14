import pygame
import random
import math

#initializes screen size, colors, etc.
WIDTH = 1000
HEIGHT = 800

TITLE = "DavidXGoliath"
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (75, 0, 130)
GOLD = (247, 181, 25)
BACKGROUND = (177, 119, 72)
GAME_BACKGROUND = (194,178,128)


class Button:
    #creates Button
    def __init__(self, screen,image='start.png', colour= BACKGROUND, position=(0,0), size=(200,50)):
        self.rect_obj = pygame.Rect((position),(size)) #Button Rect object.
        self.screen = screen #Screen button will be displayed on.
        self.colour = colour #Button colour.
        self.pos_x = position[0] #Button x coord.
        self.pos_y = position[1] #Button y coord.
        self.size = size #Button size.
        self.image = pygame.image.load(image)#Button image
        self.active = None #Initialize button flag.

    def draw(self):
        #draws button
        pygame.draw.rect(self.screen, self.colour, self.rect_obj)
        self.screen.blit(self.image, (self.pos_x, self.pos_y)) #Display to screen.


class Animation:
    def __init__(self, images=None, speed = 1):
        self.images = images
        self.speed = speed
        self.interval_count = 0
        self.frame = 0
        self.complete = False

    def draw(self, screen, position):
        if type(self.images) == list:
            if self.frame <= (len(self.images) - 1):
                screen.blit(self.images[self.frame], (position[0], position[1])) #Display image to screen.
                self.increaseFrame()
                self.complete = False

            else:
                self.frame = 0
                screen.blit(self.images[self.frame], (position[0], position[1])) #Display image to screen.
                self.complete = True

        elif type(self.images) == str:
            screen.blit(self.images, (position[0], position[1])) #Display image to screen.

    def increaseFrame(self):
        self.interval_count += 1
        if self.interval_count == self.speed:
            self.frame += 1 #Increase frame/index
            self.interval_count = 0
        else:
            self.frame = self.frame


class Player:
    def __init__(self):
        #images for animation
        self.standing1 = pygame.image.load('Animations/DavidIdle1.png')
        self.standing2 = pygame.image.load('Animations/DavidIdle2.png')
        self.standing3 = pygame.image.load('Animations/DavidIdle3.png')
        self.standing4 = pygame.image.load('Animations/DavidIdle4.png')
        self.standing5 = pygame.image.load('Animations/DavidIdle5.png')
        self.standing6 = pygame.image.load('Animations/DavidIdle6.png')

        self.walking1 =  pygame.image.load('Animations/DavidMoving1.png')
        self.walking2 =  pygame.image.load('Animations/DavidMoving2.png')
        self.walking3 =  pygame.image.load('Animations/DavidMoving3.png')
        self.walking4 =  pygame.image.load('Animations/DavidMoving4.png')
        self.walking5 =  pygame.image.load('Animations/DavidMoving5.png')
        self.walking6 =  pygame.image.load('Animations/DavidMoving6.png')

        self.standingR = Animation(images=[self.standing1, self.standing2, self.standing3])
        self.standingL = Animation(images=[self.standing4, self.standing5, self.standing6])
        self.walkingR = Animation(images=[self.walking1, self.walking2, self.walking3, self.walking2])
        self.walkingL = Animation(images=[self.walking4, self.walking5, self.walking6, self.walking5])

        #initialize player dimensions
        self.xPos = (0.5*WIDTH)
        self.yPos = (0.5*HEIGHT)
        self.wSize = 30
        self.hSize = 30
        #speed changing variable
        self.speedX = 0
        self.speedY = 0
        self.speedT = 0
        self.speedB = 0
        self.speedL = 0
        self.speedR = 0
        #creates a hitbox for the player
        self.hitbox = (self.xPos, self.yPos, self.wSize, self.hSize)
        #initialize health
        self.health = 150
        self.maxhealth = 150
        self.moving = False
        #variables for maze
        self.maze1X = [60,  575,    60,     60,     60,     920,  920,  350,188,188,188,790,760,760]
        self.maze1Y = [75,  75,     700,    95,     475,    95,   475,  163,240,240,520,240,240,520]
        self.maze1W = [365, 365,    880,    20,     20,     20,   20,  300,20,50,50,20,50,50]
        self.maze1H = [20,  20,     20,     230,    240,    230,  240,  20,300,20,20,300,20,20]
        self.maze1_EX = [425,60,920]
        self.maze1_EY = [75,325,325]
        self.maze1_EW = [150,20,20]
        self.maze1_EH = [20,150,150]
        self.clock = pygame.time.Clock()
        #sets up images for animations
        self.Direction = 'RIGHT'
        self.image1 = self.standingR

    def updateHitbox(self):
        #updates hitbox after movement
        self.hitbox = (self.xPos, self.yPos, self.wSize, self.hSize)

    def draw(self, screen):
        #screen.blit(self.image,[self.xPos, self.yPos, self.wSize, self.hSize])
        self.image1.draw(screen, (self.xPos,self.yPos))

    def updateMovement(self):
            #Updates player animation
            self.updateAnimation()
            keypresses = {'A':pygame.K_a,
                      'D':pygame.K_d,
                      'W':pygame.K_w,
                      'S':pygame.K_s,
                      'LEFT':pygame.K_LEFT,
                      'RIGHT':pygame.K_RIGHT,
                      'UP':pygame.K_UP,
                      'DOWN':pygame.K_DOWN}
            #Checks boundary collision.
            for i in range(len(self.maze1X)):
                if self.collisionDetected(self.xPos,self.yPos,self.wSize,self.hSize,self.maze1X[i],self.maze1Y[i],self.maze1W[i],self.maze1H[i]):
                    if self.collissionLocation(self.xPos,self.yPos,self.wSize,self.hSize,self.maze1X[i],self.maze1Y[i],self.maze1W[i],self.maze1H[i]):
                        #prevents downward movement
                        if self.message=="Top":
                            self.speedB = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if up key for movement was pressed.
                                    if event.key == keypresses['UP'] or event.key == keypresses['W']:
                                        self.speedT = -1
                                        self.Direction = 'UP'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Check if right key for movement was pressed.
                                    if event.key == keypresses['D'] or event.key == keypresses['RIGHT']:
                                        self.speedR = 1
                                        self.Direction = 'RIGHT'
                                    #Diagonal movement.
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
                        #prevents upward movement
                        elif self.message=="Bottom":
                            self.speedT = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if down key for movement was pressed.
                                    if event.key == keypresses['DOWN'] or event.key == keypresses['S']:
                                        self.speedB = 1
                                        self.Direction = 'DOWN'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Check if right key for movement was pressed.
                                    if event.key == keypresses['D'] or event.key == keypresses['RIGHT']:
                                        self.speedR = 1
                                        self.Direction = 'RIGHT'
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
                        #prevents left movement
                        if self.message=="Left":
                            self.speedR = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if down key for movement was pressed.
                                    if event.key == keypresses['DOWN'] or event.key == keypresses['S']:
                                        self.speedB = 1
                                        self.Direction = 'DOWN'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
                        #prevents right movement
                        elif self.message=="Right":
                            self.speedL = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if up key for movement was pressed.
                                    if event.key == keypresses['UP'] or event.key == keypresses['W']:
                                        self.speedT = -1
                                        self.Direction = 'UP'
                                    #Check if down key for movement was pressed.
                                    if event.key == keypresses['DOWN'] or event.key == keypresses['S']:
                                        self.speedB = 1
                                        self.Direction = 'DOWN'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['RIGHT'] or event.key == keypresses['D']:
                                        self.speedR =1
                                        self.Direction = 'RIGHT'
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0

            for i in range(len(self.maze1_EX)):
                if self.collisionDetected(self.xPos,self.yPos,self.wSize,self.hSize,self.maze1_EX[i],self.maze1_EY[i],self.maze1_EW[i],self.maze1_EH[i]):
                    if self.collissionLocation(self.xPos,self.yPos,self.wSize,self.hSize,self.maze1_EX[i],self.maze1_EY[i],self.maze1_EW[i],self.maze1_EH[i]):
                        #prevents downward movement
                        if self.message=="Top":
                            self.speedB = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if up key for movement was pressed.
                                    if event.key == keypresses['UP'] or event.key == keypresses['W']:
                                        self.speedT = -1
                                        self.Direction = 'UP'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Check if right key for movement was pressed.
                                    if event.key == keypresses['D'] or event.key == keypresses['RIGHT']:
                                        self.speedR = 1
                                        self.Direction = 'RIGHT'
                                    #Diagonal movement.
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
                        #prevents upward movement
                        elif self.message=="Bottom":
                            self.speedT = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if down key for movement was pressed.
                                    if event.key == keypresses['DOWN'] or event.key == keypresses['S']:
                                        self.speedB = 1
                                        self.Direction = 'DOWN'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Check if right key for movement was pressed.
                                    if event.key == keypresses['D'] or event.key == keypresses['RIGHT']:
                                        self.speedR = 1
                                        self.Direction = 'RIGHT'
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
                        #prevents left movement
                        if self.message=="Left":
                            self.speedR = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if down key for movement was pressed.
                                    if event.key == keypresses['DOWN'] or event.key == keypresses['S']:
                                        self.speedB = 1
                                        self.Direction = 'DOWN'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                                        self.speedL =-1
                                        self.Direction = 'LEFT'
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
                        #prevents right movement
                        elif self.message=="Right":
                            self.speedL = 0
                            #pygame.time.delay(40)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    #Check if up key for movement was pressed.
                                    if event.key == keypresses['UP'] or event.key == keypresses['W']:
                                        self.speedT = -1
                                        self.Direction = 'UP'
                                    #Check if down key for movement was pressed.
                                    if event.key == keypresses['DOWN'] or event.key == keypresses['S']:
                                        self.speedB = 1
                                        self.Direction = 'DOWN'
                                    #Check if left key for movement was pressed.
                                    if event.key == keypresses['RIGHT'] or event.key == keypresses['D']:
                                        self.speedR =1
                                        self.Direction = 'RIGHT'
                                    #Diagonal movement.
                                    if self.speedX != 0 and self.speedY != 0:
                                        self.speedL*=math.cos(1)
                                        self.speedR*=math.cos(1)
                                        self.speedU*=math.sin(1)
                                        self.speedB*=math.sin(1)
                                #Check for key release.
                                if event.type == pygame.KEYUP:
                                    if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                                        self.speedT = 0
                                        self.speedB = 0
                                        self.speedL = 0
                                        self.speedR = 0
    #checks if collision was detected
    def collisionDetected(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        result = (player_x<object_x+object_w) and (player_y<object_y+object_h) and (player_x+player_w>object_x) and (player_y+player_h>object_y)
        return result

    #checks location of collision
    def collissionLocation(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        self.collissionBottom = (player_y+player_h-object_y)*1.0
        self.collissionLeft = (object_x+object_w-player_x)*1.0
        self.collissionRight = (player_x+player_w-object_x)*1.0
        self.collissionTop = (object_y+object_h-player_y)*1.0
        if (self.collissionBottom <= self.collissionTop  and self.collissionBottom <= self.collissionLeft and self.collissionBottom <=  self.collissionRight):
            self.message = "Top"
        elif (self.collissionTop <= self.collissionBottom  and  self.collissionTop <= self.collissionLeft and self.collissionTop <=  self.collissionRight):
            self.message = "Bottom"
        elif(self.collissionLeft <=  self.collissionBottom and self.collissionLeft <= self.collissionTop and  self.collissionLeft <= self.collissionRight):
            self.message = "Right"
        elif(self.collissionRight <=  self.collissionBottom and self.collissionRight <= self.collissionTop and  self.collissionRight <= self.collissionLeft):
            self.message = "Left"
        else:
            self.message = "NONE"
        return self.message

    #updates player animation
    def updateAnimation(self):
        if self.Direction == 'RIGHT':
            self.image1 = self.walkingR
        if self.Direction == 'LEFT':
            self.image1 = self.walkingL

class Enemy:
    def __init__(self):
        #initializes enemy position
        self.xPos = 0
        self.yPos = 0
        self.width = 30
        self.height = 30
        #speed change of enemy
        self.xSpeed = 0.5
        self.ySpeed = 0.5
        #health of enemy
        self.health = 100
        #barrier
        self.maze1X = [60,  575,    60,     60,     60,     920,  920,  350,188,188,188,790,760,760]
        self.maze1Y = [75,  75,     700,    95,     475,    95,   475,  163,240,240,520,240,240,520]
        self.maze1W = [365, 365,    880,    20,     20,     20,   20,  300,20,50,50,20,50,50]
        self.maze1H = [20,  20,     20,     230,    240,    230,  240,  20,300,20,20,300,20,20]
        #enemy hitbox
        self.hitbox = (self.xPos,self.yPos, self.width, self.height)
        self.damagecount = 0
        self.health = 100
        self.index = None
        self.message = None
        #divine retribution sound effect
        self.soundeffect = pygame.mixer.Sound("Music/spell2.wav")
        #amount of speed
        self.mov_Speed = 0.75
        self.Direction = 'RIGHT'
        self.enemy_image1 = pygame.image.load('Animations/GoliathMoving1.png')
        self.enemy_image2 = pygame.image.load('Animations/GoliathMoving2.png')
        self.enemy_image3 = pygame.image.load('Animations/GoliathMoving3.png')
        self.enemy_image4 = pygame.image.load('Animations/GoliathMoving4.png')
        self.enemy_image5 = pygame.image.load('Animations/GoliathMoving5.png')
        self.enemy_image6 = pygame.image.load('Animations/GoliathMoving6.png')

        self.walkingR = Animation(images=[self.enemy_image1, self.enemy_image2, self.enemy_image3, self.enemy_image2])
        self.walkingL = Animation(images=[self.enemy_image4, self.enemy_image5, self.enemy_image6, self.enemy_image5])

        self.image2 = self.walkingR

    def spawnEnemy(self):
        ranNum = random.randint(0,3)
        #randomizes enemy x position
        self.xPos = random.randint(-50, 1050)
        if ranNum == 0 or ranNum == 1:
            if self.xPos >= 0 and self.xPos <= WIDTH:
                #randomizes enemy y position
                self.yPos = -50
            else:
                self.yPos = random.randint(0, HEIGHT)
        if ranNum == 2:
            self.yPos = random.randint(0, HEIGHT)
            self.xPos = random.randint(-50,0)
        if ranNum == 3:
            self.yPos = random.randint(0, HEIGHT)
            self.xPos = random.randint(1000,1050)

    def calculatePosition(self, player):
        #updates enemy character
        self.updateAnimation()
        # causes enemy to move
        rect = pygame.Rect(self.hitbox)
        player_rect = pygame.Rect(player.hitbox)
        if (self.xPos <50) or (self.xPos>900) or (self.yPos<=45):
            if self.xPos<70 and self.yPos>45:
                if self.yPos<350:
                    self.ySpeed = self.mov_Speed
                    self.xSpeed=0
                    self.Direction = 'DOWN'
                if self.yPos>430:
                    self.ySpeed = -self.mov_Speed
                    self.xSpeed=0
                    self.Direction = 'UP'
                if self.yPos>= 350 and self.yPos<=430:
                    self.xSpeed = self.mov_Speed
                    self.ySpeed=0
                    self.Direction = 'RIGHT'
            if self.yPos<45:
                if self.xPos<450:
                    self.xSpeed = self.mov_Speed
                    self.ySpeed=0
                    self.Direction = 'RIGHT'
                elif self.xPos>500:
                    self.xSpeed = -self.mov_Speed
                    self.ySpeed=0
                    self.Direction = 'LEFT'
                elif self.xPos >= 450 and self.yPos<=500:
                    self.ySpeed = self.mov_Speed
                    self.xSpeed=0
                    self.Direction = 'DOWN'
            if self.xPos>940 and self.yPos>45:
                if self.yPos<350:
                    self.ySpeed = self.mov_Speed
                    self.xSpeed=0
                    self.Direction = 'DOWN'
                if self.yPos>430:
                    self.ySpeed = -self.mov_Speed
                    self.xSpeed=0
                    self.Direction = 'UP'
                if self.yPos>= 350 and self.yPos<=430:
                    self.xSpeed = -self.mov_Speed
                    self.ySpeed=0
                    self.Direction = 'LEFT'
        else:
            if player.xPos + player.wSize/2 > self.xPos + self.width/2:
                    self.xSpeed = self.mov_Speed
                    self.Direction = 'RIGHT'
            elif player.xPos + player.wSize/2 < self.xPos + self.width/2:
                    self.xSpeed = -self.mov_Speed
                    self.Direction = 'LEFT'
            if player.yPos + player.hSize/2 > self.yPos + self.height/2:
                    self.ySpeed = self.mov_Speed
                    self.Direction = 'DOWN'
            elif player.yPos + player.hSize/2 < self.yPos + self.height/2:
                    self.ySpeed =  -self.mov_Speed
                    self.Direction = 'UP'

        #checks for enemy collision
        for i in range (len(self.maze1X)):
            if self.collisionDetected(self.xPos,self.yPos,self.width,self.height,self.maze1X[i],self.maze1Y[i],self.maze1W[i],self.maze1H[i]):
                self.collissionLocation(self.xPos,self.yPos,self.width,self.height,self.maze1X[i],self.maze1Y[i],self.maze1W[i],self.maze1H[i])
                if self.message == "Top":
                    self.ySpeed = - self.mov_Speed
                    self.Direction = 'UP'
                elif self.message == "Bottom":
                    self.ySpeed = self.mov_Speed
                    self.Direction = 'DOWN'
                elif self.message == "Left":
                    self.Direction = 'LEFT'
                    self.xSpeed = -self.mov_Speed
                elif self.message == "Right":
                    self.xSpeed = self.mov_Speed
                    self.Direction = 'RIGHT'


        #Move the enemy
        self.xPos += self.xSpeed
        self.yPos += self.ySpeed

    def updateEnHitbox(self):
        #updates enemy position
        self.hitbox = (self.xPos, self.yPos, self.width, self.height)

    def draw(self, screen):
        #pygame.draw.rect(screen, RED, [self.xPos, self.yPos, self.width, self.height])
        self.image2.draw(screen, (self.xPos,self.yPos))

    def collisionDetected(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        result = (player_x<object_x+object_w) and (player_y<object_y+object_h) and (player_x+player_w>object_x) and (player_y+player_h>object_y)
        return result

    def collissionLocation(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        self.collissionBottom = (player_y+player_h-object_y)*1.0
        self.collissionLeft = (object_x+object_w-player_x)*1.0
        self.collissionRight = (player_x+player_w-object_x)*1.0
        self.collissionTop = (object_y+object_h-player_y)*1.0
        if (self.collissionBottom <= self.collissionTop  and self.collissionBottom <= self.collissionLeft and self.collissionBottom <=  self.collissionRight):
            self.message = "Top"
        elif (self.collissionTop <= self.collissionBottom  and  self.collissionTop <= self.collissionLeft and self.collissionTop <=  self.collissionRight):
            self.message = "Bottom"
        elif(self.collissionLeft <=  self.collissionBottom and self.collissionLeft <= self.collissionTop and  self.collissionLeft <= self.collissionRight):
            self.message = "Right"
        elif(self.collissionRight <=  self.collissionBottom and self.collissionRight <= self.collissionTop and  self.collissionRight <= self.collissionLeft):
            self.message = "Left"
        else:
            self.message = "NONE"
        return self.message

    def updateAnimation(self):
        if self.Direction == 'RIGHT':
            self.image2 = self.walkingR
        if self.Direction == 'LEFT':
            self.image2 = self.walkingL

    def divineRetribution(self):
        self.health -=1
        self.soundeffect.play()


class Consumable:
    def __init__(self, pos_x, pos_y):
        self.image = None
        self.fuel = 0
        self.health = 0
        self.spiritPoint = 0

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = 0
        self.height = 0

        self.hitbox = None
        self.rect = None

        self.index = None

    def consume(self, player):
        if player.health + self.health > player.maxhealth:
            player.health = player.maxhealth
        else:
            player.health += self.health


    def draw(self, screen):
        screen.blit(self.image, (self.pos_x - self.width/2, self.pos_y - self.height/2))

    def createHitbox(self):
        self.hitbox = (self.pos_x - self.width/2, self.pos_y - self.width/2, self.width, self.height)
        self.rect = pygame.Rect(self.hitbox)

class Medkit(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.spiritPoint = 0
        self.health = 50
        self.width = 32
        self.height = 32
        self.image = pygame.image.load('battleImgs/medkit.png')
        self.createHitbox()

class Sword(Consumable):
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x, pos_y)
        self.spiritPoint = 100
        self.health = 20
        self.width = 32
        self.height = 32
        self.image = pygame.image.load('battleImgs/sword.png')
        self.createHitbox()


class Bullet(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, dest_x, dest_y):
        super().__init__()

        #image for the bullet
        self.bullet_w = 5
        self.bullet_h = 5
        self.image = pygame.Surface([self.bullet_w, self.bullet_h])
        self.image.fill(RED)
        self.image = pygame.image.load('battleImgs/rock.png').convert()
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        # starting location of bullet
        self.rect.x = start_x
        self.rect.y = start_y
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        #calculate bullet angle
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);

        #bullet speed and change
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
        #creates barrier
        self.maze1X = [60,  575,    60,     60,     60,     920,  920,  350,188,188,188,790,760,760]
        self.maze1Y = [75,  75,     700,    95,     475,    95,   475,  163,240,240,520,240,240,520]
        self.maze1W = [365, 365,    880,    20,     20,     20,   20,  300,20,50,50,20,50,50]
        self.maze1H = [20,  20,     20,     230,    240,    230,  240,  20,300,20,20,300,20,20]
        self.maze1_EX = [425,60,920]
        self.maze1_EY = [75,325,325]
        self.maze1_EW = [150,20,20]
        self.maze1_EH = [20,150,150]

        self.enemy = Enemy()
        self.enemy.updateEnHitbox()

    def update(self):
        #updates bullet position
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        #removes bullet when it hits barrier
        for i in range (len(self.maze1X)):
            if self.collisionDetected(self.rect.x, self.rect.y,self.bullet_w, self.bullet_h,self.maze1X[i],self.maze1Y[i],self.maze1W[i],self.maze1H[i]):
                self.kill()

        for i in range (len(self.maze1_EX)):
            if self.collisionDetected(self.rect.x, self.rect.y,self.bullet_w, self.bullet_h,self.maze1_EX[i],self.maze1_EY[i],self.maze1_EW[i],self.maze1_EH[i]):
                self.kill()

        #if the bullet flies of the screen, remove
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

    #detects collision
    def collisionDetected(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        result = (player_x<object_x+object_w) and (player_y<object_y+object_h) and (player_x+player_w>object_x) and (player_y+player_h>object_y)
        return result


class MainMenu:
    def __init__(self, parent, screen):
        self.color = BACKGROUND
        self.screen = screen
        #switches screen
        self.screenNum = 0
        #plays game
        self.playing = False
        #runs mainmenu
        self.running = True
        #button position
        self.playButtonX = 400
        self.playButtonY = 447
        self.playButtonW = 200
        self.playButtonH = 59
        self.howtoplayX = 400
        self.howtoplayY = 641
        self.howtoplayW = 200
        self.howtoplayH = 59
        self.MainMenuX = 400
        self.MainMenuY = 10
        self.MainMenuW = 180
        self.MainMenuH= 60
        self.exitButtonX = 950
        self.exitButtonY = 0
        self.exitButtonW = 60
        self.exitButtonH = 40
        self.creditsX = -6
        self.creditsY = -2
        self.creditsW = 200
        self.creditsH = 59
        self.movementX = 100
        self.movementY = 200
        self.movementW = 400
        self.movementH = 300

        #creates background images
        self.background0 = Button(screen, image = 'Background/backgroundImg.png' , position = (0,0),size = (0,0))
        self.gameExit = Button(self.screen, image = 'buttonImgs/button_x.png' , position = (self.exitButtonX,self.exitButtonY) , size = (self.exitButtonW,self.exitButtonH))
        self.screen0 = [self.background0, self.gameExit]
        self.background2 = Button(screen, image = 'Tutorial/HowToPlay.png', position = (0,0) , size = (0,0))
        self.background20 = Button(screen, image = 'Tutorial/HowToPlay2.png', position = (0,0) , size = (0,0))
        self.screen2 = [self.background2, self.gameExit]
        self.screen20 = [self.background20, self.gameExit]
        self.background3 = Button(screen, image = 'Background/Story.png' , position = (0,0),size = (0,0))
        self.screen3 = [self.background3, self.gameExit]
        self.background4 = Button(screen, image = 'Tutorial/Credits.png' , position = (0,0) , size = (0,0))
        self.screen4 = [self.background4, self.gameExit]
        self.battleMaze1 = Button(screen, image = 'battleImgs/rockImg.jpg',position = (100,400), size = (200, 100))
        self.buttons = [self.battleMaze1]

    def run(self):
       # starts music
        pygame.mixer.music.rewind()
        music = pygame.mixer.Sound("Music/MainMenuMusic.ogg")
        music.play()
        pygame.mixer.music.set_volume(0.35)
        while self.running:
            self.events()
            self.draw()
            self.update()
        music.stop()

    def update(self):
        pygame.display.update() #Update the screen.

    def draw(self):

        #draws background for different screens
        if self.screenNum == 0:
            for button in self.screen0:
                button.draw()

        if self.screenNum == 2:
            for button in self.screen2:
                button.draw()

        if self.screenNum == 20:
            for button in self.screen20:
                button.draw()

        if self.screenNum == 3:
            for button in self.screen3:
                button.draw()

        if self.screenNum == 4:
            for button in self.screen4:
                button.draw()

    def events(self):
        for event in pygame.event.get():
            self.mouse_pos = pygame.mouse.get_pos() # Get mouse position at time of press.
            self.mouseX = self.mouse_pos[0]
            self.mouseY = self.mouse_pos[1]

            #Check for window exit.
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = event.pos  # Get mouse position at time of press.
                for button in self.buttons:
                    if button.rect_obj.collidepoint(self.mouse_pos):
                        button.active = True #Activate button.

                if self.screenNum == 0:
                        if(self.mouseX>=400 and self.mouseX <= 600) and (self.mouseY >= 447 and self.mouseY <= 506): #play
                            self.playing = True
                            self.running = False
                        if(self.mouseX>= 400 and self.mouseX <= 600) and (self.mouseY>= 641 and self.mouseY <= 700): #how to Play
                            self.screenNum = 2
                        if(self.mouseX >= 400 and self.mouseX <= 600) and (self.mouseY >= 545 and self.mouseY <= 604):
                            self.screenNum = 3
                        if(self.mouseX>= 0 and self.mouseX <= 406) and (self.mouseY>= 1 and self.mouseY <= 60): #credits
                            print('hir')
                            self.screenNum = 4
                        if(self.mouseX>= 950 and self.mouseX <= 1000) and (self.mouseY>= 0 and self.mouseY <= 40): #exit
                            self.quit()

                if self.screenNum == 2:
                        if(self.mouseX>=15 and self.mouseX <= 214) and (self.mouseY >= 19 and self.mouseY <= 72): #return to menu
                            self.screenNum = 0
                        if(self.mouseX>=860 and self.mouseX <= 1000) and (self.mouseY >= 720 and self.mouseY <= 800):
                            self.screenNum = 20
                        if(self.mouseX>= 950 and self.mouseX <= 1000) and (self.mouseY>= 0 and self.mouseY <= 40): #exit
                            self.quit()

                if self.screenNum == 3:
                        if(self.mouseX>=15 and self.mouseX <= 214) and (self.mouseY >= 19 and self.mouseY <= 72): #return to menu
                            self.screenNum = 0
                        if(self.mouseX>= 950 and self.mouseX <= 1000) and (self.mouseY>= 0 and self.mouseY <= 40): #exit
                            self.quit()

                if self.screenNum == 4:
                        if(self.mouseX>=15 and self.mouseX <= 220) and (self.mouseY >= 19 and self.mouseY <= 80): #return to menu
                            self.screenNum = 0
                        if(self.mouseX>= 950 and self.mouseX <= 1000) and (self.mouseY>= 0 and self.mouseY <= 40): #exit
                            self.quit()

                if self.screenNum == 20:
                    if(self.mouseX>=30 and self.mouseX <= 240) and (self.mouseY >= 640 and self.mouseY <= 670):
                        self.screenNum = 0
                    if(self.mouseX>=865 and self.mouseX <= 965) and (self.mouseY >= 645 and self.mouseY <= 685):
                        self.screenNum = 2
                    if(self.mouseX>= 950 and self.mouseX <= 1000) and (self.mouseY>= 0 and self.mouseY <= 40): #exit
                        self.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseX = -10
                self.mouseY = -10

    def quit(self):
        self.running = False
        self.playing = False

class Game:
    def __init__(self):
        pygame.init()
        #initializes screen and other values
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
        screen = self.screen
        self.menu = MainMenu(self, self.screen)
        self.menu.running = True #Activate menu flag
        self.running = True
        self.playing = False
        self.img = pygame.image.load('Background/GameBackground.png').convert()
        self.img2 = pygame.transform.smoothscale(self.img, [1000,800])
        #boundaries
        self.maze1X = [60,  575,    60,     60,     60,     920,  920,  350,188,188,188,790,760,760]
        self.maze1Y = [75,  75,     700,    95,     475,    95,   475,  163,240,240,520,240,240,520]
        self.maze1W = [365, 365,    880,    20,     20,     20,   20,  300,20,50,50,20,50,50]
        self.maze1H = [20,  20,     20,     230,    240,    230,  240,  20,300,20,20,300,20,20]
        self.maze1_EX = [425,60,920]
        self.maze1_EY = [75,325,325]
        self.maze1_EW = [150,20,20]
        self.maze1_EH = [20,150,150]
        self.spiritPoint = 0
        self.spiritPoint_Max = 140
        self.message = None
        self.startTime = None
        self.time = None
        self.enemyTime_Spawn = 1
        self.spiritRelease = False
        self.game_over = False
        self.activatePower = False

    def new(self):
        self.player = Player()
        self.player.health = 150
        self.spiritPoint = 0
        self.enemies = []
        self.consumables = []
        self.bullets = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.bullet = Bullet(self.player.xPos, self.player.yPos, self.mouse_x, self.mouse_y)
        self.score = 0
        self.wave = 0
        self.max_enemies = 3
        self.enemy_spawnrate = [1,90]
        self.startTime = pygame.time.get_ticks()
        # This is a list of every sprite. All blocks and the player block as well.
        self.all_sprites_list = pygame.sprite.Group()

        # List of each bullet
        self.bullet_list = pygame.sprite.Group()
        self.spiritRelease = False
        self.game_over = False

    def draw(self):
        self.drawBackground()
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
            pygame.draw.rect(self.screen, BLACK, (enemy.hitbox[0], enemy.hitbox[1] - 15, enemy.width, 10)) #Draw black (background) enemy health bar.
            pygame.draw.rect(self.screen, RED, (enemy.hitbox[0], enemy.hitbox[1] - 15, (enemy.health*enemy.width/100), 10))

        for consumable in self.consumables:
            consumable.draw(self.screen)

        #Draw sp bar
        pygame.draw.rect(self.screen, PURPLE, (667, 13, self.spiritPoint/10, 10))

        #Draw player health
        pygame.draw.rect(self.screen, RED, (667, 48, self.player.health, 10))

        if self.spiritRelease:
            font = pygame.font.SysFont('impact', 20)
            text = font.render('Press SPACEBAR to activate DIVINE RETRIBUTION!!!', True, GOLD)
            self.screen.blit(text, (280,730))

    def run(self):
        pygame.mixer.music.rewind()
        music = pygame.mixer.Sound("Music/BattleMusic.ogg")
        music.play()
        pygame.mixer.music.set_volume(0.35)
        while self.playing:
            self.events()
            self.clock.tick(FPS)
            self.draw()
            self.update()
        music.stop()

    def events(self):
        keypresses = {'A':pygame.K_a,
                      'D':pygame.K_d,
                      'W':pygame.K_w,
                      'S':pygame.K_s,
                      'LEFT':pygame.K_LEFT,
                      'RIGHT':pygame.K_RIGHT,
                      'UP':pygame.K_UP,
                      'DOWN':pygame.K_DOWN}
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running = False
                self.playing = False

            #Check for key press
            if event.type == pygame.KEYDOWN:
                if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S' ]or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                    self.player.moving = True
                #Check if left key for movement was pressed.
                if event.key == keypresses['A'] or event.key == keypresses['LEFT']:
                    self.player.speedL = -1
                    self.player.Direction = 'LEFT'
                #Check if right key for movement was pressed.
                elif event.key == keypresses['D'] or event.key == keypresses['RIGHT']:
                    self.player.speedR = 1
                    self.player.Direction = 'RIGHT'
                #Check if up key for movement was pressed.
                if event.key == keypresses['W'] or event.key == keypresses['UP']:
                    self.player.speedT = -1
                    self.player.Direction = 'UP'
                #Check if down key for movement was pressed.
                elif event.key == keypresses['S']or event.key == keypresses['DOWN']:
                    self.player.speedB = 1
                    self.player.Direction = 'DOWN'
                #Diagonal movement.
                if self.player.speedX != 0 and self.player.speedY != 0:
                    self.player.speedL*=math.cos(1)
                    self.player.speedR*=math.cos(1)
                    self.player.speedU*=math.sin(1)
                    self.player.speedB*=math.sin(1)

            #Check for key release.
            if event.type == pygame.KEYUP:
                if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S'] or event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                    self.player.speedT = 0
                    self.player.speedB = 0
                    self.player.speedL = 0
                    self.player.speedR = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.spiritRelease == True:
                    self.activatePower = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button

                # Get the mouse position
                self.pos = pygame.mouse.get_pos()
                self.mouse_x = self.pos[0]
                self.mouse_y = self.pos[1]
                # create bullet list
                self.bullet = Bullet(self.player.xPos, self.player.yPos, self.mouse_x, self.mouse_y)

                        # Add the bullet to the lists
                self.all_sprites_list.add(self.bullet)
                self.bullet_list.add(self.bullet)

        self.all_sprites_list.update()

        # Draw bullet sprites
        self.all_sprites_list.draw(self.screen)

        # update screen
        pygame.display.flip()

        self.player.updateMovement()

        if len(self.consumables) > 0:
            for consumable in self.consumables:
                if self.collisionDetected(self.player.xPos,self.player.yPos,self.player.wSize,self.player.hSize,consumable.rect[0],consumable.rect[1],consumable.rect[2],consumable.rect[3]):
                    #Consume consumable and get its health.
                    consumable.consume(self.player)
                    if self.spiritPoint == 1500:
                        self.spiritPoint +=0
                    elif (consumable.spiritPoint + self.spiritPoint> 1500):
                       self.spiritPoint = 1500
                    else:
                        self.spiritPoint+=consumable.spiritPoint

                    #Delete consumable.
                    del self.consumables[consumable.index]

                #Reset consumables list.
                x_consumables =[]
                for consumable in self.consumables:
                    consumable.index = len(x_consumables)
                    x_consumables.append(consumable)
                    self.consumables = x_consumables

        for enemy in self.enemies:
            enemy.calculatePosition(self.player)
            enemy.updateEnHitbox()
            if self.collisionDetected(self.player.xPos,self.player.yPos,self.player.wSize,self.player.hSize,enemy.xPos,enemy.yPos,enemy.width,enemy.height):
                self.player.health -= 0.5
            if self.collisionDetected(self.bullet.rect.x, self.bullet.rect.y, self.bullet.bullet_w, self.bullet.bullet_h, enemy.xPos,enemy.yPos,enemy.width,enemy.height):
                for bullet in self.bullet_list:
                    self.bullet_list.remove(bullet)
                    self.bullet.kill()
                    self.bullet.rect.x = -100
                self.all_sprites_list.update()
                enemy.damagecount +=25
                enemy.health -= 25
                if enemy.health<=0:
                    self.enemies.remove(enemy)
                    self.score +=100
                    if self.spiritPoint < ((self.spiritPoint_Max+1)*10):
                        self.spiritPoint += 100
                    if self.spiritPoint==1500:
                        self.spiritRelease = True
                    if self.score%300 == 0:
                        x_consumable = Sword(enemy.xPos + enemy.width/2, enemy.yPos + enemy.height/2)
                        #Spawn consumable.
                        x_consumable.index = len(self.consumables)
                        self.consumables.append(x_consumable)
                    elif self.score%800 == 0:
                        x_consumable = Medkit(enemy.xPos + enemy.width/2, enemy.yPos + enemy.height/2)
                        #Spawn consumable.
                        x_consumable.index = len(self.consumables)
                        self.consumables.append(x_consumable)

        self.player.xPos +=self.player.speedL
        self.player.xPos +=self.player.speedR
        self.player.yPos +=self.player.speedT
        self.player.yPos +=self.player.speedB

        if self.getSpawnChance(self.enemy_spawnrate[0], self.enemy_spawnrate[1]) == True and len(self.enemies) < self.max_enemies:
            enemy = Enemy()
            self.time = pygame.time.get_ticks()
            if (self.time-self.startTime>2500*self.enemyTime_Spawn):
                enemy.spawnEnemy()
                enemy.index = len(self.enemies)
                self.enemies.append(enemy)

        if self.activatePower == True:
            for enemy in self.enemies:
                if len(self.enemies)>1:
                    enemy.divineRetribution()
                    if enemy.health<=0:
                        self.enemies.remove(enemy)
                        self.score +=100
                else:
                    self.activatePower = False
                    self.spiritRelease = False
                    self.spiritPoint = 0

        if self.score/100 == self.max_enemies:
            self.enemy = Enemy()
            self.max_enemies+=3
            self.enemy.mov_Speed+=0.25

        if self.player.health<0:
            self.game_over = True

        if self.game_over:
            self.playing = False

    def getMainMenu(self):
        self.menu.run() #Run menu.
        if self.menu.playing:
            self.playing = True
        if not self.menu.running and not self.playing:
            self.running = False

    def drawBackground(self):
        pygame.draw.rect(self.screen,GAME_BACKGROUND,[0,0,1000,800])
        self.screen.blit(self.img2,[0,0])
        self.drawMaze()
        font = pygame.font.SysFont('bahnschrift', 45)
        text = font.render(str(self.score), True, BLACK)
        self.screen.blit(text,(210,10))

    #Calculate if an enemy should spawn.
    def getSpawnChance(self, x_start=1, x_end=20):
        spawn_chance = random.randint(x_start, x_end)
        if spawn_chance == 1:
            return True
        else:
            return False

    def drawMaze(self):
        self.collissionTop = False
        self.collissionBottom = False
        self.collissionLeft = False
        self.collissionTop = False

    def collisionDetected(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        result = (player_x<object_x+object_w) and (player_y<object_y+object_h) and (player_x+player_w>object_x) and (player_y+player_h>object_y)
        return result

    def collissionLocation(self,player_x,player_y,player_w,player_h, object_x, object_y, object_w, object_h):
        self.collissionBottom = (player_y+player_h-object_y)*1.0
        self.collissionLeft = (object_x+object_w-player_x)*1.0
        self.collissionRight = (player_x+player_w-object_x)*1.0
        self.collissionTop = (object_y+object_h-player_y)*1.0
        if (self.collissionBottom <= self.collissionTop  and self.collissionBottom <= self.collissionLeft and self.collissionBottom <=  self.collissionRight):
            self.message = "Top"
        elif (self.collissionTop <= self.collissionBottom  and  self.collissionTop <= self.collissionLeft and self.collissionTop <=  self.collissionRight):
            self.message = "Bottom"
        elif(self.collissionLeft <=  self.collissionBottom and self.collissionLeft <= self.collissionTop and  self.collissionLeft <= self.collissionRight):
            self.message = "Right"
        elif(self.collissionRight <=  self.collissionBottom and self.collissionRight <= self.collissionTop and  self.collissionRight <= self.collissionLeft):
            self.message = "Left"
        else:
            self.message = "NONE"
        return self.message

    def update(self):
        pygame.display.update() #Update the screen.

    def getGameOver(self):
        self.exitButtonX = 950
        self.exitButtonY = 0
        self.exitButtonW = 60
        self.exitButtonH = 40
        self.MainMenuX = 400
        self.MainMenuY = 10
        self.MainMenuW = 180
        self.MainMenuH = 60
        img = pygame.image.load('Background/GameOver.png').convert()
        img2 = pygame.transform.smoothscale(img, [1000,800])
        self.gameExit = Button(self.screen, image = 'buttonImgs/button_x.png' , position = (self.exitButtonX,self.exitButtonY) , size = (self.exitButtonW,self.exitButtonH))
        self.over_Screen = [self.gameExit]

        while self.game_over:
            self.screen.fill(BLACK)
            font = pygame.font.SysFont('bahnschrift', 60)
            for button in self.over_Screen:
                button.draw()
            self.screen.blit(img2,[0,0])
            text_S = font.render(str(self.score), True, WHITE)
            self.screen.blit(text_S, (460,360))
            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    self.game_over = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = event.pos  # Get mouse position at time of press.
                    self.mouse_x = self.mouse_pos[0]
                    self.mouse_y = self.mouse_pos[1]
                    if(self.mouse_x>=0 and self.mouse_x <= 220) and (self.mouse_y >= 720 and self.mouse_y <= 800): #return to menu
                        self.playing = False
                        self.menu.running = True
                        self.game_over = False
                        self.screenNum = 0
                    if(self.mouse_x>=790 and self.mouse_x <= 1000) and (self.mouse_y >= 720 and self.mouse_y <= 800): #try again
                        self.game_over = False
                        self.playing = True
                    for button in self.over_Screen:
                        if button.rect_obj.collidepoint(self.mouse_pos):
                            button.active = True #Activate button.

            if self.gameExit.active == True:
                self.playing = False
                self.running = False
                self.game_over = False

def main():
    pygame.init()
    inGame = Game()

    while inGame.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               inGame.running=False
            if inGame.menu.running:
                inGame.getMainMenu()
            if inGame.playing:
                inGame.new()
                inGame.run()
            if inGame.game_over==True:
                inGame.getGameOver()

        pygame.display.flip()
    pygame.quit()
if __name__ == "__main__":
    main()