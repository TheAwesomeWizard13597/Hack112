from cmu_112_graphics import *
import math, random, time, copy
from PIL import Image

from ta import *
from student2 import *
from kos import *

class myApp(App):

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
        startX = [174, 304, 444]
        startY = [70*i for i in range(1,6)]
        for i in range (5):
            x = random.choice(startX)
            y = random.choice(startY)
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
        if app.ta.rec.intersects(app.kos.rec):
            return True
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
        ##################################
        elif (event.key=="1"):
            app.inBattle=True
        if app.inBattle:
            if (event.key=="Enter" and app.battleEnterCount==0):
                app.kosInitMessage=True
                app.battleEnterCount+=1
            elif (event.key=="Enter" and app.battleEnterCount==1):
                app.attackChoice=True
                app.battleEnterCount+=1
            elif (app.attackChoice):
                if event.key=="a":
                    app.TAHealth+=1
                    if (app.TAHealth==3):
                        app.TAlose=True
                elif event.key=="s":
                    app.profHealth+=1
                    if (app.profHealth==3):
                        app.TAwin=True
                elif event.key=="r":
                    app.inBattle=False
            elif (event.key=="r" and (app.TAlost or app.TAwin)):
                app.appStarted()

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
        app.checkCollisionsTA()
        #print(app.ta.xpos,app.ta.ypos)
        print(app.adis[0].xpos,app.adis[0].ypos)
        directions = ['left', 'right', 'up', 'down', 0]
        for pupil in app.adis:
            direction = random.randint(0, len(directions)-1)
            if app.studentHitsDesk(pupil):
                print("hit")
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
        app.drawBattleground(canvas)
        app.drawBattleGround(canvas)

###################################################################
###################################################################
###################################################################
# This demos sprites using Pillow/PIL images
# See here for more details:
# https://pillow.readthedocs.io/en/stable/reference/Image.html

