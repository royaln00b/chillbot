#			Importing stuff

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import time
import re
import random
import datetime
import dbhandler
import os

bot=commands.Bot(description="",command_prefix="-",pm_help=False)

#			Commands

# Help command
@bot.command(pass_context=True)
async def help(ctx,*,command=None):
	if command == None:
		embed=discord.Embed(title="❔ HELP ❔",description="Hi welcome to the help file for **KING BOT**\n\n**Commands**\n1. avatar",colour=0xFFC600)
		embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
		await bot.send_message(ctx.message.channel,embed=embed)

# Avatar Command
@bot.command(pass_context=True)
async def avatar(ctx,*,member:discord.Member=None):
	if member == None:
		member = ctx.message.author
	embed=discord.Embed(title="Avatar of "+member.display_name,description=None,colour=0xFFC600)
	embed.set_image(url = member.avatar_url)
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.send_message(ctx.message.channel,embed=embed)


#			Events



#			Running

token = os.getenv('TOKEN')
bot.run(token)
