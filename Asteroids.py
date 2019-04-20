# Import modules
import math
import random

import pygame

from asteroid import Asteroid
from bullet import Bullet
from constants import display_width, display_height, black, white, player_max_rtspd, player_size, \
    small_saucer_accuracy
from deadPlayer import DeadPlayer
from player import Player
from saucer import Saucer

pygame.init()

# snd_fire = pygame.mixer.Sound("Sounds/fire.wav")
# snd_bangL = pygame.mixer.Sound("Sounds/bangLarge.wav")
# snd_bangM = pygame.mixer.Sound("Sounds/bangMedium.wav")
# snd_bangS = pygame.mixer.Sound("Sounds/bangSmall.wav")
# snd_extra = pygame.mixer.Sound("Sounds/extra.wav")
# snd_saucerB = pygame.mixer.Sound("Sounds/saucerBig.wav")
# snd_saucerS = pygame.mixer.Sound("Sounds/saucerSmall.wav")
# Make surface and display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()


# Create function to draw texts
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)


# Create funtion to chek for collision
def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False


def gameLoop(startingState):
    # Init variables
    gameState = startingState
    player_state = "Alive"
    player_blink = 0
    player_pieces = []
    player_dying_delay = 0
    player_invi_dur = 0
    hyperspace = 0
    next_level_delay = 0
    bullet_capacity = 4
    bullets = []
    asteroids = []
    stage = 3
    score = 0
    live = 2
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    player = Player(display_width / 2, display_height / 2, gameDisplay)
    saucer = Saucer(gameDisplay)

    # Main loop
    while gameState != "Exit":
        # Game menu
        while gameState == "Menu":
            gameDisplay.fill(black)
            drawText("ASTEROIDS", white, display_width / 2, display_height / 2, 100)
            drawText("Press any key to START", white, display_width / 2, display_height / 2 + 100, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "Playing"
            pygame.display.update()
            timer.tick(5)

        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rtspd = -player_max_rtspd
                if event.key == pygame.K_RIGHT:
                    player.rtspd = player_max_rtspd
                if event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player.x, player.y, player.dir, gameDisplay))
                    # Play SFX
                    # pygame.mixer.Sound.play(snd_fire)
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rtspd = 0

        # Update player
        player.updatePlayer()

        # Checking player invincible time
        if player_invi_dur != 0:
            player_invi_dur -= 1
        elif hyperspace == 0:
            player_state = "Alive"

        # Reset display
        gameDisplay.fill(black)

        # Hyperspace
        if hyperspace != 0:
            player_state = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                player.x = random.randrange(0, display_width)
                player.y = random.randrange(0, display_height)

        # Check for collision w/ asteroid
        for a in asteroids:
            a.updateAsteroid()
            if player_state != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    # Create ship fragments
                    player_pieces.append(
                        DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(
                        DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(DeadPlayer(player.x, player.y, player_size))

                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                        score += 20
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                        score += 50
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

        # Update ship fragments
        for f in player_pieces:
            f.updateDeadPlayer()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                player_pieces.remove(f)

        # Check for end of stage
        if len(asteroids) == 0 and saucer.state == "Dead":
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                # Spawn asteroid away of center
                for i in range(stage):
                    xTo = display_width / 2
                    yTo = display_height / 2
                    while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                        xTo = random.randrange(0, display_width)
                        yTo = random.randrange(0, display_height)
                    asteroids.append(Asteroid(xTo, yTo, "Large", gameDisplay))
                next_level_delay = 0

        # Update intensity
        if intensity < stage * 450:
            intensity += 1

        # Saucer
        if saucer.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                saucer.createSaucer()
                # Only small saucers >40000
                if score >= 40000:
                    saucer.type = "Small"
        else:
            # Set saucer targer dir
            acc = small_saucer_accuracy * 4 / stage
            saucer.bdir = math.degrees(
                math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(random.uniform(acc, -acc)))

            saucer.updateSaucer()
            saucer.drawSaucer()

            # Check for collision w/ asteroid
            for a in asteroids:
                if isColliding(saucer.x, saucer.y, a.x, a.y, a.size + saucer.size):
                    # Set saucer state
                    saucer.state = "Dead"

                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangM)
                    else:
                        pass
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

            # Check for collision w/ bullet
            for b in bullets:
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    # Add points
                    if saucer.type == "Large":
                        score += 200
                    else:
                        score += 1000

                    # Set saucer state
                    saucer.state = "Dead"

                    # Play SFX
                    # pygame.mixer.Sound.play(snd_bangL)

                    # Remove bullet
                    bullets.remove(b)

            # Check collision w/ player
            if isColliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                if player_state != "Died":
                    # Create ship fragments
                    player_pieces.append(
                        DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(
                        DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    # Play SFX
                    # pygame.mixer.Sound.play(snd_bangL)

            # Saucer's bullets
            for b in saucer.bullets:
                # Update bullets
                b.updateBullet()

                # Check for collision w/ asteroids
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                            asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                            # Play SFX
                            # pygame.mixer.Sound.play(snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                            asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                            # Play SFX
                            # pygame.mixer.Sound.play(snd_bangL)
                        else:
                            pass
                            # Play SFX
                            # pygame.mixer.Sound.play(snd_bangL)

                        # Remove asteroid and bullet
                        asteroids.remove(a)
                        saucer.bullets.remove(b)

                        break

                # Check for collision w/ player
                if isColliding(player.x, player.y, b.x, b.y, 5):
                    if player_state != "Died":
                        # Create ship fragments
                        player_pieces.append(
                            DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                       gameDisplay))
                        player_pieces.append(
                            DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                       gameDisplay))
                        player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                        # Kill player
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            gameState = "Game Over"

                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangL)

                        # Remove bullet
                        saucer.bullets.remove(b)

                if b.life <= 0:
                    try:
                        saucer.bullets.remove(b)
                    except ValueError:
                        continue

        # Bullets
        for b in bullets:
            # Update bullets
            b.updateBullet()

            # Check for bullets collide w/ asteroid
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay))
                        score += 20
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay))
                        score += 50
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Play SFX
                        # pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)
                    bullets.remove(b)

                    break

            # Destroying bullets
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        # Extra live
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            # pygame.mixer.Sound.play(snd_extra, 60)

        # Draw player
        if gameState != "Game Over":
            if player_state == "Died":
                if hyperspace == 0:
                    if player_dying_delay == 0:
                        if player_blink < 5:
                            if player_blink == 0:
                                player_blink = 10
                            else:
                                player.drawPlayer()
                        player_blink -= 1
                    else:
                        player_dying_delay -= 1
            else:
                player.drawPlayer()
        else:
            drawText("Game Over", white, display_width / 2, display_height / 2, 100)
            drawText("Press \"R\" to restart!", white, display_width / 2, display_height / 2 + 100, 50)
            live = -1

        # Draw score
        drawText(str(score), white, 60, 20, 40, False)

        # Draw Lives
        for l in range(live + 1):
            Player(75 + l * 25, 75, gameDisplay).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps
        timer.tick(30)


# Start game
gameLoop("Menu")

# End game
pygame.quit()
quit()
