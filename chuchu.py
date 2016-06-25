import discord
import asyncio
import time
import datetime

import chatbot.main as chatbot
import kdw.main as kdw
import stock.main as stock
import overwatch.main as ow

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

    #typing
    async def typing():
        await bot.send_typing(message.channel)
        time.sleep(0.750)

    #message in same channel
    async def msgInChannel(content):
        await typing()
        await bot.send_message(message.channel, content)

    #message in server's default channel
    async def msgInMain(content):
        await typing()
        await bot.send_message(message.server, content)

    #reply to message
    async def reply(content):
        replyformat = '{0.mention} {1}'
        await msgInChannel(replyformat.format(message.author, content))

    #change playing game
    async def changeGame(game):
        await bot.change_status(game)

    async def clearChannel(amount = 100):
        await bot.purge_from(channel = message.channel, limit = amount)
        

    #message log
    print(message.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + (message.author.name[:13] + ': ').ljust(15) + message.content)
    
    #don't respond to self
    if message.author.id == bot.user.id:
        return

    #cleverbot
    if bot.user.mentioned_in(message):
        await reply(chatbot.message(message.content))
        return
    
    #command list
    if message.content.startswith('!help'):
        await msgInChannel("I'm ChuChu, here's a list of what I can do:")
        await msgInChannel(
            "```\n"
            "@ChuChu              - I can respond to mentions.\n"
            "!help                - Display this message.\n"
            "!punch [person]      - Punch the person specified.\n"
            "!stock [symbol]      - Get the price of a stock.\n"
            "!kdwstatus           - Check if KDW is online.\n"
            "!ow [username]       - Get general Overwatch stats.\n"
            # "!owheroes [username] - Get top 5 Overwatch heroes.\n"
            "```"
        )
        return

    #check if kdw online
    if message.content.startswith('!kdwstatus'):
        await msgInChannel(kdw.status(address, port))
        return

    #punch someone
    if message.content.startswith('!punch'):
        try:
            punchtarget = message.content.split(' ', 1)[1]
        except:
            punchtarget = 'someone'
        await msgInChannel('I am going to punch {0}.'.format(punchtarget))
        return

    #get stock prices
    if message.content.startswith('!stock'):
        try:
            stocksym = message.content.split(' ', 1)[1]
            stockInfo = (
                "```\n" +
                "Stock Information for {0}\n".format(stock.get_name(stocksym)) +
                "  Price:   {0}\n".format(stock.get_price(stocksym)) +
                "  Open:    {0}\n".format(stock.get_open(stocksym)) +
                "  High:    {0}\n".format(stock.get_high(stocksym)) +
                "  Low:     {0}\n".format(stock.get_low(stocksym)) +
                "  Volume:  {0}\n".format(stock.get_vol(stocksym)) +
                "```"
            )
        except:
            stockInfo = "Please give a valid stock symbol"
        await msgInChannel(stockInfo)
        return

    #ow top heroes
    # if message.content.startswith('!owheroes'):
    #     try:
    #         owuser = message.content.split(' ', 1)[1]
    #         owmessage = ow.owheroes(owuser)
    #     except:
    #         owmessage = "Please provide a valid username"
    #     await msgInChannel(owmessage)
    #     return

    #overall ow stats
    if message.content.startswith('!ow'):
        await bot.send_typing(message.channel)
        try:
            owuser = message.content.split(' ', 1)[1]
            owmessage = ow.ow(owuser)
        except:
            owmessage = "Please provide a valid username"
        await msgInChannel(owmessage)
        return

    #change game
    if message.content.startswith('!game'):
        if message.author.id == catid:
            try:
                gametarget = message.content.split(' ', 1)[1]
                newGame = discord.Game()
                newGame.name = gametarget
            except:
                newGame = defaultGame
            await changeGame(newGame)
        else:
            await msgInChannel('Sorry, only Cat can do that.')
        return

    #clear channel
    if message.content.startswith('!clear'):
        if message.author.id == catid:
            try:
                clearamount = message.content.split(' ', 1)[1]
                await clearChannel(clearamount)
            except:
                await clearChannel()
        else:
            await msgInChannel('Sorry, only Cat can do that.')
        return


bot.run('MTkyNzgwOTU2NDY4Mzc5NjQ4.CkN0wQ.8A51zVZjbwBCtqp5WPtHrWVPsuw')
