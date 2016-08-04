import discord
import asyncio
import time
import datetime
import argparse
import subprocess

import chatbot.main as chatbot
import kdw.main as kdw
import stock.main as stock
import overwatch.main as ow

address = '76.77.225.51'
port = 4002
bot = discord.Client()
defaultGame = discord.Game()
defaultGame.name = "SHOW BY ROCK!!"
catid = '132072321421672448'
logfile = open('log.txt', 'a')

parser = argparse.ArgumentParser()
parser.add_argument("token", help = "the application token for the bot to use")
args = parser.parse_args()

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
    await bot.send_typing(server)
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
    logmsg = message.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + (message.author.name[:13] + ': ').ljust(15) + message.content
    logfile.write(logmsg + '\n')
    print(logmsg)
    
    #don't respond to self
    if message.author.id == bot.user.id:
        return
    
    if message.content.startswith('!'):
        try:
            cmd = message.content.split(' ', 1)[0].replace('!','')
            args = message.content.split(' ', 1)[1]
        except:
            cmd = message.content.replace('!','')
            args = ''

        #command list
        if (cmd == 'help'):
            await msgInChannel(
                "```\n"
                "@ChuChu                   - I can respond to mentions.\n"
                "!help                     - Display this message.\n"
                "!punch [person]           - Punch the person specified.\n"
                "!stock [symbol]           - Get the price of a stock.\n"
                "!kdwstatus                - Check if KDW is online.\n"
                "!ow [username]            - Get general Overwatch stats.\n"
                "!owheroes [username]      - Get top 5 Overwatch heroes.\n"
                "!owhero [username] [hero] - Get stats for specific hero.\n"
                "!cowsay [text]            - Have a cow say something.\n"
                "!cowthink [text]          - Have a cow think about something.\n"
                "```"
            )
            return
    
        #check if kdw online
        if (cmd == 'kdwstatus'):
            await msgInChannel(kdw.status(address, port))
            return

        #punch someone
        if (cmd == 'punch'):
            if (args != ''):
                punchtarget = args
            else:
                punchtarget = 'someone'
            await msgInChannel('I am going to punch {0}.'.format(punchtarget))
            return

        #get stock prices
        if (cmd == 'stock'):
            if (args != ''):
                try:
                    stocksym = args
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
                    stockInfo = "Invalid stock symbol"
            else:
                stockInfo = "Please provide a stock symbol"
            await msgInChannel(stockInfo)
            return

        #ow top heroes
        if (cmd == 'owheroes'):
            if (args != ''):
                try:
                    owuser = args
                    owmessage = ow.owheroes(owuser)
                except:
                    owmessage = "Either the username is invalid or the API is down"
            else:
                owmessage = "Please provide a username"
            await msgInChannel(owmessage)
            return

        #hero specific stats
        if (cmd == 'owhero'):
            if (args != ''):
                try:
                    owuser = args.split(' ', 1)[0]
                    print(owuser)
                    owhero = args.split(' ', 1)[1]
                    print(owhero)
                    owmessage = ow.owhero(owuser, owhero)
                except:
                    owmessage = "Either the username/hero is invalid or the API is down"
            else:
                owmessage = "Please provide a username and hero"
            await msgInChannel(owmessage)
            return

        #overall ow stats
        if (cmd == 'ow'):
            if (args != ''):
                try:
                    owuser = args
                    owmessage = ow.ow(owuser)
                except:
                    owmessage = "Either the username is invalid or the API is down"
            else:
                owmessage = "Please provide a username"
            await msgInChannel(owmessage)
            return

        if (cmd == 'cowsay'):
            if (args != ''):
                if args.startswith('-'):
                    args = args.replace('-', '')
                cowmessage = subprocess.check_output(['cowsay', args]).decode('utf-8')
            else:
                cowmessage = subprocess.check_output(['cowsay', 'Please provide some text']).decode('utf-8')
            await msgInChannel('```\n' + cowmessage + '```')

        if (cmd == 'cowthink'):
            if (args != ''):
                cowmessage = subprocess.check_output(['cowthink', args]).decode('utf-8')
            else:
                cowmessage = subprocess.check_output(['cowthink', 'Please provide some text']).decode('utf-8')
            await msgInChannel('```\n' + cowmessage + '```')

        #change game
        if (cmd == 'game'):
            if message.author.id == catid:
                if (args != ''):
                    gametarget = args
                    newGame = discord.Game()
                    newGame.name = gametarget
                else:
                    newGame = defaultGame
                await changeGame(newGame)
            else:
                await msgInChannel('Sorry, only Cat can do that.')
            return

        #clear channel
        if (cmd == 'clear'):
            if message.author.id == catid:
                if (args != ''):
                    clearamount = args
                    await clearChannel(clearamount)
                else:
                    await clearChannel()
            else:
                await msgInChannel('Sorry, only Cat can do that.')
            return

    #cleverbot
    if bot.user.mentioned_in(message) or message.channel.is_private:
        await reply(chatbot.message(message.content))
        return


bot.run(args.token)
