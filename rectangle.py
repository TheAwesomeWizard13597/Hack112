
class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

class Rectangle:
    def __init__(self, x1, y1, x2, y2, color=""):
        self.l1 = Point(x1,y1) 
        self.r1 = Point(x2, y2) 
        self.color = color

    def intersects(self, other): 
        if(self.l1.x >= other.r1.x or other.l1.x >= self.r1.x): 
            return False
        if(self.l1.y >= other.r1.y or other.l1.y >= self.r1.y): 
            return False
        return True
    
    def draw(self,canvas):
        canvas.create_rectangle(self.l1.x,self.l1.y,self.r1.x,self.r1.y,fill = self.color)