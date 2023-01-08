import pygame
import pygame.math
from random import uniform, randint, choice
import math
from sys import exit
from pygame.locals import *
from config import width, height, screen, tb_border_width, tb_border_color, \
    initial_proj_speed, level_square_width, hearts_color, col_text_boxes, Topics, environment, science, history, math, qa, custom, player_health
from asteroid import Asteroid
from player import Player
import os

topic = Topics()
# pygame.init()
pygame.font.init()

pygame.display.set_caption("Astro-Academy")

font = pygame.font.SysFont("Arial", 72)

fps = 60
question_font = pygame.font.SysFont("Courier", 30)
base_font = pygame.font.SysFont("Courier", tb_border_width//2)
big_base_font = pygame.font.SysFont("Courier", 48)
large_base_font = pygame.font.SysFont("Courier", 55)
massive_base_font = pygame.font.SysFont("Courier", 90)
# main game loop

counter_of_gen_asteroids = 0


def gen_asteroid(player, topic):
    global counter_of_gen_asteroids
    words = qa[topic]
    if len(words) == 0:
        custom_loop()
    for i in range(len(words)):
        words[i] = (words[i][0], words[i][1])
    index = counter_of_gen_asteroids % len(words)
    counter_of_gen_asteroids += 1
    return Asteroid(words[index][1], words[index][0], player.asteroid_currrent_speed)


def game_loop(should_start_new_game=True, topic=None):
    crash_sound = pygame.mixer.Sound(
        "explosion-sound-effect-free-download_2_cut_1sec.wav")
    if should_start_new_game:
        background_image = pygame.image.load("background.png").convert()
        background_image = pygame.transform.scale(
            background_image, (width, background_image.get_height()*width/background_image.get_width()))

        # Create a variable to store the y coordinate of the background
        background_y = 0

        # Set the speed at which the background should scroll
        scroll_speed = -0.6
        clock = pygame.time.Clock()

        player = Player()

        ast = gen_asteroid(player, topic)
        current_text = ''
        input_rect = pygame.Rect(
            0, height-tb_border_width, width, tb_border_width)
        prompt_rect = pygame.Rect(0, 0, width, tb_border_width)
        level_rect = pygame.Rect(
            width-3*level_square_width, level_square_width, level_square_width, level_square_width)
        score_rect = pygame.Rect(
            width-3*level_square_width, level_square_width*3//2, level_square_width, level_square_width)

        counter_for_ast_explosion = 0
        count_for_ast_explosion = False

        spaceship_image = pygame.image.load(os.path.join("spaceship.png"))
        spaceship_image = pygame.transform.scale(spaceship_image, (150, 150))
    while True:
        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, background_y))
        screen.blit(background_image, (0, background_y +
                    background_image.get_height()))
        clock.tick(fps)
        # spaceship = pygame.image.load(os.path.join("spaceship.png"))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # pygame.quit()
                    # exit()
                    pause_loop()
                # 13 for enter key
                if event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]
                elif event.key != 13:
                    current_text += event.unicode

                if event.key == 13 and not player.should_follow_ast:
                    if current_text == ast.word:
                        player.shoot_asteroid(ast)
                    else:
                        pass
                    current_text = ''
        if player.lives <= 0:
            death_loop(player)
        player.update()

        if count_for_ast_explosion:
            counter_for_ast_explosion += 1
            ast.draw()
            ast.color = (0, 255, 0)
        else:
            ast.update()

        if ast.is_out_of_bounds():
            player.lives -= 1
            count_for_ast_explosion = False
            counter_for_ast_explosion = 0
            player.wrong_stuffs.append(ast.prompt)
            player.wrong_stuffs.append(ast.word)
            ast = gen_asteroid(player, topic)
            current_text = ''

        if player.should_follow_ast:
            if player.has_collided_with_asteroid():
                pygame.mixer.Sound.play(crash_sound)
                count_for_ast_explosion = True
                ast.image = pygame.image.load(os.path.join("explosion.png"))
                ast.image = pygame.transform.scale(
                    ast.image, (2*ast.radius, 2*ast.radius))

        if counter_for_ast_explosion >= 5:
            count_for_ast_explosion = False
            counter_for_ast_explosion = 0
            ast = gen_asteroid(player, topic)
            current_text = ''

        if player.is_new_level():
            pass

            # add on the flashing
        # Update the y coordinate of the background
        background_y -= scroll_speed

        # If the background has moved off the screen, reset its y coordinate
        if background_y < -background_image.get_height():
            background_y = 0
        if background_y > 0:
            background_y = -background_image.get_height()

        text_surface = base_font.render(
            f'A: {current_text}', True, (255, 255, 255))
        text_surface_prompt = question_font.render(
            f'Q: {ast.prompt}', True, (255, 255, 255))

        text_surface_level = base_font.render(
            f'Lvl. {player.level}', True, (255, 255, 255))

        text_surface_score = base_font.render(
            f'Score: {int(player.score)}', True, (255, 255, 255))

        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        screen.blit(text_surface_prompt, (prompt_rect.x+5, prompt_rect.y+5))
        screen.blit(text_surface_level, (level_rect.x+5, level_rect.y+5))
        screen.blit(text_surface_score, (score_rect.x+5, score_rect.y+5))

        player.hearts_draw()

        screen.blit(spaceship_image,
                    (width/2-spaceship_image.get_width()/2, height-150))

        pygame.display.update()


