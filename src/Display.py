from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Layer import Layer
from Game import Game
from collections import deque

import thread
class Display():

	BARRIER = [
			  [[0b00000, # Frame 0
			    0b00000,
			    0b00000,
			    0b00100,
			    0b01110,
			    0b01110,
			    0b11111,
			    0b11111],
			   [0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000]],
			  [[0b00000, # Frame 1 in
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000],
			   [0b00000,
			    0b00000,
			    0b00000,
			    0b01000,
			    0b11100,
			    0b11100,
			    0b11110,
			    0b11110]],
			  [[0b00000, # Frame 1
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00001,
			    0b00001],
			   [0b00000,
			    0b00000,
			    0b00000,
			    0b10000,
			    0b11000,
			    0b11000,
			    0b11100,
			    0b11100]],
			  [[0b00000, # Frame 2 in
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00001,
			    0b00001,
			    0b00011,
			    0b00011],
			   [0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b10000,
			    0b10000,
			    0b11000,
			    0b11000]],
			  [[0b00000, # Frame 2
			    0b00000,
			    0b00000,
			    0b00001,
			    0b00011,
			    0b00011,
			    0b00111,
			    0b00111],
			   [0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b10000,
			    0b10000]],
			  [[0b00000, # Frame 3
			    0b00000,
			    0b00000,
			    0b00010,
			    0b00111,
			    0b00111,
			    0b01111,
			    0b01111],
			   [0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000]]]

	RUNNER = [
			  [[0b00000, # Frame 0
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000],
			   [0b00000, 
			    0b00000,
			    0b00000,
			    0b01110,
			    0b11111,
			    0b11111,
			    0b11111,
			    0b01110]],
			  [[0b00000, # Frame 1
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000],
			   [0b00000, 
			    0b00000,
			    0b00000,
			    0b01110,
			    0b11111,
			    0b11111,
			    0b11111,
			    0b01110]],
			  [[0b00000, # Frame 2
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000],
			   [0b00100, 
			    0b01110,
			    0b11111,
			    0b11111,
			    0b11111,
			    0b01110,
			    0b01110,
			    0b00000]],
			  [[0b00000, # Frame 3
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00100],
			   [0b01110, 
			    0b11111,
			    0b11111,
			    0b11111,
			    0b01110,
			    0b00000,
			    0b00000,
			    0b00000]],
			  [[0b00000, # Frame 4
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00100,
			    0b01110,
			    0b01110],
			   [0b11111, 
			    0b11111,
			    0b01110,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000]],
			  [[0b00000, # Frame 5
			    0b00000,
			    0b00000,
			    0b00000,
			    0b01110,
			    0b11111,
			    0b11111,
			    0b11111],
			   [0b01110, 
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000]],
			  [[0b00000, # Frame 6
			    0b00000,
			    0b01100,
			    0b01110,
			    0b11111,
			    0b11111,
			    0b11111,
			    0b01110],
			   [0b00000, 
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000,
			    0b00000]]]

	def __init__(self):
		# Init LCD 
		self.lcdString = [[' ' for col in range(Layer.WIDTH)] for row in range(Layer.HEIGHT)]
		# Init layer
		self.canvas  = Layer()
		self.runner  = Layer()
		self.barrier = Layer()
		# Init pixelSet
		self.pixelSet = [list(Layer.EMPTY) for i in range(8)]
		# Init LCD
		self.lcd = Adafruit_CharLCDPlate()
		self.lcd.begin(16, 2)
		self.lcd.backlight(Adafruit_CharLCDPlate.ON)
		# Init Game
		self.game = Game()

	def mergeLayers(self):
		# Merge layer to canvas
		#self.canvas.mergeLayer(self.runner).mergeLayer(self.barrier)
		self.canvas.mergeLayer(self.barrier)
		self.canvas.mergeLayer(self.runner)


	def updateLcdString(self):
		# Update game screen
		count = 0
		for row in range(Layer.HEIGHT):
			for col in range(Layer.WIDTH):
				if self.canvas.bitmap[row][col] == Layer.EMPTY:
					self.lcdString[row][col] = ' '
				else:
					index = self.findInPixelSet(self.canvas.bitmap[row][col])
					if index == -1:
						self.pixelSet[count] = self.canvas.bitmap[row][col]
						self.lcdString[row][col] = chr(count)
						count += 1
					else:
						self.lcdString[row][col] = chr(index)

		# Update score board
		score = str(self.game.score)
		index = 0
		for i in range(Layer.WIDTH - len(score), Layer.WIDTH):
			self.lcdString[0][i] = score[index]
			index += 1
		

	def loadCharset(self):
		for i, item in enumerate(self.pixelSet):
			self.lcd.createChar(i, item)

	def findInPixelSet(self, pixel):
		for i in range(8):
			if self.pixelSet[i] == pixel:
				return i
		return -1

	def draw(self):
		line_1 = ''.join(self.lcdString[0])
		line_2 = ''.join(self.lcdString[1])
		self.lcd.clear()
		self.loadCharset()
		self.lcd.message(line_1 + '\n' + line_2)

	def drawBarriers(self):
		for barrier in self.game.barriers:
			self.barrier.drawPointX(barrier[1], barrier[0], self.game.frame, self.BARRIER[self.game.frame])

	def drawRunner(self):
		self.runner.drawPointY(1, 0, self.RUNNER[self.game.runner])

	def run(self):
		while True:
			self.game.tick()
			print 'frame: ', self.game.frame
			self.drawBarriers()
			print 'barriers: ', self.game.barriers
			self.drawRunner()
			self.mergeLayers()
			self.updateLcdString()
			self.draw()
			self.canvas  = Layer()
			self.runner  = Layer()
			self.barrier = Layer()
			sleep(.08)

if __name__ == '__main__':
	display = Display()
	display.run()