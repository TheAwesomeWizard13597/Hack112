# This demos sprites using Pillow/PIL images
# See here for more details:
# https://pillow.readthedocs.io/en/stable/reference/Image.html

# This uses a spritestrip from this tutorial:
# https://www.codeandweb.com/texturepacker/tutorials/how-to-create-a-sprite-sheet

from cmu_112_graphics import *

class MyApp(App):
    def appStarted(self):
        url = '/Users/tony/Desktop/15112/hack112/sprite.png'
        self.x=self.x
        self.y=self.y
        spritestrip = self.loadImage(url)
        self.spritesDown = [ ]
        spriteRow = spritestrip.crop((0, 0, 256, 64))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            self.spritesDown.append(sprite)
        self.spritesLeft = [ ]
        spriteRow = spritestrip.crop((0, 64, 256, 128))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            self.spritesLeft.append(sprite)
        self.spritesRight = [ ]
        spriteRow = spritestrip.crop((0, 128, 256, 192))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            self.spritesRight.append(sprite)
        self.spritesUp = [ ]
        spriteRow = spritestrip.crop((0, 192, 256, 256))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            self.spritesUp.append(sprite)
        self.down=True
        self.up=False
        self.left=False
        self.right=False
        self.spriteCounter = 0
        self.timerDelay=500

    def keyPressed(self,event):
        if (event.key=="Up"):
            self.up=True
            self.left=False
            self.right=False
            self.down=False
            self.y-=5
            self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesUp))
        elif (event.key=="Down"):
            self.up=False
            self.left=False
            self.right=False
            self.down=True
            self.y+=5
            self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesDown))
        elif (event.key=="Right"):
            self.up=False
            self.left=False
            self.right=True
            self.down=False
            self.x+=5
            self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesRight))
        elif (event.key=="Left"):
            self.up=False
            self.left=True
            self.right=False
            self.down=False
            self.x-=5
            self.spriteCounter = (self.spriteCounter+1)%(len(self.spritesLeft))
        #self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)

    def redrawAll(self, canvas):
        if self.up:
            sprite=self.spritesUp[self.spriteCounter]
        elif self.down:
            sprite=self.spritesDown[self.spriteCounter]
        elif self.right:
            sprite=self.spritesRight[self.spriteCounter]
        elif self.left:
            sprite=self.spritesLeft[self.spriteCounter]
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))

MyApp(width=400, height=400)
