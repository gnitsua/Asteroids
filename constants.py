# Initialize constants
import math

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
empty = (0,0,0,100)

# game_width = 640
# game_height = 480

game_width = 640
# game_width = game_width - 400
game_height = 480
# game_height = game_width - 400

# game_offset_x = math.floor((game_width-game_width)/2)
game_offset_x = 0
# game_offset_y = math.floor((display_height-game_height)/2)
game_offset_y = 0


player_size = 10
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspd = 10
bullet_speed = 15
saucer_speed = 5
small_saucer_accuracy = 10
