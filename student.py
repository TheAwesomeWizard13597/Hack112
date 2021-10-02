
class student():
    def __init__(self, xpos, ypos, sleepLevel):
        self.xpos = xpos
        self.ypos = ypos
        self.fatness = 5
        self.tallness = 10
        self.sleepLevel = sleepLevel
        self.undertanding = 0
        self.affinity = 0
        self.anxietyLevel = 0
        self.isAlive = True
        self.width = 10
        self.height = 10
        self.speed = 5
    
    def move(self, direction):
        if direction == "up":
            self.ypos -= self.speed
        elif direction == "down":
            self.ypos += self.speed
        elif direction == "right":
            self.xpos += self.speed
        elif direction == "left":
            self.xpos -= self.speed

    def explain(self, qualOfExplaination): #qualOfExplanation is the Quality of Explanation from 1-5 (just like the recitation polls)
        self.understanding += qualOfExplaination * self.affinity
        if qualOfExplanation < 3:
            self.anxietyLevel += 1
        elif qualOfExplanation == 5:
            self.anxietylevel -= 1
        pass

    def exam(self, difficulty): #Difficulty is a property of each exam
        ability = self.understanding * self.sleepLevel * (1/self.anxietyLevel)
        if ability > difficulty:
            self.anxietyLevel -= 1
            return True
        else:
            self.anxietyLevel += 1
            return False
    
    def sleep(self, quality): 
        self.sleepLevel += quality
        if quality >= 8:
            self.anxietyLevel -= 1


    def noSleep(self):
        if self.sleepLevel == 0:
            self.anxietylevel += 1       
        else:
            self.sleepLevel -= 1 
    
    def social(self, effectiveness): #Effectiveness is a property of the social event, and can be negative
        self.affinity += effectiveness
    


    
    
    
    