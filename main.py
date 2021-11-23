from tkinter import *
from tkinter import messagebox
import random as r

#- Screen creation -#
window = Tk()
window.title("Mad Dash")
window.geometry("1920x1080")
width = 1920
height = 1080
#-------------------#

#- Global Variables -#
global run, jumptimer, score, timer, max_timer, pause_game, initial, canvas, pause_canvas, start_canvas
jumptimer = score = timer = 0
max_timer = 1000
pause_game = False
initial = True
canvas = Canvas(window, bg="white", width=width, height=height)
pause_canvas = start_canvas = None
#--------------------#

#- Other Variables -#
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
	if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
		window.destroy()
		run = False

def createCanvas():
	global score, max_timer
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
		if (score % 25) == 0 and (max_timer > 400):
			max_timer -= 50

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
		recordScore()
		rocks.clear()
		canvasDeletion()
		canvas.delete('rock')
		canvas.pack_forget()
		start_canvas.pack()

def pause(event=None):
	global pause_game
	if pause_game:
		pause_game = False
	else:
		pause_game = True

def pauseMenu():
	global initial, pause_canvas
	if initial:
		initial = False
		pause_canvas = Canvas(window, bg="white", width=width, height=height)
		pause_canvas.create_text(width // 2 - 30, 40, text="PAUSED", font=('Franklin Gothic Medium', 24))
		but_resume = Button(pause_canvas, text="Resume", width=15, height=2, command=pause)
		but_resume.config(font=('Franklin Gothic Medium', 24))
		but_resume.place(x=width // 3 + 140, y=height // 4)
		canvas.pack_forget()
		pause_canvas.bind("<Escape>", pause)
		pause_canvas.pack()
	return

def recordScore():
	def writeToLeaderboard():
		characters = ent_initials.get()
		while len(characters) < 3:
			characters += "#"
		with open("leaderboard.txt",'a') as file:
			file.write(characters[:3].upper() + "," + str(score) + "\n")
		add_window.destroy()

	global score
	add_window = Tk()
	add_window.title("GAME OVER")
	add_window.geometry("500x100")
	text = Label(add_window, text="Enter 3 characters to record your score:", font=('',18))
	text.pack()
	ent_initials = Entry(add_window)
	ent_initials.pack()
	but_initials = Button(add_window, text="Submit", command=writeToLeaderboard)
	but_initials.pack()

def mainGame():
	global run, jumptimer, score, timer, max_timer, initial, start_canvas, canvas
	score = 0
	run = True
	max_timer = 1000
	start_canvas.pack_forget()
	canvas.create_image(120,height // 2 - 60, image=playerImages[0], tags='player')
	player_image_used = 0
	createCanvas()
	canvas.bind("<Key>", keypress)
	canvas.bind("<Escape>", pause)
	canvas.focus_set()

	canvas.pack()
	window.update()

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
			if timer == max_timer:
				timer = 0
				canvasDeletion()
				canvas.create_text(width // 2, 30, text="Score: " + str(score), font=('Franklin Gothic Medium', 16), tags='score')
				rock = r.randint(1,10)
				if rock == 1 and (len(rocks) == 0 or canvas.coords(rocks[-1])[0] < (width - 320)):
					rocks.append(canvas.create_image(width, height // 2 - 60, image=jumprock, tags='rock'))

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
		try:
			window.update()
		except:
			pass
	return

def second(elem):
	return elem[1]

def displayLeaderboard():
	leader_window = Tk()
	leader_window.title("Mad Dash Leaderboard")
	leader_window.geometry("300x400")
	title = Label(leader_window, text="LEADERBOARD", relief=RAISED, font=('', 24))
	title.pack()
	try:
		with open('leaderboard.txt','r') as file:
			all_scores = file.read().splitlines()
	except:
		all_scores = []
	for i in range(len(all_scores)):
		all_scores[i] = all_scores[i].split(',')
		all_scores[i][1] = int(all_scores[i][1])
	all_scores.sort(key=second, reverse=True)
	if len(all_scores) < 10:
		count = 10 - len(all_scores)
		for i in range(count):
			all_scores.append(["---",0])
	for i in range(10):
		label_text = all_scores[i][0] + "."*25 + str(all_scores[i][1])
		score_label = Label(leader_window, text=label_text, font=('',16))
		score_label.pack(side=TOP, anchor=NW)



def startMenu():
	global start_canvas, canvas
	if start_canvas == None:
		start_canvas = Canvas(window, bg="white", width=width, height=height)
		start_canvas.create_text(width // 2 - 20, 40, text="MAD DASH", font="Times 32")
		but_start = Button(start_canvas, text="Start Game", width=20, height=2, font=('',16), command=mainGame)
		but_start.place(x=width // 3 + 140, y=height // 4)
		but_leader = Button(start_canvas, text="Leaderboard", width=20, height=2, font=('',16), command=displayLeaderboard)
		but_leader.place(x=width // 3 + 140, y=height // 4 + 100)
		but_quit = Button(start_canvas, text="Quit", width=20, height=2, font=('',16), command=onClosing)
		but_quit.place(x=width // 3 + 140, y=height // 2)
	start_canvas.pack()

#---------------#

window.protocol("WM_DELETE_WINDOW", onClosing)
startMenu()
window.mainloop()


#-------TO DO-------#
# Add Save/Load 	#
# Add cheat code 	#
# Add boss key 		#
# Add leaderboard 	#
#-------------------#


