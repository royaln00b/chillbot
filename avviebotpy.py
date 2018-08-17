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

# Ping command
@bot.command(pass_context=True)
async def ping(ctx):
	channel = ctx.message.channel
	t1 = time.perf_counter()
	await bot.send_typing(channel)
	t2 = time.perf_counter()
	embed=discord.Embed(title="🏓 PING 🏓", description='\n**{}ms**\n'.format(round(((t2-t1)*1000)-100)), colour = 0xFFC600)
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.say(embed=embed)

# Info Command
@bot.command(pass_context=True)
async def info(ctx,*,member:discord.Member=None):
	if member == None:
		embed=discord.Embed(title="SERVER INFORMATION",description=ctx.message.server.name+" info:\nServer Created - "+ctx.message.server.created_at.strftime("%Y-%m-%d %H:%M:%S")+"\nMember Count - "+str(ctx.message.server.member_count)+"\nVerification level - "+str(ctx.message.server.verification_level)+"\nOwner - "+ctx.message.server.owner.name+"\nId - "+str(ctx.message.server.id)+"\nRegion - "+str(ctx.message.server.region),colour=0xFFC600)
		embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
		embed.set_thumbnail(url = ctx.message.server.icon_url)
	else:
		if member.game == None:
			game="None"
		else:
			game=member.game
		embed=discord.Embed(title=member.name+"'s Info",description="Current nickname - "+member.nick+"\nId - "+str(member.id)+"\nGame being played - "+game+"\nTop Role - "+str(member.top_role)+"\nRole Colour - "+member.colour+"\nJoined "+ctx.message.server.name+" - "+member.joined_at.strftime("%Y-%m-%d %H:%M:%S")+"\nStatus - "+member.status,colour=0xFFC600)
		embed.set_thumbnail(url = member.avatar_url)
		embed = embed.replace(None,"None")
		embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.say(embed=embed)


# Avatar Command
@bot.command(pass_context=True)
async def avatar(ctx,*,member:discord.Member=None):
	if member == None:
		member = ctx.message.author
	embed=discord.Embed(title="Avatar of "+member.display_name,description=None,colour=0xFFC600)
	embed.set_image(url = member.avatar_url)
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.send_message(ctx.message.channel,embed=embed)

	
#			Settings commands
_settings=["moderation","joins","leaves"]
_status=["on","off"]
# Display settings
@bot.command(pass_context=True)
async def settings(ctx,setting=None,*,status=None):
	if setting == None:
		status = str(dbhandler.display(ctx))
		status = status.replace("'","")
		status = status.replace("(","")
		status = status.replace(")","")
		status = status.replace(","," - ")
		status = status.replace(" on","✅")
		status = status.replace(" off","❌")
		embed=discord.Embed(title="Server Settings | "+ctx.message.server.name,description=status,colour=0xFFC600)
		embed.set_thumbnail(url = ctx.message.server.icon_url)
		await bot.send_message(ctx.message.channel,embed=embed)
	# Turn options off / on
	if ctx.message.author.server_permissions.administrator == True:
		if setting in _settings:
			if setting == "moderation":
				if status in _status:
					dbhandler.settingchange(ctx,setting,status)
					embed=discord.Embed(title="⚙️ SETTINGS ⚙️",description=ctx.message.author.name+" changed "+setting+" to "+status,colour=0xFFC600)
					await bot.say(embed=embed)
				else:
					embed=discord.Embed(title="⛔️ SETTINGS ERROR ⛔️",description="`ERROR` "+status+" not applicable!",colour=0xFFC600)
					await bot.say(embed=embed)
			elif setting == "joins":
				if status in _status:
					dbhandler.settingchange(ctx,setting,status)
					embed=discord.Embed(title="⚙️ SETTINGS ⚙️",description=ctx.message.author.name+" changed "+setting+" to "+status,colour=0xFFC600)
					await bot.say(embed=embed)
				else:
					embed=discord.Embed(title="⛔️ SETTINGS ERROR ⛔️",description="`ERROR` "+status+" not applicable!",colour=0xFFC600)
					await bot.say(embed=embed)
			elif setting == "leaves":
				if status in _status:
					dbhandler.settingchange(ctx,setting,status)
					embed=discord.Embed(title="⚙️ SETTINGS ⚙️",description=ctx.message.author.name+" changed "+setting+" to "+status,colour=0xFFC600)
					await bot.say(embed=embed)
				else:
					embed=discord.Embed(title="⛔️ SETTINGS ERROR ⛔️",description="`ERROR` "+status+" not applicable!",colour=0xFFC600)
					await bot.say(embed=embed)
		else:
			embed=discord.Embed(title="⛔️ SETTINGS ERROR ⛔️",description="`ERROR` "+setting+" not applicable!",colour=0xFFC600)
			await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="⛔️ PERMISSION ERROR ⛔️",description=ctx.message.author.name+", you need to have the `administrator` permission to edit the server settings!",colour=0xFFC600)
		await bot.say(embed=embed)
		


