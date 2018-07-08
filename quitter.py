from tkinter import * # импортировать классы виджетов
from tkinter.messagebox import askokcancel # импортировать стандартный диалог


class Quitter(Frame): # подкласс графич. интерфейса
    def __init__(self, parent=None): # метод конструктора
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Выход', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)
    def quit(self):
        ans = askokcancel('Verify exit', 'Really quit?')
        if ans: Frame.quit(self)

if __name__ == '__main__': Quitter().mainloop()