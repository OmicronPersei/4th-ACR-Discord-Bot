# 4th Armored Cavalry Regiment Discord Bot
This is a [Discord](https://discordapp.com/) bot that makes use of the [`discord.py`](https://github.com/Rapptz/discord.py) package with a few configurable features:
* Welcome message, user leave notifications.
* Configurable to mention specific users, roles, users who joined/left, channels.
* Configurable self service role management.
* User reaction to message report.
* Announcement/message creator.

## Requirements
* Python 3.6.x
  * Visit [https://www.python.org/downloads/](https://www.python.org/downloads/) for a list of versions for download, or use your OS's package manager..

## Starting up the bot
1. First ensure that both `config.json` and `secrets.json` are properly setup.
2. `pip install -r requirements.txt`
4. Windows: `python .\bot.py` or on linux: `python3 ./bot.py`.

*Note that the specific name for the python binary may vary based on the installation method/OS.*

## Bot commands
### user_roles_service
This command allows users to add/remove themselves from available, whitelisted roles.  Roles may be segregated into individual channels, as seen in the config example.
#### Usage
* **`!roles`**: Lists all available roles.
* **`!roles add <role name>`**: Adds self to the provided `<role name>`.
* **`!roles remove <role name>`**: Removes self from the provided `<role name>`.

### user_reaction_reporter
This command is used to aggregate all users who have given a specific emoji reaction to a message into a predefined hiearchy of roles defined in the `config.json`.  Any emojis can be watched for, and each have a corresponding display template for how each user (given their specific reaction) is displayed.
#### Usage
**`!expected-attendance <channel> <msg id> <root role name>`**
* `<channel msg is in>`: The channel that the message to be aggregated is located.  The bot must have read access to this channel.
* `<msg id>`: The message ID that is targeted for aggregation.
* `<root role name>`: The top role of which to display users who have reacted.

Example: `!expected-attendance operations 610626077920067585 1st platoon` would aggregate all reactions for the message "610626077920067585" in the "operations" channel who is located at or underneath the role "1st platoon" as defined in the role structure in the config.

### announcement_service
This command allows the bot to make messages on your behalf in any channel with the ability to edit them for mistakes.  It also allows you to place and edit reactions to the target message.

#### Usage
* **`!announce create <channelName> <announcementContent>`**: Create an announcement in the channel `<channelName>` with the message of `<announcementContent>`.
* **`!announce edit <channelName> <announcementMessageId> <newAnnouncementContent>`**: Edit an existing announcement within the channel `<channelName>`, having a message id of `<announcementMessageId>` to now display `<newAnnouncementContent>`.
* **`!announce set-reactions <channelName> <announcementMessageId> <spaceSeparatedEmojis>`**: Edit an existing announcement's reactions within the channel `<channelName>`, having a message id of `<announcementMessageId>` to now have reactions within the `<spaceSeparatedEmojis>` list.

## Configuration files
### `config.json`
Primary configuration file for the bot, not including sensitive information.

Example:

*Please note that the below is not valid JSON as comments aren't allowed.  Simply remove the comments (lines of text with `//` after them, including the slashes) for it to be a valid example.*
```
{
    //Config is cached and not reloaded for 300 seconds (5 minutes)
    "config_cache_expires_after": 300,
    //The maximum allowable characters per message to be sent.  At the time of writing it is 2000.
    "discord_max_char_limit": 2000,
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
    },
    "user_role_self_service": {
        //Channel IDs as the key for an array of role IDs accessable within that channel
        "channels_available_roles": {
            "11111": [
                "1",
                "2"
            ]
        },
        "command_keyword": "!roles",
        "enabled": true
    },
    "user_reaction_reporter": {
        "enabled": true,
        "command_keyword": "!expected-attendance",
        "restrict_to_channel": "expected-attendance",
        //The following emojis will be mapped to the given display template.
        //{user} represents the display name of a member, and {role} is the name of that role.
        //The blank emoji represents the template to be used when a member of a given {role} has not reacted to the post at all
        "emojis": [
            { "emoji": "👍", "display_template": "**{user} ({role})**" },
            { "emoji": "👎", "display_template": "~~{user} ({role})~~" },
            { "emoji": "🤷", "display_template": "*{user} ({role})?*" },
            { "emoji": "", "display_template": "~~{user} ({role})~~" }
        ],
        //These represents roles, when given to the command, will map to a new role.
        //This is used to map a more general role to a specific role within the role structure.
        "role_aliases": {
            "12234234232423": "1234234234"
        },
        //The hierarchical layout of roles and their children.  It can support as many children and depth as needed.
        "role_structure": {
            "role_id": "1",
            "children": [
                {
                    "role_id": "2"
                }
            ]
        }
    },
    "announcement_service": {
        "enabled": true,
        "command_keyword": "!announce",
        //The role IDs allowed to make use of this command
        "allowed_roles": [
            611325505114734593
        ]
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
