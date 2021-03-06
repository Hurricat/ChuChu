# ChuChu
A simple Discord bot using discord.py

## Using ChuChu

### Prerequisites
ChuChu requires the following to be installed:
* Python 3.5 or later
* cleverbot module
* discord.py module
* cowsay in PATH

### Features
The following commands can be used:
```
@ChuChu                   - Respond to mentions.
!help                     - Display this message.

----- Other Commands -----
!cowsay [text]            - Have a cow say something.
!cowthink [text]          - Have a cow think about something.
!punch [person]           - Punch the person specified.
!kdwstatus                - Gets server status of Kirby's Dream World
!horoscope [sign]         - Get a horoscope because why not.

----- Admin Commands -----
!clear                    - Clears all messages in the current channel.
!game [game name]         - Displays specified game as currently playing.
!logout                   - Logs out the current instance of the bot.
```

### Usage
`python chuchu.py token`
Where token is a Discord app Oauth2 token

If you run your own instance and wish to use the
bot's admin commands, be sure to change the catid
variable to your own Discord ID. The instance I
run only allows me to run these commands.

Alternatively, to add ChuChu to a server without
running the bot yourself, use the following link:

https://discordapp.com/oauth2/authorize?client_id=192780916710572032&scope=bot

## Acknowledgements
* Rapptz - discord.py
* folz - cleverbot module
