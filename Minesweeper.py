import pygame
import random

pygame.init()

X_TILES = 30
Y_TILES = 16
TILE_SIZE = 30
WIDTH = round(X_TILES * TILE_SIZE)
HEIGHT = round(Y_TILES * TILE_SIZE)
TOTAL_MINES = 10

NUM_FONT = pygame.font.SysFont('arial', 20)
NUM_COLORS = {1: "blue", 2: "green4", 3: "red", 4: "dodgerblue4", 5: "firebrick4", 6: "cyan4", 7: "black", 8: "grey"}
BG_COLOR = "white"
RECT_COLOR = "lightgrey"
BORDER_COLOR = "black"
CLICKED_RECT_COLOR = "darkgray"
FLAG_COLOR = "deeppink4"
BOMB_COLOR = "black"

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

def get_grid_pos(mouse_pos):
    """ Get the grid column and row of the current tile
    the player has clicked. """
    mouse_x, mouse_y = mouse_pos
    col = int(mouse_x // TILE_SIZE)
    row = int(mouse_y // TILE_SIZE)

    return col, row

def makeGrid(col, row):
    """ Make a 2D grid with column and rows. """
    return [[Tile(i*TILE_SIZE, j*TILE_SIZE) for j in range(row)] for i in range(col)]
    
def drawGrid(grid):
    """ Draw the tiles of the grid. """
    for col in range(0, X_TILES):
        for row in range(0, Y_TILES):
            tile = grid[col][row]
            tile.drawTile()

def main():
    """ Runs the game. """
    run = True
    
    window.fill(BG_COLOR)
    grid = makeGrid(X_TILES, Y_TILES)
    drawGrid(grid)
    
    while run:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()

class Tile:
    def __init__(self, xPos, yPos) -> None:
        """ Initialise the values of the tile """
        self.xPos = xPos
        self.yPos = yPos
        self.isOpen = False
        self.isFlagged = False
        self.hasMine = False
        self.nearbyMines = 0
        
    def drawTile(self):
        """ Draw the tile onto the window. """
        pygame.draw.rect(window, RECT_COLOR, (self.xPos, self.yPos, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(window, BORDER_COLOR, (self.xPos, self.yPos, TILE_SIZE, TILE_SIZE), 1)
        
if __name__ == "__main__":
    main()