import itertools
import math
from itertools import permutations 
import pprint
from copy import deepcopy
import asyncpg
import asyncio
import json
import multiprocessing
from multiprocessing import Process
#import os


class exchanges_arbitrage :
	# this first section od this class is to find the right paths as necessary fro the number of loops that is specified
	#this function is to find currencies in all the specific pairs
	def currencies(self,pairs):
		currencies = []
		for pair in pairs :
			# this is the position of the "/" in the pair in order to seperate tge base and the quote currencies
			pos= pair.find('/')
			#the next two line is for the base and the quote currencies
			base = pair[:pos]
			quote = pair[pos+1:]

			currencies.append(base)
			currencies.append(quote)
		currencies = list(dict.fromkeys(currencies))
		return(currencies)
	#this function is to location each currecny with the pairs that it is present in
	def currency_and_pairs(self,pairs,currencies) :
		data = {}
		for currency in currencies :
			partitial_data = []
			for pair in pairs :
				# this is the position of the "/" in the pair in order to seperate tge base and the quote currencies
				pos= pair.find('/')
				#the next two line is for the base and the quote currencies
				base = pair[:pos]
				quote = pair[pos+1:]
				if currency == base or currency == quote :
					partitial_data.append(pair)
					data[currency] = partitial_data
		return(data)
	#this function is to find the arbitrage path from the base currency
	def base_addition(self,pairs,currency_and_pairs,data):
		total_data = []
		for pairs in data :
			for j in range(0,len(pairs)):
				pair = pairs[len(pairs)-1]
				# this is the position of the "/" in the pair in order to seperate tge base and the quote currencies
				pos= pair.find('/')
				#the next two line is for the base and the quote currencies
				base = pair[:pos]
				quote = pair[pos+1:]
				base_of_pairs = currency_and_pairs[base]
				quote_of_pairs = currency_and_pairs[quote]			
				for i in range(0,len(base_of_pairs)):
					new_data = pairs.copy()
					if base_of_pairs[i] in pairs :
						pass
					else :
						new_data.append(base_of_pairs[i])
						total_data.append(new_data)
		return(total_data)
	#this function is to find the arbitrage path from the quote currency
	def quote_addition(self,pairs,currency_and_pairs,data):
		total_data = []
		for pairs in data :
			for j in range(0,len(pairs)):
				pair = pairs[len(pairs)-1]
				# this is the position of the "/" in the pair in order to seperate tge base and the quote currencies
				pos= pair.find('/')
				#the next two line is for the base and the quote currencies
				base = pair[:pos]
				quote = pair[pos+1:]
				base_of_pairs = currency_and_pairs[base]
				quote_of_pairs = currency_and_pairs[quote]			
				for i in range(0,len(quote_of_pairs)):
					new_data = pairs.copy()
					if quote_of_pairs[i] in pairs :
						pass
					else :
						new_data.append(quote_of_pairs[i])
						total_data.append(new_data)
		return(total_data)
	#this function is designed the currency that begins the path circulation
	# example two pairs btc/usdt and usdt/eth .....
	# the currenct is btc in orde to star tthe path 
	def find_the_currency(self,path):
		pair1 = path[0]
		pair2 = path[1]
		pos1= pair1.find('/')
		#the next two line is for the base and the quote currencies
		base1 = pair1[:pos1]
		quote1 = pair1[pos1+1:]
		pos2= pair2.find('/')
		#the next two line is for the base and the quote currencies
		base2 = pair2[:pos2]
		quote2 = pair2[pos2+1:]
		if base1 != base2 or base1 != quote2 :
			currency= base1
		if quote1 != base2 or quote1 != quote2 :
			currency= quote1
		return(currency)
	#thhis fucntion is to check if the path is possible 
	#example of impossible paths :
	# btc/usdt usdt/eth usdt/eos
	def possible_path(self,path):
		response = 'true'
		currencies = []
		for pair in path :
			# this is the position of the "/" in the pair in order to seperate tge base and the quote currencies
			pos= pair.find('/')
			#the next two line is for the base and the quote currencies
			base = pair[:pos]
			quote = pair[pos+1:]
			currencies.append(base)
			currencies.append(quote)
		for currency in currencies :
			num = currencies.count(currency)
			if num > 2 :
				response = 'false'
			else : 
				pass
		return(response)
	#this function to combine the base and quote path and find the desierd path 
	def four_way_arbitrage(self,pairs,currency_and_pairs,data_x):
		data = data_x
		data = exchanges_arbitrage().base_addition(pairs,currency_and_pairs,data)
		data = exchanges_arbitrage().quote_addition(pairs,currency_and_pairs,data)
		return(data)
	#this function is using the last functions in one place
	def total_paths (self,pairs) :
		data = []
		for pair in pairs :
			new_data = []
			new_data.append(pair)
			data.append(new_data)
		currencies =  exchanges_arbitrage().currencies(pairs)
		currency_and_pairs = exchanges_arbitrage().currency_and_pairs(pairs,currencies)
		additions = exchanges_arbitrage().four_way_arbitrage(pairs , currency_and_pairs , data)
		paths = []
		for new_path in additions :
			response = exchanges_arbitrage().possible_path(new_path)
			if response == 'false' :
				pass
			else:
				paths.append(new_path)
		fianl_paths = []
		for path in paths :
			currecny = exchanges_arbitrage().find_the_currency(path)
			length = len(path)
			if currecny in path[length-1] :
				fianl_paths.append(path)
		return(fianl_paths)

