# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 40
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# paddle's point and position
left_paddle_point1 = [0,(HEIGHT/2)-PAD_HEIGHT]
left_paddle_point2 = [PAD_WIDTH,(HEIGHT/2)-PAD_HEIGHT]
left_paddle_point3 = [PAD_WIDTH,(HEIGHT/2)+PAD_HEIGHT]
left_paddle_point4 = [0, (HEIGHT/2)+PAD_HEIGHT]
paddle1_pos = [left_paddle_point1,left_paddle_point2,left_paddle_point3,left_paddle_point4]
right_paddle_point1 = [WIDTH - PAD_WIDTH, (HEIGHT/2)-PAD_HEIGHT]
right_paddle_point2 = [WIDTH, (HEIGHT/2)-PAD_HEIGHT]
right_paddle_point3 = [WIDTH, (HEIGHT/2)+PAD_HEIGHT]
right_paddle_point4 = [WIDTH - PAD_WIDTH, (HEIGHT/2)+PAD_HEIGHT]
paddle2_pos = [right_paddle_point1,right_paddle_point2,right_paddle_point3,right_paddle_point4]
# Paddle collision width
left_paddle_width = [left_paddle_point1[1],left_paddle_point4[1]]
right_paddle_width = [right_paddle_point1[1],right_paddle_point4[1]]
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0,0]
    ball_vel[0] = random.randrange(120, 240) / 60
    ball_vel[1] = random.randrange(60, 180) / 60
    if direction == RIGHT:
        ball_vel[0] = ball_vel[0] * 1
        ball_vel[1] = ball_vel[1] * -1
    elif direction == LEFT:
        ball_vel[0] = ball_vel[0] * -1
        ball_vel[1] = ball_vel[1] * -1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel   
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")    
    # update ball
    if ((ball_pos[0] + BALL_RADIUS)>= WIDTH):
        spawn_ball(LEFT)
        score1 += 1
    if ((ball_pos[0]- BALL_RADIUS) <= 0):
        spawn_ball(RIGHT)
        score2 += 1
    if ((ball_pos[1]- BALL_RADIUS) <= 0):
        ball_vel[1] = ball_vel[1] * -1
    if((ball_pos[1]+ BALL_RADIUS) >= HEIGHT):
        ball_vel[1] = ball_vel[1] * -1
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 3, 'Orange', 'Purple')
    # update paddle's vertical position, keep paddle on the screen
    #changing y-axis of all points in paddle 1
    paddle1_pos[0][1] += paddle1_vel
    paddle1_pos[1][1] += paddle1_vel
    paddle1_pos[2][1] += paddle1_vel
    paddle1_pos[3][1] += paddle1_vel
    #changing y-axis of all points in paddle 2
    paddle2_pos[0][1] += paddle2_vel
    paddle2_pos[1][1] += paddle2_vel
    paddle2_pos[2][1] += paddle2_vel
    paddle2_pos[3][1] += paddle2_vel
    
    # stopping paddle when hit top or botton
    if (paddle1_pos[0][1] <= 0) or (paddle1_pos[1][1]<= 0):
        paddle1_vel = 0
    if (paddle1_pos[2][1] >= HEIGHT) or (paddle1_pos[3][1]>= HEIGHT):
        paddle1_vel = 0
    if (paddle2_pos[0][1] <= 0) or (paddle2_pos[1][1]<= 0):
        paddle2_vel = 0
    if (paddle2_pos[2][1] >= HEIGHT) or (paddle2_pos[3][1]>= HEIGHT):
        paddle2_vel = 0
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 2, 'Red', 'Blue')
    canvas.draw_polygon(paddle2_pos, 2, 'Pink', 'White')
    
    # determine whether paddle and ball collide  
    if ((ball_pos[0]-BALL_RADIUS <= PAD_WIDTH) and ((ball_pos[1]>=paddle1_pos[0][1]) and (ball_pos[1]<=paddle1_pos[3][1]))):
        ball_vel[0] = ball_vel[0] * -1.5
    if ((ball_pos[0]+BALL_RADIUS >= (WIDTH-PAD_WIDTH)) and ((ball_pos[1]>=paddle2_pos[0][1]) and (ball_pos[1]<=paddle2_pos[3][1]))):
        ball_vel[0] = ball_vel[0] * -1.5
    print(ball_pos[0])
    # draw scores
    canvas.draw_text(str(score1),[250,30],30,'Yellow')
    canvas.draw_text(str(score2),[350,30],30,'Yellow')
def restart_game():
    new_game()
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -2
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 2
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -2
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 2
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart_button = frame.add_button("RESTART GAME", restart_game, 200)


# start frame
new_game()
frame.start()