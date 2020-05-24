import pygame
import random
import math
import time

def player(x,y):
    #it displays the background image and the player image
    screen.blit(bgImg,(0,0))
    screen.blit(playerImg,(x,y))
    return 

def enemy(enemyImg,x,y):
    #for enemy image
    screen.blit(enemyImg,(x,y))

def fire_bullet(x,y):
    #it controls the state of bullet(whether it is currently firing or not)
    #displays the bullet
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16,y))
    return 

#It checks for the collision b/w bullet an enemy
def collision(bullet_x,bullet_y,enemy_x,enemy_y):
    #The distance is used so as to take care of the size of enemy and the bullet.Otherwise only a small 
    #point will result in collsion
    distance = math.sqrt(((bullet_x-enemy_x)**2) + ((bullet_y-enemy_y)**2))
    if distance<27:
        return True
    return False

#Displaying the score
def show_score(x,y):
    score = font.render("Score : " + str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))
    return 
 
#The function  where all the activities take place
def run():
    #player image(x and y co-ordinates)
    player_x = 370
    player_y = 600
    
    #An array of enemies has been maintained and each element has all the corresponding prop in diff arrays
    enemyImg = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    num_enemies = 10
    
    for i in range(num_enemies):
        enemyImg.append(pygame.image.load("skull.png"))
        enemy_x.append(random.randint(0,800))
        enemy_y.append(random.randint(50,150))
        enemy_x_change.append(1.5)
        enemy_y_change.append(40)
    
    #Initial co-ordinates of bullets
    bullet_x = 0
    bullet_y = 600
    bullet_y_change = 15
    
    #Initial rate of movement of the spaceship(ie our player)
    rate_x = 0
    rate_y = 0
    
    running = True
    
    while running:
        screen.fill((123,43,230))
        for event in pygame.event.get():
            #If the user presses cross button
            if event.type == pygame.QUIT:
                running== False
                pygame.quit()
                return
            #if user presses any button from keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_bullet(player_x,bullet_y)

                if event.key == pygame.K_LEFT:

                    rate_x =-2

                elif event.key == pygame.K_RIGHT:

                    rate_x =2

         #release of that button{program to stop the movement of the spaceship once the key is released} 
            elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                        rate_x =0

                    elif event.key == pygame.K_RIGHT:

                        rate_x =0
    
        #calling the player function to display player and background
        player(player_x,player_y)
        
        global bullet_state
        #A for loop to control all the movement and function of all the enemies
        for i in range(num_enemies):
            #displaying enemies
            enemy(enemyImg[i],enemy_x[i],enemy_y[i])
            #checking if any enemy goes out of screen
            if enemy_x[i]>=750 or enemy_x[i]<0:
                enemy_x_change[i]*=-1  #changing the direction of it's movement.
                enemy_y[i]+=enemy_y_change[i]
            enemy_x[i] +=enemy_x_change[i]
            #checking for collision for any enemy
            if collision(bullet_x,bullet_y,enemy_x[i],enemy_y[i]):
                enemy_x[i] = random.randint(0,700)  #generating a new enemy
                enemy_y[i] = random.randint(50,150)
                bullet_state = 'ready'  #changing the bullet state from fired to ready 
                bullet_x = player_x  #now the bullet again starts from the location of spaceship
                bullet_y = player_y
                enemy(enemyImg[i],enemy_x[i],enemy_y[i]) #respawning the enemy
                global score_val  #declaring it as global
                score_val+=1
        #ready means that bullet is not fired or not in moving state
        if bullet_state is 'ready':
            bullet_x = player_x
         
        #if the bullet is fired then we have to change it's y co-ordinate
        if bullet_state is 'fire':
            fire_bullet(bullet_x,bullet_y)
            bullet_y -= bullet_y_change
            
        #if bullet goes out of screen then reload it
        if bullet_y<=0:
            bullet_y = 600
            bullet_state = 'ready'
            
        #displaying score
        show_score(20,10)
        pygame.display.update() 
        #ensuring spaceship does not go out of screen
        if player_x>=750 or player_x<=0:
            rate_x*=-1
       #moving spaceship in case a key was pressed(rate_x would be adjusted accordingly)
        player_x+=rate_x
        #if any of the enemy reaches bottom then the game ends
        if(max(enemy_y)>=580):
            pygame.quit()
            return 



#initializing
pygame.init()
screen = pygame.display.set_mode((800,700))
pygame.display.set_caption("space fighter 3D")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)
playerImg = pygame.image.load("space-invaders.png")

bgImg = pygame.image.load("my-backgr1.png").convert()

bulletImg = pygame.image.load("bullet.png")

bullet_state = 'ready'

pygame.mixer.music.load("game_music.mp3")
pygame.mixer.music.set_volume(1.2)
pygame.mixer.music.play(-1)
score_val = 0
font= pygame.font.Font('freesansbold.ttf',32)

run()
