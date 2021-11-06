from tkinter import *
from tkinter import messagebox
import random as r

window = Tk()
window.title("Mad Dash")
window.geometry("1920x1080")
width = 1920
height = 1080

canvas = Canvas(window, bg="white", width=width, height=height)

# Image Loading #
playerImages = [PhotoImage(file="player1.png"), PhotoImage(file="player2.png")]
ground = PhotoImage(file="ground.png")
underground = PhotoImage(file="underground.png")
# ------------- #

# Subroutines #
def on_closing():
	global run
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		run = False


test = canvas.create_image(60,height // 2 - 60, image=playerImages[0], tags='player')
player_image_used = 0
x = 0
while x < 1920:
	temp = canvas.create_image(x, height // 2, image=ground)
	x += r.randint(60, 120)
x = 0
y = height // 2 + 120
while y < height:
	while x < 1920:
		temp = canvas.create_image(x, y, image=underground)
		x += r.randint(30,90)
	x = 0
	y += r.randint(30, 90)

canvas.pack()
window.update()


global run
run = True

timer = 0
while run:
	timer += 1
	if timer == 1000:
		timer = 0
		canvas.delete('player')
		if player_image_used == 0:
			player_image_used = 1
		else:
			player_image_used = 0
		canvas.create_image(60, height // 2 - 60, image=playerImages[player_image_used], tags='player')
	window.protocol("WM_DELETE_WINDOW", on_closing)
	window.update()



