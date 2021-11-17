import pygame as pg
import settings
import random

from menu import *
from sprites import sprites

vec = pg.math.Vector2


class Game:
    rectCenter = (settings.SCREENWIDTH / 2 - settings.TILE_SIZE, settings.SCREENHEIGHT - 4 * settings.TILE_SIZE)
    position = vec(settings.SCREENWIDTH / 2 - settings.TILE_SIZE / 1.5, settings.SCREENHEIGHT - 4 * settings.TILE_SIZE)

    def __init__(self):

        self.score = Score(0)

        # for main menu of the game
        self.click = False
        self. fontName = 'fonts/8-BIT WONDER.TTF'
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
        self.ESC_KEY = False
        self.mainMenu = MainMenu(self)
        self.currentMenu = self.mainMenu
        self.paused = PausedMenu(self)
        self.gameOver = GameOverMenu(self)

        pg.init()

        self.screen = pg.display.set_mode((settings.SCREENWIDTH, settings.SCREENHEIGHT))
        self.clock = pg.time.Clock()

        self.player = sprites.Player(self.rectCenter, self.position)

        self.running = True
        self.playing = True

        # container for car-object
        self.listOfCar = []
        self.listOfLines = []


    def new(self):

        self.initializeObjects()
        self.run()

    def run(self):

        while self.playing:
            self.clock.tick(settings.FPS)
            self.events()

            if self.player.condition == "Alive":
                self.update()

            self.draw()
            self.enterThePausedMenu()

    def events(self):
        # Game loop events handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.currentMenu.runDisplay = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_ESCAPE:
                    self.ESC_KEY = True
                    self.currentMenu = PausedMenu(self)
                if event.key == pg.K_r and self.player.condition != "Alive":
                    self.player.condition = "Alive"
                    self.initializeObjects()
                    print("I am alive")

    def update(self):

        self.player.update(self.listOfCar)

        # update car-sprites
        for car in self.listOfCar:
            car.update(self)
            self.score.update(car)

        #TODO изменение позиции линий
        for line in self.listOfLines:
            line.update()

    def draw(self):

        # fill the screen with black color
        self.screen.fill(settings.BLACK)

        #TODO прорисовка разметки на экране
        for line in self.listOfLines:
            line.draw(self.screen)

        self.drawLineOfRoad()
        # draw car-sprites
        for car in self.listOfCar:
            car.draw(self.screen)

        self.player.draw(self.screen)

        if self.player.condition == "Alive":
            self.score.draw(self)
        else:
            self.showGameOverScreen()

        pg.display.flip()

    def drawText(self, text, size, x, y):
        font = pg.font.Font(self.fontName, size)
        textSurface = font.render(text, True, settings.WHITE)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.screen.blit(textSurface, textRect)

    def resetKeys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False


    def enterThePausedMenu(self):
        if self.ESC_KEY:
            self.ESC_KEY = False
            self.playing = False
            self.currentMenu.displayMenu()

    def drawGrid(self):
        for x in range(0, settings.SCREENWIDTH, settings.TILE_SIZE):
            pg.draw.line(self.screen, settings.LIGHT_GREY, (x, 0), (x, settings.SCREENHEIGHT))

        for y in range(0, settings.SCREENHEIGHT, settings.TILE_SIZE):
            pg.draw.line(self.screen, settings.LIGHT_GREY, (0, y), (settings.SCREENWIDTH, y))

    def drawLineOfRoad(self):
        pg.draw.line(self.screen, settings.LIGHT_GREY, (7 * settings.TILE_SIZE, 0), (7 * settings.TILE_SIZE,
                                                                                     settings.SCREENHEIGHT))

        pg.draw.line(self.screen, settings.LIGHT_GREY, (18 * settings.TILE_SIZE, 0), (18 * settings.TILE_SIZE,
                                                                                      settings.SCREENHEIGHT))

    def showGameOverScreen(self):
        self.screen.fill(settings.BLACK)
        self.drawText("Game over", 30, settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2)
        self.drawText("Score " + str(self.score.score), 25, settings.SCREENWIDTH / 2, (settings.SCREENHEIGHT / 2 + 50))

    def initializeObjects(self):
        startY = -100
        self.score.score = 0

        self.listOfCar.clear()
        self.listOfLines.clear()

        for _ in range(0, 4):
            self.listOfCar.append(sprites.Car(startY))
            startY -= 210
        startY = 30

        for line in range(0, 7):
            self.listOfLines.append(sprites.RoadLine(startY))
            startY += 120

class Score:

    def __init__(self, startValue):
        self.score = startValue

    def update(self, car):
        if car.rect.y > settings.SCREENHEIGHT - 2:
            self.score += 1
            print("+1")


    def draw(self, game):
        game.drawText("Score " + str(self.score), 25, 105, 45)
