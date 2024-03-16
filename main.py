import discord
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

basea = ['Русс','Лите','Алге','Геом','Инфо','Обще','Англ','Биол','Хими','Исто','Физи','Геог','ОБЖ','Веро']
baseb = ['Физкультура','Разговоры о важном','Индивидуальный проект']
timetable = [[],[],[],[],[]]
baseaddress = r"C:\Program Files (x86)\NTBot\baza.txt"
yesterdayaddress = r"C:\Program Files (x86)\NTBot\yesterday.txt"

cfg = open(r"C:\Program Files (x86)\NTBot\settings.txt", 'r').readlines()
for i in range(0,5):
    day = cfg[i + 2].split(', ')
    for n in range(0,7):
        subjname = ''
        for symb in day[n]:
            a = 0
            if a < 4:
                subjname += symb
                a += 1
            if subjname in basea:
                timetable[i].append(subjname)
                break
            elif day[n] in baseb:
                timetable[i].append(day[n])
                break
timetable = timetable[1:] + [timetable[0]]
print(timetable)
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

def replace():
    file = open(baseaddress, 'r')
    bazalines = file.readlines()
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
    replace_line(0,f"Задание на {tomorrow.strftime('%d.%m')}:\n",yesterdayaddress)
    for i in range(0, 14):
        if basea[i] in currentbaza:
            if currentbaza.count(basea[i]) > 1:
                replace_line(currentbaza.index(basea[i],currentbaza.index(basea[i])+1)+1,str(currentbaza.index(basea[i])+1)+". "+bazalines[i], yesterdayaddress)
            replace_line(currentbaza.index(basea[i])+1,str(currentbaza.index(basea[i])+1)+". "+bazalines[i], yesterdayaddress)
        else:
            for a in currentbaza:
                if a not in basea:
                    missing = a
                    replace_line(currentbaza.index(missing)+1,f'{(currentbaza.index(missing)+1)}. {missing}\n',yesterdayaddress)

@bot.event
async def on_ready():
    channel = bot.get_channel(channel1id)
    for thread in channel.threads:
        print(thread.name)
        async for message in thread.history():
            if message.attachments:
                task = f"{message.content} ((Задание на картинке, переходи в ветку)) (<#{str(thread.id)}>)\n"
            else:
                task = f'{message.content} (<#{str(thread.id)}>)\n'
            subjname = ''
            n = 0
            print(message.content)
            for symb in message.content:
                if n < 4:
                    subjname += symb
                    n += 1
                for i in range(0,14):
                    if subjname == basea[i]:
                        replace_line(i,task,baseaddress)
    replace()
    await send(yesterdayaddress)

bot.run('')

