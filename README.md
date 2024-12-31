Blue-Square-Jump
https://youtu.be/6sQuSzlTItY
2d-Plattformer:
My name is Lars Germann, as my project i choose something a bit on the easy side. this game contains only one lever and the code is not the most beautifull tbh. 
my github is Neet2work my cs50 username is Lars Germann.
I am from ...Betzdorf a small town in germany (lol)



Main.py:
imports essential packages (pygame, time, sys, sqlite3) aswell as the other 2 files (game_mechanics.py, game_variables
sets start_time and elapsed_time (stores final time) to 0
connection to databse (times.db) and creates cursor object to use sqlite3 queries and commands
defining function for username input before the game starts
screen-layout for the username-input-screen
event for the username-input

defining show_leaderboard function, to show the times, ranks and names with date from players (top10) and the general layout

initializing game after usernameinput (ENTER)

game loop

def reset_game function, so after pressing restart the coins and the jumpheightincrease are reseted

defining function draw_winner_screen, after reaching the finish_flag. contains the username, the time and 2 buttons, one for looking at the leaderboard, on for restarting


general logic: keys to use, the layout of the game itself 
gravity, to make sure, the player comes back to the ground after jumping

implementation of the colission from the file game_mechanics, for the varios objects (red_obstacle, black_obstacle, coin and finish_flag

camera logic, the palyer is always centered. 

implementation of the objects

game_variables.py:
screen-dimensions of the game
defining the colors used
frmae-rate-controll and setting framerate to 60
player-setting like dimesnions, jump-height (initial), speed, gravity etc.
camera-settings
obstacle-dimesnions
red_obstacle_movement
where the obstacles appear in the game (layout)

where the finish_flag will appear

game_mechanics.py:

black_obstacle_collision side/bottom/and top collision

red_obstacle_collision side/bottom/and top collision aswell as the mechanic, that the player moves with the red obstacle if he is on top
finish_flag_collission 

game_borders (bounds)

times.db :
contains the table where the usernames, times and dates are stored. 
