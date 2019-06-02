import pygame, time, pickle, socket

WIDTH = 800 
HEIGHT = 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

pygame.init()
time = pygame.time.Clock()
display_game = pygame.display.set_mode((WIDTH, HEIGHT))
cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_socket.connect(("localhost", 9090))

def ball_draw(coord_X,coord_Y):
    pygame.draw.circle(display_game, BLACK, [coord_X,coord_Y], 5)
	
def block_draw(coord_X,coord_Y,p):
    if p == 1:
        pygame.draw.rect(display_game, RED, [coord_X, coord_Y, 10, 60])
    if p == 2:
        pygame.draw.rect(display_game, BLUE, [coord_X, coord_Y, 10, 60])


def text_objects(text, font, colour):
    surface = font.render(text, True, colour)
    return surface, surface.get_rect()

def message(text,coord_X,coord_Y):
    text1 = pygame.font.Font('freesansbold.ttf',45)
    surface, rect = text_objects(str(text), text1, GREEN)
    rect.center = ((coord_X),(coord_Y))
    display_game.blit(surface, rect)

    pygame.display.update()
	
def data_recieving():
    return pickle.loads(cl_socket.recv(1024)) 

def display():
    game_finished = False
    data = []
    up = False
    down = False
    while game_finished == False:
        info = data_recieving()
        display_game.fill(WHITE)
		
        block_draw(10, info[0], 1)
        block_draw(WIDTH-20, info[1], 2)
        ball_draw(info[3], info[2])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_finished = True
                    break
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False


        arr = [up, down]
        cl_socket.send(pickle.dumps(arr))
        message(info[4], 250, 300)
        message(info[5], 550, 300)


display()