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
		self.enemy2= enemy2()
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
		self.screen.blit(self.player.player,(posY*SCALE,posX*SCALE))

		self.enemy.chaze(posX,posY)
		self.screen.blit(self.enemy.image,(self.enemy.posX*SCALE,self.enemy.posY*SCALE))

		self.enemy2.chaze(posX,posY)
		self.screen.blit(self.enemy2.image,(self.enemy2.posX*SCALE,self.enemy2.posY*SCALE))
		
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
			if matriz[posX][posY+1]!='#': return False
		elif cod==1:
			if matriz[posX+1][posY]!='#': return False	
		elif cod==2:
			if matriz[posX][posY-1]!='#':return False	
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

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
    	heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)

    def print(self):
    	for temp in self.elements:
    		print(temp[0],temp[1].position)

    def content(self,item):
    	for temp in self.elements:
    		if temp[1]==item:
    			return True
    	return False


class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.f = 0
    def __lt__(self, other):
    	return self.f < other.f

class  enemy:
	def __init__(self):
		self.image= pygame.image.load("sprites/enemy.png") 
		self.posX=13
		self.posY=1
		self.rectEnemy = self.image.get_rect(topleft=(self.posX*SCALE,self.posY*SCALE))
		self.index=0
		self.player=Node(None,None)	
		self.angle=0

	def heuristic(self,a, b):
		(x1, y1) = a
		(x2, y2) = b
		return abs(x1 - x2) + abs(y1 - y2)

	def astar(self,maze, poStart,end):
		frontier= PriorityQueue()
		Start=Node(None,poStart)
		Start.f=self.heuristic(poStart,end)
		frontier.put(Start,0)
		finish=0
		visited=[]
		while finish!=1:
			temp=frontier.get()
			visited.append(temp[1].position)
			if (temp[1].position==end):
				finish=1
				path=[]
				current=temp[1]
				while current.parent is not None:
					path.append(current.position)
					current=current.parent[1]
				path=path[::-1] 
				return path 		
			else:
				children=[]
				for neighbors in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
					new_pos=(temp[1].position[0]+neighbors[0],temp[1].position[1]+neighbors[1])
					if new_pos[0]>mazeHeight or new_pos[1]>mazeWidth or new_pos[0]<0 or new_pos[1]<0:
						continue
					if maze[new_pos[0]][new_pos[1]]=='#':
						continue
					if new_pos in visited or frontier.content(new_pos)==True:
						continue
					nodo=Node(temp,new_pos)
					nodo.f= self.heuristic(poStart,new_pos)+self.heuristic(new_pos,end)
					frontier.put(nodo,nodo.f)

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
		if dist<=9:
			if self.neighbors(PlayerY,PlayerX,self.posX,self.posY):
				self.image= pygame.image.load("sprites/attack.png") 
				self.image= pygame.transform.rotate(self.image,self.angle)
				g.player.health-=10
			else:
				self.image= pygame.image.load("sprites/enemy.png") 
				self.image= pygame.transform.rotate(self.image,self.angle)
				end= (PlayerX,PlayerY)
				start= (self.posY,self.posX)	
				path = self.astar(matriz,start,end)	
				print(path)
				if self.posY+1==path[0][0] :
					print("entro11")
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,90)
					self.angle=90
				if self.posY-1==path[0][0]:
					print("entro12")
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,-180)
					self.angle=-90
				if self.posX+1==path[0][1]:
					print("entro13")
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,-180)
					self.angle=-180
				if self.posX-1==path[0][1]:
					print("entro14")
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,0)
					self.angle=0
				if end!=(path[0][0],path[0][1]):
					self.posX=path[0][1]
					self.posY=path[0][0]	
					self.rectEnemy.y=self.posY*SCALE
					self.rectEnemy.x=self.posX*SCALE
			
# =====================================================================================================				
				
# ==================== ENEMY 2 ( PERSECUTION ) ==========================================================
		
class enemy2:
	def __init__(self):
		self.image= pygame.image.load("sprites/enemy_2.png") 
		self.posX=14
		self.posY=13
		self.rectEnemy = self.image.get_rect(topleft=(self.posX*SCALE,self.posY*SCALE))
		self.index=0
		self.player=Node(None,None)	
		self.angle=0

	def heuristic(self,a, b):
		(x1, y1) = a
		(x2, y2) = b
		return abs(x1 - x2) + abs(y1 - y2)

	def distance(self,a,b,c,d):
		return abs(c-a)+ abs(d-b)

	def neighbors(self,x,y,X,Y):
		if x==X and abs(y-Y)==1:
			return True
		elif y==Y and abs(x-X)==1:
			return True
		else:
			return False

	def dijkstra_search(self,maze, poStart, end):
	    frontier= PriorityQueue()
	    Start=Node(None,poStart)
	    Start.f=self.heuristic(poStart,end)
	    frontier.put(Start,0)
	    finish=0
	    visited=[]
	    while finish!=1:
	    	temp=frontier.get()
	    	visited.append(temp[1].position)
	    	if (temp[1].position==end):
	    		finish=1
	    		path=[]
	    		current=temp[1]
	    		while current.parent is not None:
	    			path.append(current.position)
	    			current=current.parent[1]
	    		path=path[::-1]
	    		#print(path) 
	    		return path 		
	    	else:
	    		children=[]
	    		for neighbors in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
	    			new_pos=(temp[1].position[0]+neighbors[0],temp[1].position[1]+neighbors[1])
	    			if new_pos[0]>mazeHeight or new_pos[1]>mazeWidth or new_pos[0]<0 or new_pos[1]<0:
	    				continue
	    			if maze[new_pos[0]][new_pos[1]]=='#':
	    				continue
	    			if new_pos in visited or frontier.content(new_pos)==True:
	    				continue
	    			nodo=Node(temp,new_pos)
	    			nodo.f= temp[1].f+1
	    			frontier.put(nodo,nodo.f)
	    		#frontier.print()
	    		#print("---------------")

	def chaze(self,PlayerX,PlayerY):
		dist= self.distance(PlayerY,PlayerX,self.posX,self.posY)
		if dist<=9:
			if self.neighbors(PlayerY,PlayerX,self.posX,self.posY):
				print("entro")
				self.image= pygame.image.load("sprites/enemy2.png") 
				self.image= pygame.transform.rotate(self.image,self.angle)
				g.player.health-=10
			else:
				self.image= pygame.image.load("sprites/enemy_2.png") 
				self.image= pygame.transform.rotate(self.image,self.angle)
				end= (PlayerX,PlayerY)
				start= (self.posY,self.posX)	
				path = self.dijkstra_search(matriz,start,end)
				
				if self.posY+1==path[0][0]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,90)
					self.angle=90
				if self.posY-1==path[0][0]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,-90)
					self.angle=-90
				if self.posX+1==path[0][1]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,-180)
					self.angle=-180
				if self.posX-1==path[0][1]:
					self.image= pygame.transform.rotate(self.image,-self.angle)
					self.image= pygame.transform.rotate(self.image,0)
					self.angle=0
				if end!=(path[0][0],path[0][1]):
					self.posX=path[0][1]
					self.posY=path[0][0]	
					self.rectEnemy.y=self.posY*SCALE
					self.rectEnemy.x=self.posX*SCALE

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