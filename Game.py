from tkinter import *
import random as r
from Copter import *
from Terrain import *

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
        self.terrain = Terrain()
        self.terrain2Flag = False
        self.terrain2 = Terrain()
        self.canvas.delete('terrain2T')
        self.canvas.delete('terrain2B')
        self.gameoverflag = False
        
        self.game_loop()
        
    #deletes and redraws terrain per cycle
    def draw_terrain(self):
        
        coordsT = self.terrain.coordTop
        coordsB = self.terrain.coordsBot
        
        self.canvas.delete('terrainT')
        self.canvas.delete('terrainB')
        self.canvas.create_rectangle(coordsT[0], coordsT[1], coordsT[0]+80, coordsT[2], fill='black', tags='terrainT')
        self.canvas.create_rectangle(coordsB[0], coordsB[1], coordsB[0]+80, self.terrain.coordBot, fill='black', tags='terrainB')
        
        if self.terrain2Flag == True:
            coordsT = self.terrain2.coordTop
            coordsB = self.terrain2.coordsBot
            
            self.canvas.delete('terrain2T')
            self.canvas.delete('terrain2B')
            self.canvas.create_rectangle(coordsT[0], coordsT[1], coordsT[0]+80, coordsT[2], fill='black', tags='terrain2T')
            self.canvas.create_rectangle(coordsB[0], coordsB[1], coordsB[0]+80, self.terrain2.coordBot, fill='black', tags='terrain2B')
        
    #move terrain
    def move_terrain(self):
        
        self.terrain.move()
        
        if self.terrain2Flag == True:
            self.terrain2.move()
        
    #collision checks
    def check_collisions(self):
        
        #Floor/Ceiling collisions
        if self.copter.coords[1] < 0 or self.copter.coords[1] > 800:
            self.gameoverflag = True
        
        #Terrain 1 top
        if self.copter.coords[1] <= self.terrain.coordsTop[2]:
            if self.terrain.coordsTop[0] <= self.copter.coords[0]+20 <= (self.terrain.coordsTop[0]+80):
                    self.gameoverflag = True
        #Terrain 1 Bot          
        if self.copter.coords[1]+20 >= self.terrain.coordBot:
            if self.terrain.coordsTop[0] <= self.copter.coords[0]+20 <= (self.terrain.coordsTop[0]+80):
                    self.gameoverflag = True
        
        #Terrain 2 top
        if self.terrain2Flag == True:
            if self.copter.coords[1] <= self.terrain2.coordsTop[2]:
                if self.terrain2.coordsTop[0] <= self.copter.coords[0]+20 <= (self.terrain2.coordsTop[0]+80):
                    self.gameoverflag = True
            #terrain 2 bot    
            if self.copter.coords[1]+20 >= self.terrain2.coordBot:
                if self.terrain2.coordsTop[0] <= self.copter.coords[0]+20 <= (self.terrain2.coordsTop[0]+80):
                        self.gameoverflag = True
      
    #deletes and redraws copter per cycle
    def draw_copter(self):
        
        pixel = SQUARESIZE
        coords = self.copter.coord
        
        self.canvas.delete('copter')
        self.canvas.create_rectangle(coords[0], coords[1], coords[0]+pixel, coords[1]+pixel, fill='red', tags='copter')
    
    #TODO add func
    def restart(self):
        
        self.rBut.destroy()
        self.canvas.delete('GOText')
        self.game_setup()
    
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
    
    #checks location of terrain for score, also spawns terrain 2 at correct time
    def check_score(self):
        
        if self.terrain.coordsTop[0]+80 < 0:
            self.terrain = Terrain()
            
        if self.terrain2.coordsTop[0]+80 < 0:
            self.terrain2 = Terrain()
            
        if self.terrain2Flag == False:
            if self.terrain.coordsTop[0]+80 < 400:
                print('Terrain2 FLAG')
                self.terrain2Flag = True
        
        if self.terrain.coordsTop[0] == 140 or self.terrain2.coordsTop[0] == 140:
            self.score += 1
            self.score_for_label.set(f'Score: {self.score}')
        
    #functions called per game cycle
    def game_loop(self):
        
        if self.gameoverflag == False:
            if self.pv == 1:
                self.pausefunc()
                self.master.wait_variable(self.pause)
                self.unpausefunc()
            self.check_collisions()
            self.draw_terrain()
            self.draw_copter()
            self.movement()
            self.check_score()
            self.move_terrain()
            #print(self.copter)
        
            if self.gameoverflag == False:
                self.master.after(self.game_speed, self.game_loop)
            else:
                self.game_over()
        
        
        
        
        
        
        