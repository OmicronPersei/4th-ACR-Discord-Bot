# 4th Squadron, 9th Cavalry Discord Bot
This is a [Discord](https://discordapp.com/) bot that makes use of the [`discord.py`](https://github.com/Rapptz/discord.py) package with a few configurable features:
* Welcome message, user leave notifications.
* Configurable to mention specific users, roles, users who joined/left.

## Requirements
* Python 3.6.x
  * Visit [https://www.python.org/downloads/](https://www.python.org/downloads/) for a list of versions for download, or use your OS's package manager.
* [`pipenv`](https://pypi.org/project/pipenv/)
  * You can install typically using `pip install pipenv`.

## Starting up the bot
1. First ensure that both `config.json` and `secrets.json` are properly setup.
2. `pipenv install`
3. `pipenv shell`
4. Windows: `python .\bot.py` or on linux: `python3 ./bot.py`.

*Note that the specific name for the python binary may vary based on the installation method/OS.*

## Configuration files
### `config.json`
Primary configuration file for the bot, not including sensitive information.

Example:

*Please note that the below is not valid JSON as comments aren't allowed.  Simply remove the comments (lines of text with `//` after them, including the slashes) for it to be a valid example.*
```
{
    "welcome_message": {
        //The following tokens are replaced with appropriate Discord mentions:
        //{joined_user} is replaced with the user who joined the Discord guild
        //{role:DesignatedCoolGuy} is replaced with the role "DesignatedCoolGuy".
        //{member:User#123} is replaced with the matching user/discriminator pair (their discord name, not guild displayname/nickname).

        "message": "{joined_user}, welcome to our discord!",
        "channel": "general",
        "enabled": false
    },
    "user_leave_notification": {
        //Supports the same tokens as "welcome_message", but uses {left_user} instead of {joined_user}
        "message": "{left_user} has left the server",
        "channel": "user-left-log",
        "enabled": true
    }
}
```

### `secrets.json`
Primary configuration file for sensitive info, primary the bot's discord secret.

Example:
```
{
    "discord-bot-token": "bot-secret-goes-here"
}
```
