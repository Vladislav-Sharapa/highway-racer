import pygame as pg
import settings
import random

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):

    def __init__(self, rectCenter, position):
        pg.sprite.Sprite.__init__(self)
        self.carSpeed = pg.mixer.Sound(r'music\sounds\car_sounds\cars_speed.wav')
        self.carCrash = pg.mixer.Sound(r'music\sounds\car_sounds\car_crash.wav')
        self.image = pg.image.load(r"D:\Py projects\2 курс\NewGame\sprites\PNG\player.png")
        self.rect = self.image.get_rect()
        self.rect.center = rectCenter
        self.position = position
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.condition = "Alive"

        self.left = False
        self.right = False

    def checkCollision(self, listOfCar):

        for car in listOfCar:
            if pg.sprite.collide_rect(self, car):
                print("Collision")
                self.carCrash.play()
                self.condition = "Dead"

    def update(self, listOfCar):


        self.acceleration = vec(0, 0) 
        keys = pg.key.get_pressed()

        if keys[pg.K_a] and keys[pg.K_d]:
            self.right = True
            self.left = True
        else:
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

        self.acceleration += self.velocity * settings.FRICTION  # surface friction effect

        self.velocity += self.acceleration 

        self.position += 2 * self.velocity + 0.5 * self.acceleration 

        if self.rect.x < 7 * settings.TILE_SIZE:
            self.position.x = 7 * settings.TILE_SIZE
            self.position.y = 20 * settings.TILE_SIZE
        if self.rect.x + 40 > 18 * settings.TILE_SIZE:
            self.position.x = 16.75 * settings.TILE_SIZE
            self.position.y = 20 * settings.TILE_SIZE

        self.checkCollision(listOfCar)

        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def animation(self):
        if self.right and self.left:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[1])  
        elif self.left:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[0])  
        elif self.right:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[2])  
        else:
            self.image = pg.image.load(settings.PLAYER_ANIMATION[1]) 

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Car(pg.sprite.Sprite):

    def __init__(self, startY, xMin, xMax, sprite_list):
        pg.sprite.Sprite.__init__(self)
        self.sprite_list = sprite_list
        self.image = pg.image.load(random.choice(sprite_list))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(xMin, xMax)
        self.rect.y = startY
        self.xMin = xMin
        self.xMax = xMax
        self.point = False

    def update(self) -> None:
        if self.rect.y > settings.SCREENHEIGHT:
            self.rect.x = random.randint(self.xMin, self.xMax)
            self.rect.y = -120
            self.image = pg.image.load(random.choice(self.sprite_list))
        if self.point is True and self.rect.y < 22 * settings.TILE_SIZE:
            self.point = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class CarLeft(Car):
    def __init__(self, startY, xMin, xMax):
        super().__init__(startY, xMin, xMax, settings.SPRITE_LIST_LEFT)

    def update(self, game):
        self.rect.y += game.speed + 1 # speed of left cars
        super().update()

class CarRight(Car):
    def __init__(self, startY, xMin, xMax):
        super().__init__(startY, xMin, xMax, settings.SPRITE_LIST_RIGHT)

    def update(self, game):
        self.rect.y += game.speed - 2 # speed of right cars
        super().update()

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