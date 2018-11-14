# =================INIT====================
import pygame
import sys
from os import path
from settings import *
from camera import *
from time import clock
import math
# ================= BOARD INITIALIZATION ===========================

# ================================================================

# ========================= ADITIONAL VARIABLES ==================
matriz=[]
StateGame=[]
posY, posX=5,5 ## main player
Ynpc, Xnpc=1,25 # Npc with pathfinding
Xpos,Ypos=50,1 #
X_State,Y_State=5,5
state='patrol'
direction='right'

# ================================================================


# =============== FUNCTIONS TO DRAW THE INITIAL BOARD ============

class Game:

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("MINER GAME")
		pygame.key.set_repeat(500, 100)
		self.player= pygame.image.load("sprites/player.png")
		self.enemy= enemy()
		self.angle=0	
		self.camera= Camera(WIDTH, HEIGHT)
		self.clock = pygame.time.Clock()

	def isBorder(self,x,y):						
		if x == 0 and (y>=0 and y < mazeHeight):
			return True
		if x == (mazeWidth-1) and (y>=0 and y < mazeHeight):
			return True
		if y == 0 and (x>=0 and x < mazeWidth):
			return True
		if y == mazeHeight-1 and (x>=0 and x < mazeWidth):
			return True
		return False


	def drawWall(self,x,y):
		self.screen.blit(wall,(x*SCALE,y*SCALE))
		#self.screen.blit(wall,(x*SCALE,y*SCALE))

	def drawFloor(self,x,y):
		self.screen.blit(floor,(x*SCALE,y*SCALE))
		#self.screen.blit(floor,(x*SCALE,y*SCALE))


	# Draw maze walls without player or objectives
	def drawMaze(self):
		for x in range(mazeHeight):
			for y in range(mazeWidth+2):
				if matriz[x][y] == '#':
					self.drawWall(y,x)
				else:
					self.drawFloor(y,x)


	def generateScene(self):
		archivo,y= open('laberinto.txt','r'),0
		for linea in archivo.readlines():
			aux= list()
			for i in linea:
				aux.append(i)
			aux.pop()
			matriz.append(aux)
			StateGame.append(aux)
		self.screen.fill(whiteColor)
		archivo.close()
		self.drawMaze()	
		

	def drawScene(self):
		global Xnpc, Ynpc
		self.screen.fill(whiteColor)
		self.drawMaze()
		RecPlayer= pygame.Rect(posX,posY,20,25)
		#pygame.draw.rect(self.screen,(100,70,70),self.rect)
		#pygame.draw.rect(self.screen,(100,70,70),self.enemy.rect)
		self.screen.blit(self.player,(posX*SCALE,posY*SCALE))
		self.enemy.chaze(posX,posY)
		self.screen.blit(self.enemy.image,(self.enemy.posX*SCALE,self.enemy.posY*SCALE))
		pygame.display.flip()


	def isBlocked(self,cod):
		if cod==0:
			if StateGame[X_State][Y_State+1]!='#': return False
		elif cod==1:
			if StateGame[X_State+1][Y_State]!='#': return False	
		elif cod==2:
			if StateGame[X_State][Y_State-1]!='#': return False	
		elif cod==3:
			if StateGame[X_State-1][Y_State]!='#': return False	
		return True

	def event(self):
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
						g.movement(0)				
				if event.key == pygame.K_DOWN:
						g.movement(1)
				if event.key == pygame.K_LEFT:
					g.movement(2)
				if event.key == pygame.K_UP:
					g.movement(3)

	def movement(self,mov):
		global posX, posY, X_State, Y_State
		if mov==0:
			if self.isBlocked(mov)==False:    ##Move to right
				posX+=1
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,0)
				self.angle=0
				Y_State+=1
		elif mov==1:
			if self.isBlocked(mov)==False:
				posY+=1   ##move to down
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,-90)
				self.angle=-90
				X_State+=1	
		elif mov==2:
			if self.isBlocked(mov)==False:   	##Move to left
				posX-=1
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,180)
				self.angle=180
				Y_State-=1	
		elif mov==3:
			if self.isBlocked(mov)==False:		##Move to up
				posY-=1
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,90)
				self.angle=90
				X_State-=1
		self.camera.update(posX,posY)


	def run(self):
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.event()
			self.drawScene()	

# ================================================================



# ==================== ENEMY 1 ( PERSECUTION ) ==========================

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0


