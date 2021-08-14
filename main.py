import json

import discord
from discord.ext import commands

from config import read_config

intents = discord.Intents.all()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix='!',
            case_insensitve=True,
            intents=intents,
            help_command=None
        )

    async def on_ready(self):
        print("Bot is online and has cached!")

    async def on_member_join(self, member):
        guild = member.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }
        c1 = await guild.create_text_channel("announcements", overwrites=overwrites)
        await c1.set_permissions(member, read_messages=True, send_messages=False)
        c2 = await guild.create_text_channel("how-to-use", overwrites=overwrites)
        await c2.set_permissions(member, read_messages=True, send_messages=False)
        c3 = await guild.create_text_channel("general", overwrites=overwrites)
        await c3.set_permissions(member, read_messages=True, send_messages=True)
        mainannouncements = discord.utils.get(member.guild.channels, id=int(read_config()['announcements_channel_id']))
        newannounce = await mainannouncements.history(limit=None).flatten()
        for x in newannounce:
            await c1.send(x.content)
        howto = discord.utils.get(member.guild.channels, id=int(read_config()['how_to_channel_id']))
        howtoa = await howto.history(limit=None).flatten()
        for x in howtoa:
            await c2.send(x.content)

        with open('Storage/channels.json', 'r') as file:
            channels = json.load(file)

        with open('Storage/ids.txt', 'r') as file:
            idn = file.read()

        channels[str(member.id)] = [str(c1.id), str(c2.id), str(c3.id), str(idn)]

        idn = str(int(idn) + 1)

        with open('Storage/ids.txt', 'w') as file:
            file.write(idn)

        with open('Storage/channels.json', 'w') as file:
            json.dump(channels, file)

    async def on_message(self, message):
        if str(message.channel.id) == str(read_config()['announcements_channel_id']):
            with open('Storage/channels.json', 'r') as file:
                channels = json.load(file)
            for x in channels:
                an = discord.utils.get(message.guild.channels, id=int(channels[x][0]))
                await an.send(message.content)
            return
        elif message.channel.id == read_config()['how_to_channel_id']:
            with open('Storage/channels.json', 'r') as file:
                channels = json.load(file)
            for x in channels:
                an = discord.utils.get(message.guild.channels, id=int(channels[x][1]))
                await an.send(message.content)
            return
        else:
            with open('Storage/channels.json', 'r') as file:
                channels = json.load(file)

            if str(message.author.id) in channels:
                if channels[str(message.author.id)][2] == str(message.channel.id):
                    for z in channels:
                        if z == str(message.author.id):
                            continue
                        else:
                            a1 = discord.utils.get(message.guild.channels, id=int(channels[z][2]))
                            await a1.send(f'**Anonymous#{channels[z][3]}:** {message.content}')

    async def on_member_remove(self, member):
        with open('Storage/channels.json', 'r') as file:
            channels = json.load(file)

        await discord.utils.get(member.guild.channels, id=int(channels[str(member.id)][0])).delete()
        await discord.utils.get(member.guild.channels, id=int(channels[str(member.id)][1])).delete()
        await discord.utils.get(member.guild.channels, id=int(channels[str(member.id)][2])).delete()

        del channels[str(member.id)]

        with open('Storage/channels.json', 'w') as file:
            json.dump(channels, file)


bot = Bot()
bot.run(read_config()['bot_token'])


