from menu import *
from sprites import sprites
import time

vec = pg.math.Vector2

class Game:
    rectCenter = (settings.SCREENWIDTH / 2 - settings.TILE_SIZE, settings.SCREENHEIGHT - 4 * settings.TILE_SIZE)
    position = vec(settings.SCREENWIDTH / 2 - settings.TILE_SIZE / 1.5, settings.SCREENHEIGHT - 4 * settings.TILE_SIZE)

    def __init__(self):
        pg.init()

        self.score = Score()

        # for main menu of the game
        self.click = False
        self.fontName = settings.FONT_LINK
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False
        self.mainMenu = MainMenu(self)
        self.currentMenu = self.mainMenu
        self.paused = PausedMenu(self)
        self.gameOver = GameOverMenu(self)

        self.screen = pg.display.set_mode((settings.SCREENWIDTH, settings.SCREENHEIGHT))
        self.clock = pg.time.Clock()

        self.player = sprites.Player(self.rectCenter, self.position)
        self.running = True
        self.playing = True
        # container for car-object
        self.listOfCar = []
        self.listOfLines = []
        self.speed = 0

    def new(self):
        self.currentMenu.carStartSound.play()
        time.sleep(4)

        self.initializeObjects()
        self.run()

    def run(self):

        while self.playing:
            self.clock.tick(settings.FPS)
            self.events()

            self.update()
            self.draw()
            self.enterThePausedMenu()

            if not pg.mixer.get_busy():
                self.player.carSpeed.play(loops=0, maxtime=0, fade_ms=1)

    def events(self):
        for event in pg.event.get():  # Game loop events handler
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
                if event.key == pg.K_r and self.player.condition != "Alive":
                    self.player.condition = "Alive"
                    self.playing = True
                    print("I am alive")

    def update(self):

        self.player.update(self.listOfCar)  # change players position

        if self.player.condition != "Alive":
            self.playing = False

        for car in self.listOfCar:  
            car.update(self)
            self.score.update(car, self) 

    
        for line in self.listOfLines:
            line.update(self.speed)

    def draw(self):

        self.screen.fill(settings.BLACK)

        # draw enviroment
        pg.draw.rect(self.screen, settings.DARK_GREY, (settings.TILE_SIZE * 7, 0, settings.TILE_SIZE * 11, settings.SCREENHEIGHT))
        pg.draw.rect(self.screen, settings.LIGHT_GREEN, (0, 0, settings.TILE_SIZE * 7, settings.SCREENHEIGHT))
        pg.draw.rect(self.screen, settings.LIGHT_GREEN, (settings.TILE_SIZE * 18, 0, settings.SCREENWIDTH, settings.SCREENHEIGHT))

        for line in self.listOfLines:  # draw road lines
            line.draw(self.screen)

        for car in self.listOfCar:  # draw cars
            car.draw(self.screen)

        self.player.draw(self.screen)  # draw player
        self.score.draw(self)

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
            self.currentMenu = PausedMenu(self)
            self.currentMenu.displayMenu()

    def drawLineOfRoad(self):
        pg.draw.line(self.screen, settings.LIGHT_GREY, (7 * settings.TILE_SIZE, 0), (7 * settings.TILE_SIZE,
                                                                                     settings.SCREENHEIGHT))

        pg.draw.line(self.screen, settings.LIGHT_GREY, (18 * settings.TILE_SIZE, 0), (18 * settings.TILE_SIZE,
                                                                                      settings.SCREENHEIGHT))

    def enterGameOverMenu(self):
        self.currentMenu = GameOverMenu(self)
        self.currentMenu.displayMenu()

    def starGameScreen(self):
        self.screen.fill(settings.BLACK)
        self.drawText('Get started . . .', 40, settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2 - 20)

    def initializeObjects(self):
        startY = -100
        self.score = Score()
        self.speed = 3

        self.listOfCar.clear()
        self.listOfLines.clear()

        for _ in range(0, 3):
            self.listOfCar.append(sprites.CarLeft(startY, 230, 345))
            startY -= 230
        startY = -120

        for _ in range(0, 3):
            self.listOfCar.append(sprites.CarRight(startY, 390, 540))
            startY -= 230
        startY = 30

        for line in range(0, 7):
            self.listOfLines.append(sprites.RoadLine(startY))
            startY += 120


        self.position = vec(settings.SCREENWIDTH / 2 - settings.TILE_SIZE / 1.5, settings.SCREENHEIGHT - 4 * settings.TILE_SIZE)
        self.player.position = self.position


class Score:

    def __init__(self,):
        self.score = 0
        self.markOfSpeedUp = 0

    def update(self, car, game):
        if car.rect.y > 22 * settings.TILE_SIZE:
            if not car.point:
                self.score += 1
                self.markOfSpeedUp += 1
                car.point = True
                print("+1")
        if self.markOfSpeedUp == 20:
            if game.speed != 8:
                game.speed += 1
                self.markOfSpeedUp = 0
                print("speed + 1")

    def draw(self, game):
        game.drawText("Score " + str(self.score), 25, 105, 45)
