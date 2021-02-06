import json
import multiprocessing
import os
# from all_pairs import *
import time
from multiprocessing import freeze_support

from websocket import create_connection

print("started")


class connection:

	def handle_msg (self,mssg,ws) :
		response =  ws.recv()
		msg = json.loads(response)
		#print(msg)
		if msg['m'] == 'bbo':
			lowest_ask = msg['data']['ask']
			highest_bid = msg['data']['bid']
			order_book={}
			order_book['ask'] = lowest_ask
			order_book['bid'] = highest_bid
			#DSN = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/bitmax"
			#conn = await asyncpg.connect(DSN)
			#UPDATE_TABLE = 'UPDATE live_feed SET live_feed ='  +"'"+str(order_book).replace("'",'"')+ "'"+' WHERE pair =  ' + "'"+str(pair)+"'"
			#print(UPDATE_TABLE)
			#await conn.execute(UPDATE_TABLE)
			#await conn.close()
			#print(msg["symbol"])
		if msg['m'] == 'ping':

			ping_msg = {"op": "pong"}
			ws.send(json.dumps(ping_msg))
			print(ping_msg)		
		return 0

	def initiations(self,pair):

		wbs_url = "wss://bitmax.io/1/api/pro/v1/stream"
		ws = create_connection(wbs_url)
		subscribe_msg= { "op": "sub", "id": str(pair) ,"ch":"bbo:"+pair+""}
		ws.send(json.dumps(subscribe_msg))	
		
		connected = True 
		while connected:
			try:
				
				response = ws.recv()
				msg = json.loads(response)

				connection().handle_msg(msg,ws)
				time.sleep(2)		
			except:
				reloaded_pairs.append(pair)
				break
		return 0

	def start (self ,reloaded_pairs,pairs) :
		if len(reloaded_pairs) == 0:
			for pair in pairs:
				print(pair)

				p = multiprocessing.Process(target=connection().initiations, args= (pair,))
				freeze_support()
				os.fork()
				p.start()
				
				

		else:
			for pair in reloaded_pairs:
				p = multiprocessing.Process(target=connection().initiations, args= (pair,))
				freeze_support()
				os.fork()
				p.start()
				freeze_support()
				reloaded_pairs.pop(pair)



		return 0





pairs = ["BTC/USDT","ETH/USDT","EOS/USDT"]

reloaded_pairs = []



connection().start (reloaded_pairs,pairs)

while True :
	
	if len(reloaded_pairs) == 0:
		pass

	else:
		pair = reloaded_pairs[0]
		p = multiprocessing.Process(target=connection().initiations, args=(pair,))
		p.start()
		reloaded_pairs.pop(pair)


