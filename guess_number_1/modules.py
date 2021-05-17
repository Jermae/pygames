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
GRAY = (100, 100, 100)

SCREENSIZE = (400, 630)
CURRENTPATH = os.getcwd()
FONTPATH = os.path.join(CURRENTPATH, 'guess_number_1\\fonts\\AdobeMingStd-Light.otf')
FONTPATH_CN = os.path.join(CURRENTPATH, 'guess_number_1\\fonts\\FZSTK.TTF')

MAXSTEP = 14

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
    pygame.display.set_caption('猜数字游戏1')
    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    global step_counter, time_counter, textSurface, screen, res
    screen = pygame.display.set_mode(SCREENSIZE)
    step_counter, time_counter = 0, 0
    textSurface = pygame.Surface((350, 500))
    textSurface.fill(WHITE)
    insSrface = pygame.Surface((400, 30))
    insSrface.fill(GRAY)
    font = pygame.font.Font(FONTPATH_CN, 20)
    text_render = font.render("A:位置和数字都对 B:数字对但位置不对", True, WHITE)
    insSrface.blit(text_render, (5, 5))

    res = random.sample(range(1, 10), 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                time_counter += 1
            elif event.type == ANSWEREVENT:
                s = str(res[0]) + str(res[1]) + str(res[2])
                showInfo(s, screen)
                pygame.display.flip()
                time.sleep(2)
            elif event.type == SUCCESSEVENT:
                while True:
                    screen.fill(AZURE)
                    showTop(screen)
                    screen.blit(textSurface, (25, 70))
                    screen.blit(insSrface, (0, 600))
                    showInfo("猜对了！", screen)
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
                    screen.blit(textSurface, (25, 70))
                    screen.blit(insSrface, (0, 600))
                    showInfo("步数耗尽！", screen)
                    pygame.display.flip()

                    event1 = pygame.event.poll()
                    if event1.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event1.type == RESTARTEVENT:
                        break
            elif event.type == ERROREVENT:
                showInfo2lines("请输入长度为3的字符串", "且是互不相同的三个数字", screen)
                pygame.display.flip()
                time.sleep(2)

        screen.fill(AZURE)
        showTop(screen)
        screen.blit(textSurface, (25, 70))
        screen.blit(insSrface, (0, 600))

        pygame.display.flip()
        clock.tick(30)


def quit_game():
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def restart_game():
    global step_counter, time_counter, res
    step_counter, time_counter = 0, 0
    res = random.sample(range(1, 10), 3)
    textSurface.fill(WHITE)
    pygame.event.post(pygame.event.Event(RESTARTEVENT))


def get_answer():
    pygame.event.post(pygame.event.Event(ANSWEREVENT))


def guess(number):#input is a string
    flag = check_input(number)
    global res,step_counter
    if flag == TYPEERROR:
        pygame.event.post(pygame.event.Event(ERROREVENT))
    else:
        updateSurface(number)
        if int(number[0])==res[0] and int(number[1])==res[1] and int(number[2])==res[2]:
            pygame.event.post(pygame.event.Event(SUCCESSEVENT))
        elif step_counter==MAXSTEP:
            pygame.event.post(pygame.event.Event(FAILEVENT))


def updateSurface(number):
    global step_counter, time_counter, textSurface, screen, res
    step_counter += 1
    a, b = getAB(number, res)
    y = 5 + (step_counter - 1) * 35

    font = pygame.font.Font(FONTPATH, 25)
    text_render1 = font.render(str(step_counter), True, BLACK)
    textSurface.blit(text_render1, (5, y))

    text_render2 = font.render(number, True, BLACK)
    textSurface.blit(text_render2, (80, y))

    drawRect(str(a),textSurface,310-105,y)
    drawRect("A", textSurface, 310-70, y)
    drawRect(str(b), textSurface, 310-35, y)
    drawRect("B", textSurface, 310, y)


def getAB(number, res):
    countA = 0
    countB = 0
    for i in range(len(res)):
        if int(number[i]) == res[i]:
            countA += 1
    for i in number:
        for j in res:
            if int(i) == j:
                countB += 1
    countB -= countA
    return countA, countB


def check_input(number):
    if not isinstance(number, str):
        return TYPEERROR
    if not number.isdigit():
        return TYPEERROR
    if len(number) != 3:
        return TYPEERROR
    if number[0] == number[1] or number[2] == number[1] or number[2] == number[0]:
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


def drawRect(text, surface, x, y):
    rect = pygame.Rect(x, y, 30, 30)
    pygame.draw.rect(surface, MISTYROSE, rect)
    font = pygame.font.Font(FONTPATH, 24)
    text_render = font.render(text, True, BLACK)
    font_size = font.size(text)
    surface.blit(text_render, (rect.x + (rect.width - font_size[0]) / 2, rect.y + (rect.height - font_size[1]) / 2))
