from cmu_112_graphics import *
import math, random, time, copy
from PIL import Image

from ta import *
from student2 import *
from kos import *
from test import *

class myApp(Mode):

    def appStarted(app):
        # app.text = None
        app.ta = ta(app.width - 50, app.height/2, 30)
        app.kos = kos(20,app.height/3,30)
        app.lectureHeight = 480
        app.lectureWidth = 544
        app.initMonkeys()
        app.initDesks()
        app.imageProcess()
        app.initSpeechInteraction()
        app.initSpeechBubble()
        app.initBattleImages()

    def initBattleImages(app):
        h1 = '/Users/tony/Desktop/15112/hack112/health0.png'
        h2 = '/Users/tony/Desktop/15112/hack112/health1.png'
        h3 = '/Users/tony/Desktop/15112/hack112/health2.png'
        h4 = '/Users/tony/Desktop/15112/hack112/health3.png'
        health1 = app.loadImage(h1)
        health2 = app.loadImage(h2)
        health3 = app.loadImage(h3)
        health4 = app.loadImage(h4)
        app.TAHealth = 0
        app.healthbars = [health4,health3,health2,health1]

    def spriteListAssignment(app, image, person):
        sheetStrip = app.loadImage(image)
        for j in range(4):
            sheetRow = sheetStrip.crop((0, j*64, 256, (j+1)*64))
            spritesDirections = [person.spritesDown, person.spritesLeft, person.spritesRight, person.spritesUp]
            for i in range(4):
                sprite = sheetRow.crop((64*i,0,64*(i+1),64))
                spritesDirections[j].append(sprite)
        return sprite

    def imageProcess(app):
        TAimage = '/Users/tony/Desktop/15112/hack112/sprite.png'
        pupilImage = '/Users/tony/Desktop/15112/hack112/sprite3.png'
        app.spriteListAssignment(TAimage, app.ta)
        for adi in app.adis:
            app.spriteListAssignment(pupilImage, adi)
        kosImage = '/Users/tony/Desktop/15112/hack112/kosbae.png'
        app.kosSprite = app.loadImage(kosImage)

    def initMonkeys(app):
        app.adis = []
        startX = [174, 304]
        startY = [70*i for i in range(1,6)]
        for i in range (5):
            x = random.choice(startX)
            y = random.choice(startY)
            # if (x,y) not
            app.adis.append( student2(x, y, 30))
        
    def initDesks(app):
        offset = 75
        app.deskWidth = 30
        app.deskHeight = 55
        app.desks = ([((app.lectureWidth / 4), (((app.lectureHeight) / 7) * i) + offset) for i in range(5)] + 
                     [((app.lectureWidth / 2) , (((app.lectureHeight) / 7) * i + offset)) for i in range(5)] +
                     [((app.lectureWidth / 4) * 3, (((app.lectureHeight) / 7) * i + offset)) for i in range(5)])
        app.deskRecs = []
        app.rectangles = []
        app.occupiedDesks = set()
        for x,y in app.desks:
            rec = Rectangle(x,y,x + app.deskWidth,y + app.deskHeight)
            app.deskRecs.append(rec)
            app.rectangles.append((x,y,x+app.deskWidth, y+ app.deskHeight))
            
    def initSpeechInteraction(app):
        app.speechInteractionDisplay = False
        app.speechInteractionXPos = None
        app.speechInteractionYPos = None
        app.speechInteractionWidth = 100
        app.speechInteractionHeight = 50

    def initSpeechBubble(app):
        app.speechBubbleList = [] #Tuple in form (text, xpos, ypos)
        app.speechBubbleWidth = 100
        app.speechBubbleHeight = 50

    def isPosInsideRect(app, x, y, rectx, recty, width, height):
        if (x > rectx and y > recty and 
            x < rectx + width and y < recty + height):
            return True
        return False

    def checkCollisionsTA(app):
        for deskRec in app.deskRecs:
            if app.ta.rec.intersects(deskRec) and app.deskRecs.index(deskRec) in app.occupiedDesks:
                print("hit student")
    
    def taHitsDesk(app):
        for deskRec in app.deskRecs:
            if app.ta.rec.intersects(deskRec):
                return True
        return False

    def studentHitsStudent(app,adi1,adi2):
        if adi1.rec.intersects(adi2.rec) and app.adis.index(adi1) != app.adis.index(adi2):
            return True
        return False
    
    def taHitsKos(app):
        # print('is hitting')
        if app.ta.rec.intersects(app.kos.rec):
            print('yay')
            return True
        # print('boo')
        return False

    def taHitsStudent(app):
        for adi in app.adis:
            if app.ta.rec.intersects(adi.rec):
                return True
        return False
    
    def studentHitsDesk(app, student):
        for deskRec in app.deskRecs:
            if student.rec.intersects(deskRec):
                return True
        return False

    def speechInteraction(app, text, xpos, ypos):
        app.text = text
        app.speechInteractionDisplay = True
        app.speechInteractionXPos = ypos
        app.speechInteractionYPos = xpos
    
    def speechBubble(app, text, xpos, ypos):
        app.speechBubbleList.append((text, xpos, ypos))

    def keyPressed(app, event):
        if (event.key == 'Space' or event.key == 'Enter') and app.speechInteractionDisplay:
            app.speechInteractionDisplay = False
        if event.key == 'Left':
            app.ta.move("left")
            if app.taHitsDesk() or app.taHitsStudent():
                app.ta.move("right")
        elif event.key == 'Right':
            app.ta.move("right")
            if app.taHitsDesk() or app.taHitsStudent():
                app.ta.move("left")
        if event.key == 'Up':
            app.ta.move('up')
            if app.taHitsDesk() or app.taHitsStudent():
                app.ta.move("down")
        elif event.key == 'Down':
            app.ta.move('down')
            if app.taHitsDesk() or app.taHitsStudent():
                app.ta.move("up")
        if app.taHitsKos() or event.key == "m":
            print('entering battlemode')
            app.app.setActiveMode(app.app.battleMode)
            print("goodbye battlemode")
        app.timerFired()

    def mousePressed(app, event):
        if app.speechInteractionDisplay:
            app.speechInteractionDisplay = False
        # trying to click to remove
        for (text, xpos, ypos) in app.speechBubbleList:
            w,h = app.speechBubbleWidth, app.speechInteractionHeight
            if isPosInsideRect(app, event.x, event.y, xpos, ypos, w,h):
                app.speechBubble.remove((text, ypos, xpos)) 
                #we can remove the tuple, or hide the text or something

    def timerFired(app):
        print('present')
        # print(app.ta.xpos,app.ta.ypos)
        # print(app.adis[0].xpos,app.adis[0].ypos)
        directions = ['left', 'right', 'up', 'down', 0]
        for pupil in app.adis:
            direction = random.randint(0, len(directions)-1)
            if app.studentHitsDesk(pupil):
                pass
                # print("hit")
            if direction != 0:
                pupilCollison = False
                for otherPupil in app.adis:
                    if app.studentHitsStudent(pupil,otherPupil):
                        pupilCollison = True   
                if not app.studentHitsDesk(pupil) and not pupilCollison:
                    pupil.move(directions[direction])
                else:
                    if pupil.direction == "up":
                        pupil.move("down")
                    elif pupil.direction == "down":
                        pupil.move("up")
                    elif pupil.direction == 'right':
                        pupil.move('left')
                    elif pupil.direction == 'left':
                        pupil.move('right')
        

    def drawTA(app, canvas):
        # x,y = app.ta.xpos, app.ta.ypos
        # width, height = app.ta.width, app.ta.height
        # canvas.create_rectangle(x, y, x+app.ta.width, 
        #                     y+app.ta.height, fill='black')
        if app.ta.direction == "up":
            sprite=app.ta.spritesUp[app.ta.spriteCounter]
        elif app.ta.direction == "down":
            sprite=app.ta.spritesDown[app.ta.spriteCounter]
        elif app.ta.direction == "right":
            sprite=app.ta.spritesRight[app.ta.spriteCounter]
        elif app.ta.direction == "left":
            sprite=app.ta.spritesLeft[app.ta.spriteCounter]
        canvas.create_image(app.ta.xpos  + 20, app.ta.ypos + 20, image=ImageTk.PhotoImage(sprite))

    def drawDesks(app, canvas):
        for x, y in app.desks:
            canvas.create_rectangle(x, y, x + app.deskWidth, y + app.deskHeight, fill = 'brown')

    def drawAdis(app, canvas):
        for pupil in  app.adis:
            if pupil.direction == "up":
                sprite=pupil.spritesUp[pupil.spriteCounter]
            elif pupil.direction == "down":
                sprite=pupil.spritesDown[pupil.spriteCounter]
            elif pupil.direction == "right":
                sprite=pupil.spritesRight[pupil.spriteCounter]
            elif pupil.direction == "left":
                sprite=pupil.spritesLeft[pupil.spriteCounter]
            canvas.create_image(pupil.xpos  + 20, pupil.ypos + 20, image=ImageTk.PhotoImage(sprite))
    
    def drawKos(app, canvas):
        canvas.create_image(app.kos.xpos +20, app.kos.ypos +20, image=ImageTk.PhotoImage(app.kosSprite))

    def drawBackgroundLecture(app, canvas):
        canvas.create_rectangle(0, 100, 10, app.height - 100, fill = 'black')
        canvas.create_rectangle(100, 0, 150, 10, fill = 'brown')

    def drawTextInteraction(app, canvas):
        canvas.create_rectangle(app.speechInteractionXPos + app.speechInteractionWidth / 2, app.speechInteractionYPos + app.speechInteractionHeight / 2, 
                                app.speechInteractionXPos - app.speechInteractionWidth / 2, app.speechInteractionYPos - app.speechInteractionHeight / 2,
                                fill = 'white', width = 8)
        canvas.create_text(app.speechInteractionXPos, app.speechInteractionYPos, text = app.text)
    
    def drawTextBubble(app, canvas):
        for (text, xpos, ypos) in app.speechBubbleList:
            canvas.create_rectangle(xpos + app.speechBubbleWidth / 2, ypos + app.speechBubbleHeight / 2, xpos - app.speechBubbleWidth / 2, 
                                    ypos - app.speechBubbleHeight / 2, fill = 'white', width = 8)
            canvas.create_text(xpos, ypos, text = text)

    def redrawAll(app, canvas):
        app.drawTextBubble(canvas)
        if app.speechInteractionDisplay:
            app.drawTextInteraction(canvas)
        app.drawDesks(canvas)
        app.drawBackgroundLecture(canvas)
        app.drawTA(canvas)
        app.drawAdis(canvas)
        app.drawKos(canvas)
        TAHealth=app.healthbars[app.TAHealth]
        health=app.scaleImage(TAHealth, .2)
        canvas.create_image(app.ta.xpos+20, app.ta.ypos, image=ImageTk.PhotoImage(health))

myApp(width = 544, height = 480)