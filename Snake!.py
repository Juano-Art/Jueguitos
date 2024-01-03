import pygame
import time
import random

snake_speed =3

#tamaño ventana
window_x =800
window_y = 600

#definir colores
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
"""
 Step 2: After importing libraries we need to initialize Pygame using pygame.init() method. 

    Create a game window using the width and height defined in the previous step.
    Here pygame.time.Clock() will be used further in the main logic of the game to change the speed of the snake.

"""

#inicia pygame
pygame.init()


#musica
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("fondo.wav")
pygame.mixer.Sound.play(sonido_fondo)


#incia game window
pygame.display.set_caption('Viper el Juegazo')
game_window = pygame.display.set_mode((window_x,window_y))
#FPS 
fps = pygame.time.Clock()

fondo = pygame.transform.scale(pygame.image.load("viper.png"), (window_x, window_y))

"""
Step 3: Initialize snake position and its size.

    After initializing snake position, initialize the fruit position randomly anywhere in the defined height and width.
    By setting direction to RIGHT we ensure that, whenever a user runs the program/game, the snake must move right to the screen.

"""

#define la posicion de la serpiente 
snake_position = [100,50]

#define los primeros 4 bloques del cuerpo
snake_body=[ [100,50],
            [90,50],
            [80,50],
            [70,50]]

fruit_position= [random.randrange(1,(window_x//10))*10,
                 random.randrange(1,(window_y//10))*10   ]
fruit_spawn = True
# configura la posicion incial de la serpiente
direction = 'RIGHT'
change_to = direction

"""
Step 4: Create a function to display the score of the player. 

    In this function, firstly we’re creating a font object i.e. the font color will go here.
    Then we are using render to create a background surface that we are going to change whenever our score updates.
    Create a rectangular object for the text surface object (where text will be refreshed)
    Then, we are displaying our score using blit. blit takes two argument screen.blit(background,(x,y))

"""

#puntaje incial
score = 0

#muestra el puntaje
def show_score(choice,color,font,size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Puntaje:'+ str(score),True,color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface,score_rect)

def show_Velocidad(choice,color,font,size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Velocidad:'+ str(snake_speed),True,color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface,score_rect)









#game over
"""
   Step 5: Now create a game over function that will represent the score after the snake is hit by a wall or itself. 

    In the first line, we are creating a font object to display scores.
    Then we are creating text surfaces to render scores.
    After that, we are setting the position of the text in the middle of the playable area.
    Display the scores using blit and updating the score by updating the surface using flip().
    We are using sleep(2) to wait for 2 seconds before closing the window using quit().

 """   
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    game_window.blit(game_over_surface, game_over_rect)
       
    pygame.display.flip()

    time.sleep(5)

    pygame.quit()
    quit()

"""
Step 6: Now we will be creating our main function that will do the following things:

    We will be validating the keys that will be responsible for the movement of the snake, then we will be creating a special condition that the snake should not be allowed to move in the opposite direction instantaneously.
    After that, if snake and fruit collide we will be incrementing the score by 10 and new fruit will be spanned.
    After that, we are checking that is the snake hit with a wall or not. If a snake hits a wall we will call game over function.
    If the snake hits itself, the game over function will be called.
    And in the end, we will be displaying the scores using the show_score function created earlier.
"""    

while True:
    #maneja eventos
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
              change_to ='UP'
            if event.key == pygame.K_DOWN:
             change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
              change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
              change_to ='RIGHT'



    #maneja el caso de apretar dos teclas
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'


                       


    #mover la serpiente
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += snake_speed*10
        snake_speed += 1
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                        random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True
    game_window.blit(fondo,(0,0))
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                        pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))



    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()


    # displaying score continuously
    show_score(1, white, 'times new roman', 20)

    #muestra velocidad
    show_Velocidad(2,red,'arial',30)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)


                     