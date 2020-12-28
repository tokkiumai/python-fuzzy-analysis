import mysql.connector as connector
from pyswip import Prolog

import random
import numpy
import tkinter as tk
import requests


class Main(tk.Frame):
    mydb = connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prologdb",
        auth_plugin='mysql_native_password'
    )

    prolog = Prolog()
    prolog.consult("./ind2.pl")

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        self.label_firstTeamWin = tk.Label(
            text="Победы первой команды:", font="times 12")
        self.label_firstTeamWin.place(relx=0.05, rely=0.01)

        self.entry_firstTeamWin = tk.Entry(
            width=20, font="times 12", justify="c")
        self.entry_firstTeamWin.place(relx=0.05, rely=0.08)

        self.label_firstTeamWeak = tk.Label(
            text="Больные первой команды:", font="times 12")
        self.label_firstTeamWeak.place(relx=0.05, rely=0.16)

        self.entry_firstTeamWeak = tk.Entry(
            width=20, font="times 12", justify="c")
        self.entry_firstTeamWeak.place(relx=0.05, rely=0.22)

        self.label_resTT = tk.Label(
            text="Победы между командами:", font="times 12")
        self.label_resTT.place(relx=0.05, rely=0.3)

        self.entry_resTT = tk.Entry(width=20, font="times 12", justify="c")
        self.entry_resTT.place(relx=0.05, rely=0.36)

        self.label_secondTeamWin = tk.Label(
            text="Победы второй команды:", font="times 12")
        self.label_secondTeamWin.place(relx=0.05, rely=0.44)

        self.entry_secondTeamWin = tk.Entry(
            width=20, font="times 12", justify="c")
        self.entry_secondTeamWin.place(relx=0.05, rely=0.5)

        self.label_secondTeamWeak = tk.Label(
            text="Больные второй команды:", font="times 12")
        self.label_secondTeamWeak.place(relx=0.05, rely=0.56)

        self.entry_secondTeamWeak = tk.Entry(
            width=20, font="times 12", justify="c")
        self.entry_secondTeamWeak.place(relx=0.05, rely=0.64)

        self.label_db = tk.Label(text="Данные в базе:", font="times 12")
        self.label_db.place(relx=0.6, rely=0.01)

        self.listbox = tk.Listbox(root)
        self.listbox.place(relx=0.6, rely=0.08)

        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.text = tk.StringVar()
        self.label_qtyFunc = tk.Label(textvariable=self.text, font="times 12")
        self.label_qtyFunc.place(relx=0.05, rely=0.8)

        btn_apply = tk.Button(text="Результат", font="times 12", width=12)
        btn_apply.place(relx=0.6, rely=0.5)
        btn_apply.bind('<Button-1>', lambda event: self.calculate(self.entry_firstTeamWin.get(), self.entry_firstTeamWeak.get(), self.entry_resTT.get(),
                                                                  self.entry_secondTeamWin.get(), self.entry_secondTeamWeak.get()))

    def solution(self, x, Mx, TgX, y, My, TgY, R, z, Mz, TgZ, x1, y1):
        try:
            URL = f'http://localhost:4040'
            PARAMS = {
                'x': x,
                'y': y,
                'z': z,
                'x1': x1,
                'y1': y1,
                'mx': Mx,
                'my': My,
                'mz': Mz,
                'tgx': TgX,
                'tgy': TgY,
                'tgz': TgZ,
                'ry': R
            }
            res = requests.get(url=URL, params=PARAMS)
            data = res.json()
            return data

        except:
            return {
                'status': False,
                'message': 'Getting personality type failed'
            }

    def calculate(self, x1, y1, z, x2, y2):
        item1 = (x1, y1, z)
        item2 = (x2, y2, z)

        cursor = self.mydb.cursor()

        query = "INSERT INTO testdb.fuzzy VALUES (null, %s, %s, %s)"
        cursor.execute(query, item1)
        cursor.execute(query, item2)

        cursor.execute("SELECT * FROM testdb.fuzzy;")
        data = cursor.fetchall()
        self.mydb.commit()

        Mx = 0
        My = 0
        Mz = 0
        x_data = list()
        y_data = list()
        z_data = list()

        for item in data:
            Mx += item[1]
            My += item[2]
            Mz += item[3]

            st = "X={}, Y={}, Z={}".format(item[1], item[2], item[3])
            self.listbox.insert(tk.END, st)

            x_data.append(item[1])
            y_data.append(item[2])
            z_data.append(item[3])

        count = len(data)

        Mx = round(Mx/count)
        My = round(My/count)
        Mz = round(Mz/count)

        sigmaX = numpy.std(x_data)
        sigmaY = numpy.std(y_data)
        sigmaZ = numpy.std(z_data)

        TgX = 1/sigmaX
        TgY = 1/sigmaY
        TgZ = 1/sigmaZ
        R = sigmaY/2
        print(item1[0], item1[1], item1[2], item2[0], item2[1])

        data = self.solution(
            item1[0], Mx, TgX, item1[1], My, TgY, R, item1[2], Mz, TgZ, item2[0], item2[1])
        if (data['type'] == 0):
            value = "Результат: победа первой команды"
        elif (data['type'] == 1):
            value = "Результат: ничья"
        else:
            value = "Результат: победа второй команды"
        self.text.set(value)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("XNJ")
    root.geometry("500x400+150+50")
    root.mainloop()
