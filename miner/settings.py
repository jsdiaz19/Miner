import pygame

WIDTH = 1200
HEIGHT = 680
SCALE=40
pixelUnit= SCALE+5
mazeWidth = 76
mazeHeight = 19
FPS = 5

widthCamera= 27*SCALE
heightCamera= 12*SCALE
whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)
wall= pygame.image.load("sprites/wall.png")
wall = pygame.transform.scale(wall, (SCALE,SCALE))
floor= pygame.image.load("sprites/floor.png")
floor = pygame.transform.scale(floor, (SCALE,SCALE))