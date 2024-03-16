import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f'{bot.user.name} запустился и готов к работе!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        print(message)
        print(f'Получено сообщение! Текст: {message.content}, Сервер: {message.guild}, Автор: {message.author}, {message.channel}')
    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send('Успешный тест!')

@bot.command()
async def spam(ctx, number: int, member):
    for i in range(0,number):
        await ctx.send(str(member))

@bot.command()
async def nap(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def history1(ctx):
    print(ctx.channel.name)
    async for message in ctx.channel.history(limit = 100):
        print(message.content)

@bot.command()
async def history2(ctx):
    for channel in ctx.guild.channels:
        async for message in channel.history(limit = 100):
            print(message.content)

@bot.command()
async def a(ctx):
    for channel in ctx.guild.channels:
        print("Id сервера",ctx.guild.id)
        print(channel.name,channel.id)


@bot.command()
async def history3(ctx):
    f = open('база.txt', 'w')
    for channel in bot.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            for thread in channel.threads:
                print(thread.name)
                f.write(thread.name)
                f.write("\n")
                async for message in thread.history():
                    print(message.content)
                    f.write(message.content)
                    f.write("\n")
    f.close()

bot.run('')