#! /usr/bin/python

import sqlite3

import pygame, pygame.mixer
from pygame.locals import *

import Xlib, Xlib.display

import sys
sys.path.append("vending_machine")
import arduino_led_controller as led_controller
import control_anything_serial_relay_control_board as vending_machine

question_set = 1
question_set_max = 4

quiz_database = sqlite3.connect('/var/db/quiz.sqlite3')
quiz_database.row_factory = sqlite3.Row
quiz = quiz_database.cursor()

led_controller = led_controller.controller()
led_controller.attract()

clock = pygame.time.Clock()
			
# Define the colors we will use in RGB format
black = [ 0, 0, 0]
white = [255,255,255]
blue = [ 0, 0,255]
green = [ 0,255, 0]
red = [255, 0, 0]
gray =[32,32,32] 
dgray =[128,128,128]

c1 = [117,186,227]
c2 = [170,219,39]
c3 = [254,117,3]
c4 = [239,253,2]
c5 = [254,0,253]

pygame.init()
pygame.mixer.init()

resolution = Xlib.display.Display().screen().root.get_geometry()
print str(resolution.width) + "x" + str(resolution.height)

screen = pygame.display.set_mode((resolution.width,resolution.height), FULLSCREEN)
pygame.init()
pygame.mouse.set_visible(0)
#toggle_fullscreen()




















class Quiz:
	level = 1
	win = 0
	ev = 0
	def __init__(self):
		self.dispensor = vending_machine.dispensor()
		self.big_win_sound = pygame.mixer.Sound("big_win.wav")

	def dispense(self, level):
		dispense_row = 7 - level
		self.dispensor.dispense(0, dispense_row)
		print "dispensing for level " + str(level) + " on row " + str(dispense_row)
		#TODO:Dispense food

	def playSound(self,index,loop):
		pygame.mixer.music.load('still_alive.mp3')
		pygame.mixer.music.play(0)




	def set_level(lvl):
		level = lvl




	def congratulate(self):
		print "Correct"

		led_controller.correct()

		for x in range(0, 6):
			clock.tick(5)
			thefont = pygame.font.Font(None,100)
			screen = pygame.display.get_surface()
			text1 = thefont.render("GOOD JOB",True,white)	
			if (x%2 == 0):			
				screen.fill([0,0,0])
			else:
				screen.fill([0,255,0])
				screen.blit(text1, [screen.get_width()/2-300,screen.get_height()/2-150])
			
			pygame.display.flip()
		



		## Animation CORRECT
	def lose(self):

		led_controller.wrong()

		for x in range(0, 6):
			clock.tick(10)
			thefont = pygame.font.Font(None,100)
			screen = pygame.display.get_surface()
			text1 = thefont.render("INCORRECT",True,white)
					
			if (x%2 == 0):			
				screen.fill([0,0,0])
			else:
				screen.fill([255,0,0])
			screen.blit(text1, [screen.get_width()/2-300,screen.get_height()/2-150])
			
			pygame.display.flip()
		print "You lose, you get nothing"
		## Animation YOU LOSE




	def win(self, lvl):		
		self.dispense(lvl)
		for x in range(0, 6):
			clock.tick(10)
			thefont = pygame.font.Font(None,120)
			screen = pygame.display.get_surface()
			text1 = thefont.render("CORRECT", True, white)
					
			if (x%2 == 0):			
				screen.fill([0,0,0])
			else:
				screen.fill([0,255,0])
			screen.blit(text1, [screen.get_width()/2-200,screen.get_height()/2])
		
			pygame.display.flip()




	def gamble(self):
		self.playSound(0,0)
		gambleloop = 1

		led_controller.attract()

		while (gambleloop == 1):
			clock.tick(10)
			#################################################
			# Gamble loop display				#
			#################################################			
			thefont2 = pygame.font.Font(None,70)
			thefont = pygame.font.Font(None,40)
			screen = pygame.display.get_surface()
			text1 = thefont2.render("Continue? or Cash out?",True,white)
			text2 = thefont.render("Continue",True,red)
			text3 = thefont.render("Continue",True,[255,255,170])
			text4 = thefont.render("Cash out",True,green)  

			text5 = thefont.render("Cash out",True,[255,255,255])
			screen.fill([0,0,0])			
			
			screen.blit(text1, [0,screen.get_height()*2.5/5])
			
			screen.blit(text2, [450,screen.get_height()/5 + 140])
			#screen.blit(text3, [450,screen.get_height()*2/5 + 140])
			#screen.blit(text4, [450,screen.get_height()*3/5 + 140])
			screen.blit(text5, [450,screen.get_height()*4/5 +140])


			pygame.display.flip()
			screen.fill([0,0,0])
			###################################################
			

			for event in pygame.event.get():
				if (event.type == KEYDOWN):			
					if (event.key == K_1) or (event.key == 257) or (event.key == K_2) or (event.key == 258):
				 		#self.level = self.level+1#@@@@@
						gambleloop = 0
						print "You are now at level"
						# print self.level

					if (event.key == K_3 or event.key==K_4) or (event.key == 259) or (event.key == 260):
						self.ev = 1
						self.thanks()
						self.dispense(self.level)
						gambleloop = 0
			
			for x in range(0, 6):
				clock.tick(10)
			
			
				
		## LOOP		
		## IF(yes)321123432
		## 	level+1
		##	breakloop
		## IF(no)
		##	Dispense(level)
		## 	event = 0
		##	breakloop
		##	
	def quizloop(self):
		global question_set
		global question_set_max

		print "Quizloop Started"
		self.ev = 0
	
		while (self.ev == 0):
			currentquestion = Question(self.level)	

			led_controller.countdown()
			b = currentquestion.test()		
			if (b == 1):
				print "WINNER!"
				self.level += 1
				
				print "level is " + str(self.level)
				#
				# We only have 6 rows of candy to dispense
				#
				if (self.level == 7):
					self.big_win_sound.play()
					self.congratulate()			
					print "YOU WIN THE GAME!"
					self.thanks()
					self.dispense(self.level)
					self.ev = 1
				else:					
					self.congratulate()
					self.gamble()
			elif (b == 0):
				print "YOU LOST THE GAME"
				self.lose()
				self.ev = 1
				
				
	
				
	
	
		for event in pygame.event.get():
			if (event.type == KEYDOWN):
				if (event.key == K_ESCAPE):
					done = True

		question_set = question_set + 1
		if question_set > question_set_max:
			question_set = 1

	def thanks(self):
		thefont = pygame.font.Font(None,200)
		screen = pygame.display.get_surface()
		text1 = thefont.render("ENJOY",True,blue)
		screen.fill([0,0,0])
		screen.blit(text1, [screen.get_width()/4,screen.get_height()/2-150])
		pygame.display.flip()

	def save_thanks(self):
		for x in range(0, 6):
			clock.tick(5)
			thefont = pygame.font.Font(None,200)
			screen = pygame.display.get_surface()
			text1 = thefont.render("ENJOY",True,blue)
					
			if (x%2 == 0):			
				screen.fill([0,0,0])
			else:
				screen.fill([0,0,0])
				screen.blit(text1, [0,screen.get_height()/2-150])
			
				pygame.display.flip()
				

	def endgame(self):
		for x in range(0, 6):
			clock.tick(5)
			thefont = pygame.font.Font(None,100)
			screen = pygame.display.get_surface()
			text1 = thefont.render("Thanks For Playing",True,blue)
					
			if (x%2 == 0):			
				screen.fill([0,0,0])
			else:
				screen.fill([0,0,0])
				screen.blit(text1, [0,screen.get_height()/2-150])
			
				pygame.display.flip()
	
	
		
