# Space-game
import pgzrun
import random
import pygame

WIDTH = 1920
HEIGHT = 1080

# Geschwindigkeiten
MOVE_SPEED = 5
METEOR_SPEED = 3
SPAWN_DELAY = 50
BULLET_SPEED = 15

# Hintergrund
background_surface = pygame.transform.scale(images.purple, (WIDTH, HEIGHT))

# Spieler
hero = Actor("playership3_orange", anchor=("center", "center"))
hero.pos = (100, HEIGHT // 2)
hero.angle = 270

# Liste für Bullets
bullets = []
#Bombe 
bomb_types = ["spacemissiles_003","spacemissiles_004","spacemissiles_005","spacemissiles_006",
            "spacemissiles_007","spacemissiles_008","spacemissiles_009","spacemissiles_010",
            "spacemissiles_011",

]
bombs = []
bomb_spawn_counter = 0
# Meteoriten
meteorite_types = [
    "meteorbrown_big4","meteorbrown_big1","meteorbrown_big2",
    "meteorbrown_big3","meteorbrown_med1","meteorbrown_small1",
    "meteorbrown_tiny1","meteorgrey_big1","meteorgrey_big2",
    "meteorgrey_big4","meteorgrey_med1","meteorgrey_med2",
    "meteorgrey_small1",
]

meteorites = []
spawn_counter = 0


# Planet am rechten Rand
planet_side = Actor("todesstern2", anchor=("center", "center"))
planet_side.midright = (WIDTH + planet_side.width // 2, random.randint(50, HEIGHT - 50))

# Planet am linken Rand
planet_side_left = Actor("planet01", anchor=("center", "center"))
planet_side_left.midleft = (-planet_side_left.width // 2, HEIGHT // 2)

# Planet02klein bei 500, 500
planet_center = Actor("planet02klein", anchor=("center", "center"))
planet_center.center = (1200, 250)


def spawn_meteorite():
    meteor_type = random.choice(meteorite_types)

    meteor = Actor(meteor_type, anchor=("center", "center"))

    meteor.x = WIDTH + 50
    meteor.y = random.randint(50, HEIGHT - 50)

    meteorites.append(meteor)

def spawn_bombe():
    bomb_type = random.choice(bomb_types)

    bomb = Actor(bomb_type, anchor=("center", "center"))
    bomb.angle = 90

    bomb.x = WIDTH + 50

    # Vermeide Spawn direkt innerhalb eines Meteoriten
    for _ in range(20):
        bomb.y = random.randint(50, HEIGHT - 50)
        if not any(bomb.colliderect(meteor) for meteor in meteorites):
            break

    bombs.append(bomb)


def shoot():
    bullet = Actor("laserblue04", anchor=("center", "center"))
    bullet.angle = 270

    # Bullet vorne am Schiff
    bullet.pos = (hero.x + 40, hero.y)

    bullet.vx = BULLET_SPEED

    bullets.append(bullet)

def restart_game():
    global meteorites
    global bullets
    global bombs
    global meteor_spawn_counter
    global bomb_spawn_counter

    # Spieler zurücksetzen
    hero.pos = (100, HEIGHT // 2)

    # Listen leeren
    meteorites.clear()
    bullets.clear()
    bombs.clear()

    # Counter zurücksetzen
    meteor_spawn_counter = 0
    bomb_spawn_counter = 0

# Tastendruck
def on_key_down(key):
    if key == keys.SPACE:
        shoot()


def draw():
    screen.surface.blit(background_surface, (0, 0))
    # Planeten zeichnen
    planet_side.draw()
    planet_side_left.draw()
    planet_center.draw()
    hero.draw()

    # Bullets zeichnen
    for bullet in bullets:
        bullet.draw()

    # Meteoriten zeichnen
    for meteor in meteorites:
        meteor.draw()
    # Bombe zeichnen
    for bomb in bombs:
        bomb.draw()
    



def update():
    global spawn_counter
    global bomb_spawn_counter

    # Spielerbewegung
    if keyboard.left:
        hero.x -= MOVE_SPEED

    if keyboard.right:
        hero.x += MOVE_SPEED

    if keyboard.up:
        hero.y -= MOVE_SPEED

    if keyboard.down:
        hero.y += MOVE_SPEED

    # Bildschirmgrenzen
    hero.x = max(0, min(WIDTH, hero.x))
    hero.y = max(0, min(HEIGHT, hero.y))

    # Meteoriten spawnen
    spawn_counter += 1

    if spawn_counter >= 35:
        spawn_meteorite()
        spawn_counter = 0

    # Bombe spawnen
    bomb_spawn_counter += 1

    if bomb_spawn_counter >= 200:
        spawn_bombe()
        bomb_spawn_counter = 0

    # Bullets bewegen
    for bullet in bullets[:]:

        bullet.x += bullet.vx

        # Bullet löschen wenn außerhalb
        if bullet.x > WIDTH + 100:
            bullets.remove(bullet)

    # Meteoriten bewegen
    for meteor in meteorites[:]:

        meteor.x -= METEOR_SPEED

        if meteor.x < -100:
            meteorites.remove(meteor)
    
    # Bombe bewegen
    for bomb in bombs[:]:

        bomb.x -= METEOR_SPEED

        if bomb.x < -100:
            bombs.remove(bomb)

    # Bullet trifft Meteor
    for bullet in bullets[:]:
        for meteor in meteorites[:]:

            if bullet.colliderect(meteor):

                if bullet in bullets:
                    bullets.remove(bullet)

    

                break
    # Bullet trifft Bombe
    for bullet in bullets[:]:
        for bomb in bombs[:]:

            if bullet.colliderect(bomb):

                if bullet in bullets:
                    bullets.remove(bullet)

                if bomb in bombs:
                    bombs.remove(bomb)

    

                break


    # Spieler trifft Meteor
    for meteor in meteorites:

        if hero.colliderect(meteor):
            print("GAME OVER")
            exit()

    # Spieler trifft Bombe
    for bomb in bombs:

        if hero.colliderect(bomb):
            print("GAME OVER")
            exit()

    # Planet trifft Bombe
    for bomb in bombs:

        if planet_side_left.colliderect(bomb):
            print("Looser")
            exit()

    if hero.colliderect(planet_side):
        restart_game()

pgzrun.go()