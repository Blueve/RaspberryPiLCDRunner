from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Layer import Layer
from collections import deque

import random

class Game():

	STATE_START   = 0
	STATE_END     = 1
	STATE_RUNNING = 2
	
	RUNNER_RUN    = 0
	RUNNER_JUMP   = 1

	OPSET = (Adafruit_CharLCDPlate.LEFT,
			 Adafruit_CharLCDPlate.RIGHT,
			 Adafruit_CharLCDPlate.UP,
			 Adafruit_CharLCDPlate.DOWN,
			 Adafruit_CharLCDPlate.SELECT)

	def __init__(self):
		self.state = self.STATE_START
		self.runner = self.RUNNER_RUN
		# barrier (row, col)
		self.barriers = deque([])
		self.lastBarriers = 0
		self.frame = 0

		self.runner = 0
		self.runnerJump = 1

		self.score = 0

	def input(self):
		while True:
			for op in self.OPSET:
				if self.lcd.buttonPressed(op):
					eventHandle(op)
					# Set a delay time to avoid run continuously
					sleep(.2)

	def tick(self):
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
		if self.runner == 6:
			self.runnerJump = -1
		elif self.runner == 0:
			self.runnerJump = 1

		# Update score
		self.score += 1


	def eventHandle(self, op):
		if self.state == STATE_START:
			self.start(op) 
		elif self.state == STATE_END:
			self.end(op)
		elif self.state == STATE_RUNNING:
			self.running(op)

	def start(self, op):
		if op == Adafruit_CharLCDPlate.SELECT:
			self.state = STATE_RUNNING
			self.runner = RUNNER_RUN

	def end(self, op):
		if op == Adafruit_CharLCDPlate.SELECT:
			self.state = STATE_START

	def running(self, op):
		if op == Adafruit_CharLCDPlate.UP:
			self.runner = RUNNER_JUMP