class Question:
	question_text = "This is the Null Placeholder"
	answer1 = []
	answer2 = []
	answer3 = []
	button_pressed = -99
	end = 0
	
	def poll_for_input(self):
		for event in pygame.event.get():
			if (event.type == KEYDOWN):
		 		# print event
				if (event.key == K_ESCAPE):
					done = True
				if (event.key == K_1) or (event.key == 257):
					return 1
				if (event.key == K_2) or (event.key == 258):
					return 2
				if (event.key == K_3) or (event.key == 259):
					return 3
				if (event.key == K_4) or (event.key == 260):
					return 4		
			return -99
	def pollDatabase(level):
		question = "null placeholder"
		a1 = [0, "Default1"]
		a2 = [0, "Default2"]
		a2 = [0, "Default3"]
		a2 = [0, "Default4"]
	#TODO: poll Database
		return [question, a1, a2, a3, a4]
		


	def __init__(self, level):
		global quiz

		quiz.execute('SELECT question_id, text FROM questions WHERE level = ? ORDER BY RANDOM() LIMIT 1', (str(level),) )
		question = quiz.fetchone()
		self.question_test = str(question["text"])

		quiz.execute('SELECT is_correct, answer FROM answers WHERE question_id = ? ORDER BY RANDOM()', (str(question["question_id"]),) )
		self.answer1 = quiz.fetchone()
		self.answer2 = quiz.fetchone()
		self.answer3 = quiz.fetchone()
		self.answer4 = quiz.fetchone()


	def __init_static__(self, lvl):
		
		global question_set
		global question_set_max

		#
		# set 1
		#
		if (lvl == 1) and (question_set == 1):
			self.question_test = "You are a(n):"
			self.answer1 = [0, "Plant"]
			self.answer2 = [1, "Animal"]
			self.answer3 = [1, "Human"]
			self.answer4 = [0, "Ferengi"]

		if (lvl == 2) and (question_set == 1):
			self.question_test = "What does a light year measure ?"
			self.answer1 = [0,"Energy"]
			self.answer2 = [0,"Speed"]
			self.answer3 = [0,"Time"]
			self.answer4 = [1,"Distance"]

		if (lvl == 3) and (question_set == 1):
			self.question_test = "The unit of current is ?"
			self.answer1 = [0,"Ohm"]
			self.answer2 = [0,"Watt"]
			self.answer3 = [1,"Ampere"]
			self.answer4 = [0,"None of These"]

		if (lvl == 4) and (question_set == 1):
			self.question_test = "What does an Angstrom measure ?"
			self.answer1 = [0,"Quantity"]
			self.answer2 = [1,"Length"]
			self.answer3 = [0,"Volume"]
			self.answer4 = [0,"Weight"]

		if (lvl == 5) and (question_set == 1):
			self.question_test = "Which is the coldest ?"
			self.answer1 = [0,"Zero Fahrenheit"]
			self.answer2 = [0,"Zero Celsius"]
			self.answer3 = [1,"Zero Kelvin"]
			self.answer4 = [0,"Zero Meters"]

		if (lvl == 6) and (question_set == 1):
			self.question_test = "The answer to life ?"
			self.answer1 = [0,"5"]
			self.answer2 = [1,"42"]
			self.answer3 = [0,"17"]
			self.answer4 = [1,"39"]
		
		#
		# set 2
		#
		if (lvl == 1) and (question_set == 2):
			self.question_test = "What is 4 + 3 ?"
			self.answer1 = [0,"1"]
			self.answer2 = [1,"seven"]
			self.answer3 = [1,"7"]
			self.answer4 = [0,"twelve"]

		if (lvl == 2) and (question_set == 2):
			self.question_test = "What is 4 - 3 ?"
			self.answer1 = [1,"1"]
			self.answer2 = [0,"seven"]
			self.answer3 = [0,"7"]
			self.answer4 = [0,"twelve"]

		if (lvl == 3) and (question_set == 2):
			self.question_test = "What is 4 x 3 ?"
			self.answer1 = [0,"1"]
			self.answer2 = [0,"seven"]
			self.answer3 = [0,"7"]
			self.answer4 = [1,"twelve"]

		if (lvl == 4) and (question_set == 2):
			self.question_test = "What is 4 / 3 ?"
			self.answer1 = [0,"1"]
			self.answer2 = [0,"0.602"]
			self.answer3 = [1,"1.33333"]
			self.answer4 = [0,"64"]

		if (lvl == 5) and (question_set == 2):
			self.question_test = "What is 4 ^ 3 ?"
			self.answer1 = [0,"1"]
			self.answer2 = [0,"0.602"]
			self.answer3 = [0,"1.33333"]
			self.answer4 = [1,"64"]

		if (lvl == 6) and (question_set == 2):
			self.question_test = "what is log(4) ?"
			self.answer1 = [0,"1"]
			self.answer2 = [1,"0.602"]
			self.answer3 = [0,"1.33333"]
			self.answer4 = [0,"64"]
		#
		# set 3
		#
		if (lvl == 1) and (question_set == 3):
			self.question_test = "What is 7 + 19 ?"
			self.answer1 = [0,"2.6"]
			self.answer2 = [0,"blue"]
			self.answer3 = [1,"26"]
			self.answer4 = [0,"27"]

		if (lvl == 2) and (question_set == 3):
			self.question_test = "What does the term 'dinosaur' mean ?"
			self.answer1 = [0,"Giant lizard"]
			self.answer2 = [1,"Terrible lizard"]
			self.answer3 = [0,"Oily lizard"]
			self.answer4 = [0,"Scaly lizard"]

		if (lvl == 3) and (question_set == 3):
			self.question_test = "Which of the following scientists studies animals ?"
			self.answer1 = [1,"Zoologist"]
			self.answer2 = [0,"Geologist"]
			self.answer3 = [0,"Botanist"]
			self.answer4 = [0,"Physicist"]

		if (lvl == 4) and (question_set == 3):
			self.question_test = "How hot is lightning ?"
			self.answer1 = [0,"1,000 F"]
			self.answer2 = [0,"40,000 F"]
			self.answer3 = [1,"70,000 F"]
			self.answer4 = [0,"140,000 F"]

		if (lvl == 5) and (question_set == 3):
			self.question_test = "Isobars are lines on a weather map. What do they represent ?"
			self.answer1 = [0,"Areas of equal temperature"]
			self.answer2 = [0,"Areas of equal precipitation"]
			self.answer3 = [1,"Areas of equal air pressure"]
			self.answer4 = [0,"Areas of equal cloudiness"]

		if (lvl == 6) and (question_set == 3):
			self.question_test = "What did Edward Binney and Harold Smith invent in 1903 ?"
			self.answer1 = [0,"Post-it Notes"]
			self.answer2 = [0,"Scotch Tape"]
			self.answer3 = [0,"Ball point pen"]
			self.answer4 = [1,"Crayola Crayons"]
		## TODO: Replace

		#
		# set 4
		#
		if (lvl == 1) and (question_set == 4):
			self.question_test = "How many horns could be found on the head of a triceratops ?"
			self.answer1 = [0,"1"]
			self.answer2 = [0,"2"]
			self.answer3 = [1,"3"]
			self.answer4 = [0,"4"]

		if (lvl == 2) and (question_set == 4):
			self.question_test = "what is 15 x 3 ?"
			self.answer1 = [0,"5"]
			self.answer2 = [0,"30"]
			self.answer3 = [0,"54"]
			self.answer4 = [1,"45"]

		if (lvl == 3) and (question_set == 4):
			self.question_test = "What does a herpetologist study ?"
			self.answer1 = [0,"Insects"]
			self.answer2 = [1,"Reptiles"]
			self.answer3 = [0,"Mammals"]
			self.answer4 = [0,"Birds"]

		if (lvl == 4) and (question_set == 4):
			self.question_test = "What was invented by Samuel F. B. Morse in 1837 ?"
			self.answer1 = [0,"Typewriter"]
			self.answer2 = [0,"Telephone"]
			self.answer3 = [1,"Telegraph"]
			self.answer4 = [0,"Television"]

		if (lvl == 5) and (question_set == 4):
			self.question_test = "When was the ENIAC computer turned on for the first time ?"
			self.answer1 = [1,"1946"]
			self.answer2 = [0,"1956"]
			self.answer3 = [0,"1964"]
			self.answer4 = [0,"1984"]

		if (lvl == 6) and (question_set == 4):
			self.question_test = "What did Edward Binney and Harold Smith invent in 1903 ?"
			self.answer1 = [0,"Post-it Notes"]
			self.answer2 = [0,"Scotch Tape"]
			self.answer3 = [0,"Ball point pen"]
			self.answer4 = [1,"Crayola Crayons"]

