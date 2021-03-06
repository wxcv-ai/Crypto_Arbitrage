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
		self.response =  ws.recv()
		self.msg = json.loads(self.response)
		#print(msg)
		if self.msg['m'] == 'bbo':
			self.lowest_ask = self.msg['data']['ask']
			self.highest_bid = self.msg['data']['bid']
			self.order_book={}
			self.order_book['ask'] = self.lowest_ask
			self.order_book['bid'] = self.highest_bid
			#DSN = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/bitmax"
			#conn = await asyncpg.connect(DSN)
			#UPDATE_TABLE = 'UPDATE live_feed SET live_feed ='  +"'"+str(order_book).replace("'",'"')+ "'"+' WHERE pair =  ' + "'"+str(pair)+"'"
			#print(UPDATE_TABLE)
			#await conn.execute(UPDATE_TABLE)
			#await conn.close()
			print(self.msg["symbol"])
		if self.msg['m'] == 'ping':

			self.ping_msg = {"op": "pong"}
			ws.send(json.dumps(self.ping_msg))
			print(self.ping_msg)		
		return 0

	def initiations(self,pair):

		self.wbs_url = "wss://bitmax.io/1/api/pro/v1/stream"
		self.ws = create_connection(self.wbs_url)
		self.subscribe_msg= { "op": "sub", "id": str(pair) ,"ch":"bbo:"+pair+""}
		self.ws.send(json.dumps(self.subscribe_msg))	
		
		self.connected = True 
		while self.connected:
			try:
				
				self.response = self.ws.recv()
				self.msg = json.loads(self.response)

				connection().handle_msg(self.msg,self.ws)
				time.sleep(2)		
			except:
				self.reloaded_pairs.append(pair)
				break
		return 0

	def start (self,reloaded_pairs,pairs) :
		if len(reloaded_pairs) == 0:
			for pair in pairs:
				print(pair)

				p = multiprocessing.Process(target=connection().initiations, args=(pair,))
				freeze_support()
				os.fork()
				freeze_support()
				os.fork()
				p.start()
				
				

		else:
			for pair in reloaded_pairs:
				p = multiprocessing.Process(target=connection().initiations, args= (pair,))
				freeze_support()
				os.fork()
				freeze_support()
				p.start()

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


