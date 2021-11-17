import pygame as pg
import settings

import pygame as pg
import settings
import game

def main():
    g = game.Game()
    g.currentMenu.displayMenu()

    while g.running:
        g.new()

    pg.display.quit()
    pg.quit()


if __name__ == "__main__":
    main()

