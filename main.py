#- IMPORTS -#

from tkinter import *
from tkinter import messagebox
import random as r

#-----------#


#- SCREEN CREATION -#

window = Tk()
window.title("Mad Dash")
window.geometry("1920x1080")
width = 1920
height = 1080

#-------------------#


#- GLOBAL VARIABLES -#

global run
global jumptimer, score, timer
jumptimer = score = timer = 0

global max_timer
max_timer = 1000

global pause_game, cheating, boss_key, loaded
pause_game = cheating = boss_key = loaded = False

global initial, initial_boss
initial = initial_boss = True

global canvas
canvas = Canvas(window, bg="#E1B460", width=width, height=height)

global pause_canvas, start_canvas, boss_canvas
pause_canvas = start_canvas = boss_canvas = None

global user_key
user_key = "w"

#--------------------#


#- OTHER VARIABLES -#

rocks = []

#-------------------#


#- IMAGE LOADING -#
playerImages = [PhotoImage(file="Images/player1.png"), 
				PhotoImage(file="Images/player2.png"), 
				PhotoImage(file="Images/player3.png"), 
				PhotoImage(file="Images/player4.png")]
ground = PhotoImage(file="Images/ground.png")
underground = PhotoImage(file="Images/underground.png")
jumprock = PhotoImage(file="Images/jumprock.png")
boss_image = PhotoImage(file="Images/boss.png")
#-----------------#


#- SUBROUTINES -#

# Used for exiting program #
def onClosing():
	global run

	if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
		window.destroy()
		run = False


# Sets whether the boss key event occurs #
def bossKey(event):
	global boss_key

	if boss_key: boss_key = False
	else: boss_key = True


# Sets whether the pause menu is displayed #
def pause(event=None):
	global pause_game

	if pause_game: pause_game = False
	else: pause_game = True


