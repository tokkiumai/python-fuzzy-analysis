import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import queue
from threading import Thread
import numpy as np

from gray_sclae import GrayScale
from gaus_blur import GausBlur
from gradient import Gradient
from lab5 import Lab5

class Main(tk.Frame):

	def __init__(self, root):
		super().__init__(root)

		self.black_var = tk.IntVar()
		self.gradient_var = tk.IntVar()

		self.create_window()


	def create_window(self):
		open_img_btn = tk.Button(text="Выбрать изображение")
		open_img_btn.place(x = 250, y = 0)
		open_img_btn.bind('<Button-1>', lambda event: self.choose_image())

		# left frame
		left_frame = tk.Frame(self)
		left_frame.grid(row=1, column=0)

		left_frame_label = tk.Label(left_frame, text="Перевод в черно-белый формат")
		left_frame_label.pack(side=tk.TOP)

		black_1_rb = tk.Radiobutton(left_frame, text="AVG", variable=self.black_var, value=0)
		black_1_rb.pack(side=tk.TOP)
		black_1_rb.bind('<Button-1>', lambda event: self.on_make_black_btn_clicked())

		black_2_rb = tk.Radiobutton(left_frame, text="LIGHTNESS", variable=self.black_var, value=1)
		black_2_rb.pack(side=tk.TOP)
		black_2_rb.bind('<Button-1>', lambda event: self.on_make_black_btn_clicked())

		black_3_rb = tk.Radiobutton(left_frame, text="LUMINOSITY", variable=self.black_var, value=2)
		black_3_rb.pack(side=tk.TOP)
		black_3_rb.bind('<Button-1>', lambda event: self.on_make_black_btn_clicked())

		# center frame

		center_frame = tk.Frame(self)
		center_frame.grid(row=2, column=0)

		center_frame_label = tk.Label(center_frame, text="Гаусовское размытие")
		center_frame_label.pack(side=tk.TOP)

		frm1 = tk.Frame(center_frame)
		frm1.pack(side=tk.TOP)

		tk.Label(frm1, text='Радиус: ').pack(side=tk.TOP)
	

		self.radius_scale = tk.Scale(frm1, orient=tk.HORIZONTAL, length = 200, from_=1.0, to = 9.0,tickinterval = 1, resolution = 1)
		self.radius_scale.pack(side=tk.TOP)

		frm2 = tk.Frame(center_frame)
		frm2.pack(side=tk.TOP)

		tk.Label(frm2, text='Сигма: ').pack(side=tk.TOP)
	

		self.sigma_scale = tk.Scale(frm2, orient=tk.HORIZONTAL, length = 200, from_=0, to = 9,tickinterval =1 , resolution = 0.1)
		self.sigma_scale.pack(side=tk.TOP)
		tk.Button(center_frame, text='Размыть', command= lambda : self.on_blur_btn_clicked()).pack(side=tk.TOP)


		# right frame
		right_frame = tk.Frame(self)
		right_frame.grid(row=3, column=0)

		right_frame_label = tk.Label(right_frame, text="Поиск градиента")
		right_frame_label.pack(side=tk.TOP)

		gradient_1_rb = tk.Radiobutton(right_frame, text="Оператор Собеля", variable=self.gradient_var, value=0)
		gradient_1_rb.pack(side=tk.TOP)
		gradient_1_rb.bind('<Button-1>', lambda event: self.notmax_suppression())

		gradient_2_rb = tk.Radiobutton(right_frame, text="Оператор Робертса", variable=self.gradient_var, value=1)
		gradient_2_rb.pack(side=tk.TOP)
		gradient_2_rb.bind('<Button-1>', lambda event: self.notmax_suppression())

		gradient_3_rb = tk.Radiobutton(right_frame, text="Оператор Прюитта", variable=self.gradient_var, value=2)
		gradient_3_rb.pack(side=tk.TOP)
		gradient_3_rb.bind('<Button-1>', lambda event: self.notmax_suppression())
		

		# right frame 2

		right_frame_2 = tk.Frame(self)
		right_frame_2.grid(row=4, column=0)

		right_frame_label_2 = tk.Label(right_frame_2, text="Двойная пороговая фильтрация")
		right_frame_label_2.pack(side=tk.TOP)

		frm3 = tk.Frame(right_frame_2)
		frm3.pack(side=tk.TOP)

		tk.Label(frm3, text='Нижняя граница: ').pack(side=tk.LEFT)
		self.bot_entry = tk.Entry(frm3)
		self.bot_entry.pack(side=tk.LEFT)

		frm4 = tk.Frame(right_frame_2)
		frm4.pack(side=tk.TOP)

		tk.Label(frm4, text='Верхняя граница: ').pack(side=tk.LEFT)
		self.top_entry = tk.Entry(frm4)
		self.top_entry.pack(side=tk.LEFT)

		tk.Button(right_frame_2, text='Фильтровать', command= lambda : self.on_filter_btn_clicked()).pack(side=tk.TOP)

		# right frame 3
		right_frame_3 = tk.Frame(self)
		right_frame_3.grid(row=5, column=0)

		right_frame_label_3 = tk.Label(right_frame_3, text="Распознование")
		right_frame_label_3.pack(side=tk.TOP)

		tk.Button(right_frame_3, text='Распознать', command= lambda : self.on_recognize_btn_clicked()).pack(side=tk.TOP)

		self.res_lbl = tk.Label(right_frame_3, text='')
		self.res_lbl.pack(side=tk.TOP)


	def on_recognize_btn_clicked(self):
		self.res_lbl.pack_forget()
		lab5 = Lab5()
		sym = lab5.start(self.filter_img)
		self.res_lbl['text'] = "Символ больше похож на {}".format(sym)
		self.res_lbl.pack(side=tk.TOP)


	def save_image(self, img) :
		path = fd.asksaveasfilename()
		print(path)
		img.save(path)


	def choose_image(self):
		file_name = fd.askopenfilename()
		if str(file_name) != "":
			self.width = 130
			self.height = 130
			self.img = Image.open(file_name).resize((self.width, self.height), Image.ANTIALIAS)
			self.image = ImageTk.PhotoImage(self.img)
			tk.Label(image = self.image).grid(row = 0, column = 1, rowspan = 5)

	def on_make_black_btn_clicked(self):
		gs = GrayScale(self.img, self.width, self.height)
		gray_type = self.black_var.get()
		self.gray_image = gs.get_gray_image(gray_type)
		self.gray_img = ImageTk.PhotoImage(self.gray_image) 
		tk.Label(image = self.gray_img).grid(row = 0, column = 1, rowspan = 5)
		tk.Button(text='Сохранить', command= lambda : self.save_image(self.gray_image)).place( x = 250, y = 27)


	def on_blur_btn_clicked(self):
		gb = GausBlur(int(self.radius_scale.get()), float(self.sigma_scale.get()))
		
		que = queue.Queue()
		th = Thread(target=gb.get_blur_img, args=[self.gray_image, que])
		th.start()
		th.join()

		self.blur_image = Image.fromarray(que.get())
		self.blur_img = ImageTk.PhotoImage(self.blur_image)
		tk.Label(image=self.blur_img).grid(row=0, column=1, rowspan=5)
		tk.Button(text='Сохранить', command= lambda : self.save_image(self.blur_image)).place( x = 250, y = 27)


	def notmax_suppression(self):
		print(self.gradient_var.get())
		grad = Gradient(self.gradient_var.get())

		grad_matrix, ang_matrix = grad.gradient_analysis(self.blur_image)
		self.notmax_suppr_img = Image.fromarray(grad.notmax_suppression(grad_matrix, ang_matrix))
		self.notmax_suppr_image = ImageTk.PhotoImage(self.notmax_suppr_img)

		tk.Label(image=self.notmax_suppr_image).grid(row=0, column=1, rowspan=5)
		tk.Button(text='Сохранить', command= lambda : self.save_image(self.notmax_suppr_img)).place( x = 250, y = 27)
	

	def double_thresold_filter(self, img, lower_thresold, upper_thresold):
		w, h = img.size

		lower_thresold *= 255
		upper_thresold *= 255

		matrix = np.array(img)
		for x in range(1, w - 1):
			for y in range(1, h - 1):
				if matrix[y][x] >= upper_thresold:
					matrix[y][x] = 255
				elif matrix[y][x] <= lower_thresold:
					matrix[y][x] = 0
				else:
					matrix[y][x] = 127
		return matrix

	def on_filter_btn_clicked(self):
		self.filter_img = Image.fromarray(self.double_thresold_filter(self.notmax_suppr_img, float(self.bot_entry.get()), float(self.top_entry.get())))
		self.filter_image = ImageTk.PhotoImage(self.filter_img)

		tk.Label(image=self.filter_image).grid(row=0, column=1, rowspan=5)
		tk.Button(text='Сохранить', command= lambda : self.save_image(self.filter_img)).place( x = 250, y = 27)
		