#red yellow green white
	def split(txt):
		lines = []
		text = ""
		counter = 0
		for car in txt:
			counter = counter + 1
			if(counter<12):
				text = text + car
			else:
				lines.append(text)
				text = ""
				text = text + char
				counter = 0
		


		return lines
		
	def test(self):
		escape_condition = 0
		performance_state = -99
		score = 0
		
		
		question = "This is where the question goes"




		questionfont = pygame.font.Font(None,screen.get_width()/15)
		#attractfont = pygame.font.Font(None,screen.get_width/10)
		questionfont2 = pygame.font.Font(None,screen.get_width()/20)
		a1 = self.answer1[1]
		a2 = self.answer2[1]
		a3 = self.answer3[1]
		a4 = self.answer4[1]
		q = self.question_test

		#loins = split(q)
		#print loins


		qtxt = questionfont2.render(q,True,white)

		text1 = questionfont.render(a1,True,white)
		text2 = questionfont.render(a2,True,black)
		text3 = questionfont.render(a3,True,white)
		text4 = questionfont.render(a4,True,black)

		#This is our background image.  
		fifthw = screen.get_width()/5
		fifthh = screen.get_height()/5

		xtran = 0
		ytran = 0
		fifth_h = screen.get_height()/5
		fifth_w = screen.get_width()/5


		while (escape_condition == 0):

			for x in range(0, 6):
				clock.tick(10)		
			
			screen.fill([0,0,0])

			#self.clock.tick(1)
			#### Display Contents###########################################################################