#			Moderation Commands
# Mute command
@bot.command(pass_context=True)
async def mute(ctx,member:discord.Member,*,reason="None"):
	if ctx.message.author.server_permissions.manage_messages == True:
		if "Muted" in [y.name for y in ctx.message.server.roles]:
			embed=discord.Embed(title="🤐 Mute 🤐",description='{}, you have been muted. \nReason : `'.format(member.display_name)+reason+'`',colour=0xFFC600)
			await asyncio.sleep(1)
			await bot.add_roles(member,discord.utils.get(ctx.message.server.roles, name="Muted"))
			await bot.say(embed=embed)
		else:
			embed=discord.Embed(title="❕ OOPS ❕",description=ctx.message.author.mention+"\nIt appears the role `Muted` is not in this server, create it to mute someone!",colour=0xFFC600)
			await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="⛔️ Permission Error ⛔️",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to Manage Messages, which is required to mute someone!",colour=0xFFC600)
		await bot.say(embed=embed)

# Kick command
@bot.command(pass_context=True)
async def kick(ctx,member:discord.Member,*,reason="None"):
	if ctx.message.author.server_permissions.kick_members == True:
		await bot.kick(member)
		embed=discord.Embed(title="⚒️ KICKED ⚒️",description=member.display_name+" has been kicked by "+ctx.message.author.display_name+"\nReason : `"+str(reason)+"`",colour=0xFFC600)
		await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="⛔️ Permission Error ⛔️",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to Kick Members, which is required to kick someone!",colour=0xFFC600)
		await bot.say(embed=embed)
# Ban command
@bot.command(pass_context=True)
async def ban(ctx,member:discord.Member,*,reason="None"):
	if ctx.message.author.server_permissions.ban_members == True:
		await bot.ban(member)
		embed=discord.Embed(title="⚒️ BANNED ⚒️",description=member.display_name+" has been banned by "+ctx.message.author.display_name+"\nReason : `"+str(reason)+"`",colour=0xFFC600)
		await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="⛔️ Permission Error ⛔️",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to ban Members, which is required to ban someone!",colour=0xFFC600)
		await bot.say(embed=embed)

# Purge command
@bot.command(pass_context=True)
async def purge(ctx,num: int):
	setting = "moderation"
	status = str(dbhandler.settingcheck(ctx,setting))
	status = status.replace("[","")
	status = status.replace("]","")
	status = status.replace("'","")
	status = status.replace("(","")
	status = status.replace(")","")
	status = status.replace(",","")
	if status == "on":
		if ctx.message.author.server_permissions.manage_messages == True:
			await bot.purge_from(ctx.message.channel,limit=num+1)
			embed=discord.Embed(title="🗑️ PURGE 🗑️",description=str(num)+" message(s) deleted from "+ctx.message.channel.name,colour=0xFFC600)
			embed.set_footer(text="Deleted by : "+ctx.message.author.display_name+" - Message will be deleted in 5 seconds", icon_url=ctx.message.author.avatar_url)
			message = await bot.say(embed=embed)
			await asyncio.sleep(5)
			await bot.delete_message(message)
		else:
			embed=discord.Embed(title="⛔️ Permission Error ⛔️",description=ctx.message.author.mention+"\nIt appears that you do not have the permission to Manage Messages, which is required to purge messages!",colour=0xFFC600)
			await bot.say(embed=embed)
	else:
		embed=discord.Embed(title="⛔️ SETTINGS ERROR ⛔️",description="It appears your server does not have the `moderation` setting turned on!",colour=0xFFC600)
		await bot.say(embed=embed)

#			Events
@bot.event
async def on_message(message):
	dbhandler.addserveronmessage(message)
	await bot.process_commands(message)
"""
@bot.event
async def on_member_join(member):
	setting = "joins"
	status = str(dbhandler.settingcheckmember(member,setting))
	status = status.replace("[","")
	status = status.replace("]","")
	status = status.replace("'","")
	status = status.replace("(","")
	status = status.replace(")","")
	status = status.replace(",","")
	if status == "on":
		server = member.server
		embed=discord.Embed(title="🔔 WELCOME 🔔",description="**{0.name}! Welcome to {1.name}. Enjoy your stay!**".format(member, server),colour=0xFFC600)
		await bot.send_message(server.default_channel.id, embed=embed)

@bot.event
async def on_member_remove(member):
	setting = "leaves"
	status = str(dbhandler.settingcheckmember(member,setting))
	status = status.replace("[","")
	status = status.replace("]","")
	status = status.replace("'","")
	status = status.replace("(","")
	status = status.replace(")","")
	status = status.replace(",","")
	if status == "on":
		server = member.server
		embed=discord.Embed(title="👋🏼 GOODBYE 👋🏼",description="**{0.name} left {1.name}!**".format(member, server),colour=0xFFC600)
		await bot.send_message(server.default_channel.id, embed=embed)
"""
#			Running

token = os.getenv('TOKEN')
bot.run(token)
