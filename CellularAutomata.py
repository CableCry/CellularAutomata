import pygame, random
import os

# Colors
BLACK = (21, 0, 26)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
ABRICOT = (210, 149, 53)
AQUA = (107, 238, 221)
viridis_colors = [
(68, 1, 84),    # Dark blue/purple
(59, 82, 139),  # Blue
(33, 144, 141), # Cyan
(92, 200, 99),  # Green
(253, 231, 37)  # Yellow
]

# Screen/Pixel Sizes
WIN_SIZE = 1280 # Size of the application (Change to simulate more)
CELL_SIZE = 6  # Size of each cell in the grid (Change to simulate more)
GRID_SIZE = WIN_SIZE // CELL_SIZE


# Misc Variable
TOTAL_TURNS = 10  # Total turns for the gradient transition
current_turn = 0
use_moore_neighborhood = True



# Create Random Starting Grid
def init_grid():
    return [[(random.random() < 0.50, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] 


# Moore Neighborhood
def count_neighbors_moore(grid, x, y): 
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 or j != 0) and 0 <= x + i < GRID_SIZE and 0 <= y + j < GRID_SIZE:
                count += grid[x + i][y + j][0]
    return count


# Von Neumann Neighborhood
def count_neighbors_von_neumann(grid, x, y):
    count = 0
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            count += grid[nx][ny][0]
    return count


# Update Grid
def update_grid(grid):
    
    # Create Empty Temporary Array
    new_grid = [[(False, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Loop Logic
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            
            # Choose the appropriate neighbor counting function
            neighbors = count_neighbors_moore(grid, x, y) if use_moore_neighborhood else count_neighbors_von_neumann(grid, x, y)
            
            alive, age = grid[x][y]
            
            # Moore Neighborhood
            if use_moore_neighborhood == True:
                
                if alive:
                    
                    # Kill cell from age
                    if neighbors in [2, 3] and age == TOTAL_TURNS:
                        new_grid[x][y] = (False, 0)  
                    
                    # Cell stays alive and age increases
                    elif neighbors in [2, 3]:
                        new_grid[x][y] = (True, age + 1)  
                        
                    # 10% chance for the cell to "reproduce"
                    elif neighbors in [1]:
                        chance = random.random() < 0.10
                        new_grid[x][y] = (chance, 1 if chance else 0)
                    
                    else:
                        # Cell dies, reset age
                        new_grid[x][y] = (False, 0)
                
                else:
                    # Cell comes to life, age is 1
                    if neighbors == 3:
                        new_grid[x][y] = (True, 1)  

                    # Cell stays dead
                    else:
                        new_grid[x][y] = (False, 0)  
            
            
            # Von Neumann Neighborhood
            else:  
                if alive:
                    
                    # Cell explodes
                    if age == TOTAL_TURNS:  
                        chance_explo = random.random() < 0.50
                        
                        if chance_explo == True:
                            new_grid[x][y] = (False, 0)
                            
                            # Make immediate neighbors
                            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                                    chance = random.random() < 0.50
                                    new_grid[nx][ny] = (chance, 1 if chance else 0)
                        
                        
                        # Neighborhood Logic
                        else:
                            new_grid[x][y] = (True, 10)
                            
                    elif neighbors in [2, 3]:
                        # Cell comes to life, age is 1
                        new_grid[x][y] = (True, age + 1)
                        
                    else:
                        # Cell dies, reset age
                        new_grid[x][y] = (False, 0)
                        
                else:
                    # Cell comes to life, age is 1
                    if neighbors == 3:
                        new_grid[x][y] = (True, 1)
                    
                    # Cell stays dead
                    else:
                        new_grid[x][y] = (False, 0)
                        
    return new_grid



"""
Calculates color gradient based on the current turn.
:param total_turns: The total number of turns for full transition.
:param current_turn: The current turn.
:return: The gradient color as a tuple.
"""
def gradient_viridis(total_turns, current_turn):

    # Determine the current turn in relation to the total turns
    factor = current_turn / total_turns

    # Calculate which two colors to switch between
    num_colors = len(viridis_colors)
    start_index = int(factor * (num_colors - 1))
    end_index = min(start_index + 1, num_colors - 1)

    # Calculate the interpolation factor between the two selected colors
    local_factor = (factor * (num_colors - 1)) % 1

    # Switch between the two colors
    start_color = viridis_colors[start_index]
    end_color = viridis_colors[end_index]
    new_color = [start_color[i] + (end_color[i] - start_color[i]) * local_factor for i in range(3)]

    return tuple(int(c) for c in new_color)

# Initialize Pygame
pygame.init()
smallfont = pygame.font.SysFont('Corbel',25, bold=True) 
quit_text = smallfont.render('QUIT', True, BLACK)
play_pause_text = smallfont.render("Play/Pause", True, BLACK)
neighborhood_text = smallfont.render("Switch Neighborhood", True, BLACK)
reset_text = smallfont.render("Reset", True, BLACK)

# Set up the screen
screen = pygame.display.set_mode((WIN_SIZE, (WIN_SIZE + 50)))
pygame.display.set_caption("Conway's Game of Life")

# Game state variables
grid = init_grid()
running = False 
done = False
clock = pygame.time.Clock()



# Main program loop
while not done:
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if quit_button.collidepoint(mouse_x, mouse_y):
                done = True

            if play_pause_button.collidepoint(mouse_x, mouse_y):
                running = not running
                
            if neighborhood_button.collidepoint(mouse_x, mouse_y):
                use_moore_neighborhood = not use_moore_neighborhood
                
            if reset_button.collidepoint(mouse_x, mouse_y):
                grid = init_grid()


    # Mouse Position
    mouse = pygame.mouse.get_pos()


    # Background
    screen.fill(BLACK)
    bar = pygame.Rect(WIN_SIZE - 1280, WIN_SIZE, 1280, 50)
    pygame.draw.rect(screen, GRAY, bar)


    # Quit Button
    quit_button = pygame.Rect(WIN_SIZE - 150, WIN_SIZE + 10, 100, 30)
    pygame.draw.rect(screen, WHITE if quit_button.collidepoint(mouse) else AQUA, quit_button)
    screen.blit(quit_text, (WIN_SIZE - 130, WIN_SIZE + 13))
    
    
    # Play / Pause button
    play_pause_button = pygame.Rect(WIN_SIZE - 1260, WIN_SIZE + 10, 130, 30)
    pygame.draw.rect(screen, WHITE if play_pause_button.collidepoint(mouse) else AQUA, play_pause_button)
    screen.blit(play_pause_text, (WIN_SIZE - 1255, WIN_SIZE + 13))
    
    
    # Switch Button
    neighborhood_button = pygame.Rect(WIN_SIZE - 1120, WIN_SIZE + 10, 250, 30)
    if use_moore_neighborhood == True:
        pygame.draw.rect(screen, WHITE if neighborhood_button.collidepoint(mouse) else AQUA, neighborhood_button)
    else:
        pygame.draw.rect(screen, WHITE if neighborhood_button.collidepoint(mouse) else ABRICOT, neighborhood_button)
    screen.blit(neighborhood_text, (WIN_SIZE - 1115, WIN_SIZE + 13))
    
    
    # Reset Button
    reset_button = pygame.Rect(WIN_SIZE - 260, WIN_SIZE + 10, 90, 30)
    pygame.draw.rect(screen, WHITE if reset_button.collidepoint(mouse) else ABRICOT, reset_button)
    screen.blit(reset_text, (WIN_SIZE - 247, WIN_SIZE + 13))


    # Update Grid
    if running:
        grid = update_grid(grid)
        
    # Draw Grid Updates
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            alive, age = grid[x][y]
            if alive:
                age_capped = min(age, TOTAL_TURNS)
                cell_color = gradient_viridis(TOTAL_TURNS, age_capped)
                pygame.draw.rect(screen, cell_color, rect, 0)
            else:
                pygame.draw.rect(screen, BLACK, rect, 0)
            pygame.draw.rect(screen, BLACK, rect, 1)


    pygame.display.flip()
    clock.tick(30)


# Quit Pygame
pygame.quit()
