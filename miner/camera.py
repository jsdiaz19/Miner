import pygame
from settings import *

class Camera:
	def __init__(self,width,height):
		self.camera= pygame.Rect(0,0,WIDTH, HEIGHT)
		self.width=width
		self.height=height

	def apply(self, entity):
		return entity.move(self.camera.topleft)

	def update(self,x,y):
		self.camera = pygame.Rect(x, y,WIDTH, HEIGHT)
