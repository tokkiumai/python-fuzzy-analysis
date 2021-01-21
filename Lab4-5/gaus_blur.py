import math
import numpy as np
from PIL import Image


class GausBlur:

	def __init__(self, radius, sigma):
		self.radius = radius
		self.sigma = sigma

		_sum = 0.0
		ker_w = 2 * self.radius + 1
		self.kernel = np.zeros((ker_w, ker_w), dtype=np.float)

		for x in range(0, ker_w):
			for y in range(0, ker_w):
				self.kernel[x][y] = self.gaus(float(x), float(y), float(self.radius), self.sigma)
				_sum += self.kernel[x][y]

		for x in range(0, ker_w):
			for y in range(0, ker_w):
				self.kernel[x][y] /= _sum
	

	def gaus(self, x, y, sigma, mu):
		return math.exp(-(((x - mu) ** 2) / sigma + ((y - mu) ** 2) / sigma) / 2.0) / (2 * math.pi * sigma ** 2)
	

	def convolve(self, x, y, w, h, img):
		_sum = 0.0

		for i in range(x - self.radius, x + self.radius + 1):
			for j in range(y - self.radius, y + self.radius + 1):
				if (i >= 0) and (i < h) and (j >= 0) and (j < w):
					_sum += img[i][j] * self.kernel[i - (x - self.radius)][j - (y - self.radius)]

		return _sum

	def get_blur_img(self, img, queue):
		width, height = img.size
		new_img = np.array(img)

		for i in range(0, height):
			for j in range(0, width):
				center = self.convolve(i, j, width, height, new_img)
				new_img[i][j] = center

		queue.put(new_img)
