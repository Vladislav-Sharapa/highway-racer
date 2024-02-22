TITLE = "RACE GAME"

SCREENWIDTH = 800
SCREENHEIGHT = 768

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREY = (65, 65, 65)
LIGHT_GREEN = (107, 142, 35)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GREY = (100, 100, 100)

FPS = 60

TILE_SIZE = 32
GRID_WIDTH = SCREENWIDTH / TILE_SIZE
GRID_HEIGHT = SCREENHEIGHT / TILE_SIZE

# Player settings
ACCELERATION = 3
# Трение
FRICTION = -0.24

FONT_LINK = 'fonts/8-BIT WONDER.TTF'

SPRITE_LIST_LEFT = [r"sprites\PNG\left_car\car_1.png", r"sprites\PNG\left_car\car_2.png",
                    r"sprites\PNG\left_car\car_3.png", r"sprites\PNG\left_car\car_4.png",
                    r"sprites\PNG\left_car\car_5.png"]

SPRITE_LIST_RIGHT = [r"sprites\PNG\right_car\car_1.png", r"sprites\PNG\right_car\car_2.png",
                     r"sprites\PNG\right_car\car_3.png",
                     r"sprites\PNG\right_car\car_4.png", r"sprites\PNG\right_car\car_5.png"]

PLAYER_ANIMATION = [r"sprites\PNG\player_left.png",
                    r"sprites\PNG\player.png",
                    r"sprites\PNG\player_right.png"]

MUSIC_LIST = [r"music\main_menu_sound.mp3", r"music\paused_menu_sound.mp3"]

