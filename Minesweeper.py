import pygame
import random

pygame.init()

X_TILES = 30
Y_TILES = 16
TILE_SIZE = 40
WIDTH = X_TILES * TILE_SIZE
HEIGHT = Y_TILES * TILE_SIZE
TOTAL_MINES = 99
UNFLAGGED_MINES = TOTAL_MINES

SAFE_TILES = X_TILES * Y_TILES - TOTAL_MINES
OPENED_TILES = 0

NUM_FONT = pygame.font.SysFont('ebrima', 20)
NUM_COLORS = {1: "blue", 2: "green4", 3: "red", 4: "dodgerblue4",
              5: "firebrick4", 6: "cyan4", 7: "black", 8: "grey"}
TEXT_FONT = pygame.font.SysFont('arialblack', 30)
TEXT_COLOR = "white"
UNFLAGGED_FONT = pygame.font.SysFont('ebrima', 30)

BG_COLOR = "white"
TILE_COLOR = "lightgrey"
BORDER_COLOR = "black"
OPEN_TILE_COLOR = "darkgray"
FLAG_COLOR = "deeppink4"
MINE_COLOR = "black"

GRID = None
HAS_FIRST_CLICK = True
IS_DEFEATED = False

window = pygame.display.set_mode((WIDTH, HEIGHT + UNFLAGGED_FONT.get_height()))
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


def draw_grid():
    """ Draw the tiles of the grid. """
    for col in range(0, X_TILES):
        for row in range(0, Y_TILES):
            tile = GRID[col][row]
            tile.draw_tile()


