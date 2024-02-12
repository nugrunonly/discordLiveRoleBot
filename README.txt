# discordLiveRoleBot
automatically assign a role when someone goes live on discord

create a .env file with the following template

TOKEN="asdf"
GUILD_ID="hjkl"
LIVE_ROLE_ID="zsav"

Token = your discord app token
guild id = your discord channel id
live role id = the id of the role you want assigned (found in developer mode within discord)


prerequisites:
pip install discord
pip install asyncio
pip install os
pip install python-dotenv


How to make a discord bot:
https://discord.com/developers/docs/intro
navigate to OAauth2 -> URL generator
Select "Bot" in scopes and also select "Manage Roles" in bot permissions
Copy & Open the URL to select the server and authorize it

Make sure your "Live Role" discord role is placed above all other roles in the roles section
