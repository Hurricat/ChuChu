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
import pokemon.main as pokemon
import horoscope.main as horoscope

address = '76.77.238.1'
port = 4002
bot = discord.Client()
defaultGame = discord.Game()
defaultGame.name = "SHOW BY ROCK!!"
catid = '132072321421672448'

parser = argparse.ArgumentParser()
parser.add_argument("token", help = "the application token for the bot to use")
args = parser.parse_args()

@bot.event
async def on_ready():

    #setup bot
    await bot.change_status(defaultGame)
    print('Bot Started.')

@bot.event
async def on_server_join(server):
    await bot.leave_server(server)

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
    if message.channel.is_private != True:
        logmsg = message.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + message.server.name + ": #" + message.channel.name + " - " + (message.author.name[:13] + ': ').ljust(15) + message.content
    else:
        logmsg = message.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ' - ' + (message.author.name[:13] + ': ').ljust(15) + message.content
    logfile = open("log.txt", "a")
    logfile.write(logmsg + '\n')
    logfile.close()
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
                "!help                     - Display this message.\n\n"
                "--- Overwatch Commands ---\n"
                "!ow [username]            - Get general Overwatch stats.\n"
                "!owheroes [username]      - Get top 5 Overwatch heroes.\n"
                "!owhero [username] [hero] - Get stats for specific hero.\n\n"
                "---- Pokemon Commands ----\n"
                "!pokeitem [item]          - Get info on an item from Pokemon.\n"
                "!pokeberry [berry]        - Get info on a berry from Pokemon.\n"
                "!pokemon [species]        - Get info on a Pokemon species.\n\n"
                "----- Other Commands -----\n"
                "!cowsay [text]            - Have a cow say something.\n"
                "!cowthink [text]          - Have a cow think about something.\n"
                "!punch [person]           - Punch the person specified.\n"
                "!stock [symbol]           - Get the price of a stock.\n"
                "!kdwstatus                - Check if KDW is online.\n"
                "!horoscope [sign]         - Get a horoscope because why not.\n"
                "```\n"
                "For more detailed information, go here: http://ailurophiliac.com/about"
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

        #explode
        if (cmd == 'explode'):
            await msgInChannel('**GARY! YOU ARE GONNA FINISH YOUR DESSERT, AND YOU ARE GONNA LIKE IT!!**')
            return

        #technique
        if (cmd == 'technique'):
            await msgInChannel(
                "First go like this, spin around. Stop! Double take three times: one, two, three. Theeeen PELVIC THRUST! Whoooo! Whooooooo! Stop on your right foot, don't forget it! Now it's time to bring it around town. Bring-it-a-round-town. Then you do this, then this, and this, and that, and-this-and-that-and-this-and-that, and then...\n" +
                "https://gyazo.com/cdadc73fffb89409f57778be7d3eeb51"
            )
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
        
        #pokemon items
        if (cmd == 'pokeitem'):
            if (args != ''):
                try:
                    pokeitem = pokemon.getItem(args)
                except:
                    pokeitem = "The item is invalid"
            else:
                pokeitem = "Please provide an item"
            await msgInChannel(pokeitem)

        #pokemon berries
        if (cmd == 'pokeberry'):
            if (args != ''):
                try:
                    pokeberry = pokemon.getBerry(args)
                except:
                    pokeberry = "The berry is invalid"
            else:
                pokeberry = "Please provide a berry"
            await msgInChannel(pokeberry)

        #pokemon
        if (cmd == 'pokemon'):
            if (args != ''):
                try:
                    poke = pokemon.getPokemon(args)
                except:
                    poke = "The Pokemon is invalid"
            else:
                poke = "Please provide a Pokemon"
            await msgInChannel(poke)

        #horoscope
        if (cmd == 'horoscope'):
            if(args != ''):
                try:
                    horo = horoscope.getToday(args)
                except:
                    horo = "Either the sign is invalid or the API is down"
            else:
                horo = "Please provide a sign."
            await msgInChannel(horo)

        #ow top heroes
        if (cmd == 'owheroes'):
            if (args != ''):
                try:
                    owuser = args
                    owmessage = await ow.owheroes(owuser)
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
                    owmessage = await ow.owhero(owuser, owhero)
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
                    owmessage = await ow.ow(owuser)
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

        if (cmd == 'logout'):
            if message.author.id == catid:
                await bot.logout()
            else:
                await msgInChannel('Sorry, only Cat can do that.')

    if "are you serious" in message.content.lower() or "are you fucking serious" in message.content.lower():
        await msgInChannel(
            'Does this look unserious to you?\n' +
            'https://gyazo.com/f238691fc191ac3ef12ba52bc4adba8e'
        )
        return

    #cleverbot
    #if bot.user.mentioned_in(message) or message.channel.is_private:
    #    await reply(chatbot.message(message.content))
    #    return

bot.run(args.token)
