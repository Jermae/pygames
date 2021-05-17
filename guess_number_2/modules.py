import os
import sys
import time
import pygame
import threading
import random

RED = (255, 0, 0)
BLACK = (0, 0, 0)
AZURE = (240, 255, 255)
WHITE = (255, 255, 255)
MISTYROSE = (255, 228, 225)
PALETURQUOISE = (175, 238, 238)
PAPAYAWHIP = (255, 239, 213)
SCREENSIZE = (400, 400)
CURRENTPATH = os.getcwd()
FONTPATH = os.path.join(CURRENTPATH, 'guess_number_2\\fonts\\AdobeMingStd-Light.otf')
FONTPATH_CN = os.path.join(CURRENTPATH, 'guess_number_2\\fonts\\FZSTK.TTF')

MAXSTEP = 10

VALID = 1
TYPEERROR = 0

ANSWEREVENT = pygame.USEREVENT + 1
SUCCESSEVENT = pygame.USEREVENT + 2
ERROREVENT = pygame.USEREVENT + 3
RESTARTEVENT = pygame.USEREVENT + 4
FAILEVENT = pygame.USEREVENT + 5

def init_game():
    t = threading.Thread(target=init_game_real, args=())
    t.start()


def init_game_real():
    pygame.init()
    pygame.display.set_caption('猜数字游戏2')
    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    global step_counter, time_counter, screen, res, low, high
    screen = pygame.display.set_mode(SCREENSIZE)
    step_counter, time_counter = 0, 0
    low, high = 1, 100
    res = random.randint(1,100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                time_counter += 1
            elif event.type == ANSWEREVENT:
                showInfo(str(res), screen)
                pygame.display.flip()
                time.sleep(2)
            elif event.type == SUCCESSEVENT:
                while True:
                    screen.fill(AZURE)
                    showTop(screen)
                    showInfo(str(res)+"猜对了！", screen)
                    pygame.display.flip()

                    event1 = pygame.event.poll()
                    if event1.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event1.type == RESTARTEVENT:
                        break
            elif event.type == FAILEVENT:
                while True:
                    screen.fill(AZURE)
                    showTop(screen)
                    showInfo("步数耗尽！", screen)
                    pygame.display.flip()

                    event1 = pygame.event.poll()
                    if event1.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event1.type == RESTARTEVENT:
                        break
            elif event.type == ERROREVENT:
                showInfo("输入1-100的整数", screen)
                pygame.display.flip()
                time.sleep(2)

        screen.fill(AZURE)
        showTop(screen)

        pygame.display.flip()
        clock.tick(30)


def quit_game():
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def restart_game():
    global step_counter, time_counter, res, low, high
    step_counter, time_counter = 0, 0
    low, high = 1, 100
    res = random.randint(1,100)
    pygame.event.post(pygame.event.Event(RESTARTEVENT))


def get_answer():
    pygame.event.post(pygame.event.Event(ANSWEREVENT))


def guess(number):
    flag = check_input(number)
    global res,step_counter
    if flag == TYPEERROR:
        pygame.event.post(pygame.event.Event(ERROREVENT))
    else:
        updateSurface(number)
        if number == res:
            pygame.event.post(pygame.event.Event(SUCCESSEVENT))
        elif step_counter==MAXSTEP:
            pygame.event.post(pygame.event.Event(FAILEVENT))


def updateSurface(number):
    global step_counter, screen, res, low, high
    step_counter += 1
    if number == res:
        return
    elif number<=low or number>=high:
        return
    elif number < res:
        low = number
    elif number > res:
        high = number


def check_input(number):
    if not isinstance(number, int):
        return TYPEERROR
    if number>100 or number<1:
        return TYPEERROR
    return VALID


def showTop(screen):
    font = pygame.font.Font(FONTPATH_CN, 20)
    text_render1 = font.render("耗时", True, BLACK)
    screen.blit(text_render1, (90, 5))

    text_render2 = font.render("步数", True, BLACK)
    screen.blit(text_render2, (290, 5))

    font1 = pygame.font.Font(FONTPATH, 30)
    text_render3 = font1.render(str(time_counter // 60) + ":" + str(time_counter % 60), True, BLACK)
    screen.blit(text_render3, (90, 30))
    text_render4 = font1.render(str(step_counter)+" / "+str(MAXSTEP), True, BLACK)
    screen.blit(text_render4, (280, 30))

    font2 = pygame.font.Font(FONTPATH, 60)
    text_render5 = font2.render(str(low) + " - " + str(high), True, BLACK)
    screen.blit(text_render5, (140, 100))

    font3 = pygame.font.Font(FONTPATH_CN, 50)
    text_render6 = font3.render(str("猜一个数字："), True, BLACK)
    screen.blit(text_render6, (80, 250))


def showInfo(text, screen):
    rect = pygame.Rect(50, 200, 300, 180)
    pygame.draw.rect(screen, PAPAYAWHIP, rect)
    font = pygame.font.Font(FONTPATH_CN, 40)
    text_render = font.render(text, True, BLACK)
    font_size = font.size(text)
    screen.blit(text_render, (rect.x + (rect.width - font_size[0]) / 2, rect.y + (rect.height - font_size[1]) / 2))


def showInfo2lines(text1, text2, screen):
    rect = pygame.Rect(50, 200, 300, 180)
    pygame.draw.rect(screen, PAPAYAWHIP, rect)
    font = pygame.font.Font(FONTPATH_CN, 22)
    text_render1 = font.render(text1, True, BLACK)
    text_render2 = font.render(text2, True, BLACK)
    font_size = font.size(text1)
    screen.blit(text_render1,
                (rect.x + (rect.width - font_size[0]) / 2, rect.y + (rect.height - font_size[1]) / 2 - 18))
    screen.blit(text_render2,
                (rect.x + (rect.width - font_size[0]) / 2, rect.y + (rect.height - font_size[1]) / 2 + 18))
