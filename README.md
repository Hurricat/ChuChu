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
!help                     - Prints a command list
!stock [symbol]           - Gets stock information
!ow [username]            - Gets general Overwatch stats
!owheroes [username]      - Gets top 5 Overwatch heroes for user
!owhero [username] [hero] - Gets hero specific stats for user
!kdwstatus                - Gets server status of Kirby's Dream World
```

### Usage
`python chuchu.py token`
Where token is a discord app Oauth2 token

Alternatively, to add ChuChu to a server without
running the bot yourself, use the following link:

https://discordapp.com/oauth2/authorize?client_id=192780916710572032&scope=bot

## Acknowledgements
* Rapptz - discord.py
* SunDwarf - Overwatch API
* folz - cleverbot module
