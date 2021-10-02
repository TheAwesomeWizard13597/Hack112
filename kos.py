from rectangle import *
from cmu_112_graphics import *
from PIL import *

class kos():
    def __init__(self, xpos, ypos, size):
        
        self.xpos = xpos
        self.ypos = ypos
        self.speed = 10
        self.inventory = dict()
        self.charisma = 0
        self.size = size
        self.width = 64
        self.height = 64
        self.recWidth = self.width*0.6
        self.recHeight = self.height*0.8
        self.offset = 0
        self.rec = Rectangle(self.xpos, self.ypos, self.xpos+self.recWidth, self.ypos+self.recHeight)
        self.room = 1 # 1 = lecture hall, 2 = dorm room
        ##################
        self.sprite = None
        self.spritesDown = [ ]

        self.spritesLeft = [ ]
       
        self.spritesRight = [ ]
    
        self.spritesUp = [ ]

        self.direction = 'down'
        self.down=True
        self.up=False
        self.left=False
        self.right=False
        self.spriteCounter = 0

    def move(self, direction):
        if self.room == 1:
            if direction == "up" and self.ypos > 10:
                self.up=True
                self.left=False
                self.right=False
                self.down=False
                self.ypos -= self.speed
                self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesUp))
                self.direction = "up"
            elif direction == "down" and self.ypos + self.height <  490:
                self.up=False
                self.left=False
                self.right=False
                self.down=True
                self.ypos += self.speed
                self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesDown))
                self.direction = "down"
            if direction == "right" and self.xpos + self.width < 564:
                self.up=False
                self.left=False
                self.right=True
                self.down=False
                self.xpos += self.speed
                self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesRight))
                self.direction = "right"
            elif direction == "left" and self.xpos > 20:
                self.up=False
                self.left=True
                self.right=False
                self.down=False
                self.xpos -= self.speed
                self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesLeft))
                self.direction = "left"
        # elif self.room == 2:
        #     if direction == "up" and self.ypos > 0:
        #         self.ypos -= self.speed
        #     elif direction == "down" and self.ypos + self.height <  480:
        #         self.ypos += self.speed
        #     if direction == "right" and self.xpos + self.width < 544:
        #         self.xpos += self.speed
        #     elif direction == "left" and self.xpos > 0:
        #         self.xpos -= self.speed
        # updates the rectangle
        self.rec = Rectangle(self.xpos, self.ypos, self.xpos+self.recWidth, self.ypos+self.recHeight)

    def changeSize(self, room):
        if room == 1:
            self.size = 2*size
        elif room == 2:
            self.size = 0.5*size

    def getItem(self, item):
        if item.name in self.inventory:
            item.amount += 1
        else:
            self.inventory[item.name] = item
            item.amount = 1
    
    def helpedStudent(self, helpfulness):
        if helpfulness >= 3:
            self.charisma += 1
        else:
            self.charisma -= 1
    
