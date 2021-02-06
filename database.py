import asyncio 
import asyncpg
from all_pairs import *

async def DELETE_ALL (exhcnage_name,dsn) :
	conn = await asyncpg.connect(dsn)
	try :
		DATABASE_DELETE = " DROP DATABASE  " + exhcnage_name
		await conn.execute(DATABASE_DELETE)
		print('deleting the database '+exhcnage_name)
	except :
		print("fail")
		pass
	try :
		DROP_TABLE = "  DROP  TABLE  live_feed "
		await conn.execute(DROP_TABLE)
		print('deleting the table live_feed')
	except :
		pass
	try :
		DATABASE_CREATE = "CREATE DATABASE " + exhcnage_name
		await conn.execute(DATABASE_CREATE)
		print('creating database '+exhcnage_name)
	except :
		pass

	await conn.close()
	return(0)

pairs = pairs()

async def CREATE_ALL (exhcnage_name,dsn) :
	conn = await asyncpg.connect(dsn)
	try:
		CREATE_TABLE  = '''CREATE TABLE live_feed (pair varchar(500),live_feed jsonb ) '''
		await conn.execute(CREATE_TABLE)
		print("creating the table live_feed")	
	except:
		pass
	try :
		CREATE_TABLE  = '''CREATE TABLE all_pairs (pair varchar(500) ) '''
		await conn.execute(CREATE_TABLE)
		print("creating the table all_pairs")
		
		pairs = pairs()
		for pair in pairs :
			DSN = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+exhcnage_name
			conn = await asyncpg.connect(DSN)
			order_book = {'ask':'0000'}
			INSERT_INTO_TABLE= 'INSERT INTO live_feed (pair,live_feed) VALUES ' +"("+"'"+ pair+"'" +","+"'"+str(order_book).replace("'",'"')+"'"+")"
			
			await conn.execute(INSERT_INTO_TABLE)
			await conn.close()
		print("all pairs has been initiates sucessfully")
	except :
		pass
	await conn.close()
	return(0)
	



exhcnage_name = 'bitmax'
total_dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/postgres"
asyncio.get_event_loop().run_until_complete(DELETE_ALL(exhcnage_name,total_dsn))

exhcnage_name = 'bitmax'
exchange_dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+exhcnage_name
asyncio.get_event_loop().run_until_complete(CREATE_ALL(exhcnage_name,exchange_dsn))

