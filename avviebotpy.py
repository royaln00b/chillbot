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
bot.remove_command('help')

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

# Display settings
@bot.command(pass_context=True)
async def settings(ctx,*,setting=None):
	if setting == None:
		status = str(dbhandler.display())
		status = status.replace("'","")
		status = status.replace("(","")
		status = status.replace(")","")
		status = status.replace(","," -")

		embed=discord.Embed(title="Server Settings",description=status,colour=0xFFC600)
		await bot.send_message(ctx.message.channel,embed=embed)

#			Moderation Commands
# Mute command
@bot.command(pass_context=True)
async def mute(ctx,member:discord.Member,*,reason="None"):
	if ctx.message.author.server_permissions.manage_messages == True:
		if "Muted" in [y.name for y in ctx.message.server.roles]:
			embed=discord.Embed(title="🤐 Mute 🤐",description='<@{}>, you have been muted. \nReason : `'.format(member.id)+reason+'`',colour=0xFFC600)
			await asyncio.sleep(1)
			await bot.add_roles(member,discord.utils.get(ctx.message.server.roles, name="Muted"))
			await bot.say(embed=embed)
		else:
			embed=discord.Embed(title="❕ OOPS ❕",description=ctx.message.author.mention+"\nIt appears the role `Muted` is not in this server, create it to mute someone!",colour=0xFFC600)
			await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="❕ Permission Error ❕",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to Manage Messages, which is required to mute someone!",colour=0xFFC600)
		await bot.say(embed=embed)

# Kick command
@bot.command(pass_context=True)
async def kick(ctx,member:discord.Member,*,reason="None"):
	if ctx.message.author.server_permissions.kick_members == True:
		await bot.kick(member)
		embed=discord.Embed(title="⚒️ KICKED ⚒️",description=member.display_name+" has been kicked by "+ctx.message.author.display_name+"\nReason : `"+str(reason)+"`",colour=0xFFC600)
		await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="❕ Permission Error ❕",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to Kick Members, which is required to kick someone!",colour=0xFFC600)
		await bot.say(embed=embed)
# Ban command
@bot.command(pass_context=True)
async def ban(ctx,member:discord.Member,*,reason="None"):
	if ctx.message.author.server_permissions.ban_members == True:
		await bot.ban(member)
		embed=discord.Embed(title="⚒️ BANNED ⚒️",description=member.display_name+" has been banned by "+ctx.message.author.display_name+"\nReason : `"+str(reason)+"`",colour=0xFFC600)
		await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="❕ Permission Error ❕",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to ban Members, which is required to ban someone!",colour=0xFFC600)
		await bot.say(embed=embed)

# Purge command
@bot.command(pass_context=True)
async def purge(ctx,num: int):
    await bot.purge_from(ctx.message.channel,limit=num)


#			Events



#			Running

token = os.getenv('TOKEN')
bot.run(token)
