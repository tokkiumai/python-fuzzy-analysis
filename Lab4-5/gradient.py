from PIL import Image
import math
import numpy as np


class Gradient:

	def __init__(self, operator):
		self.operator = operator


	def roberts(self):
		return {'MGx' : [[1, 0, 0],
						[0, -1, 0],
						[0, 0, 0]],
						
				'MGy' : [[0, 1, 0],
						[-1, 0, 0],
						[0, 0, 0]]
			}

	def sobel(self):
		return {'MGx' : [[-1, 0, 1],
						[-2, 0, 2],
						[-1, 0, 1]],
						
				'MGy' : [[-1, -2, -1],
						[0, 0, 0],
						[1, 2, 1]]
				}

	def prewitt(self):
		return {'MGx' : [[1, 0, -1],
						[1, 0, -1],
						[1, 0, -1]],
						
				'MGy' : [[1, 1, 1],
						[0, 0, 0],
						[-1, -1, -1]]
				}


	def round_angle(self, angle):
		if angle >= 22 and angle < 67:
			return 45
		elif angle < 112:
			return 90
		elif angle < 158:
			return 135
		else:
			return 0

	def gradient(self, x, y, img):
		gx, gy = 0, 0

		if self.operator == 0:
			MGx = self.sobel()['MGx']
			MGy = self.sobel()['MGy']
		elif self.operator == 1:
			MGx = self.roberts()['MGx']
			MGy = self.roberts()['MGy']
		else:
			MGx = self.prewitt()['MGx']
			MGy = self.prewitt()['MGy']

		for i in range(0, 3):
			for j in range(0, 3):
				pix = img.getpixel((x - 1 + i, y - 1 + j))
				gx += pix[0] * MGx[i][j]
				gy += pix[0] * MGy[i][j]

		g = math.sqrt(gx ** 2 + gy ** 2)
		ang = self.round_angle(abs(math.atan2(gy, gx) * 180 / math.pi))
		return g, ang

	def gradient_analysis(self, img):
		w, h = img.size

		grad_matrix = np.zeros((h, w), dtype=np.float)
		ang_matrix = np.zeros((h, w), dtype=np.float)

		for x in range(1, w - 1):
			for y in range(1, h - 1):
				g, ang = self.gradient(x, y, img)
				grad_matrix[y][x] = g
				ang_matrix[y][x] = ang

		return grad_matrix, ang_matrix


	def find_neighbours(self, x,y, ang):
		if ang == 45:
			return x + 1, y - 1, x - 1, y + 1
		elif ang == 90:
			return x, y + 1, x, y - 1
		elif ang == 135:
			return x - 1, y - 1, x + 1, y + 1
		else:
			return x + 1, y, x - 1, y

	def notmax_suppression(self, grad_matrix, ang_matrix):
		h, w = len(grad_matrix), len(grad_matrix[0])

		res = np.zeros((h, w), dtype=np.float)

		for x in range(1, w - 1):
			for y in range(1, h - 1):
				x1, y1, x2, y2 = self.find_neighbours(x, y, ang_matrix[y][x])
				if grad_matrix[y][x] >= grad_matrix[y1][x1] and grad_matrix[y][x] >= grad_matrix[y2][x2]:
					res[y][x] = grad_matrix[y][x]
				else:
					res[y][x] = 0
		
		return res