import pygame, sys, random

#Make Start Screen

def draw_floor():
    screen.blit(floor,(floor_xpos, 725))
    screen.blit(floor,(floor_xpos + 1300, 725))

def create_pipe():
    random_pipepos = random.choice(pipe_height)
    botttom_pipe = pipe_image.get_rect(midtop=(1500, random_pipepos))
    top_pipe = pipe_image.get_rect(midbottom=(1500, random_pipepos-200))
    return botttom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 6
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_image, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_image, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score

    for pipe in pipes:
        if dillon_rect.colliderect(pipe):
            hit_sound.play()
            can_score = True
            return False
      
    if dillon_rect.top <= -100 or dillon_rect.bottom >= 725:
        hit_sound.play()
        can_score = True
        return False
  
    return True

def rotate_dillon(dillon):
    new_dillon = pygame.transform.rotozoom(dillon, -dillon_movement * 2, 1)
    return new_dillon

def start_screen(game_state):
    print('make start screen')


def score_display(game_state):
    if game_state == 'main_game':
       score_text = game_font.render(str(int(score)), True, (255, 255, 255))
       score_rect = score_text.get_rect(center = (650, 100))
       screen.blit(score_text, score_rect)
    if game_state == 'game_over':
       score_text = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
       score_rect = score_text.get_rect(center = (650, 100))
       screen.blit(score_text, score_rect)

       highscore_text = game_font.render(f'High Score: {int(highscore)}', True, (255, 255, 255))
       highscore_rect = highscore_text.get_rect(center = (650, 200))
       screen.blit(highscore_text, highscore_rect)

def update_score(score, highscore):
    if score > highscore:
        highscore = score
    return highscore

def save_highscore(game_state, highscore):
    if game_state == 'game_over':
        f = open('scores.txt', "w")
        f.write(str(highscore))
        f.close()

def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 198 < pipe.centerx <= 205 and can_score == True:
                score += 1
                point_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

def achievements(game_state, score):
    if game_state == 'game_over':
        if score >= 60:
            screen.blit(gold_medal, gold_medal_rect)
        elif score >= 40:
            screen.blit(silver_medal, silver_medal_rect)
        elif score >= 20:
            screen.blit(bronze_medal, bronze_medal_rect)

pygame.init()
pygame.display.set_caption('Flappy Dillon')
screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()
FPS = 60
game_font = pygame.font.Font('assets/font.ttf', 40)

gravity = 0.25
dillon_movement = 0
game_active = False
game_started = False
score = 0

with open('scores.txt', 'r') as file:
    highscore_file = file.read()

highscore = int(highscore_file)

can_score = True

bg = pygame.image.load('assets/images/background.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('assets/images/floor.png').convert()
floor_xpos = 0

dillon_image = pygame.image.load('assets/images/mrdillon.png').convert_alpha()
dillon_rect = dillon_image.get_rect(center = (200, 400))

pipe_image = pygame.image.load('assets/images/computer.jpeg')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [325,450,575]

game_over_message = pygame.image.load('assets/images/gameover.png')
game_over_message = pygame.transform.scale2x(game_over_message)
game_over_rect = game_over_message.get_rect(center=(650, 325))

start_message = pygame.image.load('assets/images/start.png')
start_message = pygame.transform.scale2x(start_message)
start_rect = start_message.get_rect(center = (650, 500))

title_message = pygame.image.load('assets/images/title.png')
title_message = pygame.transform.scale2x(title_message)
title_rect = title_message.get_rect(center = (650, 150))


flap_sound = pygame.mixer.Sound('assets/audio/assets_audio_wing.ogg')
hit_sound = pygame.mixer.Sound('assets/audio/assets_audio_hit.ogg')
point_sound = pygame.mixer.Sound('assets/audio/assets_audio_point.ogg')

gold_medal = pygame.image.load('assets/images/gold.png')
gold_medal = pygame.transform.scale2x(gold_medal)
gold_medal_rect = gold_medal.get_rect(center = (650, 500))

silver_medal = pygame.image.load('assets/images/silver.png')
silver_medal = pygame.transform.scale2x(silver_medal)
silver_medal_rect = silver_medal.get_rect(center = (650, 500))

bronze_medal = pygame.image.load('assets/images/bronze.png')
bronze_medal = pygame.transform.scale2x(bronze_medal)
bronze_medal_rect = bronze_medal.get_rect(center = (650, 500))


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                if not game_started:
                    game_started = True
                    game_active = True
                    dillon_movement = 0
                    score = 0
                    dillon_rect.center = (200, 400)
                    pipe_list.clear()
                else:
                    game_active = True
                    dillon_movement = 0
                    score = 0
                    dillon_rect.center = (200, 400)
                    pipe_list.clear()
            if event.key == pygame.K_SPACE and game_active:
                dillon_movement = 0
                dillon_movement -= 7
                flap_sound.play()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg,(0,0))

    if game_active:
        dillon_movement += gravity
        rotated_dillon = rotate_dillon(dillon_image)
        dillon_rect.centery += dillon_movement
        screen.blit(rotated_dillon,dillon_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()
        score_display('main_game')
    elif not game_started:
        screen.blit(start_message, start_rect)
        screen.blit(title_message, title_rect)
        screen.blit(dillon_image, dillon_rect)
    else:
        screen.blit(game_over_message, game_over_rect)
        highscore = update_score(score, highscore)
        score_display('game_over')
        save_highscore('game_over', highscore)
        achievements('game_over', score)

    floor_xpos -= 4
    draw_floor()
    if floor_xpos <= -1300:
        floor_xpos = 0

    pygame.display.update()
    clock.tick(FPS) 