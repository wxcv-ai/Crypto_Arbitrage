# Crypto_Arbitrage
this is a project that takes advantages of the crypto market inefficiencies to make a profit out of it (in my case I used the BITMEX exchange as an example but with some modification it can work at any exchange in the world)


this ReadME file is designed to give you a general idea about the project idea and architecture

The theory behind the project (the goal) :

the crypto market is new to the financial sector in general with lots of coins and tokens that suffer from iliquidity and here it comes our opportunity
so to simplfy the caluclation I am going to use prices of my own 
let's say :
btc/usdt = 1000$
eth/usdt = 700$
eth/btc = 0.6
this is a triangular arbitrage opportunity 
we can move our moeny as follow btc--> eth ---> usdt --> btc and 
we started with btc and ended up with btc and we made a profit 
let's go back to the example :
first sell the eth/btc pair --> to conver btc to eth so  btc = 1/0.6 eth = 1.66 eth
now we transfer the eth to usdt --> usdt = 1.66*700 = 1162 
and finally back to btc --> btc = 1162/1000 = 1.162
and here we are we started from 1 btc and we ended up with 1.162 btc which is 16.2% profit  (of course in real life it is so much smaller like 0.5% but we can make this transaction thousands of times a month wihch add up over time to make a nice profit overall
to better understand what triangular arbitrage is you can watch this video (in this video it talks about forex but the concept is the same ) :https://www.youtube.com/watch?v=lKu2LAgEcpU


The architecturre :

this project is decomposed into four  parts :
all_pairs : which collects al the avaiable asset classes in the exchange and other necessary data stucture
live feed : which takes the live orderbook prices from the exchange and store them in a database
arbitrage modules : this is where the algoithmic part of the arbitrage function resides it cointaines the classes and functions that perform tasks such as : choose the oath od triangular arbitrage that cna make money , loop in diffrent prices , monitor the gap of the divergence between the prices , ...
arbitrage_execution : this is the part where it uses the previous two to make a real time profit or loss for the triangular pairs that we chssen and notfy us when an opportunity comes into play