class  enemy:
	def __init__(self):
		self.image= pygame.image.load("sprites/enemy.png") 
		self.posX=14
		self.posY=13
		self.index=0
		self.player=Node(None,None)	
		self.angle=0

	def astar(self,maze, start, end):
	    start_node = Node(None, start)
	    start_node.g = start_node.h = start_node.f = 0
	    end_node = Node(None, end)
	    end_node.g = end_node.h = end_node.f = 0
	   
	    open_list = [] 
	    closed_list = []

	    open_list.append(start_node)
	    # Loop until you find the end
	    while len(open_list) > 0:
	      
	        current_node = open_list[0]
	        current_index = 0
	        for index, item in enumerate(open_list):
	            if item.f < current_node.f:					## Se escoge el menor heuristico
	                current_node = item
	                current_index = index
	        #print(current_node.position)
	        open_list.pop(current_index)
	        closed_list.append(current_node)
	        
	        if current_node.position == end_node.position:
	            path = []
	            current = current_node
	            while current is not None:
	                path.append(current.position)
	                current = current.parent
	            return path[::-1] 
	       
	        children = []
	        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
	            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
	            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
	                continue
	          
	            if maze[node_position[0]][node_position[1]] == '#':
	                continue
	            
	            new_node = Node(current_node, node_position)
	            
	            if new_node not in closed_list:
	            	children.append(new_node)
	        
	        for child in children:
	           
	            child.g = current_node.g + 1
	            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
	            child.f = child.g + child.h
	       
	            for open_node in open_list:
	                if child == open_node and child.g > open_node.g:
	                    continue
	            open_list.append(child)

	def distance(self,a,b,c,d):
		return abs(c-a)+ abs(d-b)
	

	def chaze(self,PlayerX,PlayerY):
		dist= self.distance(PlayerX,PlayerY,self.posX,self.posY)
		if dist<=5:
			end= (PlayerY,PlayerX)
			start= (self.posY,self.posX)
			if end!=(self.posY,self.posX):	
				path = self.astar(matriz, start, end)
				if self.posY+1==path[1][0]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,90)
					self.angle=90
				if self.posY-1==path[1][0]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,-90)
					self.angle=-90
				if self.posX+1==path[1][1]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,-180)
					self.angle=-180
				if self.posX-1==path[1][1]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,0)
					self.angle=0
				if end!=(path[1][0],path[1][1]):	
					self.posX=path[1][1]
					self.posY=path[1][0]
					self.index+=1

		







  
# index=3

# def npc(cont=3):
# 	global Xnpc, Ynpc, index
# 	start = (Ynpc, Xnpc)
# 	end = (posY, posX)
# 	path = astar(matriz, start, end)
# 	Xnpc=path[cont][1]
# 	Ynpc=path[cont][0]
# 	index-=1
# 	threading.Timer(2, npc).start()


# ================================================================




# ================= ENEMY 2 ( DECISION ) =========================





# def change_state(a,b):
# 	global state
# 	if distance(a,b)<2.0:
# 		state='shoot'
# 	else:
# 		state='patrol'


# def execute():
# 	global state, Xpos, Ypos, direction
# 	print(Xpos)
# 	if state=='patrol':
# 		if Xpos==63:
# 			direction=='left'
# 		else:
# 			direction=='right'
# 		if direction=='right':
# 			Xpos+=1
# 		elif direction=='left':
# 			Xpos-=1

# 	elif state=='shoot':
# 		print("s")
		
# ================= ENEMY 2 ( DECISION ) =========================


# ================= MAIN  ========================================



g= Game()
g.generateScene()
while True:
	g.run()


# g= Game()
# g.generateScene()
# #a = 0
# while True:	
# 	#b = clock()
# 	for event in pygame.event.get():	
# 		if event.type == pygame.QUIT:
# 			pygame.quit()
# 			sys.exit()
# 		elif event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_RIGHT:
# 					g.movement(0)				
# 			if event.key == pygame.K_DOWN:
# 					g.movement(1)
# 			if event.key == pygame.K_LEFT:
# 				g.movement(2)
# 			if event.key == pygame.K_UP:
# 				g.movement(3)
# 	while self.playing:
#             self.dt = self.clock.tick(FPS) / 1000
#             self.events()
#             self.update()
#             self.draw()
# 	g.drawScene()

# ================= MAIN  ========================================