def get_neighbours(tile):
    """ Get all neighbours of the given tile. """
    neighbours = []

    points = [[-1, -1],  # Top left
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
            neighbours.append(GRID[grid_x][grid_y])

    return neighbours


def get_all_tiles():
    """ Get all the tiles of the grid. """
    tiles = []

    for col in range(0, X_TILES):
        for row in range(0, Y_TILES):
            tiles.append(GRID[col][row])

    return tiles


def generate_mines(tile):
    """ Place mines randomly on tiles other than
    the given tile, and its neighbours. """
    tiles = get_all_tiles()

    # Remove given tile and its neighbours
    tiles.remove(tile)
    neighbours = get_neighbours(tile)
    for i in range(0, len(neighbours)):
        tiles.remove(neighbours[i])

    unplaced_mines = TOTAL_MINES

    while unplaced_mines != 0:
        num = random.randrange(0, len(tiles))

        if tiles[num].has_mine == False:
            tiles[num].has_mine = True
            unplaced_mines -= 1


def get_nearby_mines(tile):
    """ Get the amount of mines from 
    the given tile's neighbours. """
    neighbours = get_neighbours(tile)
    nearby_mines = 0

    for i in range(0, len(neighbours)):
        if neighbours[i].has_mine == True:
            nearby_mines += 1

    return nearby_mines


def set_nearby_mines():
    """ Set the number of nearby mines
    for all the tiles in the grid. """
    for col in range(0, X_TILES):
        for row in range(0, Y_TILES):
            tile = GRID[col][row]
            nearby_mines = get_nearby_mines(tile)
            tile.nearby_mines = nearby_mines


def get_unopened_neighbours(tile):
    """ Get all the tile's neighbours which
    are not opened. """
    return list(filter(lambda x: (x.is_open == False), get_neighbours(tile)))


def open_neighbour_tiles(tile):
    """ Open the tile's neighbouring tiles. """
    neighbours = get_unopened_neighbours(tile)

    for i in range(0, len(neighbours)):
        current_tile = neighbours[i]

        if current_tile.is_open == False and current_tile.is_flagged == False:
            current_tile.open_tile()
            global OPENED_TILES
            OPENED_TILES += 1

        if current_tile.nearby_mines == 0:
            open_neighbour_tiles(current_tile)


def draw_center_text(text):
    """ Draw some text in the center of the window. """
    text = TEXT_FONT.render(text, 1, TEXT_COLOR)
    pygame.draw.rect(window, BORDER_COLOR, (0, HEIGHT/2 -
                     text.get_height()/2, X_TILES*TILE_SIZE, text.get_height()))
    window.blit(text, (WIDTH/2 - text.get_width() /
                2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()


def get_nearby_flags(tile):
    """ Get the neighbouring tiles that are flagged. """
    return list(filter(lambda x: (x.is_flagged == True), get_neighbours(tile)))


def open_all_mines():
    """ Open all the tiles that are unopened
    and contain a mine. """
    unopened_mine_tiles = list(
        filter(lambda x: (x.has_mine == True and x.is_open == False), get_all_tiles()))
    for i in range(0, len(unopened_mine_tiles)):
        unopened_mine_tiles[i].open_tile()


def flag_all_mines():
    """ Flag all the tiles that has mines. """
    unflagged_mine_tiles = list(filter(lambda x: (
        x.has_mine == True and x.is_flagged == False), get_all_tiles()))
    for i in range(0, len(unflagged_mine_tiles)):
        unflagged_mine_tiles[i].toggle_flag()


def open_all_safe_tiles():
    """ Open all the tiles that has no mines. """
    unopened_safe_tiles = list(
        filter(lambda x: (x.has_mine == False and x.is_open == False), get_all_tiles()))
    for i in range(0, len(unopened_safe_tiles)):
        unopened_safe_tiles[i].open_tile()


def reset():
    """ Draw the new grid, and set the variables
    back to their starting states. """
    global GRID
    GRID = make_grid(X_TILES, Y_TILES)
    draw_grid()
    global HAS_FIRST_CLICK
    HAS_FIRST_CLICK = True
    global IS_DEFEATED
    IS_DEFEATED = False
    global OPENED_TILES
    OPENED_TILES = 0
    global UNFLAGGED_MINES
    UNFLAGGED_MINES = TOTAL_MINES
    update_unflagged_mines_text()


def update_unflagged_mines_text():
    """ Update the text of how many mines are unflagged,
    calculated from the total amount of mines minus the 
    amount of flagged files. """
    text = TEXT_FONT.render(str(UNFLAGGED_MINES), 1, BORDER_COLOR)
    pygame.draw.rect(window, BG_COLOR, (WIDTH - 2*TILE_SIZE,
                     HEIGHT, 2*TILE_SIZE, text.get_height()))
    window.blit(text, (WIDTH - text.get_width(), HEIGHT))
    pygame.display.update()


def main():
    """ Runs the game. """
    is_running = True
    global HAS_FIRST_CLICK
    global IS_DEFEATED
    global GRID

    window.fill(BG_COLOR)
    reset()

    while is_running:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:  # Space-bar is let up
                    col, row = get_grid_pos(pygame.mouse.get_pos())
                    marked_tile = GRID[col][row]

                    if marked_tile.is_open == False:  # Flag tile
                        marked_tile.toggle_flag()
                    else:  # Reveal neighbours
                        if len(get_nearby_flags(marked_tile)) == marked_tile.nearby_mines:
                            open_neighbour_tiles(marked_tile)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                col, row = get_grid_pos(pygame.mouse.get_pos())

                if col >= X_TILES or row >= Y_TILES:
                    continue

                clicked_tile = GRID[col][row]

                if mouse_pressed[0]:  # Left click
                    if clicked_tile.is_open == False and clicked_tile.is_flagged == False:
                        if HAS_FIRST_CLICK == True:
                            generate_mines(clicked_tile)
                            set_nearby_mines()
                            HAS_FIRST_CLICK = False

                        clicked_tile.open_tile()
                        global OPENED_TILES
                        OPENED_TILES += 1

                        if clicked_tile.nearby_mines == 0 and clicked_tile.has_mine == False:
                            open_neighbour_tiles(clicked_tile)

                elif mouse_pressed[2]:  # Right click
                    if clicked_tile.is_open == False:
                        clicked_tile.toggle_flag()

            if OPENED_TILES == SAFE_TILES:
                open_all_safe_tiles()
                flag_all_mines()
                pygame.display.update()
                pygame.time.delay(500)

                draw_center_text("Congrats, you win!")
                pygame.time.delay(3000)

                reset()

            if IS_DEFEATED == True:
                open_all_mines()
                pygame.display.update()
                pygame.time.delay(500)

                draw_center_text("You lost. Try again!")
                pygame.time.delay(3000)

                reset()

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
        pygame.draw.rect(window, TILE_COLOR, (self.x_pos,
                         self.y_pos, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(window, BORDER_COLOR, (self.x_pos,
                         self.y_pos, TILE_SIZE, TILE_SIZE), 1)

    def open_tile(self):
        """ Draw the open tile onto the window. """
        if self.has_mine:
            global IS_DEFEATED
            IS_DEFEATED = True

        self.is_open = True

        pygame.draw.rect(window, OPEN_TILE_COLOR,
                         (self.x_pos, self.y_pos, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(window, BORDER_COLOR, (self.x_pos,
                         self.y_pos, TILE_SIZE, TILE_SIZE), 1)

        if self.has_mine == True:
            pygame.draw.circle(window, MINE_COLOR, (self.x_pos +
                               TILE_SIZE/2+1, self.y_pos + TILE_SIZE/2+1), TILE_SIZE/3)
        elif self.nearby_mines > 0:
            text = NUM_FONT.render(
                str(self.nearby_mines), 1, NUM_COLORS[self.nearby_mines])
            window.blit(text, (self.x_pos + (TILE_SIZE/2 - text.get_width()/2),
                        self.y_pos + (TILE_SIZE/2 - text.get_height()/2)))

    def toggle_flag(self):
        """ Toggle the flag. Remove the flag if it
        the tile is flagged, and add the flag if the 
        tile is not flagged. """
        self.is_flagged = not self.is_flagged

        if self.is_flagged == False:
            self.draw_tile()
            global UNFLAGGED_MINES
            UNFLAGGED_MINES += 1
        else:
            pygame.draw.polygon(window, FLAG_COLOR, ((self.x_pos + TILE_SIZE/5, self.y_pos + TILE_SIZE/5),
                                                     (self.x_pos + TILE_SIZE/5, self.y_pos + TILE_SIZE - TILE_SIZE/5), (self.x_pos + TILE_SIZE - TILE_SIZE/5, self.y_pos + TILE_SIZE/2)))
            UNFLAGGED_MINES -= 1
        update_unflagged_mines_text()


if __name__ == "__main__":
    main()
