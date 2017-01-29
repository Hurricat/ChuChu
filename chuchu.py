import discord
import asyncio
import time
import datetime
import argparse
import subprocess

import chatbot.main as chatbot
import kdw.main as kdw
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
    await bot.change_presence(game = defaultGame)
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
        await bot.change_presence(game = game)
    
    #clear channel of messages
    async def clearChannel(amount = 100):
        await bot.purge_from(channel = message.channel, limit = amount)
    
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
                "----- Other Commands -----\n"
                "!cowsay [text]            - Have a cow say something.\n"
                "!cowthink [text]          - Have a cow think about something.\n"
                "!punch [person]           - Punch the person specified.\n"
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
            return

        #cowsay
        if (cmd == 'cowsay'):
            if (args != ''):
                if args.startswith('-'):
                    args = args.replace('-', '')
                cowmessage = subprocess.check_output(['cowsay', args]).decode('utf-8')
            else:
                cowmessage = subprocess.check_output(['cowsay', 'Please provide some text']).decode('utf-8')
            await msgInChannel('```\n' + cowmessage + '```')
            return

        #cowthink
        if (cmd == 'cowthink'):
            if (args != ''):
                cowmessage = subprocess.check_output(['cowthink', args]).decode('utf-8')
            else:
                cowmessage = subprocess.check_output(['cowthink', 'Please provide some text']).decode('utf-8')
            await msgInChannel('```\n' + cowmessage + '```')
            return

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
    if bot.user.mentioned_in(message) or message.channel.is_private:
        await reply(chatbot.message(message.content))
        return

bot.run(args.token)
