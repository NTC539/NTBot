import discord
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


timetable = [['ОБЖ','Исто','Физ-ра','Биол','Алге','Веро','Обще'],
             ['Алге','Физ-ра','Физи','Обще','Лите','Англ','Геом'],
             ['Русс','Хими','Исто','Русс','Лите','Англ','Индивидуальный проект'],
             ['Обще','Геог','Физи','Геом','Алге','Инфо','Англ'],
             ['Разговоры о важном','Физ-ра','Обще','Русс','Геом','Лите','Алге']]
baza = ['Русс','Лите','Алге','Геом','Инфо','Обще','Англ','Биол','Хими','Исто','Физи','Геог','ОБЖ','Веро']

def replace_line(line_num, text, txt):
    lines = open(txt, 'r').readlines()
    lines[line_num] = text
    out = open(txt, 'w')
    out.writelines(lines)
    out.close()

async def send(txt):
    baza = open(txt, 'r')
    channel = bot.get_channel(1156612750945026089)
    bazafile = baza.read()
    await channel.send(bazafile)

def replace():
    txt = 'дзназавтра.txt'
    file = open('база.txt', 'r')
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
    replace_line(0,f"Задание на {tomorrow.strftime('%d.%m')}:\n",txt)
    for i in range(0, 14):
        if baza[i] in currentbaza:
            if currentbaza.count(baza[i]) > 1:
                replace_line(currentbaza.index(baza[i],currentbaza.index(baza[i])+1)+1,str(currentbaza.index(baza[i])+1)+". "+bazalines[i], txt)
            replace_line(currentbaza.index(baza[i])+1,str(currentbaza.index(baza[i])+1)+". "+bazalines[i], txt)
        else:
            for a in currentbaza:
                if a not in baza:
                    missing = a
                    replace_line(currentbaza.index(missing)+1,f'{(currentbaza.index(missing)+1)}. {missing}\n',txt)

@bot.event
async def on_ready():
    channel = bot.get_channel(968476610435088441)
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
                    if subjname == baza[i]:
                        replace_line(i,task,'база.txt')
    replace()
    await send('дзназавтра.txt')

bot.run('')
