import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEVOUR the yummies")

BG = pygame.transform.scale(pygame.image.load("bg_gingerbread.png"), (WIDTH, HEIGHT))

PLAYER_WIDTH= 40
PLAYER_HEIGHT = 60

FOOD_WIDTH = 10
FOOD_HEIGHT = 20
FOOD_VEL = 3
WAVE_COUNT = 0

PLAYER_VEL = 14

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, start_game, foods, eat, collected_yummies):
    global WAVE_COUNT
    WIN.blit(BG, (0, 0))
    space_to_start = ("Press space to start")
    press_text = FONT.render(f"{space_to_start}", 1, (255, 255, 255))
    start_game_dialouge = ("EAT THE YUMMIES!")
    dialouge_text = FONT.render(f"{start_game_dialouge}", 1, (255, 255, 255))
    time_text = FONT.render(f"hungry for: {round(elapsed_time)} seconds", 1, (255, 255, 255))    
    waved_print_clear = (f"Wave {WAVE_COUNT} Cleared!")
    yummies_counter = FONT.render(f"yummies: {collected_yummies}", 1, (255, 255, 255))
    waved_clear_text = FONT.render(f"{waved_print_clear}", 1, (255, 255, 255))
        
    if start_game == False:
        WIN.blit(press_text, (WIDTH/2 - press_text.get_width()/2, 635))
    if eat == False and start_game == True:
        WIN.blit(dialouge_text, (WIDTH/2 - dialouge_text.get_width()/2, 635)) 
    if start_game == True:
        WIN.blit(time_text, (40, 30))
        for food in foods:
            pygame.draw.rect(WIN, "white", food)
    if eat == True:
        WIN.blit(yummies_counter, (WIDTH/2 - yummies_counter.get_width()/2, 600))
    if WAVE_COUNT > 0:
        WIN.blit(waved_clear_text, (700, 40))

    pygame.draw.rect(WIN, (200, 110, 175), player)
    pygame.display.update()

def wave(food_add_increment, collected_yummies):
    global WAVE_COUNT
    if collected_yummies >= 10:
        food_add_increment = max(500, food_add_increment - 50)
        WAVE_COUNT = 1
    if collected_yummies >= 25: #this is the second wave- 25 collected yummies
        food_add_increment = max(300, food_add_increment - 50)
        WAVE_COUNT = 2

    if collected_yummies >= 45: 
        food_add_increment = max(100, food_add_increment - 50)
        WAVE_COUNT = 3
    if collected_yummies >= 46: 
        food_add_increment = max(200, food_add_increment - 50)

    if collected_yummies >= 65:
        food_add_increment = max(75, food_add_increment - 50)
        WAVE_COUNT = 4
    if collected_yummies >= 68:
        food_add_increment = max(50, food_add_increment - 50)

    if collected_yummies >= 85: 
        food_add_increment = max(50, food_add_increment - 50)
        WAVE_COUNT = 5
    if collected_yummies >= 90: 
        food_add_increment = max(200, food_add_increment - 50)

    if collected_yummies >= 100: 
        food_add_increment = 2000
    
    if collected_yummies >= 105:
        food_add_increment = max(100, food_add_increment - 60)
        WAVE_COUNT = 6
    if collected_yummies >= 110: 
        food_add_increment = max(75, food_add_increment - 60)
        WAVE_COUNT = 7
    if collected_yummies >= 115: 
        food_add_increment = max(50, food_add_increment - 60)
        WAVE_COUNT = 8
    if collected_yummies >= 120: 
        food_add_increment = max(50, food_add_increment - 60)
        WAVE_COUNT = 9
    if collected_yummies >= 130: 
        food_add_increment = max(50, food_add_increment - 60)
        WAVE_COUNT = 10
    return food_add_increment

def lost():
    lost_text = FONT.render("WHAT AN UNGRATEFUL CHILD.", 1, (255, 255, 255))
    WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
    pygame.display.update()
    time.sleep(6)
    pygame.quit()

def main():
    run = True
    start_game = False  
    player = pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    CLOCK = pygame.time.Clock()
    elapsed_time = 0
    elapsed_b4start = 0 # takes the time when game = true or space is pressed

    collected_yummies = 0
    food_add_increment = wave(2000, collected_yummies)  # Initial food add increment
    food_milis_count = 0
    foods = []
    eat = False

    times_space_pressed = 0
    
    while run:
        food_milis_count += CLOCK.tick(60)
        keys = pygame.key.get_pressed()
        WAVE_COUNT = 0  # Reset wave count at the start of the game
        draw(player, elapsed_time, start_game, foods, eat, collected_yummies)

        if keys[pygame.K_SPACE]:
            start_game = True
            times_space_pressed += 1
            if times_space_pressed == 1:
                elapsed_b4start = time.time()
        
        if start_game == True:
            elapsed_time = time.time() - elapsed_b4start
            if food_milis_count > food_add_increment:
                for _ in range(1):
                    food_x = random.randint(0, WIDTH - FOOD_WIDTH)
                    food = pygame.Rect(food_x, -FOOD_HEIGHT, FOOD_WIDTH, FOOD_HEIGHT)
                    foods.append(food)

                food_add_increment = max(1000, food_add_increment - 20)
                food_milis_count = 0

                wave(food_add_increment, collected_yummies)
    
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0 and start_game == True:
            player.x -= PLAYER_VEL
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL < 0:
            player.x = 0
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH and start_game == True:
            player.x += PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH > WIDTH:
            player.x = WIDTH - PLAYER_WIDTH

        for food in foods[:]:
            food.y += FOOD_VEL
            if food.y > HEIGHT:
                foods.remove(food)
                
                lost()
            
            elif food.y + food.height >= player.y and food.colliderect(player):
                foods.remove(food)
                eat = True
                collected_yummies += 1  #adds 1 everytime player eats yummies
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()

if __name__ == "__main__":
    main()