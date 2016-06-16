import discord
import asyncio
import cleverbot
import re
from kdwcheck import sockcheck

address = '76.77.225.51'
port = 4002
bot = discord.Client()
cleverbot = cleverbot.Cleverbot()

@bot.event
async def on_ready():
    print('Bot Started.')

@bot.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await bot.send_message(server, fmt.format(member, server))

@bot.event
async def on_message(message):
    print(message.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + (message.author.name[:14] + ': ').ljust(15) + message.content)
    if message.author.id != bot.user.id:
        if bot.user.mentioned_in(message):
            bot.send_typing(message.channel)
            cbotmessage = re.sub(r'\<[^>]*\>[ ]', '', message.content)
            cbotreply = cleverbot.ask(cbotmessage)
            fmt = '{0.mention} {1}'
            await bot.send_message(message.channel, fmt.format(message.author, cbotreply))

        if message.content.startswith('!kdwstatus'):
            await bot.send_message(message.channel, sockcheck(address, port, 'KDW'))

        if message.content.startswith('!punch'):
            try:
                punchtarget = message.content.split(' ', 1)[1]
                await bot.send_message(message.channel, 'I am going to punch ' + message.content.split(' ', 1)[1] + '.')
            except:
                await bot.send_message(message.channel, 'I am going to punch someone.')

        if message.content.startswith('!game'):
            try:
                gametarget = message.content.split(' ', 1)[1]
                newGame = discord.Game()
                newGame.name = gametarget
                await bot.change_status(newGame)
            except:
                await bot.change_status()

bot.run('MTkyNzgwOTU2NDY4Mzc5NjQ4.CkN0wQ.8A51zVZjbwBCtqp5WPtHrWVPsuw')
