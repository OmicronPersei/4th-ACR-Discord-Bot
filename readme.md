## Example `config.json`
```
{
    "welcome_message": {
        //The following tokens are replaced with appropriate Discord mentions:
        //{joined_user} is replaced with the user who joined the Discord guild
        //{role:DesignatedCoolGuy} is replaced with the role "DesignatedCoolGuy".
        //{member:User#123} is replaced with the matching user/discriminator pair (their discord name, not guild displayname/nickname).
        
        "message": "{joined_user}, welcome to our discord!",
        "channel": "general"
    }
}
```

## Example `secrets.json`
```
{
    "discord-bot-token": "bot-secret-goes-here"
}
```
