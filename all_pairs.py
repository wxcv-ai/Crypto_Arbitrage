import json
import requests
import asyncpg 
import asyncio
import subprocess
def pairs():
	base_url = "https://bitmax.io"
	quote_url = "/api/pro/v1/products"
	url = base_url+quote_url
	response = requests.request("GET", url)
	message = json.loads(response.text)
	final_message = message['data']
	pairs = []
	for symbol in final_message:
		symbol = symbol["symbol"]
		pairs.append(symbol)
	return pairs

pairs()

async def get_pairs():
	base_url = "https://bitmax.io"
	quote_url = "/api/pro/v1/products"
	url = base_url+quote_url
	response = requests.request("GET", url)
	message = json.loads(response.text)
	final_message = message['data']
	pairs = []
	exchange = 'bitmax'
	dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+exchange
	print('inserting pairs is in process ...')
	for symbol in final_message:
		symbol = symbol["symbol"]
		pairs.append(symbol)
		conn = await asyncpg.connect(dsn)
		INSERT_INTO_TABLE= 'INSERT INTO all_pairs (pair) VALUES ' +"("+"'"+str(symbol)+"'"+")"
		await conn.execute(INSERT_INTO_TABLE)
		await conn.close()
	print('all pairs has been inserted successfully')
	return pairs

asyncio.get_event_loop().run_until_complete(get_pairs())




