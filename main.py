import turtle
import math
import random
import pygame
 
# Setup Screen
 
wn = turtle.Screen()
wn.setup(600, 800)
wn.bgcolor("black")
wn.tracer(0)
wn.bgpic("bg.gif")


pygame.mixer.init()  # Initialize mixer
pygame.mixer.music.load("NON.mp3")  # Your music file
pygame.mixer.music.set_volume(0.5)  # Optional: volume 0.0 - 1.0
pygame.mixer.music.play(-1)  # -1 means loop indefinitely


# Difficulty Selection

difficulty = wn.textinput("Select Difficulty", "Choose difficulty: easy / medium / hard").lower()
if difficulty not in ["easy", "medium", "hard"]:
    difficulty = "easy"


# Load Sprites
 
for direction in ["up", "down", "left", "right", "boss"]:
    wn.addshape(f"{direction}.gif")

 
# Player Setup
 
player = turtle.Turtle()
player.shape("down.gif")
player.penup()
player.goto(0, -300)
SPEED = 5

player_max_health = 100
player_current_health = 100

 
# Boss Setup
 
boss = turtle.Turtle()
boss.shape("boss.gif")
boss.penup()
boss.goto(0, 250)

boss_max_health = 100
boss_current_health = 100

boss_speed_x = 4
boss_direction_x = 1

 
# Health Bars
 
health_bar_boss = turtle.Turtle()
health_bar_boss.hideturtle()
health_bar_boss.penup()
health_bar_boss.goto(-20, 370)
health_bar_boss.pendown()
health_bar_boss.color("red")
health_bar_boss.pensize(10)

health_bar_player = turtle.Turtle()
health_bar_player.hideturtle()
health_bar_player.penup()
health_bar_player.goto(-20, -390)
health_bar_player.pendown()
health_bar_player.color("green")
health_bar_player.pensize(10)

def draw_health_bar():
    health_bar_boss.clear()
    health_bar_boss.penup()
    health_bar_boss.goto(10, 370)
    health_bar_boss.pendown()
    health_bar_boss.forward(200 * (boss_current_health / boss_max_health))
    
    health_bar_player.clear()
    health_bar_player.penup()
    health_bar_player.goto(10, -390)
    health_bar_player.pendown()
    health_bar_player.forward(200 * (player_current_health / player_max_health))

draw_health_bar()

 
# Movement State
 
keys_pressed = {"Up": False, "Down": False, "Left": False, "Right": False}

def key_press(key):
    keys_pressed[key] = True
    update_player_shape()

def key_release(key):
    keys_pressed[key] = False

def update_player_shape():
    if keys_pressed["Up"]:
        player.shape("up.gif")
    elif keys_pressed["Down"]:
        player.shape("down.gif")
    elif keys_pressed["Left"]:
        player.shape("left.gif")
    elif keys_pressed["Right"]:
        player.shape("right.gif")

 
# Bullets
 
boss_bullets = []
player_bullets = []

def create_bullet(x, y, dx, dy, color="yellow"):
    bullet = turtle.Turtle()
    bullet.shape("circle")
    bullet.color(color)
    bullet.shapesize(0.3, 0.3)
    bullet.penup()
    bullet.goto(x, y)
    bullet.speed(0)
    bullet.dx = dx
    bullet.dy = dy
    return bullet

