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
		pygame.font.init()
		self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("MINER GAME")
		pygame.key.set_repeat(500, 100)
		self.player=player()
		self.enemy= enemy()
		self.camera= Camera(WIDTH, HEIGHT)
		self.clock = pygame.time.Clock()
		self.move=0

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
			for y in range(self.move,mazeWidth+2):
				if matriz[x][y] == '#':
					self.drawWall(y-self.move,x)
				else:
					self.drawFloor(y-self.move,x)


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
		#print(self.move)
		self.screen.fill(whiteColor)
		self.drawMaze()
		RecPlayer= pygame.Rect(posX,posY,20,25)
		#pygame.draw.rect(self.screen,(100,70,70),self.player.rectPlayer)
		self.screen.blit(self.player.player,((posY-self.move)*SCALE,posX*SCALE))
		self.enemy.chaze(posX,posY)
		 #pygame.draw.rect(self.screen,(70,70,70),self.enemy.rectEnemy)
		self.screen.blit(self.enemy.image,((self.enemy.posX-self.move)*SCALE,self.enemy.posY*SCALE))
		if self.player.health<=30:
			pygame.draw.rect(self.screen,RED,[950, 10, 2*self.player.health, 20])

		elif self.player.health>30 and self.player.health<=60:
			pygame.draw.rect(self.screen,YELLOW,[950, 10, 2*self.player.health, 20])

		elif self.player.health>60:
			pygame.draw.rect(self.screen,GREEN,[950, 10, 2*self.player.health, 20])
		textsurface = self.myfont.render(str(self.player.health), False, (0, 0, 0))
		self.screen.blit(textsurface,(900,0))
		pygame.display.update()

	def run(self):
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.player.event(self.enemy.rectEnemy)
			self.drawScene()
			if self.player.health==0:
				pygame.quit()
				sys.exit()

# ======================== MAIN PLAYER ========================================================================

class player:
	def __init__(self):
		self.player= pygame.image.load("sprites/player.png")
		self.rectPlayer = self.player.get_rect(topleft=(posX*SCALE,posY*SCALE))
		self.angle=0
		self.health=100

	def event(self,enemy):
		global posY, posX
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:     ##Derecha
						self.movement(0,enemy)
								
				if event.key == pygame.K_DOWN:      ## Abajo
						self.movement(1,enemy)
				if event.key == pygame.K_LEFT:		##Izquierda
					self.movement(2,enemy)	
				if event.key == pygame.K_UP:		##Arriba
					self.movement(3,enemy)

	def isBlocked(self,cod):
		if cod==0:
			if matriz[posX][posY+1]!='#': 
				if g.move<=47:
					g.move+=1	
				return False
		elif cod==1:
			if matriz[posX+1][posY]!='#': return False	
		elif cod==2:
			if matriz[posX][posY-1]!='#':
				if g.move-1>=0:
					g.move-=1 
				return False	
		elif cod==3:
			if matriz[posX-1][posY]!='#': return False	
		return True


	def movement(self,mov,enemy):
		global posX, posY, X_State, Y_State
		if mov==0:
			if self.isBlocked(mov)==False:    ##Move to right
				
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,0)
				self.angle=0
				if posY+1!=g.enemy.posX or posX!=g.enemy.posY:
					self.rectPlayer.x+=SCALE
					posY+=1

		elif mov==1:
			if self.isBlocked(mov)==False:
				   ##move to down
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,-90)
				self.angle=-90
				if posY!=g.enemy.posX or posX+1!=g.enemy.posY:
					self.rectPlayer.y+=SCALE
					posX+=1
				
		elif mov==2:
			if self.isBlocked(mov)==False:   	##Move to left
				
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,180)
				self.angle=180
				if posY-1!=g.enemy.posX or posX!=g.enemy.posY:
					self.rectPlayer.x-=SCALE	
					posY-=1
					
		elif mov==3:
			if self.isBlocked(mov)==False:		##Move to up
				
				self.player= pygame.transform.rotate(self.player,-self.angle)
				self.player= pygame.transform.rotate(self.player,90)
				self.angle=90
				if posY!=g.enemy.posX or posX-1!=g.enemy.posY:
					self.rectPlayer.y-=SCALE	
					posX-=1

					


# ==================== ENEMY 1 ( PERSECUTION ) ==========================================================

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
		self.rectEnemy = self.image.get_rect(topleft=(self.posX*SCALE,self.posY*SCALE))
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
	
	def neighbors(self,x,y,X,Y):
		if x==X and abs(y-Y)==1:
			return True
		elif y==Y and abs(x-X)==1:
			return True
		else:
			return False


	def chaze(self,PlayerX,PlayerY):
		dist= self.distance(PlayerY,PlayerX,self.posX,self.posY)

		if dist<=3:
			if self.neighbors(PlayerY,PlayerX,self.posX,self.posY):
				self.image= pygame.image.load("sprites/attack.png") 
				self.image= pygame.transform.rotate(self.image,self.angle)
				g.player.health-=10
			else:
				self.image= pygame.image.load("sprites/enemy.png") 
				self.image= pygame.transform.rotate(self.image,self.angle)
				end= (PlayerX,PlayerY)
				start= (self.posY,self.posX)	
				
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
					self.rectEnemy.y=self.posY*SCALE
					self.rectEnemy.x=self.posX*SCALE
			
				
				

		







  
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