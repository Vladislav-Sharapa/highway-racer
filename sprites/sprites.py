import pygame as pg
import settings
import random

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):

    def __init__(self, rectCenter, position):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((1.5 * settings.TILE_SIZE, 2 * settings.TILE_SIZE))
        #self.image.fill(settings.GREEN)
        self.image = pg.image.load(r"D:\Py projects\NewGame\sprites\PNG\player.png")
        self.rect = self.image.get_rect()
        self.rect.center = rectCenter
        self.position = position
        # скорость персонажа
        self.velocity = vec(0, 0)
        # ускорение персонажа
        self.acceleration = vec(0, 0)
        self.condition = "Alive"

        self.left = False
        self.right = False

    #TODO изменение скорости линий и машин при коллизии игрока и объектов
    def checkCollision(self, listOfCar):

        for car in listOfCar:
            if pg.sprite.collide_rect(self, car):
                print("Collision")
                self.condition = "Dead"

    def update(self, listOfCar):
        # start acceleration of player
        self.acceleration = vec(0, 0)

        # start acceleration of player
        self.acceleration = vec(0, 0)

        keys = pg.key.get_pressed()
        # update velocity of player
        if keys[pg.K_a]:
            self.velocity.x = -settings.ACCELERATION
            self.left = True
        else:
            self.left = False

        if keys[pg.K_d]:
            self.velocity.x = settings.ACCELERATION
            self.right = True
        else:
            self.right = False

        self.animation()

        # apply player friction
        self.acceleration += self.velocity * settings.FRICTION

        # equation of motion
        self.velocity += self.acceleration

        # change the direction of the manager vector
        self.position += 2 * self.velocity + 0.5 * self.acceleration

        if self.rect.x < 7 * settings.TILE_SIZE:
            self.position.x = 7 * settings.TILE_SIZE
            self.position.y = 20 * settings.TILE_SIZE
        if self.rect.x + (1.5 * settings.TILE_SIZE) > 18 * settings.TILE_SIZE:
            self.position.x = 16.5 * settings.TILE_SIZE
            self.position.y = 20 * settings.TILE_SIZE

        self.checkCollision(listOfCar)

        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def animation(self):
        if self.left:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[0])
        elif self.right:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[2])
        else:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[1])

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Car(pg.sprite.Sprite):

    def __init__(self, startY):
        pg.sprite.Sprite.__init__(self)

        # self.image = pg.Surface((1.5 * settings.TILE_SIZE, 3 * settings.TILE_SIZE))
        # self.image.fill(settings.YELLOW)
        self.image = pg.image.load(random.choice(settings.SPRITE_LIST))
        self.rect = self.image.get_rect()
        self.point = False

        self.rect.x = random.randint(250, 520)
        self.rect.y = startY

    def update(self, game):
        self.rect.y += game.speed

        if self.rect.y > settings.SCREENHEIGHT:
            self.rect.x = random.randint(250, 520)
            self.rect.y = -120
            self.image = pg.image.load(random.choice(settings.SPRITE_LIST))
        if self.point is True and self.rect.y < 22 * settings.TILE_SIZE:
            self.point = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class RoadLine:

    def __init__(self, y):
        self.image = pg.Surface((10, 30))
        self.rect = self.image.get_rect()
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = settings.SCREENWIDTH / 2 - 5
        self.rect.y = y

    def update(self, speed):
        self.rect.y += speed

        if self.rect.y > settings.SCREENHEIGHT:
            self.rect.y = -130

    def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))