def pause_loop():
    running = True
    # menu = pygame.draw.rect(screen, (255,255,255), pygame.Rect(width, height))
    clock = pygame.time.Clock()

    exit_to_main_menu = big_base_font.render(
        "Press [esc] to escape to main menu", True, (255, 255, 255))
    continue_to_game = big_base_font.render(
        "Press [space] to resume game", True, (255, 255, 255))

    background = pygame.image.load(
        os.path.join('title screen image.png'))
    background = pygame.transform.scale(
        background, (width, height))
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    title_loop()
                if event.key == K_SPACE:
                    return

        screen.blit(exit_to_main_menu, (width/8, height/2))
        screen.blit(continue_to_game, (width/8, height/2+200))

        pygame.display.update()


def death_loop(player: Player):
    fail_sound = pygame.mixer.Sound(
        "wa-wa-wa-sound-effect-trending-sound-effect-no-copyright.wav")
    pygame.mixer.Sound.play(fail_sound)

    clock = pygame.time.Clock()

    you_died = big_base_font.render(
        f'You Died!', True, (255, 255, 255))
    results = big_base_font.render(
        f'Score: {int(player.score)} | Level: {player.level}', True, (255, 255, 255))
    exit_to_main_menu = big_base_font.render(
        "Press [esc] to Exit to Title Screen", True, (255, 255, 255))
    continue_to_game = big_base_font.render(
        "Press [space] to Continue to Review", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    title_loop()
                if event.key == K_SPACE:
                    review_loop(player)

        screen.blit(you_died, (width/8, height/2-400))
        screen.blit(results, (width/8, height/2-200))
        screen.blit(exit_to_main_menu, (width/8, height/2))
        screen.blit(continue_to_game, (width/8, height/2+200))

        pygame.display.update()


def review_loop(player: Player):
    clock = pygame.time.Clock()

    displays = [None]*(2*player_health)

    for i in range(2*player_health):
        displays[i] = question_font.render(
            player.wrong_stuffs[i], True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    title_loop()
                if event.key == K_SPACE:
                    title_loop()
        for i in range(2*player_health):
            screen.blit(displays[i], (width/8, 50*i))

        pygame.display.update()


def custom_loop():
    clock = pygame.time.Clock()

    current_text = ''

    instr = big_base_font.render(
        "Custom Question/Answer Creation", True, (255, 255, 255))

    enter_question = big_base_font.render(
        "Give a question for the user to answer", True, (255, 255, 255))
    enter_answer = big_base_font.render(
        "Give the answer to the previous question", True, (255, 255, 255))

    custom_qa = []

    on_question = True

    topleft = large_base_font.render(
        "If You Want to Leave : Press Quit", True, (255, 255, 255))
    topright = large_base_font.render(
        "After Finishing : Press Start", True, (255, 255, 255))
    topleft_rect = pygame.Rect(0, 0, width, 100)
    topright_rect = pygame.Rect(
        0, height-topleft.get_height(), width, 100)

    background = pygame.image.load(
        os.path.join('title screen image.png'))
    background = pygame.transform.scale(
        background, (width, height))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]
                elif event.key != 13:  # 13 back
                    current_text += event.unicode
                else:
                    if on_question:
                        custom_qa.append((current_text,))
                    else:
                        custom_qa[-1] = (custom_qa[-1][0], current_text)
                    on_question = not on_question
                    current_text = ''

        screen.blit(instr, (width/8, height/2-200))
        if on_question:
            screen.blit(enter_question, (width/8, height/2))
        else:
            screen.blit(enter_answer, (width/8, height/2))

        if on_question:
            user_text = base_font.render(
                f'Enter Q: {current_text}', True, (255, 255, 255))
        else:
            user_text = base_font.render(
                f'Enter A: {current_text}', True, (255, 255, 255))
        screen.blit(user_text, (width/8, height/2+200))

        mx, my = pygame.mouse.get_pos()

        chang_amnt = 50
        if topleft_rect.collidepoint(mx, my):
            topic.environment_current_time = min(
                topic.environment_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                if on_question:
                    qa[custom] = custom_qa
                else:
                    qa[custom] = custom_qa[:-1]
                game_loop(True, custom)
        else:
            topic.environment_current_time = max(
                topic.environment_current_time-1, 0)
        topic.environment_current_color = (
            topic.environment_color-pygame.math.Vector3(topic.default_color))*(min(topic.environment_current_time, chang_amnt))//chang_amnt+topic.default_color

        if topright_rect.collidepoint(mx, my):
            topic.history_current_time = min(
                topic.history_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                title_loop()
        else:
            topic.history_current_time = max(
                topic.history_current_time-1, 0)
        topic.history_current_color = (
            topic.history_color-pygame.math.Vector3(topic.default_color))*(min(topic.history_current_time, chang_amnt))//chang_amnt+topic.default_color
        pygame.draw.rect(screen, topic.environment_current_color, topleft_rect)
        pygame.draw.rect(screen, topic.history_current_color, topright_rect)

        screen.blit(topright, (width//2 - topleft.get_width()//2, 0))

        screen.blit(topleft, (width//2-topleft.get_height() -
                    topleft.get_width()//2, height-topleft.get_height()))

        pygame.display.update()


def menu_loop():
    clock = pygame.time.Clock()

    pos_start_game = width
    join_game_text = large_base_font.render(
        "Click on the topic of choice to start game!", True, (255, 255, 255))

    background = pygame.image.load(
        os.path.join('title screen image.png'))
    background = pygame.transform.scale(
        background, (width, height))

    background_words = pygame.image.load(
        os.path.join('title words.png'))
    background_words = pygame.transform.scale(
        background_words, (width*3//4, background_words.get_height()*width*3//(4*background_words.get_width())))

    dx, dy = 400, 100

    topleft = massive_base_font.render("Environmental", True, (255, 255, 255))

    topright = massive_base_font.render("History", True, (255, 255, 255))
    botleft = massive_base_font.render("Math", True, (255, 255, 255))
    botright = massive_base_font.render("Science", True, (255, 255, 255))

    botbot = massive_base_font.render("Custom", True, (0, 0, 0))

    # screen.blit(topright, (width/8, height/2))
    topleft_rect = pygame.Rect(width//2-dx-botleft.get_height() //
                               1-150, -botleft.get_height()//1 + height//1.5-dy, 700, 100)

    topright_rect = pygame.Rect(width//2+dx-botleft.get_height() //
                                1, -botleft.get_height()//1 + height//1.5-dy, 385, 100)

    botleft_rect = pygame.Rect(width//2-dx-botleft.get_height() //
                               1, -botleft.get_height()//1 + height//1.5+dy, 215, 100)
    botright_rect = pygame.Rect(width//2+dx-botleft.get_height() //
                                1, -botleft.get_height()//1 + height//1.5+dy, 385, 100)

    botbot_rect = pygame.Rect(
        width//2-botbot.get_width()//2, 3*height//4, 330, 100)

    while True:
        clock.tick(fps)
        screen.fill((0, 0, 128))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    title_loop()
                # if event.key == K_SPACE:
                #    game_loop()
        mx, my = pygame.mouse.get_pos()

        chang_amnt = 50
        if topleft_rect.collidepoint(mx, my):
            topic.environment_current_time = min(
                topic.environment_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                game_loop(True, environment)
        else:
            topic.environment_current_time = max(
                topic.environment_current_time-1, 0)
        topic.environment_current_color = (
            topic.environment_color-pygame.math.Vector3(topic.default_color))*(min(topic.environment_current_time, chang_amnt))//chang_amnt+topic.default_color

        if topright_rect.collidepoint(mx, my):
            topic.history_current_time = min(
                topic.history_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                game_loop(True, history)
        else:
            topic.history_current_time = max(
                topic.history_current_time-1, 0)
        topic.history_current_color = (
            topic.history_color-pygame.math.Vector3(topic.default_color))*(min(topic.history_current_time, chang_amnt))//chang_amnt+topic.default_color

        if botleft_rect.collidepoint(mx, my):
            topic.math_current_time = min(
                topic.math_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                game_loop(True, math)
        else:
            topic.math_current_time = max(
                topic.math_current_time-1, 0)
        topic.math_current_color = (
            topic.math_color-pygame.math.Vector3(topic.default_color))*(min(topic.math_current_time, chang_amnt))//chang_amnt+topic.default_color

        if botright_rect.collidepoint(mx, my):
            topic.science_current_time = min(
                topic.science_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                game_loop(True, science)
        else:
            topic.science_current_time = max(
                topic.science_current_time-1, 0)
        topic.science_current_color = (
            topic.science_color-pygame.math.Vector3(topic.default_color))*(min(topic.science_current_time, chang_amnt))//chang_amnt+topic.default_color
        if botbot_rect.collidepoint(mx, my):
            topic.custom_current_time = min(
                topic.custom_current_time+1, chang_amnt)
            if pygame.mouse.get_pressed()[0]:
                custom_loop()
        else:
            topic.custom_current_time = max(
                topic.custom_current_time-1, 0)
        topic.custom_current_color = (
            topic.custom_color-pygame.math.Vector3(topic.default_color))*(min(topic.custom_current_time, chang_amnt))//chang_amnt+topic.default_color

        screen.blit(join_game_text, (width//2 -
                    join_game_text.get_width()//2, height*1/6))
        # screen.blit(background_words, (width//2 -
        #                               background_words.get_width()//2, height//2-background_words.get_height()))

        pygame.draw.rect(screen, topic.environment_current_color, topleft_rect)
        pygame.draw.rect(screen, topic.history_current_color, topright_rect)
        pygame.draw.rect(screen, topic.math_current_color, botleft_rect)
        pygame.draw.rect(screen, topic.science_current_color, botright_rect)
        pygame.draw.rect(screen, topic.custom_current_color, botbot_rect)

        screen.blit(topright, (width//2+dx - botleft.get_height() //
                    1, -botleft.get_height()//1 + height//1.5-dy))

        screen.blit(topleft, (width//2-dx-botleft.get_height() //
                    1-150, -botleft.get_height()//1 + height//1.5-dy))

        screen.blit(botright, (width//2+dx-botleft.get_height() //
                    1, -botleft.get_height()//1 + height//1.5+dy))

        screen.blit(botleft, (width//2-dx-botleft.get_height() //
                    1, -botleft.get_height()//1 + height//1.5+dy))

        screen.blit(botbot, (width//2-botbot.get_width()//2, height*3/4))
        pygame.display.update()


def title_loop():
    clock = pygame.time.Clock()

    pos_start_game = width
    join_game_text = big_base_font.render(
        "Press [space] to start game", True, (255, 255, 255))
    background = pygame.image.load(
        os.path.join('title screen image.png'))
    background = pygame.transform.scale(
        background, (width, height))

    background_words = pygame.image.load(
        os.path.join('title words.png'))
    background_words = pygame.transform.scale(
        background_words, (width*3//4, background_words.get_height()*width*3//(4*background_words.get_width())))

    num_asts = 13
    asts = [None]*num_asts
    for i in range(num_asts):
        x1, x2 = (width/num_asts*i*6) % width, (width/num_asts*i*6+100) % width
        if x1 > x2:
            x2, x1 = x1, x2
        asts[i] = Asteroid('Easter Egg', '', 3, (uniform(x1, x2), -100),
                           (uniform(-0.7, 0.7), uniform(0.4, 0.8)))

    ast_delays = [randint(200*i, 100+200*i) for i in range(num_asts)]
    ast_timers = [0 for _ in range(num_asts)]

    while True:
        clock.tick(fps)
        screen.fill((0, 0, 128))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_SPACE:
                    menu_loop()
        for i in range(num_asts):
            ast = asts[i]
            if ast_timers[i] >= ast_delays[i]:
                ast.update()
            if ast.pos.y >= height+200:
                ast.pos.y = -100
                ast.pos.x = (ast.pos.x) % width

            ast_timers[i] += 1
        screen.blit(join_game_text, (pos_start_game, height*2/3))
        screen.blit(background_words, (width//2 -
                                       background_words.get_width()//2, height//2-background_words.get_height()))

        # screen.blit(esc_text, (width/8, height/2+200))
        pos_start_game -= 1
        if pos_start_game >= width+1:
            pos_start_game = -800
        if pos_start_game <= -801:
            pos_start_game = width

        pygame.display.update()


if __name__ == "__main__":
    title_loop()
