import discord
import asyncio
import time
import datetime

import chatbot
import kdw
import ystock
import overwatch

address = '76.77.225.51'
port = 4002
bot = discord.Client()
defaultGame = discord.Game()
defaultGame.name = "Kirby's Dream World"
catid = '132072321421672448'

@bot.event
async def on_ready():

    #setup bot
    await bot.change_status(defaultGame)
    print('Bot Started.')


@bot.event
async def on_member_join(member):

    #welcome message
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await bot.send_typing(message.server)
    time.sleep(0.750)
    await bot.send_message(server, fmt.format(member, server))

@bot.event
async def on_message(message):

    #message log
    print(message.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + (message.author.name[:13] + ': ').ljust(15) + message.content)
    
    #don't respond to self
    if message.author.id == bot.user.id:
        return

    #cleverbot
    if bot.user.mentioned_in(message):
        await bot.send_typing(message.channel)
        time.sleep(0.750)
        fmt = '{0.mention} {1}'
        await bot.send_message(message.channel, fmt.format(message.author, chatbot.message(message.content)))
        return
    
    #command list
    if message.content.startswith('!help'):
        await bot.send_typing(message.channel)
        time.sleep(0.750)
        await bot.send_message(message.channel,"I'm ChuChu, here's a list of what I can do:")
        await bot.send_typing(message.channel)
        time.sleep(1.5)
        await bot.send_message(message.channel,
            "```\n"
            "@ChuChu              - I can respond to mentions.\n"
            "!help                - Display this message.\n"
            "!punch [person]      - Punch the person specified.\n"
            "!stock [symbol]      - Get the price of a stock.\n"
            "!kdwstatus           - Check if KDW is online.\n"
            "!ow [username]       - Get general Overwatch stats.\n"
            "!owheroes [username] - Get top 5 Overwatch heroes.\n"
            "```"
        )
        return

    #check if kdw online
    if message.content.startswith('!kdwstatus'):
        await bot.send_typing(message.channel)
        time.sleep(0.750)
        await bot.send_message(message.channel, kdw.status(address, port))
        return

    #punch someone
    if message.content.startswith('!punch'):
        await bot.send_typing(message.channel)
        time.sleep(0.750)
        try:
            punchtarget = message.content.split(' ', 1)[1]
            await bot.send_message(message.channel, 'I am going to punch ' + message.content.split(' ', 1)[1] + '.')
        except:
            await bot.send_message(message.channel, 'I am going to punch someone.')
        return

    #get stock prices
    if message.content.startswith('!stock'):
        await bot.send_typing(message.channel)
        time.sleep(0.750)
        try:
            stock = message.content.split(' ', 1)[1]
            await bot.send_message(message.channel,
                "```\n" +
                "Stock Information for {0}\n".format(ystock.get_name(stock)) +
                "  Price:   {0}\n".format(ystock.get_price(stock)) +
                "  Open:    {0}\n".format(ystock.get_open(stock)) +
                "  High:    {0}\n".format(ystock.get_high(stock)) +
                "  Low:     {0}\n".format(ystock.get_low(stock)) +
                "  Volume:  {0}\n".format(ystock.get_vol(stock)) +
                "```"
            )
        except:
            await bot.send_message(message.channel, 'You must provide a stock symbol.')
        return

    #ow top heroes
    if message.content.startswith('!owheroes'):
        await bot.send_typing(message.channel)
        try:
            owuser = message.content.split(' ', 1)[1]
            owmessage = overwatch.owheroes(owuser)
            await bot.send_message(message.channel, owmessage)
        except:
            time.sleep(0.750)
            await bot.send_message(message.channel, 'Please provide a valid username.')
        return

    #overall ow stats
    if message.content.startswith('!ow'):
        await bot.send_typing(message.channel)
        try:
            owuser = message.content.split(' ', 1)[1]
            owmessage = overwatch.ow(owuser)
            await bot.send_message(message.channel, owmessage)
        except:
            time.sleep(0.750)
            await bot.send_message(message.channel, 'Please provide a valid username.')
        return

    #change game
    if message.content.startswith('!game'):
        if message.author.id == catid:
            try:
                gametarget = message.content.split(' ', 1)[1]
                newGame = discord.Game()
                newGame.name = gametarget
                await bot.change_status(newGame)
            except:
                await bot.change_status(defaultGame)
        else:
            await bot.send_message(message.channel, 'Sorry, only Cat can do that.')
        return

    #clear channel
    if message.content.startswith('!clear'):
        if message.author.id == catid:
            try:
                clearamount = message.content.split(' ', 1)[1]
                await bot.purge_from(channel = message.channel, limit = clearamount)
            except:
                await bot.purge_from(channel = message.channel, limit = 1000000)
        else:
            await bot.send_message(message.channel, 'Sorry, only Cat can do that.')
        return


bot.run('MTkyNzgwOTU2NDY4Mzc5NjQ4.CkN0wQ.8A51zVZjbwBCtqp5WPtHrWVPsuw')
