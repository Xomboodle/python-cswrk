from tkinter import *
from tkinter import messagebox
import random as r

#- Screen creation -#
window = Tk()
window.title("Mad Dash")
window.geometry("1920x1080")
width = 1920
height = 1080
canvas = Canvas(window, bg="white", width=width, height=height)
#-------------------#

#- Global Variables -#
global run, jumptimer, score, pause_game, initial, pause_canvas
run = True
jumptimer = 0
score = 0
pause_game = False
initial = True
pause_canvas = None
#--------------------#

#- Local Variables -#
timer = 0
game_speed = 400
rocks = []
#-------------------#




#- Image Loading -#
playerImages = [PhotoImage(file="Images/player1.png"), PhotoImage(file="Images/player2.png"), PhotoImage(file="Images/player3.png"), PhotoImage(file="Images/player4.png")]
ground = PhotoImage(file="Images/ground.png")
underground = PhotoImage(file="Images/underground.png")
jumprock = PhotoImage(file="Images/jumprock.png")
#-----------------#

#- Subroutines -#
def onClosing():
	global run
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		run = False

def createCanvas():
	global score
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
		canvas.move(i, -20, 0)
		if (canvas.coords(i)[0] + 120) <= 0:
			to_remove.append(rocks.index(i))
	for i in to_remove:
		del rocks[i]
		score += 1

def canvasDeletion():
	canvas.delete('player')
	canvas.delete('grounds')
	canvas.delete('score')

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

def pause(event=None):
	global pause_game
	if pause_game:
		pause_game = False
	else:
		pause_game = True

def unpause():
	global pause_game
	pause_game = False

def pauseMenu():
	global initial, pause_canvas
	if initial:
		initial = False
		pause_canvas = Canvas(window, bg="white", width=width, height=height)
		pause_canvas.create_text(width // 2, 40, text="PAUSED", font=('Franklin Gothic Medium', 24))
		but_resume = Button(pause_canvas, text="Resume", width=15, height=2, font=('Franklin Gothic Medium',16), command=pause)
		but_resume.config(font=('Franklin Gothic Medium', 24))
		but_resume.place(x=20, y=height // 4)
		canvas.pack_forget()
		pause_canvas.bind("<Escape>", pause)
		pause_canvas.pack()
	return

#---------------#

canvas.create_image(120,height // 2 - 60, image=playerImages[0], tags='player')
player_image_used = 0
createCanvas()
canvas.bind("<Key>", keypress)
canvas.bind("<Escape>", pause)
canvas.focus_set()

canvas.pack()
window.update()

window.protocol("WM_DELETE_WINDOW", onClosing)

while run:
	if pause_game:
		pauseMenu()
	else:
		if not initial:
			initial = True
			canvas.pack()
			try:
				pause_canvas.destroy()
			except:
				pass
		timer += 1

		if timer == 1000:
			timer = 0
			canvasDeletion()
			canvas.create_text(width // 2, 30, text="Score: " + str(score), font=('Franklin Gothic Medium', 16), tags='score')
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

			createCanvas()
			if len(rocks) >= 1:
				collisionTest()
	#window.protocol("WM_DELETE_WINDOW", on_closing)
	window.update()



