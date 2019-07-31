import pygame
import random
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.init()

size         = [320,336]
x            = size[0]/2
y            = (size[1] - 16)/2
block_size   = size[0]/20
white        = (255, 255, 255) 
black        = (0, 0, 0)
red          = (255, 0, 0)
screen       = pygame.display.set_mode(size)
clock        = pygame.time.Clock()
snake        = pygame.image.load("snake.png").convert_alpha()
empty        = pygame.image.load("empty.png").convert_alpha()
fruit        = pygame.image.load("fruit.png").convert_alpha()

font         = pygame.font.Font(None, 25)
_exit        = font.render("Exit",True,red)
_restart     = font.render("Restart",True,red)
_game_over   = font.render("GAME OVER",True,white)
_leaderboard = font.render("Leaderboard",True,red)

tail         = 0
old_tail     = 0
tail_array_x = []
tail_array_y = []
UP           = 0
DOWN         = 0
LEFT         = 0
RIGHT        = 1
running      = True
new_fruit    = True
fruit_x      = random.randrange(0, size[0], block_size)
fruit_y      = random.randrange(0, size[1], block_size)

def WorkWithFile(tail):
    try:
        file = open('leaderboard.txt', 'r')
        data = file.read().splitlines()
        file.close()
        
        for d in data:
            if (int(d) < tail):
                newscore = d
                data.insert(data.index(newscore), tail)
                break
            elif(int(d) == tail):
                return
        
        if int(len(data)) > 10:
            data.remove(data[10])
        else:
            file = open('leaderboard.txt', 'w')
            for d in data:
                file.write(str(d) + '\n')
            file.write(str(tail) + '\n')
            file.close()
            return
    
        file = open('leaderboard.txt', 'w')
        for d in data:
            file.write(str(d) + '\n')
        file.close()
    except IOError as e:
        file = open('leaderboard.txt', 'w')
        file.write(str(tail) + '\n')
        file.close()
        

def PrintLeaderboard(tail):
    _leaderboard = font.render('Leaderboard',True,white)
    screen.blit(_leaderboard, [size[0]/2 - _leaderboard.get_width() / 2, 32])

    try:
        file = open('leaderboard.txt', 'r')
        data = file.read().splitlines()
        
        file.close()
        temp = 1 
        for d in data:
            leaderlist = font.render(d,True,white)
            screen.blit(font.render('#' + str(temp),True,white), [16, 17 * temp + 64])
            screen.blit(leaderlist, [64, 17 * temp + 64])
            temp += 1
    except IOError as e:
        leaderlist = font.render('No scores',True,white)
        screen.blit(leaderlist, [size[0]/2 - leaderlist.get_width() / 2, 64])
    
    

def Tail():
    global x, y, tail, old_tail, tail_array_x, tail_array_y, running, _game_over
    tail_array_x.append(x)
    tail_array_y.append(y)

    if tail == old_tail:
        screen.blit(empty, (tail_array_x.pop(0), tail_array_y.pop(0)))
    else:
        old_tail = tail

    for i in range(len(tail_array_x) - 1):
        if x == tail_array_x[i] and y == tail_array_y[i]:
            screen.blit(_game_over, [size[0]/2 - _game_over.get_width() / 2, size[1]/2 - _game_over.get_height() / 2])
            font = pygame.font.Font(None, 16)
            _current_score = font.render("Your score: " + str(tail),True,white)
            screen.blit( _current_score, [size[0]/2 - _current_score.get_width() / 2, size[1]/2 - _current_score.get_height() / 2 + _game_over.get_height()])
            WorkWithFile(tail)
            return True
    return False

def MoveLogic():
    global x, y
      
    if UP == 1:
        y -= block_size
    elif DOWN == 1:
        y += block_size
    elif LEFT == 1:
        x -= block_size
    elif RIGHT == 1:
        x += block_size

    if x == size[0]:
        x = 0
    elif x == -block_size:
        x = size[0]
    elif y == size[1]:
        y = 16
    elif y == 0:
        y = size[1]

def FruitLogic():
    global x, y, new_fruit, fruit_x, fruit_y, tail, old_tail, _continue
    _continue = False
    if new_fruit:
        while _continue == False:
            fruit_x = random.randrange(0, size[0], block_size)
            fruit_y = random.randrange(16, size[1], block_size)
            if(fruit_x in tail_array_x and fruit_y in tail_array_y):
                continue
            else:
                screen.blit(fruit, (fruit_x, fruit_y))
                new_fruit = False
                _continue = True
        
    
    if x == fruit_x and y == fruit_y:
        screen.blit(empty, (fruit_x, fruit_y))
        tail += 1
        new_fruit = True

def main():
    global running, _score, _restart, _exit, UP, DOWN, LEFT, RIGHT, tmp, screen, new_fruit, font
    pygame.display.set_caption('Snake')

    tmp = ""
    game_active = True
    game_over = False
    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:  
                    if (event.key == pygame.K_UP and tmp != "DOWN"):
                        UP = 1
                        DOWN = 0
                        LEFT = 0
                        RIGHT = 0
                        tmp = "UP"
                    elif (event.key == pygame.K_DOWN and tmp != "UP"):
                        DOWN = 1
                        UP = 0
                        LEFT = 0
                        RIGHT = 0
                        tmp = "DOWN"
                    elif (event.key == pygame.K_LEFT and tmp != "RIGHT"):
                        LEFT = 1
                        UP = 0
                        DOWN = 0
                        RIGHT = 0
                        tmp = "LEFT"
                    elif (event.key == pygame.K_RIGHT and tmp != "LEFT"):
                        RIGHT = 1
                        UP = 0
                        DOWN = 0
                        LEFT = 0
                        tmp = "RIGHT"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cursor_pos = event.pos
                        for i in range(100):
                            for j in range(16):
                                if cursor_pos[0] == 256 + i and cursor_pos[1] == 0 + j:
                                    os.execl(sys.executable, sys.executable, *sys.argv)
                                elif cursor_pos[0] == 128 + i and cursor_pos[1] == 0 + j:
                                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 320, 336))
                                    PrintLeaderboard(tail)
                                    if game_active:
                                        game_active = False
                                    elif not game_active and not game_over:
                                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 320, 336))
                                        new_fruit = True
                                        game_active = True
                                    else:
                                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 320, 336))
                                        screen.blit(_game_over, [size[0]/2 - _game_over.get_width() / 2, size[1]/2 - _game_over.get_height() / 2])
                                        font = pygame.font.Font(None, 16)
                                        _current_score = font.render("Your score: " + str(tail),True,white)
                                        screen.blit( _current_score, [size[0]/2 - _current_score.get_width() / 2, size[1]/2 - _current_score.get_height() / 2 + _game_over.get_height()])
                                        game_active = True
                                    
        if(game_active and not game_over):                                
            game_over = Tail()
            MoveLogic()
            FruitLogic()
            screen.blit(snake, (x,y))

        font = pygame.font.Font(None, 25)
        _score = font.render("Score: " + str(tail),True,black)
        pygame.draw.line(screen, (0, 255, 0), (0, 0), (320, 0), 32)
        screen.blit(_score, [0,0])
        screen.blit(_leaderboard, [128,0])
        screen.blit(_restart, [256,0])
            
        pygame.display.flip()
        clock.tick(10)
    #pygame.quit()
main()   
