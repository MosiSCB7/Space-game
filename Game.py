# Space-game
import pgzrun
import random
import pygame

WIDTH = 1920
HEIGHT = 1080

# Globale Variable
MOVE_SPEED = 5
METEOR_SPEED = 3
SPAWN_DELAY = 50
BULLET_SPEED = 10

# Hintergrund
background_surface = pygame.transform.scale(images.purple, (WIDTH, HEIGHT))

# Charakter
hero = Actor("playership3_orange", anchor=("center", "center"))
hero.midcenter = (100, 10000)
hero.angle = 0
hero.vx = 0
hero.vy = 500

bullet = Actor("laserblue04", anchor=("center", "center"))
bullet.midcenter = (hero.x, hero.y)
bullet.vx = 0
    
  
# Meteoriten
meteorite_types = [
    "meteorbrown_big4"
    
]

meteorites = []
spawn_counter = 0


def spawn_meteorite():
    """Spawn einen zufälligen Meteoriten von rechts"""
    meteor_type = random.choice(meteorite_types)
    meteor = Actor(meteor_type, anchor=("center", "center"))
    
    # Zufällige Y-Position
    meteor.y = random.randint(50, HEIGHT - 50)
    # Rechts vom Rand
    meteor.x = WIDTH + 50
    
    meteorites.append(meteor)


def draw():
    screen.surface.blit(background_surface, (0, 0))
    hero.draw()
    if keyboard.space:
        bullet.draw()
    for meteor in meteorites:
        meteor.draw()


def update():
    global spawn_counter
    
    # x - Geschwindigkeit berechnen (links/rechts)
    hero.vx = 0
    if keyboard.left:
        hero.vx = -MOVE_SPEED
    elif keyboard.right:
        hero.vx = MOVE_SPEED
    hero.x += hero.vx
    
    if keyboard.up:
        hero.vy = -MOVE_SPEED
    elif keyboard.down:
        hero.vy = MOVE_SPEED
    hero.y += hero.vy
    hero.vy = 0
    
    # Meteoriten spawnen
    spawn_counter += 1
    if spawn_counter >= SPAWN_DELAY:
        spawn_meteorite()
        spawn_counter = 30

     # Schießen
    if keyboard.space and bullet.vx == 0:
        bullet.vx = -BULLET_SPEED

    
    # Meteoriten bewegen
    for meteor in meteorites[:]:
        meteor.x -= METEOR_SPEED
        # Meteoriten löschen wenn sie links das Fenster verlassen
        if meteor.x < -100:
            meteorites.remove(meteor)
    
    # Kollisionsprüfung
    for meteor in meteorites:
        if hero.colliderect(meteor):
            print("Game Over!")
            exit()






pgzrun.go()