#			pygame.draw.line(screen, (0, 0, 255), (fifthw, 0), (fifthw, screen.get_height()))	
#			pygame.draw.line(screen, (0, 0, 255), (2*fifthw, 0), (2*fifthw, screen.get_height()))	
#			pygame.draw.line(screen, (0, 0, 255), (3*fifthw, 0), (3*fifthw, screen.get_height()))	
#			pygame.draw.line(screen, (0, 0, 255), (4*fifthw, 0), (4*fifthw, screen.get_height()))	
	
#			pygame.draw.line(screen, (255, 0, 0), (0,fifthh), (screen.get_width(),fifthh))	
#			pygame.draw.line(screen, (255, 0, 0), (0,2*fifthh), (screen.get_width(),2*fifthh))	
#			pygame.draw.line(screen, (255, 0, 0), (0,3*fifthh), (screen.get_width(),3*fifthh))	
#			pygame.draw.line(screen, (255, 0, 0), (0,4*fifthh), (screen.get_width(),4*fifthh))	

			pygame.draw.rect(screen, [255,0,0], (0,xtran + fifth_h,screen.get_width(), 200-20), 0)
			pygame.draw.rect(screen, [255,255,0], (0,xtran + fifth_h*2,screen.get_width(), 200-20), 0)
			pygame.draw.rect(screen, [0,255,0], (0,xtran + fifth_h*3,screen.get_width(), 200-20), 0)
			pygame.draw.rect(screen, [255,255,255],(0,xtran + fifth_h*4,screen.get_width(), 200-20), 0)
			

		#	pygame.draw.rect(screen, c1, (0,s1,screen.get_width(),h1), 0)

			screen.blit(qtxt, [0,fifthh/2])	
			screen.blit(text1, [fifthw/2,fifthh+fifthh/4])	
			screen.blit(text2, [fifthw/2,fifthh*2+fifthh/4])	
			screen.blit(text3, [fifthw/2,fifthh*3+fifthh/4])	
			screen.blit(text4, [fifthw/2,fifthh*4+fifthh/4])	

			clock.tick(10)


			#### Poll for input#############################################################################
			button_pressed = self.poll_for_input()
			#### Check validity
			if (button_pressed ==1 ):
				if (self.answer1[0] == 1):			
					performance_state = 1
				else:
					performance_state = 0
			if (button_pressed == 2):
				if (self.answer2[0] ==1):
					performance_state = 1
				else:
					performance_state = 0
			if (button_pressed == 3):
				if (self.answer3[0] ==1):
					performance_state = 1
				else:
					performance_state = 0
			if (button_pressed == 4):  
				if (self.answer4[0] ==1):
					performance_state = 1
				else:
					performance_state = 0		
			
			#### Go through animation/suspense loop. It shows that the question was selected.			
			if (performance_state != -99):
				suspense_loop_condition = 0			
				while (suspense_loop_condition == 0):
					## Loopit
					if (1):
						suspense_loop_condition =1
						escape_condition =1
				

			pygame.display.flip()
		return performance_state