class exchanges_permutation :
	#this function is to seperate each exchange with its correspanding pairs
	def pairs_to_exchanges (all_pairs_of_all_exchanges,all_pairs_of_all_exchanges_sperated_by_exchange):
		data = {}
		for pair in all_pairs_of_all_exchanges :
			liste = []
			for exchange_pairs in all_pairs_of_all_exchanges_sperated_by_exchange :
				all_pairs_f_a_particular_exchnage = all_pairs_of_all_exchanges_sperated_by_exchange[exchange_pairs]
				if pair in all_pairs_f_a_particular_exchnage :
					liste.append(exchange_pairs)
					data[pair] = liste
		return(data)
	# this function is just to delete any duplicates of tuples in a liste of tuples 
	def removeDuplicates(lst): 

		return [t for t in (set(tuple(i) for i in lst))] 
	# this function is designed to find the majro permutation
	def major_permutations (self,liste):
		new_liste = list(itertools.permutations(list(liste)))
		for i in range(0,len(new_liste)) :
			new_liste[i] = list(new_liste[i])
		return(new_liste)
	#this function is designed to find all the secondary permutation from the major ones
	def possible_permutation_exchnages(self,exchange_liste,all_exchanges_permutations):
		data = []
		for exchange in exchange_liste :
			for permutation in all_exchanges_permutations :
				for i in range (0,len(permutation)) :
					if permutation[i] == exchange :
						pass
					else: 
						new_permutaion = list(permutation).copy()
						new_permutaion[i] = exchange
						if new_permutaion in data :
							pass
						else:
							data.append(new_permutaion)
		for permutations in all_exchanges_permutations :
			data.append(list(permutations))
		return(data)
	# this function is to delete duplicates and one exchange paths
	def delete_one_exchange_arbitrage(self,total,r) :
		data = []
		for j in range(0,len(total))  :
			tot  = total[j]
			for i in range(0,len(tot)) :
				counting = tot.count(tot[i]) 
				if counting == r :
					#print(tot)
					#print(j)
					pass
				else :
					if tot in data :
						pass
					else :
						data.append(list(tot))
		return(data)
	#this function is to combine the last  3 functions into one place 
	def total_exchanges_paths (self,exchange_liste) :
		# this for 1 repeated exchange in a list 
		major_permutations = exchanges_permutation().major_permutations(exchange_liste)
		# this for 2 repeated exchange in a list 
		permutation_exchnages_n1 = exchanges_permutation().possible_permutation_exchnages(exchange_liste,major_permutations)
		# this for 3 repeated exchange in a list 
		permutation_exchnages_n2 = exchanges_permutation().possible_permutation_exchnages(exchange_liste,permutation_exchnages_n1)
		# this is to orgonize the liste 
		permutation_exchnages_n2.sort()
		return (permutation_exchnages_n2)
	#this functuon is to check if a particualar path of pairs and exchanges can be arbitraged
	def check_if_pairs_in_exchanges (self,pairs_path,exchnage_path,pairs_to_exchanges):
		bool_value = 'false'
		results = []
		for pair in pairs_path :
			pair_index = pairs_path.index(pair)
			exchange_of_the_pair = exchnage_path[pair_index]
			pairs_of_the_exchnage = pairs_to_exchanges[exchange_of_the_pair]
			if pair in pairs_of_the_exchnage :
				results.append('true')
		if len(results) == len(pairs_path) :
			bool_value = 'true'
		return(bool_value)
	# this functuon will find all the  path of pairs and exchanges that can be arbitraged
	def final_pairs_to_exchanges (self,all_pairs_path,exchnage_path,pairs_to_exchanges):
		final_pairs_pathts = []
		for pairs_paths in all_pairs_path :
			if exchanges_permutation().check_if_pairs_in_exchanges (pairs_path,exchnage_path,pairs_to_exchanges) =='true' :
				final_pairs_pathts.append()
		return(final_pairs_pathts)
