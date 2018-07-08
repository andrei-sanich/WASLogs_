import os, fnmatch, time, re
from collections import Counter
from tkinter import *
from tkinter import filedialog
from quitter import Quitter
from scrolledtext import ScrolledText



class StatLogs(ScrolledText):


    def __init__(self, parent=None, file=None):

        
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text="Выбрать каталог с логами", command=self.onStat).pack(side=LEFT)
        Button(frm, text='Сохранить', command=self.onSave).pack(side=LEFT)
        Quitter(frm).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file)
        self.text.config(font=('courier', 9, 'normal'))

        self.pattern_SQL = r'SQLCODE=-[0-9][0-9][0-9]'
        self.pattern_E = r'\s[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]E'
        self.pattern_JMS = r'JMS\w{1,6}\d{4}'

        self.types_of_stat = ['Сообщения об ошибках', 'Сообщения JMS', 'Сообщения DB2']


    def onSave(self):

        filename = filedialog.asksaveasfilename(filetypes=[('TXT', ".txt")],
                                            defaultextension=".txt")
        if filename:
            alltext = self.gettext() # от начала до конца
            open(filename, 'w').write(alltext) # сохранить текст в файл


    def onStat(self):
        self.text.delete('0.0','end')
        directory = filedialog.askdirectory()
    
        SystemOuts = self.get_files(directory, 'SystemOut*.log')
        ffdcs = self.get_files(directory, 'server*.txt')
        activeSystemOut = self.get_activelogfile(SystemOuts, '*SystemOut.log')

        period_SystemOut = self.get_period(SystemOuts)
        period_ffdc = self.get_period(ffdcs)

        stat_activeSystemOut = [x for x in self.get_amounts(self.get_data(activeSystemOut))]
        stat_SystemOuts = [x for x in self.get_amounts(self.get_data(SystemOuts))]
        stat_ffdc = [x for x in self.get_amounts(self.get_data(ffdcs))]

        self.text.insert(END,'_____________________________________________\n')
        self.text.insert(END,'Статистика по самому свежему логу SystemOut \n')
        for active_stat, all_stat, type_of_stat in zip(stat_activeSystemOut,
                                                   stat_SystemOuts,
                                                   self.types_of_stat):
            if active_stat and all_stat:
                self.text.insert(END, type_of_stat + ':\n')
                self.out_activelog(active_stat, all_stat)    
            else:
                self.text.insert(END, type_of_stat + ' отсутствуют \n\n')
        self.text.insert(END,'_____________________________________________\n')
        self.text.insert(END,'Статистика по всем логам SystemOut \n')
        self.text.insert(END, self.period_text(period_SystemOut[0], period_SystemOut[1]))
        self.output_stat(stat_SystemOuts)
        self.text.insert(END,'_____________________________________________\n')
        self.text.insert(END,'Статистика по логам из каталога FFDC \n')
        self.text.insert(END, self.period_text(period_ffdc[0], period_ffdc[1]))
        self.output_stat(stat_ffdc)

    
    def get_files(self, directory, pattern):
    
        logfiles = []
    
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                logfiles.append(os.path.join(root, filename))
    
        return logfiles


    
    def get_activelogfile(self, SystemOuts, pattern):
    
        return [filename for filename in fnmatch.filter(SystemOuts, pattern)]   


    def get_period(self, logfiles):
   
        if logfiles:
            date_list = [[x, os.path.getmtime(x)] for x in logfiles]
            sort_date_list = sorted(date_list, key=lambda x: x[1], reverse=True)
            start = time.ctime(sort_date_list[-1][1])
            end = time.ctime(sort_date_list[0][1])

        return start, end


    def period_text(self, start, end):    
    
        return "Период: {} - {} \n\n".format(start, end)

    
    def get_data(self, logfiles):
    
        if logfiles:

            errors = []
            msgs_jms = []
            sqlcodes = []

            for file in logfiles:
                errors.extend(self.parse_file(file, self.pattern_E))
                msgs_jms.extend(self.parse_file(file, self.pattern_JMS))
                sqlcodes.extend(self.parse_file(file, self.pattern_SQL))

        data = [errors, msgs_jms, sqlcodes]

        return data

   
    def parse_file(self, file, pattern):
    
        data = open(file).read()
        text = re.findall(pattern, data)
    
        return text

    
    def get_amounts(self, msgs):
    
        return [Counter(x).most_common(20) for x in msgs]      
    

    def get_ratio(self, part, all):
    
        return  str(round(int(part)/int(all)*100))
    

    def out_activelog(self, active_stat, all_stat):        
    
        for key, value in active_stat:
            for key2, value2 in all_stat:
                if key == key2:
                    text = "{} - {} ({}%) \n".format(str(key),
                                                 str(value),
                                                 self.get_ratio(value, value2))
                    self.text.insert(END, text)
        self.text.insert(END, '\n')    

    
    def output_stat(self, stats): 
    
        for stat, type_of_stat in zip(stats, self.types_of_stat):
            if stat:
                self.text.insert(END, type_of_stat + ':\n')
                self.out(stat)    
            else:
                self.text.insert(END, type_of_stat + ' отсутствуют \n\n')    


    def out(self, stat):        
    
        for key, value in stat:
            text = "{} - {} \n".format(str(key), str(value))
            self.text.insert(END, text)
        self.text.insert(END, '\n')         
    

if __name__ == '__main__':

    if len(sys.argv) > 1:
        StatLogs(file=sys.argv[1]).mainloop() # имя файла в ком. строке
    else:
        StatLogs().mainloop()