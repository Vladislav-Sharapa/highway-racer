import pygame as pg
import game

def main():
    g = game.Game()
    g.currentMenu.displayMenu()

    while g.running:
        g.new()
        if g.player.condition != "Alive":
            g.enterGameOverMenu()

    pg.display.quit()
    pg.quit()

    print("Thanks for playing. . .")

if __name__ == "__main__":
    main()