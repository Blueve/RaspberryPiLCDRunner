
class Layer():

	WIDTH  = 16
	HEIGHT = 2

	EMPTY = [0b00000, # Empty bitmap, equal to char ' '
			 0b00000,
			 0b00000,
			 0b00000,
			 0b00000,
			 0b00000,
			 0b00000,
			 0b00000]

	def __init__(self):
		# Init layer bitmap
		self.bitmap = [[list(self.EMPTY) for col in range(self.WIDTH)] for row in range(self.HEIGHT)]

	def drawPointX(self, col, row, frame, pixel):
		# ..... ..... .....  
		# ..... ..... .....  
		# ..... ..... .....  
		# ..... ..... .....  
		# ..... ..... .....  ... LCD Pixel        : pixel(bitmap, bitmap)
		# ..... ..... .....  
		# ..... ..... .....  
		# ..... ..... .....  
		# 0     1     2      ... LCD Bitmap Index : col, row
		# 0 1 2 0 1 2 0 1 2  ... Key Frame Index  : frame
		if col >= 0 and col < self.WIDTH:
			self.bitmap[row][col] = pixel[0]
		# Draw right pixel
		if frame != 0 and col < self.WIDTH - 1:
			self.bitmap[row][col + 1] = pixel[1]

	def drawPointY(self, col, row, pixel):
		# .....0 0
		# .....
		# .....  
		# .....  1
		# .....  
		# .....
		# .....  2
		# .....
		#
		# .....1 0
		# .....
		# .....
		# .....  1
		# .....
		# .....
		# .....  2
		# .....
		self.bitmap[row][col] = pixel[0]
		self.bitmap[row + 1][col] = pixel[1]

	def mergeLayer(self, layer):
		# Merge pixel
		for row in range(self.HEIGHT):
			for col in range(self.WIDTH):
				for i in range(8):
					self.bitmap[row][col][i] = self.bitmap[row][col][i] | layer.bitmap[row][col][i]