class price :

	# this function is to calculate the price
	def price_calculation(self,path,price,bid,ask):
		for pair in path :
			value = path[pair]
			if value == "3" :
				calculus = bid[pair]
				price += 1*calculus
			if value == "4" :
				calculus = ask[pair]
				price += 1/calculus

		return(price)
	# this function ues the previous buy_or_sell to fins the buy and sell of the path that we specify  
	def buy_sell_path(self,path,currency,pair) :
		#path = ['gol/btc', 'cyber/gol', 'cyber/usdt', 'usdt/uah']
		data = price().buy_or_sell(currency,pair,'',{})[0]
		currency2 =  price().buy_or_sell(currency,pair,'',{})[1]
		path.pop(0)
		for pair in path :
			data = price().buy_or_sell(currency2,pair,'',data)[0]
			currency2 =  price().buy_or_sell(currency2,pair,'',data)[1]
		return(data)
	# thsi function is designed to find if it is a buy or sell of that pair
	def buy_or_sell (self,currency,pair,currency2,data):
		total_data = []
		# this is the position of the "/" in the pair in order to seperate tge base and the quote currencies
		pos= pair.find('/')
		#the next two line is for the base and the quote currencies
		base = pair[:pos]
		quote = pair[pos+1:]
		if currency == base :
			data[pair] = "sell"
		if currency == quote :
			data[pair] = "buy"
		currency2 = ''
		if currency == base :
			currency2 = quote
		if currency == quote :
			currency2 = base
		total_data.append(data)
		total_data.append(currency2)
		#print(total_data)
		#print("\n")
		return(total_data)
	# this function is to find the currenyc of the buy_sell_path function
	# where pair one and two are the firdst two pairs in the desired path
	def choose_currency(self,pair_one,pair_two):
		currency = 'x'
		pos_one = pair_one.find('/')
		base_one = pair_one[:pos_one]
		quote_one = pair_one[pos_one+1:]

		pos_two = pair_two.find('/')
		base_two = pair_two[:pos_two]
		quote_two = pair_two[pos_two+1:]

		if base_one != base_two and base_one != quote_two :
			currency = base_one
		if quote_one != base_two and  quote_one != quote_two :
			currency = quote_one

		return(currency)
	# this function is designed to get 	the order_book necessary value from the database 
	def get_price_db (self,echange_name,pair,value) :
		# value can be either asks or bids
		dsn ="postgres://postgres:kirahavethedeathnote123A@localhost:5432/" + echange_name
		#conn = await asyncpg.connect(dsn)
		SELECT_STATEMENT = 'SELECT * FROM live_feed WHERE pair = ', pair
		#order_book = await conn.fetchrow(SELECT_STATEMENT)
		# value can be either asks or bids
		final_result = order_book[value]
		#await conn.close()
		return()
	# this function import all the prices of a specific path
	def get_all_prices_db (self,echange_name,pairs) :
		# value can be either asks or bids
		dsn ="postgres://postgres:kirahavethedeathnote123A@localhost:5432/" + echange_name
		bid_and_ask = []
		for pair in path :
			#conn = await asyncpg.connect(dsn)
			SELECT_STATEMENT = 'SELECT * FROM live_feed WHERE pair = ', pair
			#order_book = await conn.fetchrow(SELECT_STATEMENT)
			ask = order_book['asks']
			bid = order_book['bids']
			bid_and_ask.append(ask)
			bid_and_ask.append(bid)
			#await conn.close()
		return(bid_and_ask)


