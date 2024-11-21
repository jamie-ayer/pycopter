import random as r

class Terrain:
    
    def __init__(self) -> None:
        length = r.randint(200, 320)
        self.coordsTop: list[int] = [800, 0, length]
        self.coordsBot: list[int] = [800, 800, -length]
        
    @property
    def coordTop(self): return self.coordsTop
    @coordTop.setter
    def coordTop(self, vals: list[int]): self.coordsTop = vals
    
    @property
    def coordBot(self): return (800 + self.coordsBot[2])
    @coordBot.setter
    def coordBot(self, vals: list[int]): self.coordsBot = vals
    
    def move(self):
        self.coordsTop[0] -= 2
        self.coordsBot[0] -= 2
        
        
        
        
        
        
    