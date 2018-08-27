import time
import datetime
import random
import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS settings(serverid BIGINT, setting TEXT, status TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS warns(serverid BIGINT, userid BIGINT, warnings INT)')
	

"""
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS currency()')
"""

def display(ctx):
	c.execute('SELECT setting, status FROM settings WHERE serverid= %s',(ctx.message.server.id,))
	rows = c.fetchall()
	lines = '\n'.join(f'{i+1}. {line}' for i, line in enumerate(rows))
	return lines

def warnings(ctx,member):
	c.execute('SELECT warnings FROM warns WHERE serverid= %s AND userid= %s',(ctx.message.server.id,member.id,))
	status = c.fetchone()
	return status

def addserveronmessage(message):
	c.execute("SELECT serverid FROM settings")
	rows = c.fetchall()
	string = '\n'.join(str(row) for row in rows)
	if not str(message.server.id) in string:
		c.execute("INSERT INTO settings VALUES(%s,%s,%s)",(message.server.id,"moderation","off",))
		c.execute("INSERT INTO settings VALUES(%s,%s,%s)",(message.server.id,"joins","off",))
		c.execute("INSERT INTO settings VALUES(%s,%s,%s)",(message.server.id,"leaves","off",))
		conn.commit()

def addwarnsonmessage(message):
	c.execute("SELECT serverid, userid FROM warns")
	rows = c.fetchall()
	string = '\n'.join(str(row) for row in rows)
	if not str(message.server.id) in string:
		if not str(message.author.id) in string:
			c.execute("INSERT INTO warns VALUES(%s,%s,%s)",(message.server.id,message.author.id,0,))
			conn.commit()

def settingchange(ctx,setting,status):
	c.execute('UPDATE settings SET status = %s WHERE serverid = %s AND setting = %s', (status,ctx.message.server.id,setting,))
	conn.commit()

def settingcheck(ctx,setting):
	c.execute("SELECT status FROM settings WHERE serverid = %s AND setting = %s",(ctx.message.server.id,setting,))
	state = c.fetchone()
	return state

def settingcheckmember(member,setting):
	c.execute("SELECT status FROM settings WHERE serverid = %s AND setting = %s",(member.server.id,setting,))
	state = c.fetchone()
	return state

create_table()
