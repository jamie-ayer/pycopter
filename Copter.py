class Copter:
    
    def __init__(self) -> None:
        self.coords: list[int] = [180, 340]
        self.acceleration: int = 0
        
    @property
    def coord(self): return self.coords
    @coord.setter
    def coord(self, vals: list): self.coords = vals
    
    @property
    def acc(self): return self.acceleration
    @acc.setter
    def acc(self, val: int): self.acceleration = val
    
    def up(self):
        if self.acceleration > 0:
            self.acceleration = 0
        self.acceleration -= 10
        self.coords[1] += self.acceleration
    def down(self):
        self.acceleration += 1
        self.coords[1] += self.acceleration
        
    def __str__(self) -> str:
        return f'Copter accel: {self.acceleration} | Y axis: {self.coords[1]}'