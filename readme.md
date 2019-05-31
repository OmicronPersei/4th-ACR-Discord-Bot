## Example `config.json`
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
    },
    "xen_foro_integration: {
        "forum_name": "my_unique_prefix",
        "base_url": "https://myforum.xyz/",
        "forums": [
            {
                "update_period": "60",
                "target_forum_id": "234",
                "target_discord_channel": "forum posts",
                "message_template": "A new forum post has appeared! {thread_url}",
                "discord_message_emojis": []
            }
        ]
    }
}
```

## Example `secrets.json`
```
{
    "discord-bot-token": "bot-secret-goes-here",
    "xen_foro_integration_api_token": "token here"
}
```
