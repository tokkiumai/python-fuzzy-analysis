import numpy as np
from PIL import Image

class GrayScale:

	def __init__(self, img, width, height):
		self.img = img
		self.width = width
		self.height = height

	def avg(self, color):
		r, g, b = color
		return (r + g + b)/3

	def luminosity(self, color):
		r, g, b = color
		return (0.07*b + 0.72*g + 0.21*r)

	def lightness(self, color):
		r, g, b = color
		return (max(r, g, b) + min(r, g, b))/2

	def get_gray_image(self, gray_type):
		if gray_type == 0:
			func = self.avg
		elif gray_type == 1:
			func = self.lightness
		elif gray_type == 2:
			func = self.luminosity

		try:
			img = self.img.convert('RGB')
		except:
			return

		data = np.zeros((self.height, self.width,3), dtype=np.uint8 )
        
		for x in range(0, self.width):
			for y in range(0, self.height):
				gray = func(img.getpixel((x, y)))
				data[y, x] = [gray] * 3

		return Image.fromarray(data)
		