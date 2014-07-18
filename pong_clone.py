#==============================================================================
# Author: Jack Scholting
# Date: 2013-02-16 Sat 08:59 PM
# Purpose: Clone of the game "Pong"
#==============================================================================

#==============================================================================
# Imports
#==============================================================================
import sys, pygame
 
#==============================================================================
# Define Constants
#==============================================================================
#------------------------------------------------------------------------------
# System Constants
#------------------------------------------------------------------------------
SCREEN_WIDTH  = 640
SCREEN_HEIGHT = 480

PADDLE_1_UP_KEY   = pygame.K_UP
PADDLE_1_DOWN_KEY = pygame.K_DOWN
PADDLE_2_UP_KEY   = pygame.K_q
PADDLE_2_DOWN_KEY = pygame.K_a

#------------------------------------------------------------------------------
# Object Constants
#------------------------------------------------------------------------------
TEXT_BUFFER = 10

PADDLE_WIDTH       = 12
PADDLE_HEIGHT      = 60
PADDLE_WALL_TOP    = 0
PADDLE_WALL_BOTTOM = SCREEN_HEIGHT - PADDLE_HEIGHT
PADDLE_SPEED       = 30

BALL_RADIUS      = 10
BALL_SPEED_X     = 4
BALL_SPEED_Y     = 2
BALL_WALL_TOP    = BALL_RADIUS
BALL_WALL_BOTTOM = SCREEN_HEIGHT - BALL_RADIUS
BALL_WALL_LEFT   = BALL_RADIUS
BALL_WALL_RIGHT  = SCREEN_WIDTH - BALL_RADIUS

#------------------------------------------------------------------------------
# Colors
#------------------------------------------------------------------------------
BLACK  = (   0,   0,   0 )
WHITE  = ( 255, 255, 255 )
GREEN  = (   0, 128,   0 )
RED    = ( 255,   0,   0 )
YELLOW = ( 255, 255,   0 )
BLUE   = (   0,   0, 255 )
GREY   = ( 100, 100, 100 )
 
#==============================================================================
# Define Game Objects
#==============================================================================
class Paddle:
    pos_x = 0
    pos_y = ( SCREEN_HEIGHT / 2 ) - ( PADDLE_HEIGHT / 2 )

    def __init__( self, side ):
        if side == "right":
            self.pos_x = SCREEN_WIDTH - PADDLE_WIDTH
        else:
            self.pos_x = 0

    def draw( self, surface ):
        self.rect_obj = pygame.draw.rect( surface, BLUE, (self.pos_x, self.pos_y, PADDLE_WIDTH, PADDLE_HEIGHT) )

    def update_position( self, direction ):
        if direction == "up":
            # Move if we can.
            if self.pos_y >= PADDLE_WALL_TOP:
                self.pos_y -= PADDLE_SPEED
            # Detect if we hit the wall.
            if self.pos_y <= PADDLE_WALL_TOP:
                self.pos_y = PADDLE_WALL_TOP
        elif direction == "down":
            # Move if we can.
            if self.pos_y <= PADDLE_WALL_BOTTOM:
                self.pos_y += PADDLE_SPEED
            # Detect if we hit the wall.
            if self.pos_y >= PADDLE_WALL_BOTTOM:
                self.pos_y = PADDLE_WALL_BOTTOM

