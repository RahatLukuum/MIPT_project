# клавиатурный тренажёр

import pygame
from pygame.locals import *
import sys
import time
import random


class Game:
    '''Класс игры'''
    def __init__(self):
        self.w = 1000
        self.h = 750
        self.active = False
        self.input_text = ''
        self.word = ''
        self.symbolcnt = 0
        self.mistake = 0
        self.time_start = 0
        self.total_time = 0
        self.results = ''
        self.instruction = 'Нажмите на поле ввода и напишите следующее предложение'
        self.spm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)  ## 255 213 102
        self.TEXT_C = (240, 240, 240)  ## 240 240 240
        self.RESULT_C = (255, 70, 70)  ## 255 70 70

        pygame.init()
        self.open_img = pygame.image.load('open_img.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))
        self.bg = pygame.image.load('background.png')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Клавиатурный тренажёр')

    def draw_text(self, screen, msg, y, fsize, color):
        ''' Метод draw_text() — это вспомогательная функция для класса Game,
        которая выводит текст на экран. В качестве аргумента она принимает экран,
        выводимое сообщение, координату y экрана, где нужно нарисовать текст,
        а также размер и цвет шрифта.'''
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        ''' В файле sentences.txt хранится список предложений.
        Метод get_sentence() будет открывать его и возвращать случайное предложение из списка.
        Целая строка будет разбиваться с помощью символа новой строки.'''
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        ''' В методе show_results() рассчитывается скорость набора. Таймер запускается в тот момент,
        когда пользователь нажимает на поле ввода, а останавливается в момент нажатия Enter.
        Затем рассчитывается разница и определяется время в секундах.'''
        if (not self.end):
            # Расчет времени
            self.total_time = time.time() - self.time_start

            # Расчет количества символов в минуту
            if len(self.input_text) == 0:
                self.spm = 0
            else:
                self.spm = 60 * len(self.input_text) / (self.total_time)
                self.end = True
            print(self.total_time)

            self.results = 'Время:' + str(round(self.total_time)) + " сек   Ошибок:" + str(
                self.mistake) + '   Символов/мин: ' + str(round(self.spm))

            # Загрузка кнопки сброса
            self.reset_img = pygame.image.load('reset.jpg')
            self.reset_img = pygame.transform.scale(self.reset_img, (150, 150))
            screen.blit(self.reset_img, (self.w / 2 - 75, self.h - 275))
            self.draw_text(screen, "Перезапустить", self.h - 200, 25, (255, 255, 255))

            d = open("Results.txt", "a")
            d.write(self.results + "\n")
            d.close()

            print(self.results)
            pygame.display.update()

    #
    def run(self):
        ''' Это основной метод класса, отвечающий за обработку всех событий.'''
        self.reset_game()

        self.running = True
        while (self.running):
            self.draw_text(self.screen, self.instruction, 150, 30, (255, 213, 102))
            self.screen.fill((0, 0, 0), (50, 250, self.w - 100, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, self.w - 100, 50), 2)
            # Обновление текста пользовательского ввода
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # Расположение окна ввода
                    if (x >= 50 and x <= self.w - 50 and y >= 250 and y <= 300):
                        self.active = True
                        self.time_start = time.time()
                        # Расположение кнопки сброса
                    if (
                            x >= self.w / 2 - 75 and x <= self.w / 2 + 75 and y >= self.h - 275 and y <= self.h - 125 and self.end):
                        self.reset_game()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.mistake += len(self.word) - len(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True

                        else:
                            try:
                                if (event.unicode == self.word[self.symbolcnt]):
                                    self.input_text += event.unicode
                                    self.i += 1
                                else:
                                    self.mistake += 1
                            except:
                                pass

                pygame.display.update()

    def reset_game(self):
        '''Метод reset_game() сбрасывает все переменные и перезапускает игру, так что проверить скорость набора можно снова.'''
        self.screen.blit(self.open_img, (0, 0))
        self.active = False

        self.i = 0
        self.mistake = 0
        pygame.display.update()
        time.sleep(1)

        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = time.time()
        self.total_time = 0
        self.wpm = 0

        # Получаем случайное предложение
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # Загрузка окна
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Клавиатурный тренажёр"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        # Отрисовка поля ввода
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # Отрисовка строки предложения
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()


Game().run()
