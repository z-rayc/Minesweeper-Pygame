import pygame
import random
from queue import Queue

pygame.init()

X_TILES = 10
Y_TILES = 5
TILE_SIZE = 10
TOTAL_MINES = 10

NUM_FONT = pygame.font.SysFont('arial', 20)
NUM_COLORS = {1: "blue", 2: "green4", 3: "red", 4: "dodgerblue4", 5: "firebrick4", 6: "cyan4", 7: "black", 8: "grey"}
RECT_COLOR = "lightgrey"
CLICKED_RECT_COLOR = "darkgray"
FLAG_COLOR = "deeppink4"
BOMB_COLOR = "black"

window = pygame.display.set_mode((X_TILES*TILE_SIZE, Y_TILES*TILE_SIZE))
pygame.display.set_caption("Minesweeper")

def makeGrid():
    return [[Tile(i*TILE_SIZE, j*TILE_SIZE) for i in range(X_TILES)] for j in range(Y_TILES)]

def main():
    grid = makeGrid()
    print(f"Grid expected xPos and yPos: [10, 10]. Actual: [{grid[1][1].xPos}, {grid[1][1].yPos}]")
    pygame.quit()

class Tile:
    def __init__(self, xPos, yPos) -> None:
        self.xPos = xPos
        self.yPos = yPos
        self.isOpen = False
        self.isFlagged = False
        self.hasMine = False
        self.nearbyMines = 0
        
    def drawTile(self):
        pygame.draw.rect(window, RECT_COLOR, (self.xPos, self.yPos, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(window, "black", (self.xPos, self.yPos, TILE_SIZE, TILE_SIZE), 1)
        
if __name__ == "__main__":
    main()