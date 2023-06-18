import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.sprite_sheet = pygame.image.load("snakered40.png")
        self.sprite_size = (cellSize, cellSize)

        self.sprite_coords = []
        self.extract_sprites()

        self.head_up = self.sprite_sheet.subsurface(self.sprite_coords[15])
        self.head_down = self.sprite_sheet.subsurface(self.sprite_coords[6])
        self.head_right = self.sprite_sheet.subsurface(self.sprite_coords[2])
        self.head_left = self.sprite_sheet.subsurface(self.sprite_coords[16])
        
        self.tail_up = self.sprite_sheet.subsurface(self.sprite_coords[8])
        self.tail_down = self.sprite_sheet.subsurface(self.sprite_coords[17])
        self.tail_right = self.sprite_sheet.subsurface(self.sprite_coords[18])
        self.tail_left = self.sprite_sheet.subsurface(self.sprite_coords[7])
        
        self.body_vertical = self.sprite_sheet.subsurface(self.sprite_coords[11])
        self.body_horizontal = self.sprite_sheet.subsurface(self.sprite_coords[5])
        
        self.body_TRLD = self.sprite_sheet.subsurface(self.sprite_coords[0])
        self.body_TLRD = self.sprite_sheet.subsurface(self.sprite_coords[10])
        self.body_DLRU = self.sprite_sheet.subsurface(self.sprite_coords[1])
        self.body_DRLU = self.sprite_sheet.subsurface(self.sprite_coords[12])
        
        self.devour_sound = pygame.mixer.Sound("Audio/crunch.mp3")
        self.collide_sound = pygame.mixer.Sound("Audio/collide.mp3")
        
    #Individual sprites from spritesheet taken and added to spriteCoords
    def extract_sprites(self):
            for x in range(0, self.sprite_sheet.get_height(), self.sprite_size[1]):
                for y in range(0, self.sprite_sheet.get_width(), self.sprite_size[0]):
                    self.sprite_coords.append(pygame.Rect(x, y, self.sprite_size[0], self.sprite_size[1]))
        
    def draw(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cellSize)
            y_pos = int(block.y * cellSize)
            block_rect = pygame.Rect(x_pos, y_pos, cellSize, cellSize)
            
            if index == 0:
                screen.blit(self.update_head_graphics(), block_rect)
            elif index == (len(self.body) - 1):
                screen.blit(self.update_tail_graphics(), block_rect)
            else:
                screen.blit(self.update_body_graphics(index), block_rect)
                
    def update_head_graphics(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == (1, 0): return self.head_right
        elif head_relation == (-1 , 0): return self.head_left
        elif head_relation == (0, 1): return self.head_down
        else: return self.head_up
        
    def update_tail_graphics(self):
        tail_relation = self.body[len(self.body) - 1] - self.body[len(self.body) - 2]
        if tail_relation == (1, 0): return self.tail_right
        elif tail_relation == (-1, 0): return self.tail_left
        elif tail_relation == (0, 1): return self.tail_down
        else: return self.tail_up
        
    def update_body_graphics(self, i):
        block_ahead = self.body[i - 1] - self.body[i]
        block_behind = self.body[i + 1] - self.body[i]
        if block_ahead.x == block_behind.x: return self.body_vertical
        elif block_ahead.y == block_behind.y: return self.body_horizontal
        else:
            if block_ahead.x == -1 and block_behind.y == -1 or block_ahead.y == -1 and block_behind.x == -1: return self.body_DRLU
            elif block_ahead.x == 1 and block_behind.y == -1 or block_ahead.y == -1 and block_behind.x == 1: return self.body_DLRU
            elif block_ahead.x == 1 and block_behind.y == 1 or block_ahead.y == 1 and block_behind.x == 1: return self.body_TRLD
            # elif block_ahead.x == -1 and block_behind.y == 1 or block_ahead.y == 1 and block_behind.x == -1:
            else: return self.body_TLRD
            
    def move(self):
        #If snake is not stationary, execute
        if self.direction != (0, 0):
            #If snake has eaten a fruit, grow the snake
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0, self.body[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            #If snake is already moving, keep moving
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, self.body[0] + self.direction)
                self.body = body_copy[:]
        
    def add_block(self):
        self.new_block = True
        
    def play_crunch_sound(self):
        self.devour_sound.play()
        
    def play_collide_sound(self):
        self.collide_sound.play()
        
    def reset(self):
        self.body = [Vector2(9, 10), Vector2(8, 10), Vector2(7, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self):
        self.peach = pygame.image.load("Assets/peach.png").convert_alpha()
        self.peach = pygame.transform.scale(self.peach, (cellSize, cellSize))
        self.randomize()

    def draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cellSize), int(self.pos.y * cellSize), cellSize, cellSize)
        screen.blit(self.peach, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()
        
    def draw(self):
        self.draw_grass()
        self.snake.draw()
        self.fruit.draw()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        #If fruit spawns on snake, respawn
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            
    def check_fail(self):
        #If snake is outside the screen, game over
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.snake.play_collide_sound()
            self.game_over()
        #If snake has collided with itself, game over
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.play_collide_sound()
                self.game_over()

    def game_over(self):
        self.snake.reset()
    
    def draw_grass(self):
        grass_color = (0, 100, 1)
        for row in range(cellNumber):
            #Even row
            if row % 2 == 0:
                #Grass drawn on even numbered columns
                for col in range(cellNumber):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            #Odd row
            else:
                #Grass drawn on odd numbered columns
                for col in range(cellNumber):                
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = f"SCORE: {len(self.snake.body) - 3}"
        score_surface = gameFont.render(score_text, 'True', (255, 255, 255))
        score_rect = score_surface.get_rect(topleft = (0, 0)) 
        screen.blit(score_surface, (5, 10), score_rect)

pygame.mixer.init(44100, -16, 2, 512)
pygame.init()
#Size of each grid
cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellNumber * cellSize,cellNumber * cellSize))
clock = pygame.time.Clock()
gameFont = pygame.font.Font(None, 40)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

mainGame = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            mainGame.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainGame.snake.direction.y != 1:
                    mainGame.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if mainGame.snake.direction.y != -1:
                    mainGame.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if mainGame.snake.direction.x != -1:
                    mainGame.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if mainGame.snake.direction.x != 1:
                    mainGame.snake.direction = Vector2(-1, 0)
                
    pygame.display.update()
    screen.fill((0, 170, 2))
    clock.tick(60)
    
    mainGame.draw()