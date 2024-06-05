import random
import pygame
import math

# SET UP YOUR SCREEN CONSTANTS HERE
WIDTH = 1000
HEIGHT = 800

asteroids = []
exploded_asteroids = []

bg = Actor("bg", center=(WIDTH / 2, HEIGHT / 2))
UFO = Actor("ufo", center=(WIDTH / 2, 700))

death_screen = Actor("death", center=(WIDTH / 2, HEIGHT / 3))

cursor = Actor("asteroid1")

bullets = []

score = 0
health = 5
death = False

music.play('music')

state = "menu"
selection = 0

bf_state = 0

sin_title = 0

play_button = Actor('button', center=(WIDTH / 2, HEIGHT / 2))
restart_button = Actor('restart', center=(WIDTH / 2, HEIGHT / 1.5))

menu = Actor("ufo", center=(WIDTH / 2, 700))

def load_asteroids():
    for i in range(15):
        new_asteroid = Actor("asteroid1")

        new_asteroid.x = random.randint(0, WIDTH)
        new_asteroid.y = random.randint(-350,0)

        asteroids.append(new_asteroid)

def draw():
    screen.clear()

    global death
    global state

    bg.draw()

    if state == "game":
        if death == False:

            # Draw asteroids
            for asteroid in asteroids:
                asteroid.draw()

            for e_asteroid in exploded_asteroids:
                e_asteroid.draw()

            # Draw bullets
            for bullet in bullets:
                bullet.draw()

            UFO.draw()

            screen.draw.text(f"SCORE: {score}", (25, HEIGHT - 50), color="white", fontname="monocraft", fontsize=30)

            for i in range(0, health):
                new_heart = Actor("heart", (40 + (i * 70), 50))
                new_heart.draw()
        else:
            death_screen.draw()
            restart_button.draw()

            screen.draw.text(f"SCORE: {score}", center=(WIDTH / 2, HEIGHT / 2), color="white", fontname="monocraft", fontsize=30)

    elif state == "menu":
        menu.draw()

        screen.draw.text(f"SPACE\nSHOOTER", center=(WIDTH / 2, (HEIGHT / 3) + sin_title * 5), color="white", fontname="monocraft", fontsize=50)
        play_button.draw()


def on_key_down(key):
    global ammo

    if key == keys.SPACE:
        fire()

def fire():
    sounds.lasershoot.play()

    bullet_instance = Actor("bullet")
    bullet_instance.top = UFO.top
    bullet_instance.center = UFO.center
    bullets.append(bullet_instance)

def on_mouse_move(pos, rel, buttons):
    cursor.left = pos[0]
    cursor.top = pos[1]

def on_mouse_down(pos, button):
    global state
    global death
    global score, health

    if state == "menu":
        if button == mouse.LEFT and play_button.collidepoint(pos):

            sounds.lasershoot.play()

            score = 0
            health = 5

            state = "game"

    elif state == "game":
        if button == mouse.LEFT:
            fire()

    if death == True:
        if button == mouse.LEFT and restart_button.collidepoint(pos):

            sounds.lasershoot.play()

            state = "menu"
            death = False

def update():
    global state, bf_state
    global sin_title

    bf_state = bf_state + 0.1

    bg.angle = bf_state

    if state == "game":
        handle_asteroids()
        handle_player()
        handle_bullets()
        manage_health()

    elif state == "menu":
        sin_title = math.sin(bf_state)

        play_button.top = play_button.top + sin_title
        menu.top = menu.top + sin_title

        if play_button.colliderect(cursor):
            play_button.image = "button_hover"
        else:
            play_button.image = "button"

    if death == True:
        if restart_button.colliderect(cursor):
            restart_button.image = "restart-hover"
        else:
            restart_button.image = "restart"


def manage_health():
    global death
    global health

    if death == True:
        return

    for asteroid in asteroids:
        if asteroid.colliderect(UFO):
            try:
                if health <= 0:
                    player_death()
                else:
                    asteroids.remove(asteroid)

                    sounds.explosion.play()

                    exploded_asteroid = Actor("asteroid_exploded")

                    exploded_asteroid.x = asteroid.x
                    exploded_asteroid.y = asteroid.y
                    exploded_asteroids.append(exploded_asteroid)

                    health = health - 1
            except:
                print("Asteroid doesn't exist")

def player_death():
    global asteroids, exploded_asteroid
    global death

    asteroids = []
    exploded_asteroids = []

    death = True


def handle_bullets():
    global death

    if death == True:
        return

    global score

    for bullet in bullets:
        bullet.y -= 15

        if bullet.y < 0:
            bullets.remove(bullet)

        for asteroid in asteroids:
            if asteroid.colliderect(bullet):
                try:
                    sounds.explosion.play()
                    exploded_asteroid = Actor("asteroid_exploded")

                    exploded_asteroid.x = asteroid.x
                    exploded_asteroid.y = asteroid.y
                    exploded_asteroids.append(exploded_asteroid)

                    asteroids.remove(asteroid)
                    bullets.remove(bullet)

                except:
                    print("Error")
                score = score + 1

def handle_player():
    global death
    global sin_title

    if death == True:
        return

    # Player Movement
    if keyboard.right:
        UFO.right += 10

    if keyboard.left:
        UFO.left += -10

    UFO.left = max(UFO.left, 0)
    UFO.right = min(UFO.right, WIDTH)

    # Shooting

def handle_asteroids():
    global death

    if death == True:
        return

    if len(asteroids) == 0:
        load_asteroids()

    for asteroid in asteroids:
        try:
            asteroid.y = asteroid.y + 4 # Move down

            if asteroid.top > HEIGHT: # Respawn them at the top
                asteroid.bottom = random.randint(-350,0)
                asteroid.left = random.randint(0, WIDTH - asteroid.width)

        except:
            print("Asteroid doesn't exist")

    for e_asteroid in exploded_asteroids:
        try:
            e_asteroid.y = e_asteroid.y + 10 # Move down

            if asteroid.top < HEIGHT:
                exploded_asteroid.remove(e_asteroid)

        except:
            print("Asteroid doesn't exist")
