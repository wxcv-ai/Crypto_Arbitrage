import json
import requests
import asyncpg 
import asyncio
import subprocess

class assets :
	def pairs(self):
		self.base_url = "https://bitmax.io"
		self.quote_url = "/api/pro/v1/products"
		self.url = self.base_url+self.quote_url
		self.response = requests.request("GET", self.url)
		self.message = json.loads(self.response.text)
		self.final_message = self.message['data']
		pairs = []
		for symbol in self.final_message:
			self.symbol = symbol["symbol"]
			pairs.append(self.symbol)
		return pairs

	

	async def get_pairs(self):
		self.base_url = "https://bitmax.io"
		self.quote_url = "/api/pro/v1/products"
		self.url = self.base_url+self.quote_url
		self.response = requests.request("GET", self.url)
		self.message = json.loads(self.response.text)
		self.final_message = self.message['data']
		pairs = []
		self.exchange = 'bitmax'
		dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+self.exchange
		print('inserting pairs is in process ...')
		for symbol in self.final_message:
			self.symbol = symbol["symbol"]
			pairs.append(self.symbol)
			self.conn = await asyncpg.connect(dsn)
			self.INSERT_INTO_TABLE= 'INSERT INTO all_pairs (pair) VALUES ' +"("+"'"+str(self.symbol)+"'"+")"
			await self.conn.execute(self.INSERT_INTO_TABLE)
			await self.conn.close()
		print('all pairs has been inserted successfully')
		return pairs

	
assets().pairs()
asyncio.get_event_loop().run_until_complete(assets().get_pairs())




