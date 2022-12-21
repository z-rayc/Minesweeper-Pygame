import pygame
import random

pygame.init()

X_TILES = 10
Y_TILES = 10
TILE_SIZE = 40
WIDTH = X_TILES * TILE_SIZE
HEIGHT = Y_TILES * TILE_SIZE
TOTAL_MINES = 10

SAFE_TILES = X_TILES * Y_TILES - TOTAL_MINES
OPENED_TILES = 0

NUM_FONT = pygame.font.SysFont('ebrima', 20)
NUM_COLORS = {1: "blue", 2: "green4", 3: "red", 4: "dodgerblue4", 5: "firebrick4", 6: "cyan4", 7: "black", 8: "grey"}
TEXT_FONT = pygame.font.SysFont('arialblack', 30)
TEXT_COLOR = "white"

BG_COLOR = "white"
TILE_COLOR = "lightgrey"
BORDER_COLOR = "black"
OPEN_TILE_COLOR = "darkgray"
FLAG_COLOR = "deeppink4"
MINE_COLOR = "black"

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

def get_grid_pos(mouse_pos):
    """ Get the grid column and row of the current 
    tile the player has clicked. """
    mouse_x, mouse_y = mouse_pos
    col = int(mouse_x // TILE_SIZE)
    row = int(mouse_y // TILE_SIZE)

    return col, row

def make_grid(col, row):
    """ Make a 2D grid with column and rows. """
    return [[Tile(i*TILE_SIZE, j*TILE_SIZE) for j in range(row)] for i in range(col)]
    
def draw_grid(grid):
    """ Draw the tiles of the grid. """
    for col in range(0, X_TILES):
        for row in range(0, Y_TILES):
            tile = grid[col][row]
            tile.draw_tile()
            
def get_neighbours(grid, tile):
    """ Get all neighbours of the given tile. """
    neighbours = []
    
    points = [[-1, -1], # Top left
              [-1, 0],  # Top center
              [-1, 1],  # Top right
              [0, -1],  # Middle left
              [0, 1],   # Middle right
              [1, -1],  # Bottom left
              [1, 0],   # Bottom center
              [1, 1]]   # Bottom right
    
    for i in range(0, len(points)):
        # The relative col and row positions of a neighbouring tile
        d_x = points[i][0]
        d_y = points[i][1]
        
        # The absolute col and row positions of a neighbouring tile
        grid_x = (tile.x_pos // TILE_SIZE) + d_x
        grid_y = (tile.y_pos // TILE_SIZE) + d_y
        
        # Check if the new positions are within the grid
        if (grid_x >= 0 and grid_x < X_TILES) and (grid_y >= 0 and grid_y < Y_TILES):
            neighbours.append(grid[grid_x][grid_y])
            
    return neighbours
    
def get_all_tiles(grid):
    """ Get all the tiles of the grid. """
    tiles = []
    
    for col in range(0, X_TILES):
        for row in range(0, Y_TILES):
            tiles.append(grid[col][row])
            
    return tiles

def generate_mines(grid, tile):
    """ Place mines randomly on tiles other than
    the given tile, and its neighbours. """
    tiles = get_all_tiles(grid)
    
    # Remove given tile and its neighbours
    tiles.remove(tile)
    neighbours = get_neighbours(grid, tile)
    for i in range(0, len(neighbours)):
        tiles.remove(neighbours[i])
    
    unplaced_mines = TOTAL_MINES
    
    while unplaced_mines != 0:
        num = random.randrange(0, len(tiles))
        
        if tiles[num].has_mine == False:
            tiles[num].has_mine = True
            unplaced_mines -= 1
    
def get_nearby_mines(grid, tile):
    """ Get the amount of mines from 
    the given tile's neighbours. """
    neighbours = get_neighbours(grid, tile)
    nearby_mines = 0
    
    for i in range(0, len(neighbours)):
        if neighbours[i].has_mine == True:
            nearby_mines += 1
            
    return nearby_mines
    
def set_nearby_mines(grid):
    """ Set the number of nearby mines
    for all the tiles in the grid. """
    for col in range (0, X_TILES):
        for row in range (0, Y_TILES):
            tile = grid[col][row]
            nearby_mines = get_nearby_mines(grid, tile)
            tile.nearby_mines = nearby_mines

def get_unopened_neighbours(grid, tile):
    """ Get allt the tile's neighbours which
    are not opened. """
    return list(filter(lambda x: (x.is_open == False), get_neighbours(grid, tile)))

def open_neighbour_tiles(grid, tile):
    """ Open the tile's neighbouring tiles. """
    neighbours = get_unopened_neighbours(grid, tile)
    
    for i in range(0, len(neighbours)):
        current_tile = neighbours[i]
        
        if current_tile.is_open == False and current_tile.is_flagged == False:
            current_tile.open_tile()
            global OPENED_TILES
            OPENED_TILES += 1
        
        if current_tile.nearby_mines == 0:
            open_neighbour_tiles(grid, current_tile)

def draw_center_text(text):
    """ Draw some text in the center of the window. """
    text = TEXT_FONT.render(text, 1, TEXT_COLOR)
    pygame.draw.rect(window, BORDER_COLOR, (0, HEIGHT/2 - text.get_height()/2, X_TILES*TILE_SIZE, text.get_height()))
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()

def get_nearby_flags(grid, tile):
    return list(filter(lambda x: (x.is_flagged == True), get_neighbours(grid, tile)))

def open_all_mines(grid):
    unopened_mine_tiles = list(filter(lambda x: (x.has_mine == True and x.is_open == False), get_all_tiles(grid)))
    for i in range(0, len(unopened_mine_tiles)):
        unopened_mine_tiles[i].open_tile()

def flag_all_mines(grid):
    unflagged_mine_tiles = list(filter(lambda x: (x.has_mine == True and x.is_flagged == False), get_all_tiles(grid)))
    for i in range(0, len(unflagged_mine_tiles)):
        unflagged_mine_tiles[i].toggle_flag()
        
def open_all_safe_tiles(grid):
    unopened_safe_tiles = list(filter(lambda x: (x.has_mine == False and x.is_open == False), get_all_tiles(grid)))
    for i in range(0, len(unopened_safe_tiles)):
        unopened_safe_tiles[i].open_tile()
        
def main():
    """ Runs the game. """
    is_running = True
    has_first_click = True
    global is_defeated
    is_defeated = False
    
    window.fill(BG_COLOR)
    grid = make_grid(X_TILES, Y_TILES)
    draw_grid(grid)
    
    while is_running:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE: # Space-bar is let up
                    col, row = get_grid_pos(pygame.mouse.get_pos())
                    marked_tile = grid[col][row]
                    
                    if marked_tile.is_open == False: # Flag tile
                        marked_tile.toggle_flag()
                    else: # Reveal neighbours
                        if len(get_nearby_flags(grid, marked_tile)) == marked_tile.nearby_mines:
                            open_neighbour_tiles(grid, marked_tile)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                col, row = get_grid_pos(pygame.mouse.get_pos())
                
                if col >= X_TILES or row >= Y_TILES:
                    continue
                
                clicked_tile = grid[col][row]
                
                if mouse_pressed[0]: # Right click
                    if has_first_click == True:
                        generate_mines(grid, clicked_tile)
                        set_nearby_mines(grid)
                    
                    if clicked_tile.is_open == False and clicked_tile.is_flagged == False:
                        clicked_tile.open_tile()
                        global OPENED_TILES
                        OPENED_TILES += 1
                        
                        if clicked_tile.nearby_mines == 0 and clicked_tile.has_mine == False:
                            open_neighbour_tiles(grid, clicked_tile)
                    
                    has_first_click = False
                    
                elif mouse_pressed[2]: # Left click
                    if clicked_tile.is_open == False:
                        clicked_tile.toggle_flag()
            
            if OPENED_TILES == SAFE_TILES:
                open_all_safe_tiles(grid)
                flag_all_mines(grid)
                pygame.display.update()
                pygame.time.delay(500)
                
                # TODO: Reset the board and start a new game
                draw_center_text("Congrats, you win!")
                pygame.time.delay(4000)
                is_running = False
            
            if is_defeated == True:
                open_all_mines(grid)
                pygame.display.update()
                pygame.time.delay(500)
                
                draw_center_text("You lost. Try again!")
                pygame.time.delay(4000)
                is_running = False
            
    pygame.quit()
    
class Tile:
    def __init__(self, x_pos, y_pos) -> None:
        """ Initialise the values of the tile. """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_open = False
        self.is_flagged = False
        self.has_mine = False
        self.nearby_mines = 0
        
    def draw_tile(self):
        """ Draw the tile onto the window. """
        pygame.draw.rect(window, TILE_COLOR, (self.x_pos, self.y_pos, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(window, BORDER_COLOR, (self.x_pos, self.y_pos, TILE_SIZE, TILE_SIZE), 1)
        
    def open_tile(self):
        """ Draw the open tile onto the window. """
        if self.has_mine:
            global is_defeated
            is_defeated = True
        
        self.is_open = True
        
        pygame.draw.rect(window, OPEN_TILE_COLOR, (self.x_pos, self.y_pos, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(window, BORDER_COLOR, (self.x_pos, self.y_pos, TILE_SIZE, TILE_SIZE), 1)
            
        if self.has_mine == True:
            pygame.draw.circle(window, MINE_COLOR, (self.x_pos + TILE_SIZE/2+1, self.y_pos + TILE_SIZE/2+1), TILE_SIZE/3)
        elif self.nearby_mines > 0:
            text = NUM_FONT.render(str(self.nearby_mines), 1, NUM_COLORS[self.nearby_mines])
            window.blit(text, (self.x_pos + (TILE_SIZE/2 - text.get_width()/2), self.y_pos + (TILE_SIZE/2 - text.get_height()/2)))
            
    
    def toggle_flag(self):
        """ Toggle the flag. Remove the flag if it
        the tile is flagged, and add the flag if the 
        tile is not flagged. """
        self.is_flagged = not self.is_flagged
        
        if self.is_flagged == False:
            self.draw_tile()
        else:
            pygame.draw.polygon(window, FLAG_COLOR, ((self.x_pos + TILE_SIZE/5, self.y_pos + TILE_SIZE/5), (self.x_pos + TILE_SIZE/5, self.y_pos + TILE_SIZE - TILE_SIZE/5), (self.x_pos + TILE_SIZE - TILE_SIZE/5, self.y_pos + TILE_SIZE/2)))
            
if __name__ == "__main__":
    main()