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
	c.execute('CREATE TABLE IF NOT EXISTS settings(setting TEXT, status TEXT)')

def defaults():
	c.execute("INSERT INTO settings VALUES(moderation,off)")

"""
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS currency()')
"""

def display():
	c.execute('SELECT setting, status FROM settings')
	rows = c.fetchall()
	lines = '\n'.join(f'{i+1}. {line}' for i, line in enumerate(rows))
	return lines


create_table()
defaults()