if __name__ == "__main__" :
    root = tk.Tk()
    app = Main(root)
    app.grid()
    root.title("Lab4")
    root.geometry("400x600")
    root.mainloop()

	# for i in range(1, 22):
	# 	path = "C:/Users/Тимофей/Desktop/Lab4/db/{}.jpg".format(i)
	# 	width = 130
	# 	height = 130
	# 	img = Image.open(path).resize((width, height), Image.ANTIALIAS)

	# 	gs = GrayScale(img, width, height)
	# 	img = gs.get_gray_image(0)

	# 	gb = GausBlur(3, 3)
	# 	que = queue.Queue()
	# 	gb.get_blur_img(img, que)
	# 	img = Image.fromarray(que.get())

	# 	gr = Gradient(1)
	# 	grad_matrix, ang_matrix = gr.gradient_analysis(img)
	# 	img = Image.fromarray(gr.notmax_suppression(grad_matrix, ang_matrix))

	# 	lower_thresold = 0.02
	# 	upper_thresold = 0.2

	# 	lower_thresold *= 255
	# 	upper_thresold *= 255

	# 	w, h = img.size

	# 	matrix = np.array(img)
	# 	for x in range(1, w - 1):
	# 		for y in range(1, h - 1):
	# 			if matrix[y][x] >= upper_thresold:
	# 				matrix[y][x] = 255
	# 			elif matrix[y][x] <= lower_thresold:
	# 				matrix[y][x] = 0
	# 			else:
	# 				matrix[y][x] = 127

	# 	img = Image.fromarray(matrix.astype(np.uint8))

	# 	img.save(r"C:/Users/Тимофей/Desktop/Lab4/db_1/{}.jpg".format(i))
			