async def polling(path):
	price = 0
	exchange = 'bitmax'
	dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+exchange
	conn = await asyncpg.connect(dsn)


	for pair in path :
		
		value = path[pair]

		if value == "3" :
			dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+exchange
			conn = await asyncpg.connect(dsn)
			sql_pair = "'"+pair.upper()+"'"
			SELECT_STATEMENT = 'SELECT live_feed FROM live_feed WHERE pair = '+sql_pair
			result = await conn.fetch(SELECT_STATEMENT)
			await conn.close()
			dictionarry = dict(result[0])
			live_feed = dictionarry['live_feed']
			dict_live_feed = json.loads(live_feed)
			ask = dict_live_feed['ask']
			bid  = dict_live_feed['bid']
			order_book = []
			order_book.append(ask)
			order_book.append(bid)
			calculus = float(order_book[0][0])
			if price == 0 :
				price += 1*calculus
			else:
				price = price*calculus


		if value == "4" :
			dsn = "postgres://postgres:kirahavethedeathnote123A@localhost:5432/"+exchange
			conn = await asyncpg.connect(dsn)
			sql_pair = "'"+pair.upper()+"'"
			SELECT_STATEMENT = 'SELECT live_feed FROM live_feed WHERE pair = '+sql_pair
			
			result = await conn.fetch(SELECT_STATEMENT)
			await conn.close()
			dictionarry = dict(result[0])
			live_feed = dictionarry['live_feed']
			dict_live_feed = json.loads(live_feed)
			
			ask = dict_live_feed['ask']
			bid  = dict_live_feed['bid']
			order_book = []
			order_book.append(ask)
			order_book.append(bid)
			calculus = float(order_book[1][0])
			
			if price == 0 :
				
				price += 1/calculus
				
			else:

				price = price/calculus


	price = price-1

	return price



