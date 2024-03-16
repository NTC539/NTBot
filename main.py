import discord
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f'{bot.user.name} запустился и готов к работе!')

monday = ['Разговоры о важном','Физра','Обще','Русс','Геом','Лите','Алге']
tuesday = ['ОБЖ','Исто','Физра','Биол','Алге','Веро','Обще']
wednesday = ['Алге','Физра','Физи','Обще','Лите','Англ','Геом']
thursday = ['Русс','Хими','Исто','Русс','Лите','Англ','Индивидуальный проект']
friday = ['Обще','Геог','Физи','Геом','Алге','Инфо','Англ']
baza = ['Русс','Лите','Алге','Геом','Инфо','Обще','Англ','Биол','Хими','Исто','Физи','Геог','ОБЖ','Веро']

def replace_line(line_num, text, txt):
    lines = open(txt, 'r').readlines()
    lines[line_num] = text
    out = open(txt, 'w')
    out.writelines(lines)
    out.close()

async def senddz(txt):
    baza = open(txt, 'r')
    channel = bot.get_channel(1156612750945026089)
    bazafile = baza.read()
    await channel.send(bazafile)

def replace(currentbaza,txt,bazalines):
    for i in range(0, 14):
        if baza[i] in currentbaza:
            print(baza[i])
            replace_line(currentbaza.index(baza[i]), bazalines[i], txt)
        else:
            print(baza[i])

@bot.command()
async def база(message):
    channel = bot.get_channel(968476610435088441)
    for thread in channel.threads:
        print(thread.name)
        async for message in thread.history():
            if message.attachments:
                task=f"{message.content} ((Задание на картинке, переходи в ветку)) (<#{str(thread.id)}>)\n"
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
    file = open('база.txt', 'r')
    bazalines = file.readlines()
    date = datetime.datetime.now()
    dayweek = date.weekday()
    if dayweek == 0:
        replace(tuesday, 'Вторник.txt', bazalines)
        await senddz('Вторник.txt')
    elif dayweek == 1:
        replace(wednesday, "Среда.txt", bazalines)
        await senddz("Среда.txt")
    elif dayweek == 2:
        replace(thursday, "Четверг.txt", bazalines)
        await senddz("Четверг.txt")
    elif dayweek == 3:
        replace(friday, "Пятница.txt", bazalines)
        await senddz("Пятница.txt")
    else:
        replace(monday, 'Понедельник.txt', bazalines)
        await senddz('Понедельник.txt')


bot.run('')

