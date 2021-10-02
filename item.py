class item():
    def __init__(self, functionality, effectiveness):
        self.amount = 0
        self.functionality = functionality
        self.effectiveness = effectiveness

    def used(self, amount):
        self.amount -= amount
        return self.functionality, self.effectiveness
    
    def upgrade(self, effective):
        self.effectiveness += effective
    
    