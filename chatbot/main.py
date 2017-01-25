import cleverbot
import re

cleverbot = cleverbot.Cleverbot('chuchu-bot')

def message(message):
    cbotmessage = re.sub(r'\<[^>]*\>[ ]', '', message)
    cbotreply = cleverbot.ask(cbotmessage)
    return cbotreply
