from tkinter import *
from tkinter import messagebox
import random as r

window = Tk()
window.title("Mad Dash")
# SCREEN RESOLUTION #
window.geometry("1920x1080")
width = 1920
height = 1080

canvas = Canvas(window, bg="white", width=width, height=height)
rocks = []

# Image Loading #
playerImages = [PhotoImage(file="Images/player1.png"), PhotoImage(file="Images/player2.png"), PhotoImage(file="Images/player3.png"), PhotoImage(file="Images/player4.png")]
ground = PhotoImage(file="Images/ground.png")
underground = PhotoImage(file="Images/underground.png")
jumprock = PhotoImage(file="Images/jumprock.png")
# ------------- #

# Subroutines #
def on_closing():
	global run
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		run = False

def create_canvas():
	x = 0
	while x < 1920:
		temp = canvas.create_image(x, height // 2, image=ground, tags='grounds')
		x += r.randint(60, 120)
	x = 0
	y = height // 2 + 120
	while y < height:
		while x < 1920:
			temp = canvas.create_image(x, y, image=underground, tags='grounds')
			x += r.randint(30,90)
		x = 0
		y += r.randint(30, 90)
	to_remove = []
	for i in rocks:
		canvas.move(i, -30, 0)
		if (canvas.coords(i)[0] + 120) <= 0:
			to_remove.append(rocks.index(i))
	for i in to_remove:
		del rocks[i]


def canvas_deletion():
	canvas.delete('player')
	canvas.delete('grounds')

def keypress(e):
	global jumptimer
	if e.char == "w":
		if jumptimer == 0:
			canvas.create_image(120, height // 2 - 120, image=playerImages[3], tags='playerjump')
			jumptimer += 1

def collisionTest():
	global run, jumptimer
	player_x = 120
	if (canvas.coords(rocks[0])[0] <= (player_x + 60)) and (canvas.coords(rocks[0])[0] + 120 >= (player_x + 120)) and (jumptimer == 0):
		run = False

test = canvas.create_image(120,height // 2 - 60, image=playerImages[0], tags='player')
player_image_used = 0
create_canvas()
canvas.bind("<Key>", keypress)
canvas.focus_set()

canvas.pack()
window.update()

# Global Variables #
global run
global jumptimer
run = True
jumptimer = 0

timer = 0
while run:
	timer += 1

	if timer == 500:
		timer = 0
		canvas_deletion()
		rock = r.randint(1,10)
		if rock == 1 and (len(rocks) == 0 or canvas.coords(rocks[-1])[0] < (width - 240)):
			rocks.append(canvas.create_image(width, height // 2 - 60, image=jumprock))

		if jumptimer != 0:
			jumptimer += 1
		if jumptimer == 0:
			player_image_used += 1
			if player_image_used == 3:
				player_image_used = 0
			canvas.create_image(120, height // 2 - 60, image=playerImages[player_image_used], tags='player')
		else:
			if jumptimer == 10:
				jumptimer = 0
				canvas.delete('playerjump')
				canvas.create_image(120, height // 2 - 60, image=playerImages[player_image_used], tags='player')

		create_canvas()
		if len(rocks) >= 1:
			collisionTest()
	window.protocol("WM_DELETE_WINDOW", on_closing)
	window.update()