# Checks the key pressed by the user. 		 #
# If specific key pressed, the player jumps. #
def keypress(e):
	global jumptimer, user_key

	if e.char == user_key:
		if jumptimer == 0:
			canvas.create_image(120, height // 2 - 120, image=playerImages[3], tags='playerjump')
			jumptimer += 1


# Checks if player collides with obstacle. #
# Game ends if this is true.			   #
def collisionTest():
	global run, jumptimer, cheating

	player_x = 120
	if ((canvas.coords(rocks[0])[0] <= (player_x + 60)) and 
		(canvas.coords(rocks[0])[0] + 120 >= (player_x + 120)) and 
		(jumptimer == 0) and not cheating):

		run = False
		recordScore()
		rocks.clear()
		canvasDeletion()
		canvas.delete('rock')
		canvas.pack_forget()
		start_canvas.pack()


# Gives user option to enter cheat code    #
# Codes: "invincible" -- removes collision #
#		 "disable" 	  -- turns cheat off   #
def cheater():
	
	# Nested function to check codes are valid #
	def checkCheat():
		global cheating

		code = ent_code.get()

		if code == "invincible": cheating = True	
		elif code == "disable": cheating = False

		cheat_window.destroy()

	cheat_window = Tk()
	cheat_window.title("Become a cheater")
	cheat_window.geometry("400x75")

	text = Label(cheat_window, text="Enter code", font=('',16))
	text.pack()

	ent_code = Entry(cheat_window, width=10)
	ent_code.pack()

	but_submit = Button(cheat_window, text="Enter", command=checkCheat)
	but_submit.pack()


# Displays the pause menu #
def pauseMenu():

	# Nested function to allow user to save score #
	def save():
		global score

		if messagebox.askokcancel("Save Game", "Save Score? This will overwrite any previous save."):
			with open("savegame.txt", 'w') as file:
				file.write(str(score))

			messagebox.showinfo("Game Saved", "Score successfully saved.")

	global initial, initial_boss, pause_canvas, boss_key

	if initial:
		initial = False
		pause_canvas = Canvas(window, bg="white", width=width, height=height)
		pause_canvas.create_text(width // 2 - 30, 40, text="PAUSED", font=('Franklin Gothic Medium', 24))
		but_resume = Button(pause_canvas, text="Resume", width=15, height=2, font=('', 24), command=pause)
		but_resume.place(x=width // 3 + 140, y=height // 4)
		but_cheat = Button(pause_canvas, text="Cheat", width=15, height=2, font=('', 24), command=cheater)
		but_cheat.place(x=width // 3 + 140, y=height // 4 + 120)
		but_save = Button(pause_canvas, text="Save", width=15, height=2, font=('',24), command=save)
		but_save.place(x=width // 3 + 140, y=height // 4 + 240)
		canvas.pack_forget()
		pause_canvas.bind("<Escape>", pause)
		pause_canvas.pack()

	if not initial_boss and not boss_key:
		initial_boss = True
		pause_canvas.pack()

		try:
			boss_canvas.pack_forget()
		except:
			pass


# Displays the image for the boss key #
def showBossKey():
	global initial_boss, boss_canvas

	canvas.pack_forget()

	try:
		pause_canvas.pack_forget()
	except:
		pass

	if initial_boss:
		initial_boss = False
		boss_canvas = Canvas(window, width=width, height=height)
		boss_canvas.create_image(width // 2, height // 2, image=boss_image)
		boss_canvas.pack()


# Allows user to add their score to the leaderboard #
def recordScore():

	# Nested function to add score to leaderboard.txt #
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


# Adds images to the canvas. Random is used for the #
# 'grounds' images to simulate movement.			#
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


# Resets the canvas so images don't overlap #
def canvasDeletion():
	global cheating

	canvas.delete('player')
	canvas.delete('grounds')
	canvas.delete('score')
	if not cheating: canvas.delete('cheating')
		

# Displays the game #
def mainGame():
	global run, jumptimer, score, timer, max_timer, initial, initial_boss, start_canvas, canvas, cheating, boss_key, loaded

	max_timer = 2000
	if loaded:
		subtractions = score // 25
		max_timer -= (50*subtractions)
	else:
		score = 0

	run = True
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
		if pause_game or boss_key:
			if pause_game: pauseMenu()
			if boss_key: showBossKey()				
		else:
			if not initial or not initial_boss:
				if not initial: initial = True
				if not initial_boss: initial_boss = True

				canvas.pack()

				try:
					pause_canvas.destroy()
				except:
					pass

				try:
					boss_canvas.destroy()
				except:
					pass

			timer += 1
			if timer == max_timer:
				timer = 0
				canvasDeletion()
				canvas.create_text(width // 2, 30, text="Score: " + str(score), font=('Franklin Gothic Medium', 16), tags='score')

				if cheating:
					canvas.create_text(width // 2, 60, text="Cheating", font=('',16), tags='cheating')

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




# Displays the leaderboard #
def displayLeaderboard():

	# Nested function used for sorting list by #
	# the second value in nested lists 		   #
	def second(elem):
		return elem[1]

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


# Displays the start menu #
def startMenu():
	

	# Nested function for loading game #
	def load():
		global score, loaded

		messagebox.showinfo("Game Loaded", "Game successfully loaded.")
		with open('savegame.txt','r') as file:
			score = int(file.read())
			loaded = True

	# Nested function for user to change keybind #
	def changeKey():

		# Secondary nested function to check validity of key entered #
		def checkChange():
			global user_key

			check = entry.get()
			if not check.isalpha() or check[0] == "b":
				messagebox.showinfo("Invalid", "Invalid key.")
				control_window.destroy()
				return
			user_key = check[0]
			messagebox.showinfo("Changed", "Key successfully changed.")
			control_window.destroy()

		control_window = Tk()
		control_window.title("Control")

		label = Label(control_window, text="Enter key to change jump keybind.").pack()
		label2 = Label(control_window, text="Only the first character will be accepted.").pack()
		label3 = Label(control_window, text="Only alphabetic characters are accepted.").pack()

		entry = Entry(control_window, width=2)
		entry.pack()

		button = Button(control_window, text="Change", command=checkChange).pack()

	global start_canvas, canvas

	if start_canvas == None:
		start_canvas = Canvas(window, bg="white", width=width, height=height)
		start_canvas.create_text(width // 2 - 20, 40, text="MAD DASH", font="Times 32")

		but_start = Button(start_canvas, text="Start Game", width=20, height=2, font=('',16), command=mainGame)
		but_start.place(x=width // 3 + 140, y=height // 4)

		but_leader = Button(start_canvas, text="Leaderboard", width=20, height=2, font=('',16), command=displayLeaderboard)
		but_leader.place(x=width // 3 + 140, y=height // 4 + 100)

		but_load = Button(start_canvas, text="Load Game", width=20, height=2, font=('',16), command=load)
		but_load.place(x=width // 3+ 140, y=height // 4 + 200)

		but_control = Button(start_canvas, text="Control", width=20, height=2, font=('',16), command=changeKey)
		but_control.place(x=width // 3 + 140, y=height // 4 + 300)

		but_quit = Button(start_canvas, text="Quit", width=20, height=2, font=('',16), command=onClosing)
		but_quit.place(x=width // 3 + 140, y=height // 4 + 400)

	start_canvas.pack()

#---------------#


window.protocol("WM_DELETE_WINDOW", onClosing)
window.bind("b", bossKey)
startMenu()
window.mainloop()


# END OF FILE #


