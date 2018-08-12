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
	c.execute('CREATE TABLE IF NOT EXISTS settings(setting TEXT, status TEXT, serverid TEXT)')

"""
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS currency()')
"""

def display():
	c.execute('SELECT setting, status, serverid FROM settings')
	rows = c.fetchall()
	lines = '\n'.join(f'{i+1}. {line}' for i, line in enumerate(rows))
	return lines

def addserveronmessage(message):
	c.execute("SELECT serverid FROM settings")
	rows = c.fetchall()
	string = '\n'.join(str(row) for row in rows)
	if not str(message.author.server.id) in string:
		c.execute("INSERT INTO settings VALUES('moderation','off',%s)",(message.author.server.id))
		conn.commit()

create_table()