pairs =['LBA/BTC', 'BCH/USDT', 'BCH/BTC', 'EOS/BTC', 'LBA/ETH', 'ETC/USDT', 'EOS/USDT', 'ETC/ETH', 'BTC/USDT',
 'ZRX/ETH', 'BAT/ETH', 'ELF/ETH', 'XRP/BTC', 'LTC/USDT', 'BAT/BTC', 'LTC/BTC', 'BCH/ETH', 'ZIL/BTC', 'ZIL/ETH',
  'EOS/ETH', 'ETH/BTC', 'ZRX/BTC', 'SEELE/BTC', 'XRP/ETH', 'LFT/BTC', 'ETC/BTC', 'LFT/ETH', 'SEELE/ETH', 'LTC/ETH',
   'IOST/ETH', 'XRP/USDT', 'ETH/USDT', 'ELF/BTC', 'IOST/BTC', 'BTMX/BTC', 'BTMX/USDT', 'BSV/BTC', 'BSV/ETH', 'BSV/USDT',
    'BTMX/ETH', 'USDC/BTC', 'USDC/USDT', 'NEO/BTC', 'NEO/USDT', 'GAS/BTC', 'ONT/BTC', 'ONT/ETH', 'ONT/USDT', 'ONG/BTC',
     'ONG/ETH', 'ONG/USDT', 'COVA/BTC', 'COVA/ETH', 'COVA/USDT', 'LAMB/BTC', 'LAMB/ETH', 'LAMB/USDT', 'CVNT/BTC', 'CVNT/ETH',
      'XLM/BTC', 'XLM/ETH', 'XLM/USDT', 'LTO/BTC', 'LTO/USDT', 'QCX/BTC', 'QCX/USDT', 'ZEC/BTC', 'ZEC/USDT', 'ZEC/ETH', 'BXA/USDT'
       'XTZ/BTC', 'XTZ/ETH', 'RNT/USDT', 'PAX/USDT', 'BTC/USDC', 'ETH/USDC', 'BTC/PAX', 'ETH/PAX', 'TRX/USDT', 'BTT/USDT',
        'TRX/BTC', 'BTT/BTC', 'TRX/ETH', 'ANKR/USDT', 'ANKR/BTC', 'BNB/USDT', 'BNB/ETH', 'BNB/BTC', 'FET/USDT', 'FET/ETH',
         'FET/BTC', 'AERGO/USDT', 'AERGO/ETH', 'AERGO/BTC', 'FTM/USDT', 'FTM/BTC', 'DOS/USDT', 'DOS/BTC', 'HT/ETH', 'HT/USDT',
          'HT/BTC', 'BOLT/USDT', 'BOLT/BTC', 'BTMX/PAX', 'CHX/USDT', 'CHX/BTC', 'CHX/ETH', 'LBA/USDT', 'KCS/USDT', 'KCS/BTC',
           'ETZ/USDT', 'ETZ/BTC', 'DUO/USDT', 'DUO/BTC', 'VALOR/USDT', 'CELR/USDT', 'CELR/BTC', 'MIX/USDT', 'BHD/USDT', 'BHD/BTC',
            'FSN/USDT', 'FSN/BTC', 'ABBC/USDT', 'ABBC/BTC', 'OKB/USDT', 'OKB/BTC', 'BTMXP/USDT', 'BTMXP/BTC', 'DREP/USDT', 'DREP/BTC',
             'BAT/USDT', 'ELF/USDT', 'IOST/USDT', 'ZIL/USDT', 'ZRX/USDT', 'ADA/USDT', 'ADA/BTC', 'ADA/ETH', 'DASH/USDT', 'DASH/BTC',
              'DASH/ETH', 'GT/USDT', 'GT/BTC', 'GT/ETH', 'ALGO/USDT', 'ALGO/BTC', 'YAP/USDT', 'YAP/BTC', 'STPT/USDT', 'STPT/BTC',
               'MATIC/USDT', 'MATIC/BTC', 'CHR/USDT', 'CHR/BTC', 'CHR/ETH', 'COTI/USDT', 'COTI/BTC', 'XEM/USDT', 'XEM/BTC', 'XEM/ETH',
                'NEO/ETH', 'OKB/ETH', 'ATOM/USDT', 'ATOM/BTC', 'ATOM/ETH', 'LINK/USDT', 'LINK/BTC', 'LINK/ETH', 'LAMBS/USDT', 'LAMBS/BTC',
                 'LAMBS/ETH', 'CHZ/USDT', 'CHZ/BTC', 'DEEP/USDT', 'DEEP/BTC', 'RVN/BTC', 'HPB/USDT', 'HPB/BTC', 'FTT/USDT', 'FTT/BTC', 'MITX/USDT',
                  'MITX/BTC', 'ONE/USDT', 'ONE/BTC', 'FRM/USDT', 'FRM/BTC', 'TRY/USDT', 'TRY/BTC', 'MHC/USDT', 'MHC/BTC', 'UAT/USDT', 'UAT/BTC',
                   'LTO/ETH', 'ERD/USDT', 'ERD/BTC', 'PROM/USDT', 'PROM/BTC', 'INFT/USDT', 'INFT/BTC', 'WAN/USDT', 'WAN/BTC', 'RUNE/USDT', 'XTZ/USDT',
                    'QTUM/USDT', 'QTUM/BTC', 'DOGE/USDT', 'DOGE/BTC', 'XRPBEAR/USDT', 'XRPBULL/USDT', 'BTCBEAR/USDT', 'BTCBULL/USDT', 'CET/USDT',
                     'CET/BTC', 'BTM/USDT', 'BTM/BTC', 'CKB/USDT', 'VET/USDT', 'VET/BTC', 'RVN/USDT', 'TOKO/USDT', 'TOKO/BTC', 'KAVA/USDT', 'KAVA/BTC',
                      'BTCUSDT', 'XNS/USDT', 'XNS/BTC', 'FLEX/USDT', 'FLEX/BTC', 'DAD/USDT', 'EXCHBEAR/USDT', 'ETHBULL/USDT', 'EXCHBULL/USDT', 'ETHBEAR/USDT',
                       'LTCBULL/USDT', 'ALTBULL/USDT', 'LTCBEAR/USDT', 'ALTBEAR/USDT', 'EOSBULL/USDT', 'BNBBEAR/USDT', 'EOSBEAR/USDT', 'BNBBULL/USDT', 'OLT/USDT',
                        'VRA/USDT', 'BVOL/USDT', 'IBVOL/USDT', 'STAKE/USDT', 'RVX/USDT', 'BAND/USDT', 'BEPRO/USDT', 'FIO/USDT', 'ORN/USDT', 'SOL/USDT', 'SWINGBY/USDT',
                       'CRO/USDT', 'SWAP/USDT', 'SRM/USDT', 'GEEQ/USDT', 'JRT/USDT', 'SRM/BTC', 'DIA/USDT']


liste = ['binance','okcoin','hitbtc','zb','bitmax']

total_paths = exchanges_arbitrage().total_paths(pairs.copy())


#total_exchanges_paths = exchanges_permutation().total_exchanges_paths(liste)

#pprint.pprint(total_paths)
path = ['gol/btc', 'cyber/gol', 'cyber/usdt', 'usdt/uah']
path =  ['LINK/USDT', 'LINK/BTC', 'BTC/USDT']

buy_sell_path = price().buy_sell_path(path,price().choose_currency(path[0],path[1]),path[0])
#print(buy_sell_path)


#price_calculation = price().price_calculation(buy_sell_path,0, bids,asks)
#print(price_calculation)


print('arbitrage library has been loaded succefully ... OK')
#price = asyncio.get_event_loop().run_until_complete(polling(buy_sell_path))
#print(price * 100)


#print(len(pairs))

#pair= 'BTC/USDT'
#order_book = {"ask": ["18850", "0.02"], "bid": ["18840", "0.45"]}
#UPDATE_TABLE = 'UPDATE live_feed SET live_feed ='  +"'"+str(order_book).replace("'",'"')+ "'"+' WHERE pair =  ' + "'"+str(pair)+"'"
#print(UPDATE_TABLE)



