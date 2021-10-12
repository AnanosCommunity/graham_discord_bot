import config
import discord
from models.command import CommandInfo
from util.env import Env

class Messages():
    @staticmethod
    async def send_usage_dm(member: discord.Member, command: CommandInfo) -> discord.Message:
        embed = discord.Embed(colour=discord.Colour.purple())
        embed.title = "Usage"
        embed.add_field(name=f"{config.Config.instance().command_prefix}{command.triggers[0]}", value=command.details, inline=False)
        try:
            return await member.send(embed=embed)
        except Exception:
            # May raise if user has blocked the bot
            return None
 
    @staticmethod
    async def send_error_dm(member: discord.Member, message: str, skip_dnd=False) -> discord.Message:
        if skip_dnd and member.status == discord.Status.dnd:
            return None
        embed = discord.Embed(colour=discord.Colour.red())
        embed.title = "Error"
        embed.description = message
        try:
            return await member.send(embed=embed)
        except Exception:
            # May raise if user has blocked the bot
            return None

    @staticmethod
    async def send_error_public(channel: discord.TextChannel, message: str) -> discord.Message:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.title = "Error"
        embed.description = message
        try:
            return await channel.send(embed=embed)
        except Exception:
            # May raise if user has blocked the bot
            return None


    @staticmethod
    async def send_success_dm(member: discord.Member, message: str, header: str = "Success", footer: str = None, skip_dnd=False) -> discord.Message:
        if skip_dnd and member.status == discord.Status.dnd:
            return None
        embed = discord.Embed(colour=discord.Colour.green())
        embed.title = header
        embed.description = message
        if footer is not None:
            embed.set_footer(text=footer)
        try:
            return await member.send(embed=embed)
        except Exception:
            # May raise if user has blocked the bot
            return None

    @staticmethod
    async def send_basic_dm(member: discord.Member, message: str, skip_dnd=False) -> discord.Message:
        if skip_dnd and member is not None and member.status == discord.Status.dnd:
            return None
        try:
            return await member.send(message)
        except Exception:
            # May raise if user has blocked the bot
            return None

    @staticmethod
    async def add_tip_reaction(msg: discord.Message, amount: float, rain: bool = False):
        if amount > 0:
            try:
                await msg.add_reaction('\:tip:425878628119871488') # TIP mark
                await msg.add_reaction('\:tick:425880814266351626') # check mark
            except Exception:
                await msg.add_reaction('\U00002611') # fallback for non-banano server
        if amount > 0 and amount < 50:
            await msg.add_reaction('\U0001F987') # S
        elif amount >= 50 and amount < 250:
            await msg.add_reaction('\U0001F412') # C
        elif amount >= 250:
            await msg.add_reaction('\U0001F98D') # W
        if rain:
            try:
                await msg.add_reaction('\:bananorain:430826677543895050') # Banano rain
            except Exception:
                await msg.add_reaction('\U0001F4A6') # Sweat Drops

    @staticmethod
    async def add_x_reaction(msg: discord.Message):
        await msg.add_reaction('\U0000274C') # X
        return

    @staticmethod
    async def add_burn_reaction(msg: discord.Message):
        await msg.add_reaction('\:tick:425880814266351626')
        await msg.add_reaction('\U0001F525')
        await msg.add_reaction('\:BanElmoFire:769726940969435177')
        return

    @staticmethod
    async def add_timer_reaction(msg: discord.Message):
        await msg.add_reaction('\U000023F2') # Timer Clock
        return

    @staticmethod
    async def delete_message_if_ok(msg: discord.Message):
        if msg.channel.id not in config.Config.instance().get_giveaway_no_delete_channels():
            try:
                await msg.delete()
            except Exception:
                pass

    @staticmethod
    async def delete_message(msg: discord.Message):
        try:
            await msg.delete()
        except Exception:
            pass