# This uses a spritestrip from this tutorial:
# https://www.codeandweb.com/texturepacker/tutorials/how-to-create-a-sprite-sheet

    def initBattleImages(app):
        p1 = '/Users/tony/Desktop/15112/hack112/sprite.png'
        p2 = '/Users/tony/Desktop/15112/hack112/sprite3.png'
        url2 = '/Users/tony/Desktop/15112/hack112/text2.png'
        url3 = '/Users/tony/Desktop/15112/hack112/battleground.jpg'
        h1 = '/Users/tony/Desktop/15112/hack112/health0.png'
        h2 = '/Users/tony/Desktop/15112/hack112/health1.png'
        h3 = '/Users/tony/Desktop/15112/hack112/health2.png'
        h4 = '/Users/tony/Desktop/15112/hack112/health3.png'
        death='/Users/tony/Desktop/15112/hack112/death.png'
        win='/Users/tony/Desktop/15112/hack112/win.png'
        health1 = app.loadImage(h1)
        health2 = app.loadImage(h2)
        health3 = app.loadImage(h3)
        health4 = app.loadImage(h4)
        app.deathIcon= app.loadImage(death)
        app.winIcon= app.loadImage(win)
        app.healthbars=[health4,health3,health2,health1]
        app.imageText = app.loadImage(url2)
        app.battleground = app.loadImage(url3)
        app.x=app.width/2
        app.y=app.height/2
        spritestrip = app.loadImage(p1)
        spritestrip2 = app.loadImage(p2)
        ############
        app.spritesDown2 = [ ]
        spriteRow = spritestrip2.crop((0, 0, 256, 64))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            app.spritesDown2.append(sprite)
        ##############
        app.spritesDown = [ ]
        spriteRow = spritestrip.crop((0, 0, 256, 64))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            app.spritesDown.append(sprite)
        app.spritesLeft = [ ]
        spriteRow = spritestrip.crop((0, 64, 256, 128))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            app.spritesLeft.append(sprite)
        app.spritesRight = [ ]
        spriteRow = spritestrip.crop((0, 128, 256, 192))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            app.spritesRight.append(sprite)
        app.spritesUp = [ ]
        spriteRow = spritestrip.crop((0, 192, 256, 256))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            app.spritesUp.append(sprite)
        app.down=True
        app.up=False
        app.left=False
        app.right=False
        app.spriteCounter = 0
        app.speech=False
        app.inBattleMode()

    def inBattleMode(app):
        app.inBattle=True
        app.kosInitMessage=False
        app.battleEnterCount=0
        app.attackChoice=False
        app.kickOut=False
        app.passed=False
        app.profHealth=0
        app.TAHealth=0
        app.TAwin=False
        app.TAlose=False

    def madeMove(app, move):
        app.attackChoice=False
        if move=="argue":
            app.kickOut=True
        elif move=="smile":
            app.passed=True

    def timerFired(app):
        print(app.TAHealth) 
        print(app.TAlose)
        
    def drawSpeech(app, canvas, text):
        canvas.create_rectangle(40,315,510,460,fill="white")
        canvas.create_image(app.width/2, app.height, anchor="s",
                            image=ImageTk.PhotoImage(app.imageText))
        
        canvas.create_text(app.width/2, app.height-90,
                            text=text,
                            font="Courier 16")

    def drawBattleground(app, canvas):
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.battleground))
        p1=app.scaleImage(app.spritesUp[2], 2.5)
        canvas.create_image(app.width/3, 4.3*app.height/8,
                            image=ImageTk.PhotoImage(p1))
        TAHealth=app.healthbars[app.TAHealth]
        health=app.scaleImage(TAHealth, .4)
        canvas.create_image(app.width/3, 4.3*app.height/8-50,  image=ImageTk.PhotoImage(health))

        p2=app.scaleImage(app.spritesDown2[2], 1.7)
        canvas.create_image(1.7*app.width/3, 1.4*app.height/4,
                            image=ImageTk.PhotoImage(p2))
        profHealth=app.healthbars[app.profHealth]
        health=app.scaleImage(profHealth, .6)
        canvas.create_image(1.7*app.width/3, 1.4*app.height/4-60,image=ImageTk.PhotoImage(health))
        app.drawSpeech(canvas,
        "You are now facing the final boss...\nProfessor Kosbae")

    def drawWinScreen(app,canvas):
        canvas.create_text(app.width/2,app.height/2,text="TA Wins",font="Courier 30")
        ta=app.scaleImage(app.spritesDown[2], 2.5)
        canvas.create_image(app.width/5, app.height/2,
                            image=ImageTk.PhotoImage(ta))
        trop=app.scaleImage(app.winIcon, .2)
        canvas.create_image(app.width/5, app.height/2+50,
                            image=ImageTk.PhotoImage(trop))
        prof=app.scaleImage(app.spritesDown2[2], 2.5)
        canvas.create_image(4*app.width/5, app.height/2,
                            image=ImageTk.PhotoImage(prof))
        death=app.scaleImage(app.deathIcon, .6)
        canvas.create_image(4*app.width/5, app.height/2,
                            image=ImageTk.PhotoImage(death))

    def drawLoseScreen(app, canvas):
        canvas.create_text(app.width/2,app.height/2,text="TA Loses",font="Courier 30")
        ta=app.scaleImage(app.spritesDown[2], 2.5)
        canvas.create_image(app.width/5, app.height/2,
                            image=ImageTk.PhotoImage(ta))
        death=app.scaleImage(app.deathIcon, .6)
        canvas.create_image(app.width/5, app.height/2,
                            image=ImageTk.PhotoImage(death))
        prof=app.scaleImage(app.spritesDown2[2], 2.5)
        canvas.create_image(4*app.width/5, app.height/2,
                            image=ImageTk.PhotoImage(prof))
        trop=app.scaleImage(app.winIcon, .2)
        canvas.create_image(4*app.width/5, 2*app.height/3+50,
                            image=ImageTk.PhotoImage(trop))
        canvas.create_text(app.width/2,2*app.height/3,text="Press r to restart",font="Courier 20")

    def drawBattleGround(app,canvas):
        if not (app.TAlose or app.TAwin):
            if app.inBattle:
                app.drawBattleground(canvas)
                if (app.kosInitMessage and app.battleEnterCount==1):
                    text="Prof Kosbae: Welcome to the Final Exam ...\nwhats your first move?"
                    app.drawSpeech(canvas, text)
                elif (app.attackChoice):
                    app.drawSpeech(canvas, """What is your first move:
                                    \n- Argue (a)\n- Smile (s)\n- Run (r)""")
                elif (app.kickOut):
                    app.drawSpeech(canvas, """You have been kicked out from 15-112,
                                            \n try harder next time""")
                elif (app.passed):
                    app.drawSpeech(canvas, """You have now passed 15-112!""")
            # else:
            #     if app.up:
            #         sprite=app.spritesUp[app.spriteCounter]
            #     elif app.down:
            #         sprite=app.spritesDown[app.spriteCounter]
            #     elif app.right:
            #         sprite=app.spritesRight[app.spriteCounter]
            #     elif app.left:
            #         sprite=app.spritesLeft[app.spriteCounter]
            #     canvas.create_image(app.x, app.y, image=ImageTk.PhotoImage(sprite))
            #     TAHealth=app.healthbars[app.TAHealth]
            #     health=app.scaleImage(TAHealth, .2)
            #     canvas.create_image(app.x, app.y-20, image=ImageTk.PhotoImage(health))
            #     if (app.speech):
            #         app.drawSpeech(canvas,"Hi, my name is TA")
        elif(app.TAwin):
            app.drawWinScreen(canvas)
        elif(app.TAlose):
            app.drawLoseScreen(canvas)
            
myApp(width = 544, height = 480)