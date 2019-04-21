# Initialize constants
import math

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
empty = (0,0,0,100)

display_width = 800
display_height = 500

game_width = display_width - 400
game_height = display_width - 400

game_offset_x = math.floor((display_width-game_width)/2)
game_offset_y = math.floor((display_height-game_height)/2)


player_size = 10
fd_fric = 0.5
bd_fric = 0.1
player_max_speed = 20
player_max_rtspd = 10
bullet_speed = 15
saucer_speed = 5
small_saucer_accuracy = 10
