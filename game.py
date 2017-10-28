import pygame
import time, random

pygame.init()
pygame.mixer.init()  #initializing mixer for music
display_width = 1200 #setting up window width and height
display_height = 700    
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
light_red = (200,0,0)
light_green = (0,200,0)
blue = (0,0,255)
green = (0,255 ,0)
car_width = 100
dodges = 0
crash_sound = pygame.mixer.Sound('Crash.ogg')  #Loading sound for crash
pygame.mixer.music.load('Jazz_in_Paris.ogg')
gamedisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car')    #Window title
clock = pygame.time.Clock()
carImage = pygame.image.load('car.jpg')
objectimage = pygame.image.load('rocky.png')
Fill = pygame.image.load('road.png')
def dodged(count):
    font = pygame.font.SysFont(None , 25)
    text = font.render('Dodged: ' + str(count), True, blue )
    gamedisplay.blit(text, (0,0))

def car(x, y):  # displaying the car
    gamedisplay.blit(carImage, (x, y))  # drawing the background or can draw image on window


def objects(objectx, objecty, objecth, objectw, color):
    # pygame.draw.rect(gamedisplay, color, [objectx, objecty , objecth, objectw] ) #we can use this code to draw a rect shaped object
    gamedisplay.blit(objectimage, (objectx, objecty))   #loading rock's image


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def msg(t):
    largetext = pygame.font.Font('freesansbold.ttf', 50)
    textsurf, textrect = text_objects(t, largetext)
    textrect.center = (600, 540)
    gamedisplay.blit(textsurf, textrect)  # display the msg
    pygame.display.update()
    time.sleep(2)
    gameloop()

def msg_display(text):
    largetext = pygame.font.Font('freesansbold.ttf', 100)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((display_width * 0.5), (display_height * 0.5))
    gamedisplay.blit(textsurf, textrect)  # display the msg
    pygame.display.update()
    #time.sleep(2)
    #gameloop()


def crash():
    msg_display('You crashed')
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    #msg('Your score: ' + str(dodges))

def button():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if 150 + 150 > mouse[0] > 150 and 500 + 70 > mouse[1] > 500:
        pygame.draw.rect(gamedisplay, green, (150, 500, 150, 70))
        pygame.draw.rect(gamedisplay, light_red, (900, 500, 150, 70))
        if click[0]== 1:
            gameloop()
    elif 900 + 150 > mouse[0] > 900 and 500 + 70 > mouse[1] > 500:
        pygame.draw.rect(gamedisplay, light_green, (150, 500, 150, 70))
        pygame.draw.rect(gamedisplay, red, (900, 500, 150, 70))
        if click[0] == 1:
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(gamedisplay, light_green, (150, 500, 150, 70))
        pygame.draw.rect(gamedisplay, light_red, (900, 500, 150, 70))
    smalltext = pygame.font.Font('freesansbold.ttf', 25)
    textsurf, textrect = text_objects("Start", smalltext)
    textrect.center = (225, 535)
    Textsurf, Textrect = text_objects("Quit", smalltext)
    Textrect.center = (900+75, 500+35)
    gamedisplay.blit(Textsurf, Textrect)

    gamedisplay.blit(textsurf, textrect)
    pygame.display.update()

def game_title():
    title = True
    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #gamedisplay.blit(Fill, (-160, -50))
        gamedisplay.fill(black)
        largetext = pygame.font.Font('freesansbold.ttf', 100)
        textsurf, textrect = text_objects("Rock Dodge", largetext)
        textrect.center = ((display_width * 0.5), (display_height * 0.5))
        gamedisplay.blit(textsurf, textrect)
        #position of mouse
        button()
        clock.tick(15)




def gameloop():
    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.709)
    x_change = 0
    object_startx = random.randrange(0, display_width)
    object_starty = -10
    object_speed = 7
    object_width = 200
    object_height = 140
    dodges =0
    file = open("High Score.txt", "w")
    exit_game = False

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:  # when key is pressed
                if event.key == pygame.K_LEFT:
                    x_change = -7
                elif event.key == pygame.K_RIGHT:
                        x_change = 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gamedisplay.blit(Fill,(-160,-50))

        # objects(objectx, objecty, objecth, objectw, color)
        objects(object_startx, object_starty, object_height, object_width, black)
        object_starty += object_speed
        car(x, y)
        dodged(dodges)
        if x > display_width - car_width or x < 0:
            crash()
            score()
        if object_starty > display_height:
            object_starty = 0 - object_height
            object_startx = random.randrange(0, (display_width - object_width))
            dodges += 1
            object_speed += 0.5
            # object_width += (dodged * 1.2)
        if y < object_starty + object_height:
            if x < object_startx + object_width and x > object_startx or x + car_width > object_startx and x + car_width < object_startx + object_width:
                crash()
                score()
        dodged(dodges)
        pygame.display.update()  # we can use flip() instead of update
        clock.tick(100)  # adjusting frames per second

        def score():
            msg('Your score: ' + str(dodges))

        file.write("\nHigh score: " + str(dodges))

#    file.close()

game_title()
gameloop()
pygame.quit()
quit()