#############################
done = False

print "PRESS ANY KEY TO PLAY"
start = False
it = 0
x,y = [0,0]
while (done == False):
	led_controller.attract()

	
	thefont = pygame.font.Font(None, 50)
	screen = pygame.display.get_surface()
	screen.fill([0, 0, 0])

	it += 1
	if (it % 2 == 0):
		text1 = thefont.render("PRESS ANY KEY",True,[0, 0, 255])
	else:
		text1 = thefont.render("PRESS ANY KEY",True,[0, 0, 0])

	screen.blit(text1, [300,1000])

	thephoto = pygame.image.load('logo.png')
	thephoto = pygame.transform.scale(thephoto, (int(800), int(800)))
	screen.blit(thephoto,[40, 110])
	

	for x in range(0, 6):
		clock.tick(10)	
	for event in pygame.event.get():
		# print event
		if (event.type == KEYDOWN):
			if (event.key == K_LEFT):
				x -= 20
			if (event.key == K_RIGHT):
				x += 20
			if (event.key == K_UP):
				y -= 20
			if (event.key == K_DOWN):
				y += 20
			if (event.key == K_ESCAPE):
				done = True
				for x in range(0, 6):
					clock.tick(10)							
			if (event.key == K_1) or (event.key == 257):
				start = True	
				for x in range(0, 6):
					clock.tick(10)

			if (event.key == K_2) or (event.key == 258):
				for x in range(0, 6):
					clock.tick(10)

				start = True
			if (event.key == K_3) or (event.key == 259):
				for x in range(0, 6):
					clock.tick(10)

				start = True
			if (event.key == K_4) or (event.key == 260):
				for x in range(0, 6):
					clock.tick(10)

				start = True	

	if (start):			
		# print start	
		a = Quiz()
		a.quizloop()
		start = False

	pygame.display.flip()

print "Gameover"
