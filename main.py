import tkinter as tk
from tkinter import ttk
import discord
import datetime
from discord.ext import commands

windows = []
timetable1 = []
timetable2 = []
dayframes = []
cfg = open(r"C:\NTBot\settings.txt", 'r').readlines()
methodsettings = []
def start(): #обновление cfg и основных переменных в соответствии с ним

    global timetable1, timetable2, dayframes, allsubjects, cfg, methodsettings
    timetable1 = []
    timetable2 = []
    dayframes = []
    cfg = open(r"C:\NTBot\settings.txt", 'r').readlines()
    for i in range(len(cfg)):
        cfg[i] = cfg[i].replace('\n', '')
    for i in range(0, (len(cfg) - 9) // 2):
        timetable1.append([])
        timetable2.append([])
        day1 = cfg[9 + i * 2].split(', ')
        for dayn in day1:
            timetable1[i].append(dayn)
        day2 = cfg[10 + i * 2].split(', ')
        for dayn in day2:
            timetable2[i].append(dayn)
    print(timetable1)
    timetable1 = timetable1[1:] + [timetable1[0]]
    timetable2 = timetable2[1:] + [timetable2[0]]
    dayframes = []
    all = cfg[3] + ", " + cfg[4]
    allsubjects = all.split(", ")
    if cfg[5] == "True":
        cfg[5] = True
    elif cfg[5] == "False":
        cfg[5] = False
    print(timetable1)
    print(timetable2)

    # подбор даты завтрашнего дня, расписания на завтрашний день
    date = datetime.datetime.now()
    dayweek = date.weekday()
    print(dayweek)
    if dayweek >= int(cfg[7]) - 1:
        days = 0 - date.weekday()
        if days <= 0:
            days += 7
        tomorrow = date + datetime.timedelta(days)
        methodsettings = [timetable1[-1], tomorrow]
    else:
        tomorrow = date + datetime.timedelta(days=1)
        methodsettings = [timetable1[dayweek], tomorrow]

start()
def mainwindow(): #запуск основного окна
    global windows
    wind = tk.Tk()
    wind.title("NTBot")
    wind.geometry("200x200")
    windows.append(wind)
    label = tk.Label(text="NTBot", font=("Obelix Pro", 20))
    label.pack(fill="x", padx=[20, 20], pady=10)
    btn = tk.Button(text="Запуск",command=startbot)
    btn.pack(fill="x", padx=[20, 20], pady=10)
    btn = tk.Button(text="Одиночный запуск", command=single)
    btn.pack(fill="x", padx=[20, 20], pady=10)
    btn = tk.Button(text="Настройки", command=settings)
    btn.pack(fill="x", padx=[20, 20], pady=10)
    wind.mainloop()

def settings(): #запуск окна настроек
    global cfg, windows
    root = tk.Tk()
    root.title("НАСТРОЙКИ")
    root.geometry("316x800")
    windows.append(root)
    class customframeentry: #поле ввода с подписью
        def __init__(self, label_text, insert, scrollneeded, place):
            self.label_text = label_text
            self.insert = insert
            frame = tk.Frame(place, borderwidth=1, relief='solid', padx=6, pady=10)
            label = tk.Label(frame, text=label_text)
            label.pack(anchor='nw')
            self.entry = tk.Entry(frame)
            self.entry.pack(anchor='nw', fill='x')
            self.entry.insert(0, insert)
            if scrollneeded:
                scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.entry.xview)
                scrollbar.pack(anchor="nw", fill="x")
                self.entry["xscrollcommand"] = scrollbar.set
            frame.pack(fill="x", anchor='nw', padx=5, pady=5)

    class customframecheckbox: #галочка с подписью
        def __init__(self, label_text, value, place):
            self.label_text = label_text
            self.value = tk.IntVar()
            self.value1 = False
            frame = tk.Frame(place, borderwidth=1, relief='solid', padx=6, pady=10)
            label = tk.Label(frame, text=label_text)
            label.pack(anchor='nw')
            checkbutton = tk.Checkbutton(frame, variable=self.value, text='hth',command=self.switch)
            checkbutton.pack(anchor='nw')
            if value:
                checkbutton.select()
                self.switch()
            frame.pack(fill="x",anchor='nw', padx=5, pady=5)

        def switch(self):
            self.value1 = not(self.value1)
    class dayframe:
        global allsubjects
        def __init__(self, countofsubjects, column, place, timetable1, timetable2, checkbox, countofdays):
            if checkbox.value1 == 0:
                day = tk.Label(place, text=f'День {column + 1}')
                day.grid(row=0, column=column, padx=4, pady=4)
                self.entries1 = []
                for i in range(countofsubjects):
                    entry = ttk.Combobox(place, values=allsubjects)
                    entry.grid(row=i + 1, column=column, padx=4, pady=4)
                    if 0 <= i < len(timetable1):
                        entry.insert(0, timetable1[i])
                    self.entries1.append(entry)
                    self.entries2 = self.entries1

            else:
                week = tk.Label(place, text=f'Чётная неделя')
                week.grid(row=0, column=int(countofdays) // 2, padx=4, pady=4)
                day = tk.Label(place, text=f'День {column + 1}')
                day.grid(row=1, column=column, padx=4, pady=4)
                self.entries1 = []
                for i in range(countofsubjects):
                    entry = ttk.Combobox(place, values=allsubjects)
                    entry.grid(row=i + 2, column=column, padx=4, pady=4)
                    if 0 <= i < len(timetable1):
                        entry.insert(0, timetable1[i])
                    self.entries1.append(entry)
                week = tk.Label(place, text=f'Нечётная неделя')
                week.grid(row=countofsubjects + 2, column=int(countofdays) // 2, padx=4, pady=4)
                self.entries2 = []
                for i in range(countofsubjects):
                    entry = ttk.Combobox(place, values=allsubjects)
                    entry.grid(row=i + countofsubjects + 3, column=column, padx=4, pady=4)
                    if 0 <= i < len(timetable2):
                        entry.insert(0, timetable2[i])
                    self.entries2.append(entry)

    def save(): #перезапись txt файла на основе cfg
        print(cfg)
        cfg[0] = bottoken.entry.get()
        cfg[1] = id1_frame.entry.get()
        cfg[2] = id2_frame.entry.get()
        cfg[3] = basea.entry.get()
        cfg[4] = baseb.entry.get()
        print(timetableconst.value1)
        cfg[5] = str(timetableconst.value1)
        print(cfg[5])
        cfg[6] = countofsubjects.entry.get()
        cfg[7] = countofdays.entry.get()
        cfg[8] = cfg[8]
        for e in range(len(cfg)):
            cfg[e] = cfg[e] + '\n'
        out = open(r"C:\NTBot\settings.txt", 'w')
        print(cfg)
        out.writelines(cfg)
        out.close()
        start()

    class timetablewindow(): #окно настройки расписания
        def __init__(self):
            global dayframes
            days = int(countofdays.entry.get())
            self.window = tk.Tk()
            self.window.title("ТАБЛИЦА РАСПИСАНИЯ")
            def disable_event():
                pass
            self.window.protocol("WM_DELETE_WINDOW", disable_event)
            windowwidth = round(151 * days)
            windowheight = round(31 * (int(countofsubjects.entry.get()) + 2))
            if not(timetableconst.value1):
                self.window.geometry(f"{windowwidth}x{windowheight}")
            else:
                self.window.geometry(f"{windowwidth}x{windowheight * 2}")
            for c in range(days):
                tt1 = []
                tt2 = []
                if c == 0:
                    tt1 = timetable1[len(timetable1) - 1]
                    tt2 = timetable2[len(timetable2) - 1]
                elif c <= len(timetable1) - 1:
                    tt1 = timetable1[c - 1]
                    tt2 = timetable2[c - 1]
                dayframes.append(dayframe(int(countofsubjects.entry.get()), c, self.window, tt1, tt2, timetableconst,
                                          countofdays.entry.get()))
                savebtn = tk.Button(self.window, text="Применить", command=self.savetimetable)
                cancelbtn = tk.Button(self.window, text="Отмена", command=self.closetimetable)
                if not timetableconst.value1:
                    savebtn.grid(row=int(countofsubjects.entry.get()) + 1, column=int(countofdays.entry.get()) - 1,
                                 padx=4, pady=4)
                    cancelbtn.grid(row=int(countofsubjects.entry.get()) + 1, column=int(countofdays.entry.get()) - 2,
                                 padx=4, pady=4)
                else:
                    savebtn.grid(row=int(countofsubjects.entry.get()) * 2 + 3, column=int(countofdays.entry.get()) - 1,
                                 padx=4, pady=4)
                    cancelbtn.grid(row=int(countofsubjects.entry.get()) * 2 + 3, column=int(countofdays.entry.get()) - 2,
                                 padx=4, pady=4)
            self.window.mainloop()

        def closetimetable(self): #адекватное закрытие окна расписания
            for frame in dayframes:
                for entr in frame.entries1:
                    entr.destroy()
                for entr in frame.entries2:
                    entr.destroy()
            self.window.destroy()
            dayframes.clear()

        def savetimetable(self): #запись расписания в cfg
            global dayframes
            for i in range(len(dayframes)):
                single1 = []
                single2 = []
                singlestr1 = ''
                singlestr2 = ''
                for n in range(len(dayframes[i].entries1)):
                    single1.append(dayframes[i].entries1[n].get())
                    single2.append(dayframes[i].entries2[n].get())
                    singlestr1 += single1[n]
                    singlestr2 += single2[n]
                    if not single1[n] == '':
                        singlestr1 += ', '
                    if not single2[n] == '':
                        singlestr2 += ', '
                cfg[9 + i * 2] = singlestr1
                cfg[10 + i * 2] = singlestr2

            self.closetimetable()

    titletext = tk.Label(root, text="НАСТРОЙКИ", font=("Obelix Pro", 30))
    titletext.pack()

    bottoken = customframeentry("Токен бота", cfg[0], False, root)
    id1_frame = customframeentry("ID канала с базой заданий", cfg[1], False, root)
    id2_frame = customframeentry("ID канала для отправки", cfg[2], False, root)
    basea = customframeentry("Предметы с заданиями (через запятую с пробелами)", cfg[3], True, root)
    baseb = customframeentry("Предметы без заданий (через запятую с пробелами)", cfg[4], True, root)
    timetableconst = customframecheckbox("Расписание меняется?", cfg[5], root)
    countofsubjects = customframeentry('Максимальное количество предметов в день', cfg[6], False, root)
    countofdays = customframeentry("Количество дней недели", cfg[7], False, root)

    btn1 = tk.Button(root, text="Обновить таблицу", command=timetablewindow)
    btn1.pack(anchor='nw', padx=6, pady=6)

    btn2 = tk.Button(root, text="Сохранить настройки", command=save)
    btn2.pack(anchor='center', padx=6, pady=6)

    label = tk.Label(root)
    label.pack(anchor='nw', padx=6, pady=6)

    def test():
        print(timetableconst.value1)

    check = tk.Button(root, text="ТЕСТ", command=test)
    check.pack(anchor='center', padx=6, pady=6)
def single(): #вывод окна единичной отправки
    global windows
    singlewindow = tk.Tk()
    singlewindow.title("Единичная отправка")
    singlewindow.geometry(f"155x{40 * (int(cfg[7]) + 2)}")
    windows.append(singlewindow)
    day = tk.Label(singlewindow, text=f'Единичная отправка')
    day.grid(row=0, column=0, padx=6, pady=6)
    entries = []
    count = int(cfg[6])
    for i in range(count):
        entry = ttk.Combobox(singlewindow, values=allsubjects)
        entry.grid(row=i + 1, column=0, padx=4, pady=4)
        entries.append(entry)
    singletimetable = []
    def letsgo(): #запуск одиночного запуска
        for i in range(len(entries)):
            singletimetable.append(entries[i].get())
            print(singletimetable)
        methodsettings[0] = singletimetable
        startbot()
    btn = tk.Button(singlewindow,text="Поехали!", command=letsgo)
    btn.grid(row=count+3,column=0, padx=6, pady=6)

    singlewindow.mainloop()

def replace_line(line_num, text, txt): #замена строки
    lines = open(txt, 'r').readlines()
    lines[line_num] = text
    out = open(txt, 'w')
    out.writelines(lines)
    out.close()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event
async def on_ready(): #основной алгоритм для
    bazalines = cfg[3].split(', ') + cfg[4].split(', ')
    yesterday = []
    for i in range(0, 100):
        bazalines.append('')
        yesterday.append('')
    channel1id = int(cfg[1])
    channel2id = int(cfg[2])
    settings = methodsettings
    print(settings)
    async def yesterdayprocessing():
        yesterdaystrings = ''
        channel = bot.get_channel(channel1id)
        for thread in channel.threads:
            print(thread.name)
            async for message in thread.history():
                if message.attachments:
                    task = f"{message.content} ((Задание на картинке, переходи в ветку)) (<#{str(thread.id)}>)"
                else:
                    task = f'{message.content} (<#{str(thread.id)}>)'
                print(message.content)
                for i in range(len(allsubjects)):
                    subjname = allsubjects[i]
                    if subjname in message.content:
                        bazalines[i] = task
        yesterday[0] = f"Задание на {settings[1].strftime('%d.%m')}:\n"
        for i in range(len(allsubjects)):
            if allsubjects[i] in settings[0]:
                if settings[0].count(allsubjects[i]) > 1:
                    yesterday[settings[0].index(allsubjects[i], settings[0].index(allsubjects[i]) + 1) + 1] = f'{str(settings[0].index(allsubjects[i]) + 1)}. {bazalines[i]} \n'
                yesterday[settings[0].index(allsubjects[i]) + 1] = f'{str(settings[0].index(allsubjects[i]) + 1)}. {bazalines[i]} \n'
                print(yesterday)
        channel = bot.get_channel(channel2id)
        print(yesterday)
        for string in yesterday:
            yesterdaystrings += string
        await channel.send(yesterdaystrings)
    await yesterdayprocessing()

def startbot(): #тупо старт бота
    global windows
    for window in windows:
        window.destroy()
    bot.run(cfg[0])
mainwindow()




