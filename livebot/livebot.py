import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.members = True

guildID = int(os.environ['GUILD_ID'])
liveRoleID = int(os.environ['LIVE_ROLE_ID'])

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("I am ready!")
    await start_role_fix_loop()


@client.event
async def on_presence_update(before, after):
    was_streaming = any(activity.type == discord.ActivityType.streaming for activity in before.activities)
    is_streaming = any(activity.type == discord.ActivityType.streaming for activity in after.activities)
    if was_streaming != is_streaming:
        await add_remove_stream_role(after, is_streaming)


async def add_remove_stream_role(member, should_add):
    guild = member.guild
    role = discord.utils.get(guild.roles, id=liveRoleID)
    if role is None:
        print("Role not found.")
        return
    if should_add and role not in member.roles:
        print(f"Adding streaming role to {member.display_name}")
        await member.add_roles(role)
    elif not should_add and role in member.roles:
        print(f"Removing streaming role from {member.display_name}")
        await member.remove_roles(role)


async def fix_stream_role():
    try:
        guild = client.get_guild(guildID)
        if guild is None:
            print("Bot isn't in a server with the specified ID.")
            return
        members = guild.members
        live_members = [member for member in members if any(activity.type == discord.ActivityType.streaming for activity in member.activities)]
        for member in live_members:
            await add_remove_stream_role(member, True)
        not_live_members_with_live_role = [member for member in members if discord.utils.get(member.roles, id=liveRoleID) and not any(activity.type == discord.ActivityType.streaming for activity in member.activities)]
        for member in not_live_members_with_live_role:
            await add_remove_stream_role(member, False)
    except Exception as e:
        print("An error occurred in fix_stream_role:")
        print(e)


async def start_role_fix_loop():
    try:
        await fix_stream_role()
        while True:
            await asyncio.sleep(5 * 60)  # Run every 5 minutes
            await fix_stream_role()
    except Exception as e:
        print("Failed to start role fix loop!")
        print(e)


client.run(os.environ['TOKEN'])
