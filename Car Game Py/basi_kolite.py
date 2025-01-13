import pygame
from pygame.locals import *
import random

pygame.font.init()

size = width, height = (1200, 800)
road_w = int(width / 1.6)
roadmark_w = int(width / 80)
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
speed = 1
score_value = 0

font = pygame.font.Font('freesansbold.ttf', 50)

pygame.init()
running = True

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Basi kolite")

screen.fill((135, 145, 110))  # RGB

pygame.display.update()

car = pygame.image.load("car.png")
car_loc = car.get_rect()
car_loc.center = right_lane, height * 0.8

car2 = pygame.image.load("otherCar.png")
car2_loc = car2.get_rect()
car2_loc.center = left_lane, height * 0.2

counter = 0

while running:
    counter += 1
    if counter == 1024:
        speed += 0.25
        counter = 0
        score_value += 1
        print("level up", speed, score_value)

    car2_loc[1] += speed
    if car2_loc[1] > height:
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200

    if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 250:
        print("GAME OVER! YOU LOST")
        break

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT]:
                car_loc = car_loc.move([-int(road_w / 2), 0])
            if event.key in [K_d, K_RIGHT]:
                car_loc = car_loc.move([int(road_w / 2), 0])

    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (width / 2 - road_w / 2, 0, road_w, height)
    )

    pygame.draw.rect(
        screen,
        (255, 240, 60),
        (width / 2 - roadmark_w / 2, 0, roadmark_w, height)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height)
    )

    score_text = font.render(f'Score: ' + str(score_value), True, (255, 255, 255))

    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)
    screen.blit(score_text, (15, 15))
    pygame.display.update()

pygame.quit()
