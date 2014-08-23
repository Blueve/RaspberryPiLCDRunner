from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Layer import Layer
from collections import deque

import thread
import random

class Game():

	STATE_START   = 0
	STATE_END     = 1
	STATE_RUNNING = 2
	
	RUNNER_RUN    = 0
	RUNNER_JUMP   = 1

	OPSET = (Adafruit_CharLCDPlate.UP,
			#Adafruit_CharLCDPlate.DOWN,
			 Adafruit_CharLCDPlate.SELECT)

	def __init__(self, lcd):
		self.lcd          = lcd
		self.state        = self.STATE_START
		self.runner       = self.RUNNER_RUN
		# barrier (row, col)
		self.barriers     = deque([])
		self.lastBarriers = 0
		self.frame        = 0
		
		self.runner       = 0
		self.runnerJump   = 1
		
		self.score        = 0
		# Init input management thread
		thread.start_new_thread(self.input, ())

	def input(self):
		print 'input hanlde thread started.'
		while True:
			for op in self.OPSET:
				if self.lcd.buttonPressed(op):
					print 'A button pressed!'
					self.eventHandle(op)
					# Set a delay time to avoid run continuously
					sleep(.2)
				sleep(.05)

	def tick(self):
		if self.state == self.STATE_RUNNING:
			# Excute by Display frame control
			# Barriers
			if self.frame == 0:
				# Random generate a barriers
				if self.lastBarriers < 15:
					rnd = random.randint(0, 100)
					if rnd < 50:
						self.barriers.append([1, 16])
						self.lastBarriers = 17
				# Move barriers
				for barrier in self.barriers:
					barrier[1] -= 1
				self.lastBarriers -= 1

				if len(self.barriers) > 0 and self.barriers[0][1] == -2:
					self.barriers.popleft()
			# Update frame
			self.frame += 1
			self.frame %= 6

			# Runner
			self.runner += self.runnerJump
			if self.runner == 9:
				self.runnerJump = -1
			elif self.runner == 0:
				self.runnerJump = 0

			# Update score
			self.score += 1
		#elif self.state == self.STATE_START:
		#elif self.state == self.STATE_END:


	def eventHandle(self, op):
		if self.state == self.STATE_START:
			self.start(op) 
		elif self.state == self.STATE_END:
			self.end(op)
		elif self.state == self.STATE_RUNNING:
			self.running(op)

	def start(self, op):
		if op == Adafruit_CharLCDPlate.SELECT:
			self.state      = self.STATE_RUNNING
			self.runner     = 0
			self.runnerJump = 0
			self.score      = 0
			self.barriers   = deque([])
			self.lcd.clear()

	def end(self, op):
		if op == Adafruit_CharLCDPlate.SELECT:
			self.lcd.clear()
			self.state = self.STATE_START

	def running(self, op):
		if op == Adafruit_CharLCDPlate.UP:
			if self.runnerJump == 0:
				self.runnerJump = 1

	def gameOver(self, block_1, block_2):
		for i in range(8):
			if block_1[i] & block_2[i] > 0:
				self.lcd.clear()
				self.state = self.STATE_END
