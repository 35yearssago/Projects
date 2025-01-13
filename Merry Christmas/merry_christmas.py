from turtle import *
import random
from pygame import mixer

screensize(100, 200)

title('Весела Коледа')
colors = ['cyan', 'yellow', 'light yellow']
height = 75
speed(0)
pensize(2)
screen = Screen()
screen.bgpic('merry_christmas.gif')

#TODO WAY TOO LOUD!!!--- set_volume not working!

# mixer.init()
# mixer.music.load('Jingle Bells.mp3')
# mixer.music.set_volume(2)
# mixer.music.play()

penup()
goto(0, -130)
pendown()
left(90)
forward(3 * height)
color('yellow', 'yellow')
begin_fill()
left(126)
for i in range(5):
    forward(height / 5)
    right(144)
    forward(height / 5)
    left(72)
end_fill()
right(126)
color('Green')
backward(height * 4.8)


def tree(d, s):
    pensize(5)
    if d <= 0:
        return
    forward(s)
    tree(d - 1, s * .8)
    right(120)
    tree(d - 3, s * .6)
    right(120)
    tree(d - 3, s * .6)
    right(120)
    backward(s)


def length_select():
    return random.randint(5, 8)


def stars(x, y):
    hideturtle()
    col = random.choice(colors)
    l = length_select()
    color(col)
    penup()
    goto(x, y)
    pendown()
    begin_fill()
    for i in range(5):
        forward(l)
        right(144)
        forward(l)
    end_fill()


tree(12, height)
backward(height/2)

pensize(2)
onscreenclick(stars, 1)

mainloop()
