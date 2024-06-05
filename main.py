# Write your code here :-)
import random

# SET UP YOUR SCREEN CONSTANTS HERE
WIDTH = 500
HEIGHT = 800

asteroids = []
for i in range(10):
    new_asteroid = Actor("cat" + str(random.randint(1, 4)))
    new_asteroid.x = random.randint(0,WIDTH)
    new_asteroid.y = random.randint(-350,0)
    asteroids.append(new_asteroid)

# SET UP YOUR ACTORS HERE
bg = Actor("alien")
ship = Actor("alien", center=(250, 700))
asteroid = Actor("cat1")
bullet = Actor("alien")
heart = Actor("alien")

# SET UP ANY GAME VARIABLES HERE


def draw():
    screen.clear()
    bg.draw()
    ship.draw()
    asteroid.draw()
    for a in asteroids:
        a.draw()


# ADD CODE TO DRAW ANY ACTORS HERE


def update():
    for a in asteroids:
        a.y = a.y + random.randint(1, 10)
        if a.top> HEIGHT:
            a.bottom = random.randint(-350,0)
            a.left = random.randint(0, WIDTH - a.width)
    asteroid.top += 4
    if keyboard.right:
        ship.right += 10
    if keyboard.left:
        ship.left += -10
    pass