class Ball:
    pos_x = SCREEN_WIDTH  / 2
    pos_y = SCREEN_HEIGHT / 2

    motion_x = BALL_SPEED_X
    motion_y = BALL_SPEED_Y

    def draw( self, surface ):
        self.rect_obj = pygame.draw.circle( surface, GREEN, (self.pos_x, self.pos_y), BALL_RADIUS )

    def update_position( self, score_board, paddle_1, paddle_2 ):
        # Make the move.
        self.pos_x += self.motion_x
        self.pos_y += self.motion_y

        # Detect if the ball hit paddle 1.
        if( self.rect_obj.colliderect( paddle_1.rect_obj ) ):
            self.pos_x = BALL_WALL_RIGHT - PADDLE_WIDTH
            self.motion_x = -BALL_SPEED_X
        # Detect if the ball hit paddle 2.
        elif( self.rect_obj.colliderect( paddle_2.rect_obj ) ):
            self.pos_x = BALL_WALL_LEFT + PADDLE_WIDTH
            self.motion_x = BALL_SPEED_X
        # Detect if the ball hit a wall.
        elif self.pos_x >= BALL_WALL_RIGHT:
            score_board.score_2_cnt += 1
            self.pos_x = BALL_WALL_RIGHT
            self.motion_x = -BALL_SPEED_X
        elif self.pos_x <= BALL_WALL_LEFT:
            score_board.score_1_cnt += 1
            self.pos_x = BALL_WALL_LEFT
            self.motion_x = BALL_SPEED_X
        if self.pos_y >= BALL_WALL_BOTTOM:
            self.pos_y = BALL_WALL_BOTTOM
            self.motion_y = -BALL_SPEED_Y
        elif self.pos_y <= BALL_WALL_TOP:
            self.pos_y = BALL_WALL_TOP
            self.motion_y = BALL_SPEED_Y

class ScoreBoard:
    score_1_cnt = 0
    score_2_cnt = 0

    def draw( self, surface ):
        # Draw the score of player 1.
        score_1_font = pygame.font.SysFont( 'Arial', 18 )
        score_1_str = "Player 1 (right): " + str( self.score_1_cnt )
        score_1_image = score_1_font.render( score_1_str, True, YELLOW )
        score_1_width, score_1_height = score_1_image.get_size()
        pos_x = (SCREEN_WIDTH / 2) - (score_1_width / 2)
        pos_y = TEXT_BUFFER
        surface.blit( score_1_image, ( pos_x, pos_y ) )

        # Draw the score of player 2.
        score_2_font = pygame.font.SysFont( 'Arial', 18 )
        score_2_str = "Player 2 (left):  " + str( self.score_2_cnt )
        score_2_image = score_2_font.render( score_2_str, True, YELLOW )
        score_2_width, score_2_height = score_2_image.get_size()
        pos_x = (SCREEN_WIDTH / 2) - (score_2_width / 2)
        pos_y = TEXT_BUFFER + score_1_height
        surface.blit( score_2_image, ( pos_x, pos_y ) )

#==============================================================================
# Initialize Pygame
#==============================================================================
# Initialize modules.
pygame.init()

# Set screen size and title.
screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
pygame.display.set_caption( "Pong Clone" )
 
# Get a clock object to use to set the fps.
clock = pygame.time.Clock()
 
#==============================================================================
# Initialize Game Objects
#==============================================================================
score_board = ScoreBoard()
paddle_1    = Paddle( "right" )
paddle_2    = Paddle( "left" )
ball        = Ball()

# Draw the game objects before the loop to capture their pygame objects.
paddle_1.draw( screen )
paddle_2.draw( screen )
ball.draw( screen )

#==============================================================================
# Main Game Loop
#==============================================================================
while True:
    # Set the frames to 50fps.
    clock.tick(50)

    # Handle any events.
    for event in pygame.event.get():
        # Close the window.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Move the paddles from keyboard input.
        elif event.type == pygame.KEYDOWN:
            if   event.key == PADDLE_1_UP_KEY:
                paddle_1.update_position( "up" )
            elif event.key == PADDLE_1_DOWN_KEY:
                paddle_1.update_position( "down" )
            elif event.key == PADDLE_2_UP_KEY:
                paddle_2.update_position( "up" )
            elif event.key == PADDLE_2_DOWN_KEY:
                paddle_2.update_position( "down" )

    # Move the ball.
    ball.update_position( score_board, paddle_1, paddle_2 )

    # Draw the background (needed to clear all previous drawings). 
    screen.fill( BLACK )

    # Draw the game objects.
    score_board.draw( screen )
    paddle_1.draw( screen )
    paddle_2.draw( screen )
    ball.draw( screen )

    # Update the entire display.
    pygame.display.flip()
