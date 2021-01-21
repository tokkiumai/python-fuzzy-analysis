from PIL import Image
import numpy as np
from numpy import sqrt

class Lab5:

    def __init__(self):
        self.matrix = [
            [0.75, 0.2, 0.1],
            [0.75, 0.2, 0.1],
            [0.75, 0.1, 0.4],
            [0.75, 0.1, 0.1],
            [0.75, 0.1, 0.3],
            [0.75, 0.2, 0.15],
            [0.7, 0.2, 0.1],
            [0.3, 0.8, 0.1],
            [0.2, 0.7, 0.3],
            [0.3, 0.75, 0.3],
            [0.1, 0.8, 0.1],
            [0.1, 0.75, 0.3],
            [0.2, 0.75, 0.3],
            [0.2, 0.75, 0.3],
            [0.1, 0.3, 0.75],
            [0.1, 0.3, 0.75],
            [0.2, 0.1, 0.75],
            [0.3, 0.4, 0.75],
            [0.2, 0.2, 0.75],
            [0.2, 0.2, 0.75],
            [0.2, 0.4, 0.75]
        ]

        self.max_coef_list = []

    def start(self, img):
        for i in range(1, 22):
            path = "C:/Users/Тимофей/Desktop/Lab4/db_1/{}.jpg".format(i)
            img_db = Image.open(path)

            coef = self.compare_imgs(img, img_db)
            
            _max = max([i * coef for i in self.matrix[i - 1]])
            self.max_coef_list.append(_max)
        
        print(self.max_coef_list)
        
        _max = self.max_coef_list[0]
        for i in range(1, 21):
            if _max < self.max_coef_list[i]:
                _max = self.max_coef_list[i]
                ind = i

        # _max = max(self.max_coef_list)
        # ind = self.max_coef_list.index(_max)

        print(_max)
        
        img = Image.open("C:/Users/Тимофей/Desktop/Lab4/db_1/{}.jpg".format(ind))
        img.show()

        if ind <= 7:
            return "+"
        elif ind <= 14:
            return "T"
        else:
            return "Г"

    

    def compare_imgs(self, img_1, img_2):
        w, h = img_1.size

        matrix_1 = np.array(img_1)
        matrix_2 = np.array(img_2)

        Mx, My = 0, 0

        for y in range(0, w):
            for x in range(0, h):
                Mx += matrix_1[y][x]
                My += matrix_2[y][x]

        Mx /= (w * h)
        My /= (w * h)

        sigma_x, sigma_y = 0, 0
        _sum = 0

        for y in range(0, w):
            for x in range(0, h):
                _sum += (matrix_1[y][x] - Mx) * (matrix_2[y][x] - My)
                sigma_x += (matrix_1[y][x] - Mx) ** 2
                sigma_y += (matrix_2[y][x] - My) ** 2

        sigma_x = sqrt(sigma_x)
        sigma_y = sqrt(sigma_y)

        return _sum / ((w * h - 1) * sigma_x * sigma_y)