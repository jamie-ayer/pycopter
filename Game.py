from tkinter import *
import random as r
from Copter import *

SQUARESIZE = 20

class Game:
    
    def __init__(self, root: Tk) -> None:
        
        self.master = root
        self.width = 800
        self.height = 800
        self.game_speed = 20
        self.copter_had_movement = False
        self.pv = 0
        self.pause = StringVar()
        self.pause.set('0')
        self.master.bind('<Key>', self.bump)
        
        self.game_frame_init()
        self.game_setup()
        
    #draws init game board
    def game_frame_init(self):
        
        self.canvas = Canvas(self.master, background='white', width=self.width, height=self.height+20)
        
        self.score_for_label = StringVar()
        Label(self.master, textvariable=self.score_for_label).place(x=150, y=800)
        
        for line in range(0, self.width, 20):
            self.canvas.create_line([(line, 0), (line, self.height)], fill='black', tags='grid_line_w')
        for line in range(0, self.height, 20):
            self.canvas.create_line([(0, line), (self.width, line)], fill='black', tags='grid_line_h')
            
        self.canvas.grid(row=0, column=0)
        
    #keybinding logic
    def bump(self, event):
        
        if event.char == ' ':
            self.copter_had_movement = True
        if event.char == 'p':
            print('pause button pressed')
            if self.pv == 0: 
                self.pause.set(1)
                self.pv = 1   
            elif self.pv == 1: 
                self.pause.set(0)
                self.pv = 0 
                
    #calls the up or down Copter class methods based on Key pressed
    def movement(self):
        
        if self.copter_had_movement:
            self.copter.up()
            self.copter_had_movement = False
        else:
            self.copter.down()
        
    #sets up game vars and objs
    def game_setup(self):
        
        self.score = 0
        self.score_for_label.set(f'Score: {self.score}')
        
        self.copter = Copter()
        self.gameoverflag = False
        self.direction = 'Down'
        
        self.game_loop()
        
    #deletes and redraws copter per cycle
    def draw_copter(self):
        
        pixel = SQUARESIZE
        coords = self.copter.coord
        
        self.canvas.delete('copter')
        self.canvas.create_rectangle(coords[0], coords[1], coords[0]+pixel, coords[1]+pixel, fill='red', tags='copter')
    
    #TODO add func
    def restart(self):
        pass
    
    #Displays game over and restart button
    def game_over(self):
        
        self.canvas.create_text(400, 400, text='Game Over', fill='red', font=('Helvetica', 30), tags='GOText')
        self.rBut = Button(self.canvas, text='restart', fg='black', command=self.restart)
        self.rBut.place(x=300, y=500)
        
    #pauses game and shows the coord of each box
    def pausefunc(self):
        print(f'GAME PAUSED pv: {self.pv}')
        c = 0
        for x in range(0, 800, 20):
            for y in range(0, 800, 20):
                self.canvas.create_text(x+10, y+10, text=f'{x//10},{y//10}', fill='black', font=('Helvetica', 7), tags=f'B{c}')
                c+=1
    
    #after pause, deletes the box coord texts
    def unpausefunc(self):
        for t in range(1600):
            self.canvas.delete(f'B{t}')
    
    #functions called per game cycle
    def game_loop(self):
        
        if self.gameoverflag == False:
            if self.pv == 1:
                self.pausefunc()
                self.master.wait_variable(self.pause)
                self.unpausefunc()
                
            self.draw_copter()
            self.movement()
            #print(self.copter)
        
            if self.gameoverflag == False:
                self.master.after(self.game_speed, self.game_loop)
            else:
                self.game_over()
        
        
        
        
        
        
        