def shoot_boss_pattern():
    global boss_current_health
    phase = 1
    if boss_current_health <= boss_max_health * 0.7: phase = 2
    if boss_current_health <= boss_max_health * 0.4: phase = 3

    if difficulty == "easy":
        bullets = 12 + (phase-1)*3
        speed = 3 + (phase-1)
        for i in range(bullets):
            angle = 2*math.pi*i/bullets
            dx = math.cos(angle)*speed
            dy = math.sin(angle)*-speed
            boss_bullets.append(create_bullet(boss.xcor(), boss.ycor(), dx, dy))
        wn.ontimer(shoot_boss_pattern, max(1200 - phase*200, 400))
    
    elif difficulty == "medium":
        bullets = 18 + (phase-1)*4
        speed = 3 + phase
        offset = random.uniform(0, 2*math.pi)
        for i in range(bullets):
            angle = 2*math.pi*i/bullets + offset
            dx = math.cos(angle)*speed
            dy = math.sin(angle)*-speed
            color = "orange" if i%2==0 else "yellow"
            boss_bullets.append(create_bullet(boss.xcor(), boss.ycor(), dx, dy, color))
        wn.ontimer(shoot_boss_pattern, max(900 - phase*150, 300))
    
    elif difficulty == "hard":
        for j in range(3):
            num_bullets = 20 + j*5 + (phase-1)*2
            speed = 3 + j + phase
            offset = random.uniform(0, 2*math.pi)
            for i in range(num_bullets):
                angle = 2*math.pi*i/num_bullets + offset
                color = "red" if j%2==0 else "orange"
                dx = math.cos(angle)*speed
                dy = math.sin(angle)*-speed
                boss_bullets.append(create_bullet(boss.xcor(), boss.ycor(), dx, dy, color))
        wn.ontimer(shoot_boss_pattern, max(800 - phase*100, 200))

def shoot_player():
    bullet = create_bullet(player.xcor(), player.ycor() + 20, 0, 7, "cyan")
    player_bullets.append(bullet)

 
# End Game / Victory
 
def game_over():
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("red")
    msg.penup()
    msg.goto(0,0)
    msg.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    wn.update()

def victory():
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("green")
    msg.penup()
    msg.goto(0,0)
    msg.write("VICTORY!", align="center", font=("Arial", 36, "bold"))
    wn.update()

 
# Movement Loop
 
def move():
    global boss_direction_x, player_current_health, boss_current_health

    if player_current_health <= 0:
        game_over()
        return
    if boss_current_health <= 0:
        victory()
        return

    # Player movement
    x, y = player.xcor(), player.ycor()
    if keys_pressed["Up"] and y + SPEED < 390: y += SPEED
    if keys_pressed["Down"] and y - SPEED > -390: y -= SPEED
    if keys_pressed["Left"] and x - SPEED > -290: x -= SPEED
    if keys_pressed["Right"] and x + SPEED < 290: x += SPEED
    player.goto(x, y)

    # Boss horizontal movement
    boss.setx(boss.xcor() + boss_speed_x * boss_direction_x)
    if boss.xcor() > 250 or boss.xcor() < -250:
        boss_direction_x *= -1

    # Update boss bullets
    for bullet in boss_bullets[:]:
        bullet.setx(bullet.xcor() + bullet.dx)
        bullet.sety(bullet.ycor() + bullet.dy)

        # Remove bullet if touches wall
        if bullet.xcor() > 290 or bullet.xcor() < -290 or bullet.ycor() > 400 or bullet.ycor() < -400:
            boss_bullets.remove(bullet)
            bullet.hideturtle()
            continue

        # Collision with player
        if bullet.distance(player) < 15:
            player_current_health -= 5
            boss_bullets.remove(bullet)
            bullet.hideturtle()

    # Update player bullets
    for bullet in player_bullets[:]:
        bullet.sety(bullet.ycor() + bullet.dy)
        if bullet.distance(boss) < 40:
            boss_current_health -= 5
            if boss_current_health < 0: boss_current_health = 0
            player_bullets.remove(bullet)
            bullet.hideturtle()
        elif bullet.ycor() > 400:
            player_bullets.remove(bullet)
            bullet.hideturtle()

    draw_health_bar()
    wn.update()
    wn.ontimer(move, 20)

 
# Key Bindings
 
wn.listen()
for key in ["Up", "Down", "Left", "Right"]:
    wn.onkeypress(lambda k=key: key_press(k), key)
    wn.onkeyrelease(lambda k=key: key_release(k), key)

wn.onkeypress(shoot_player, "e")

 
# Start Game
 
shoot_boss_pattern()
move()
wn.mainloop()
