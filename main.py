
import discord
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
timetablefull = []
timetable = []
basea = ['Русс','Лите','Алге','Геом','Инфо','Обще','Англ','Биол','Хими','Исто','Физи','Геог','ОБЖ','Веро']
baseb = ['Физкультура','Разговоры о важном','Индивидуальный проект']
bazalines = ['Русский язык','Литература','Алгебра','Геометрия','Информатика','Обществознание','Английский язык','Биология','Химия','История','Физика','География','ОБЖ','Вероятность и статистика']
yesterday = []
yesterdaystrings = ''
cfg = open(r"C:\NTBot\settings.txt", 'r').readlines()
countofsubjects = int(cfg[2])
for i in range(0,100):
    bazalines.append('')
    yesterday.append('')
for i in range(0,countofsubjects):
    timetablefull.append([])
    timetable.append([])
    day = cfg[i + 3].split(', ')
    n = -1
    for dayn in day:
        n += 1
        subjname = ''
        for symb in dayn:
            a = 0
            if a < 4:
                subjname += symb
                a += 1
            if subjname in basea:
                timetablefull[i].append(dayn)
                timetable[i].append(subjname)
                break
            elif day[n] in baseb:
                timetable[i].append(dayn)
                timetablefull[i].append(dayn)
                break
timetable = timetable[1:] + [timetable[0]]
print(timetable)
print(timetablefull )
channel1id = int(cfg[0])
channel2id = int(cfg[1])

def replace_line(line_num, text, txt):
    lines = open(txt, 'r').readlines()
    lines[line_num] = text
    out = open(txt, 'w')
    out.writelines(lines)
    out.close()

async def send(txt):
    baza = open(txt, 'r')
    channel = bot.get_channel(channel2id)
    bazafile = baza.read()
    await channel.send(bazafile)

def processing():
    global yesterday, yesterdaystrings
    for string in yesterday:
        yesterdaystrings += string
def replace():
    date = datetime.datetime.now()
    dayweek = date.weekday()
    if dayweek >= 4:
        currentbaza = timetable[4]
        days = 0 - date.weekday()
        if days <= 0:
            days += 7
        tomorrow = date + datetime.timedelta(days)
    else:
        currentbaza = timetable[dayweek]
        tomorrow = date + datetime.timedelta(days=1)
    yesterday[0] = f"Задание на {tomorrow.strftime('%d.%m')}:\n"
    for i in range(0, 14):
        if basea[i] in currentbaza:
            if currentbaza.count(basea[i]) > 1:
                yesterday[currentbaza.index(basea[i],currentbaza.index(basea[i])+1)+1] = f'{str(currentbaza.index(basea[i])+1)}. {bazalines[i]} \n'
            yesterday[currentbaza.index(basea[i])+1] = f'{str(currentbaza.index(basea[i])+1)}. {bazalines[i]} \n'
        else:
            for missing in currentbaza:
                if missing in baseb:
                    yesterday[currentbaza.index(missing)+1] = f'{(currentbaza.index(missing)+1)}. {missing}\n'

@bot.event
async def on_ready():
    channel = bot.get_channel(channel1id)
    for thread in channel.threads:
        print(thread.name)
        async for message in thread.history():
            if message.attachments:
                task = f"{message.content} ((Задание на картинке, переходи в ветку)) (<#{str(thread.id)}>)"
            else:
                task = f'{message.content} (<#{str(thread.id)}>)'
            subjname = ''
            n = 0
            print(message.content)
            for symb in message.content:
                if n < 4:
                    subjname += symb
                    n += 1
                for i in range(0,14):
                    if subjname == basea[i]:
                        bazalines[i] = task
    replace()
    channel = bot.get_channel(channel2id)
    print(yesterday)
    print(yesterdaystrings)
    processing()
    await channel.send(yesterdaystrings)

bot.run('')