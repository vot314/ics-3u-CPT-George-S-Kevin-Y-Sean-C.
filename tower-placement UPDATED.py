
'''
This program allows the user to place towers. When selecting a 
 tower and trying to place it, affected  tiles will display GREEN if 
 placement is allowed, else it will display RED for any tiles that 
 are already occupied.

+=+ NOTES +=+
- The grid is made up of 20 x 20 pixel squares
- Left click to place
- WIDTH and HEIGHT should preferably both be multiples of 20
- towerSize controls the size of the towers (any POSITIVE integer 
    value will work). All shapes are n x n squares (no rectangles)
'''

import pygame
import random
import math
from pygame import mouse

# ==========
# OBJECTS
# ==========

# Define point and structure classes
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def call(self):
        return [self.x, self.y]
    
    def move(self, dx, dy):
        return [self.x + dx, self.y + dy]
    
    def moveX(self, dx, dy):
        return self.x + dx
    
    def moveY(self, dx, dy):
        return self.y + dy

    def snapToGrid(self):
       self.x = round(self.x/20)
       self.y = round(self.y/20)

class structure:
    Health = 0
    buildTime = 0

    def __init__(self, location: point, size):
        self.size = size
        self.location = location
    
    # Checks if the location collides with an existing structure
    def checkCollision(self, occupiedTiles):
        canBePlaced = True
        for coordinate in centeredMatrix(self.size):
            if self.location.move(*coordinate) in occupiedTiles:
                canBePlaced = False
        return canBePlaced
    
    # Returns the locations of all conflicting tiles within build zone
    def findOverlapping(self, occupiedTiles):
        tileOverlaps = []
        for coordinate in centeredMatrix(self.size):
            if self.location.move(*coordinate) in occupiedTiles:
                tileOverlaps.append(self.location.move(*coordinate))
        return tileOverlaps
    
    # Returns the locations of all non-conflicting tiles within build zone
    def findPlaceableTiles(self, occupiedTiles):
        availableTiles = []
        for coordinate in centeredMatrix(self.size):
            if self.location.move(*coordinate) not in occupiedTiles:
                availableTiles.append(self.location.move(*coordinate))
        return availableTiles

# ==========
# FUNCTIONS
# ==========

# Returns each coordinate in an n x n matrix in a list, with the origin as the center:
# Note: for even values of n, the matrix is shifted up and to the left
# This is to make up for the fact that the cursor blocks a bit of the bottom right
def centeredMatrix(n: int):
    coords = []
    lowerBound = -int(n/2)
    upperBound = n + lowerBound
    for x in range(lowerBound, upperBound):
        for y in range(lowerBound, upperBound):
            coords.append([x,y])
    return coords

# ==========
# MAIN CODE
# ==========

pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

grid = [[0]*int(WIDTH/20)]*int(HEIGHT/20)
occupiedTiles = []
structureList = []

towerSize = 3
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Attempts to place a tower on clicked location
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # When a tile is clicked, its location is snapped to grid and converted to structure object
            clickedTile = point(*event.pos)
            clickedTile.snapToGrid()
            clickedTile = structure(clickedTile, towerSize)
            if clickedTile.checkCollision(occupiedTiles):
                for coordinate in centeredMatrix(clickedTile.size):
                    occupiedTiles.append(clickedTile.location.move(*coordinate))
                structureList.append(clickedTile)

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    mouseGrid = point(*pygame.mouse.get_pos())
    mouseGrid.snapToGrid()

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    # Draw a BLUE tile for each occupied tile
    for tile in structureList: # returns as a STRUCTURE
        for coordinate in centeredMatrix(tile.size):
            pygame.draw.rect(screen, (25,25,255), (20 * (tile.location.moveX(*coordinate))-10, 20 * (tile.location.moveY(*coordinate))-10,20,20))

    # Draw a RED tile around the cursor if placement is impossible
    for tile in structure(mouseGrid, towerSize).findOverlapping(occupiedTiles): # returns as a LIST, not a POINT
        pygame.draw.rect(screen, (255, 50, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))

    # Draw a GREEN tile around the cursor if placement is possible
    for tile in structure(mouseGrid, towerSize).findPlaceableTiles(occupiedTiles): # returns as a LIST, not a POINT
        pygame.draw.rect(screen, (50, 255, 50), (20 * tile[0]-10, 20 * tile[1]-10,20,20))

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
