import pygame
import random

pygame.init()

width = 1200
height = 700

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("space game")



spaceship = pygame.image.load("spaceship.png")
spaceship_x = 50
spaceship_y = 300
spaceship_speed = 5

elmas = pygame.image.load("diamond.png")
elmas_x = random.randint(0, width)
elmas_y = random.randint(0, height)


elmas_speed = 5
elmas_limit = 600



dusman = pygame.image.load("ufo.png")
dusman_x = random.randint(0, width)
dusman_y = random.randint(0, height)
dusman_speed = 4
dusman_limit = 700



font = pygame.font.Font(None, 36)
puan = 0
can = 3
def elmas_collect():
    global puan
    puan += 10

def can_lose():
    global can
    can -= 1
    if can == 0:
        game_over()

def game_over():

    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (width // 2 - 100, height // 2))






clock = pygame.time.Clock()




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elmas_x -= elmas_speed
    if elmas_x < -elmas_limit:
        elmas_x = width
        elmas_y = random.randint(0, height)
        elmas_speed += 1



    dusman_x -= dusman_speed
    if dusman_x < -dusman_limit:
        dusman_x = width
        dusman_y = random.randint(0, height)
        dusman_speed += 1



    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        spaceship_y -= spaceship_speed
    if keys[pygame.K_DOWN]:
        spaceship_y += spaceship_speed

    screen.fill((0, 0, 0))
    elmas_rect = elmas.get_rect(topleft=(elmas_x, elmas_y))
    spaceship_rect = spaceship.get_rect(topleft=(spaceship_x, spaceship_y))
    if elmas_rect.colliderect(spaceship_rect):
        elmas_x = random.randint(0, width)
        elmas_y = random.randint(0, height)
        elmas_speed += 1
        elmas_collect()

    # Düşman ve uzay gemisi çarpışması
    dusman_rect = dusman.get_rect(topleft=(dusman_x, dusman_y))
    if dusman_rect.colliderect(spaceship_rect):
        dusman_x = random.randint(0, width)
        dusman_y = random.randint(0, height)
        dusman_speed += 1
        can_lose()
    if can == 0:
        game_over()
        pygame.display.update()
        pygame.time.delay(4000)
        spaceship_x = 50
        spaceship_y = 300
        elmas_x = random.randint(0, width)
        elmas_y = random.randint(0, height)
        elmas_speed = 5
        dusman_x = random.randint(0, width)
        dusman_y = random.randint(0, height)
        dusman_speed = 4
        puan = 0
        can = 3
        running = True



    screen.blit(spaceship, (spaceship_x, spaceship_y))
    screen.blit(elmas, (elmas_x, elmas_y))
    screen.blit(dusman, (dusman_x, dusman_y))

    puan_text = font.render(f"Puan: {puan}", True, (255, 255, 255))
    can_text = font.render(f"Can: {can}", True, (255, 255, 255))
    screen.blit(puan_text, (10, 10))
    screen.blit(can_text, (width - 100, 10))




    pygame.display.update()
    clock.tick(60)

    

pygame.quit()
