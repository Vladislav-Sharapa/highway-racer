import pygame as pg
import settings


class Menu:

    def __init__(self, game):
        self.game = game
        self.middleWidth, self.middleHeight = settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2
        self.runDisplay = True
        self.cursorRect = pg.Rect(0, 0, 20, 20)
        self.offset = - 160
        pg.mixer.init()
        self.menuSound = pg.mixer.Sound(r'music\sounds\menu_selection.wav')  
        self.carStartSound = pg.mixer.Sound(r'music\sounds\car_sounds\car_start.wav')

    def drawCursor(self):
        self.game.drawText("*", 25, self.cursorRect.x, self.cursorRect.y)


    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0, 0))
        pg.display.update()
        self.game.resetKeys()

    def soundSelection(self):
        if self.game.UP_KEY or self.game.DOWN_KEY:
            self.menuSound.play()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startX, self.startY = self.middleWidth, self.middleHeight + 40
        self.creditsX, self.creditsY = self.middleWidth, self.middleHeight + 80
        self.exitX, self.exitY = self.middleWidth, self.middleHeight + 120
        self.cursorRect.midtop = (self.startX + self.offset, self.startY)
        self.creditMenu = CreditMenu(game)
        pg.mixer.music.load(r"music\main_menu_sound.mp3")
        pg.mixer.music.set_volume(0.8)


    def displayMenu(self):
        self.runDisplay = True
        pg.mixer.music.play(loops=-1)  # проигрываем мелодию main_menu_music
        while self.runDisplay:
            self.game.events()
            self.checkInputs()
            self.game.screen.fill(settings.BLACK)
            self.game.drawText('Main menu', 40, settings.SCREENWIDTH/ 2, settings.SCREENHEIGHT / 2 - 20)
            self.game.drawText("Start game", 30, self.startX, self.startY)
            self.game.drawText("Credits", 30, self.creditsX, self.creditsY)
            self.game.drawText("Exit", 30, self.exitX, self.exitY)
            self.drawCursor()
            self.blitScreen()

    def moveCursor(self):
        self.soundSelection()
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursorRect.midtop = (self.creditsX + self.offset, self.creditsY)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursorRect.midtop = (self.exitX + self.offset, self.exitY)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursorRect.midtop = (self.startX + self.offset, self.startY)
                self.state = "Start"

        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursorRect.midtop = (self.exitX + self.offset, self.exitY)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursorRect.midtop = (self.creditsX + self.offset, self.creditsY)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursorRect.midtop = (self.startX + self.offset, self.startY)
                self.state = "Start"

    def checkInputs(self):
        self.moveCursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                self.runDisplay = False
                pg.mixer.music.stop()  
                pg.mixer.music.unload()
                pg.mixer.music.load(r"music\paused_menu_sound.mp3")

            elif self.state == "Exit":
                self.runDisplay = False
                self.game.playing = False
                self.game.running = False
            elif self.state == "Credits":
                self.creditMenu.displayMenu()



class CreditMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.startX, self.startY = self.middleWidth, self.middleHeight + 40

    def displayMenu(self):
        self.runDisplay = True
        while self.runDisplay:
            self.game.events()
            self.checkInputs()
            self.game.screen.fill(settings.BLACK)
            self.game.drawText('Made by student of 1220', 30, settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2 - 20)
            self.game.drawText("BNTU", 30, self.startX, self.startY)
            self.blitScreen()

    def checkInputs(self):
        if self.game.ESC_KEY:
            self.runDisplay = False

class GameOverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.currentMenu = PausedMenu(game)

    def displayMenu(self):
        self.game.player.carSpeed.stop()
        self.runDisplay = True
        while self.runDisplay:
            self.game.events()
            self.checkInputs()
            self.game.screen.fill(settings.BLACK)
            self.game.drawText("Game over", 30, settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2)
            self.game.drawText("Score " + str(self.game.score.score), 25, settings.SCREENWIDTH / 2,
                               (settings.SCREENHEIGHT / 2 + 50))
            self.game.drawText("Press r to restart", 15, settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2 + 80)
            self.game.enterThePausedMenu()
            self.blitScreen()

    def checkInputs(self):
        if self.game.player.condition == "Alive":
            self.runDisplay = False
        if not self.game.running:
            self.runDisplay = False

class PausedMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Continue"
        self.continueX, self.continueY = self.middleWidth, self.middleHeight + 40
        self.exitX, self.exitY = self.middleWidth, self.middleHeight + 80
        self.cursorRect.midtop = (self.continueX - 120, self.continueY)
        self.running = True

    def displayMenu(self):
        self.game.player.carSpeed.stop()
        pg.mixer.music.play()
        self.runDisplay = True
        while self.runDisplay:
            self.game.events()
            self.checkInputs()
            self.game.screen.fill(settings.BLACK)
            self.game.drawText('Paused game', 40, settings.SCREENWIDTH / 2, settings.SCREENHEIGHT / 2 - 20)
            self.game.drawText("Continue", 30, self.continueX, self.continueY)
            self.game.drawText("Exit", 30, self.exitX, self.exitY)
            self.drawCursor()
            self.blitScreen()


    def moveCursor(self):
        self.soundSelection()
        if self.game.DOWN_KEY:
            if self.state == "Continue":
                self.cursorRect.midtop = (self.exitX - 120, self.exitY)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursorRect.midtop = (self.continueX - 120, self.continueY)
                self.state = "Continue"

        elif self.game.UP_KEY:
            if self.state == "Continue":
                self.cursorRect.midtop = (self.exitX - 120, self.exitY)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursorRect.midtop = (self.continueX - 120, self.continueY)
                self.state = "Continue"


    def checkInputs(self):
        self.moveCursor()
        if self.game.START_KEY:
            if self.state == "Continue":
                self.runDisplay = False
                self.running = True
                pg.mixer.music.stop()
            elif self.state == "Exit":
                self.runDisplay = False
                self.game.playing = False
                self.game.running = False
                self.running = False