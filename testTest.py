from cmu_112_graphics import *

class MyApp(App):
    def appStarted(self):
        self.initBattleImages()

    def initBattleImages(self):
        p1 = '/Users/tony/Desktop/15112/hack112/sprite.png'
        p2 = '/Users/tony/Desktop/15112/hack112/sprite3.png'
        url2 = '/Users/tony/Desktop/15112/hack112/text2.png'
        url3 = '/Users/tony/Desktop/15112/hack112/battleground.jpg'
        self.healthbars = self.app.classRoomMode.healthbars
        death='/Users/tony/Desktop/15112/hack112/death.png'
        win='/Users/tony/Desktop/15112/hack112/win.png'
        desk='/Users/tony/Desktop/15112/hack112/pixeldesk.png'
        self.deskImg = self.loadImage(desk)
        self.deathIcon= self.loadImage(death)
        self.winIcon= self.loadImage(win)
        self.healthbars=[health4,health3,health2,health1]
        self.imageText = self.loadImage(url2)
        self.battleground = self.loadImage(url3)
        self.x=self.width/2
        self.y=self.height/2
        spritestrip = self.loadImage(p1)
        spritestrip2 = self.loadImage(p2)
        ############
        self.spritesDown2 = [ ]
        spriteRow = spritestrip2.crop((0, 0, 256, 64))
        for i in range(4):
            sprite=spriteRow.crop((64*i,0,64*(i+1),64))
            self.spritesDown2.append(sprite)
        ##############
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
        self.speech=False
        self.inBattleMode()

    def inBattleMode(self):
        self.inBattle=True
        self.kosInitMessage=False
        self.battleEnterCount=0
        self.attackChoice=False
        self.kickOut=False
        self.passed=False
        self.profHealth=0
        self.TAHealth=0
        self.TAwin=False
        self.TAlose=False
        self.codeBattle()
        self.testCount=0

    def codeBattle(self):
        self.codeBattleMode=False
        self.question1=True
        self.question2=False
        self.question3=False
        self.question1Ans1=0
        self.question1Ans2=2
        self.question2Ans1=0
        self.question2Ans2=1
        self.question3Ans1=0
        self.question3Ans2=1
        self.ansBox1=[False,False,False]
        self.ansBox2=[False,False,False]
        self.ansPos1=[(self.width/5+17,60+87),(self.width/5+17,60+127),(self.width/5+17,60+167)]
        self.ansPos2=[(self.width/5+17,60+210+87),(self.width/5+17,60+210+127),(self.width/5+17,60+210+167)]


    def dist(self,x0,y0,x1,y1):
        return (((x1-x0)**2+(y1-y0)**2)**.5)

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
        elif (event.key=="Enter"):
            self.speech=not self.speech
        #Battle
        elif (event.key=="1"):
            self.inBattle=True
        if self.inBattle:
            if (event.key=="Enter" and self.battleEnterCount==0):
                self.kosInitMessage=True
                self.battleEnterCount+=1
            elif (event.key=="Enter" and self.battleEnterCount==1):
                self.attackChoice=True
                self.battleEnterCount+=1
            elif (self.attackChoice):
                if event.key=="a":
                    self.TAHealth+=1
                    #if (self.TAHealth>=3):
                        #self.TAlose=True
                elif event.key=="f":
                    self.codeBattleMode=True
                    #if (self.profHealth>=3):
                        #self.TAwin=True
                elif event.key=="r":
                    self.inBattle=False
            elif (event.key=="r" and (self.TAlost or self.TAwin)):
                self.appStarted()
            count=0
            if (self.codeBattleMode and event.key=="Enter"):
                print(self.testCount)
                print(self.question1)
                print(self.question2)
                print(self.question3)
                anspos1=0
                anspos2=0
                for i in range (len(self.ansBox1)):
                    if self.ansBox1[i]==True:
                        anspos1=i
                for j in range (len(self.ansBox2)):
                    if self.ansBox2[j]==True:
                        anspos2=j
                if (self.question1):
                    if self.checkForCorrect(anspos1,self.question1Ans1):
                        count+=1
                    if self.checkForCorrect(anspos2,self.question1Ans2):
                        count+=1
                elif (self.question2):
                    if self.checkForCorrect(anspos1,self.question2Ans1):
                        count+=1
                    if self.checkForCorrect(anspos2,self.question2Ans2):
                        count+=1
                elif (self.question3):
                    if self.checkForCorrect(anspos1,self.question3Ans1):
                        count+=1
                    if self.checkForCorrect(anspos2,self.question3Ans2):
                        count+=1
                if count>=2:
                    self.profHealth+=1
                elif count==1:
                    self.TAHealth+=1
                self.codeBattle()
                self.testCount=(self.testCount+1)%3

    def checkForCorrect(self,ansPos,givenAnsPos):
        if ansPos==givenAnsPos:
            return True
        return False

    def mousePressed(self,event):
        for i in range(len(self.ansPos1)):
            x,y = self.ansPos1[i]
            if self.dist(event.x, event.y, x, y) <= 7:
                self.ansBox1[i] = True
                self.ansBox1[(i+1)%3] = False
                self.ansBox1[(i-1)%3] = False
        for i in range(len(self.ansPos2)):
            x,y = self.ansPos2[i]
            if self.dist(event.x, event.y, x, y) <= 7:
                self.ansBox2[i] = True
                self.ansBox2[(i+1)%3] = False
                self.ansBox2[(i-1)%3] = False

    def madeMove(self, move):
        self.attackChoice=False
        if move=="argue":
            self.kickOut=True
        elif move=="smile":
            self.passed=True
    def timerFired(self):
        if (self.testCount==0):
            self.question1=True
            self.question2=False
            self.question3=False
        elif (self.testCount==1):
            self.question1=False
            self.question2=True
            self.question3=False
        elif (self.testCount==2):
            self.question1=False
            self.question2=False
            self.question3=True
        if (self.TAHealth>=3):
            self.TAlose=True
        if (self.profHealth>=3):
            self.TAwin=True
       
    def drawSpeech(self, canvas, text):
        canvas.create_rectangle(40,315,510,460,fill="white")
        canvas.create_image(self.width/2, self.height, anchor="s",
                            image=ImageTk.PhotoImage(self.imageText))
        
        canvas.create_text(self.width/2, self.height-90,
                           text=text,
                           font="Courier 16")
    
    def drawBattleground(self,canvas):
        canvas.create_image(self.width/2, self.height/2,
                            image=ImageTk.PhotoImage(self.battleground))
        p1=self.scaleImage(self.spritesUp[2], 2.5)
        canvas.create_image(self.width/3, 4.3*self.height/8,
                            image=ImageTk.PhotoImage(p1))
        TAHealth=self.healthbars[self.TAHealth]
        health=self.scaleImage(TAHealth, .4)
        canvas.create_image(self.width/3, 4.3*self.height/8-50,  image=ImageTk.PhotoImage(health))

        p2=self.scaleImage(self.spritesDown2[2], 1.7)
        canvas.create_image(1.7*self.width/3, 1.4*self.height/4,
                            image=ImageTk.PhotoImage(p2))
        profHealth=self.healthbars[self.profHealth]
        health=self.scaleImage(profHealth, .6)
        canvas.create_image(1.7*self.width/3, 1.4*self.height/4-60,image=ImageTk.PhotoImage(health))
        self.drawSpeech(canvas,
        "You are now facing the final boss...\nProfessor Kosbae")

    def drawWinScreen(self,canvas):
        canvas.create_text(self.width/2,self.height/2,text="TA Wins",font="Courier 30")
        ta=self.scaleImage(self.spritesDown[2], 2.5)
        canvas.create_image(self.width/5, self.height/2,
                            image=ImageTk.PhotoImage(ta))
        trop=self.scaleImage(self.winIcon, .2)
        canvas.create_image(self.width/5, self.height/2+150,
                            image=ImageTk.PhotoImage(trop))
        prof=self.scaleImage(self.spritesDown2[2], 2.5)
        canvas.create_image(4*self.width/5, self.height/2,
                            image=ImageTk.PhotoImage(prof))
        death=self.scaleImage(self.deathIcon, .6)
        canvas.create_image(4*self.width/5, self.height/2,
                            image=ImageTk.PhotoImage(death))

    def drawLoseScreen(self, canvas):
        canvas.create_text(self.width/2,self.height/2,text="TA Loses",font="Courier 30")
        ta=self.scaleImage(self.spritesDown[2], 2.5)
        canvas.create_image(self.width/5, self.height/2,
                            image=ImageTk.PhotoImage(ta))
        death=self.scaleImage(self.deathIcon, .6)
        canvas.create_image(self.width/5, self.height/2,
                            image=ImageTk.PhotoImage(death))
        prof=self.scaleImage(self.spritesDown2[2], 2.5)
        canvas.create_image(4*self.width/5, self.height/2,
                            image=ImageTk.PhotoImage(prof))
        trop=self.scaleImage(self.winIcon, .2)
        canvas.create_image(4*self.width/5, 2*self.height/3+50,
                            image=ImageTk.PhotoImage(trop))
        canvas.create_text(self.width/2,2*self.height/3,text="Press r to restart",font="Courier 20")

    def drawCodeBattle(self,canvas):
        desk=self.scaleImage(self.deskImg, 1.2)
        canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(desk))
        canvas.create_rectangle(self.width/5,20,self.width*4/5,self.height-20,fill="white")
        if (self.question1):
            canvas.create_text(self.width/2,40,text="Final Exam Part 1", font="Courier 16")
            self.drawQuestion(canvas,"1","""def checkForWin(board, player):
                                                \n        winningWord = player * 4
                                                \n        return _____""",

                                "(wordSearch(board, winningWord) != None)","(wordSearch(board, winningWord) = None)","(wordSearchFromCell(board, winningWord)",
                                self.ansBox1)
            self.drawQuestion(canvas,"2","""What is the big O of this function?\n\nL.sort()""",

                                "O(N)","O(logN)","O(NlogN)",
                                self.ansBox2)
        elif (self.question2):
            canvas.create_text(self.width/2,40,text="Final Exam Part 2", font="Courier 16")
            self.drawQuestion(canvas,"1","""def distance(x1, y1, x2, y2):
                            \n  return (_______ + (y2 - y1)**2)**0.5""",

                                "(x2 - x1)**2","(y2 + y1)**2","Ans 3",self.ansBox1)
            self.drawQuestion(canvas,"2","""Given the list L=[3,None,False], \n\nwhich of the following functions \n\n    crashes?""",
                                                
                                
                                "min(L)","L.pop(-2)","L[Carpe Diem]+1",self.ansBox2)
        elif (self.question3):
            canvas.create_text(self.width/2,40,text="Final Exam Part 3", font="Courier 16")
            self.drawQuestion(canvas,"1","""How do you access the number of 
                                     \n    columns in the 2D List L?""",
                                
                                "len(L[0)]","set(len(L[5])",":/",self.ansBox1)
            self.drawQuestion(canvas,"2","""What type of animal is Professor
                                        \n    Taylor's pet?""",
                                
                                "pig","axolotl","dragon",self.ansBox2)

    def drawQuestion(self, canvas, num, question,a1,a2,a3,ansBox):
        color=[]
        r=7
        for boo in ansBox:
            if boo==False:
                color.append("white")
            else:
                color.append("green")
        canvas.create_oval(self.width/5+17-r,60+210*(int(num)-1)+87-r,self.width/5+17+r,60+210*(int(num)-1)+87+r,fill=color[0])
        canvas.create_oval(self.width/5+17-r,60+210*(int(num)-1)+127-r,self.width/5+17+r,60+210*(int(num)-1)+127+r,fill=color[1])
        canvas.create_oval(self.width/5+17-r,60+210*(int(num)-1)+167-r,self.width/5+17+r,60+210*(int(num)-1)+167+r,fill=color[2])
        canvas.create_text(self.width/5+10,60+210*(int(num)-1), anchor="nw",text=num+".) "+ question,font="Courier 13")
        canvas.create_text(self.width/5+35,60+210*(int(num)-1)+80, anchor="nw",text=a1,font="Courier 12")
        canvas.create_text(self.width/5+35,60+210*(int(num)-1)+120, anchor="nw",text=a2,font="Courier 12")
        canvas.create_text(self.width/5+35,60+210*(int(num)-1)+160, anchor="nw",text=a3,font="Courier 12")
        
        
    def redrawAll(self, canvas):
        if not (self.TAlose or self.TAwin):
            if self.inBattle:
                self.drawBattleground(canvas)
                if (self.kosInitMessage and self.battleEnterCount==1):
                    text="Prof Kosbae: Welcome to the Final Exam ...\nwhats your first move?"
                    self.drawSpeech(canvas, text)
                elif (self.attackChoice):
                    self.drawSpeech(canvas, """What is your move?:
                                    \n- Argue (a)\n- Start the test (f)\n- Run (r)""")
                if (self.codeBattleMode):
                    self.drawCodeBattle(canvas)
                elif (self.kickOut):
                    self.drawSpeech(canvas, """You have been kicked out from 15-112,
                                            \n try harder next time""")
                elif (self.passed):
                    self.drawSpeech(canvas, """You have now passed 15-112!""")
            else:
                if self.up:
                    sprite=self.spritesUp[self.spriteCounter]
                elif self.down:
                    sprite=self.spritesDown[self.spriteCounter]
                elif self.right:
                    sprite=self.spritesRight[self.spriteCounter]
                elif self.left:
                    sprite=self.spritesLeft[self.spriteCounter]
                canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))
                TAHealth=self.healthbars[self.TAHealth]
                health=self.scaleImage(TAHealth, .2)
                canvas.create_image(self.x, self.y-20, image=ImageTk.PhotoImage(health))
                if (self.speech):
                    self.drawSpeech(canvas,"Hi, my name is TA")
        elif(self.TAwin):
            self.drawWinScreen(canvas)
        elif(self.TAlose):
            self.drawLoseScreen(canvas)


MyApp(width=544, height=480)