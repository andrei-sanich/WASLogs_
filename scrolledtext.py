from tkinter import *


class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH) # сделать растягиваемым
        self.makewidgets()

    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview) # связать sbar и text
        text.config(yscrollcommand=sbar.set) # сдвиг одного = сдвиг другого
        sbar.pack(side=RIGHT, fill=Y) # первым добавлен - посл. обрезан
        text.pack(side=LEFT, expand=YES, fill=BOTH) # Text обрезается первым
        self.text = text

    def gettext(self): # возвращает строку
         return self.text.get('1.0', END+'-1c') # от начала до конца

if __name__ == '__main__':
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1]) # имя файла в командной строке
    else:
        st = ScrolledText(text='Words\ngo here') # иначе: две строки
    def show(event):
        print(repr(st.gettext())) # вывести как простую строку
    root.bind('<Key-Escape>', show) # esc = выводит дамп текста
    root.mainloop()