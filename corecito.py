#!/usr/bin/env python3
import asyncio
import time
import logging
import cryptocom.exchange as cro
from cryptocom.exchange.structs import Pair
from cryptocom.exchange.structs import PrivateTrade

CRYPTOCOM_API_KEY = "MY_KEY"
CRYPTOCOM_API_SECRET = "MY_SECRET"

DEFAULT_CORE_NUMBER = 2 # Ethers

async def main():
  safe_mode_on = True # Set to False to enable trading, True just prints to the console log what it would do
  logger = setupLogger('logfile.log')
  exchange = cro.Exchange()
  account = cro.Account(api_key=CRYPTOCOM_API_KEY, api_secret=CRYPTOCOM_API_SECRET)
  core_number = DEFAULT_CORE_NUMBER
  pair = cro.pairs.ETH_BTC
  base_currency = 'BTC'
  core_number_currency = 'ETH'

  # Get BTC/ETH ticker info
  tickers = await exchange.get_tickers()
  ticker = tickers[pair]
  buy_price = ticker.buy_price
  sell_price = ticker.sell_price
  high = ticker.high
  low = ticker.low
  logger.info(f'\nMarket {pair.name}\nbuy price: {buy_price} - sell price: {sell_price} <> low: {low} - high: {high}\n')

  # EXAMPLE ticker = MarketTicker(pair=Pair(name='ETH_BTC'), 
    # buy_price=0.027638, sell_price=0.027641, trade_price=0.027641, 
    # time=1608466157, volume=10596.948, 
    # high=0.028549, low=0.027439, change=-0.001)

  # Get my BTC balance
  balances = await account.get_balance()
  btc_balance = balances[cro.coins.BTC]
  btc_available = btc_balance.available
  # EXAMPLE btc_balance:Balance(total=0.04140678, available=3.243e-05, in_orders=0.04137435, in_stake=0, coin=Coin(name='BTC'))

  # Get my ETH balance
  eth_balance = balances[cro.coins.ETH]

  logger.info(f'Balances\nBTC balance:{btc_balance} \nETH balance:{eth_balance}\n')

  ###########################
  # Core Number Adjustments #
  ###########################
  deviated_core_number = btc_available / buy_price
  logger.info(f'Core number adjustments')
  logger.info(f'Core number: {core_number} {core_number_currency}')
  logger.info(f'Deviated Core number:{deviated_core_number:.6f} {core_number_currency}')
  excess = deviated_core_number - core_number
  increase_percentage = excess * 100 / core_number
  missing = core_number - deviated_core_number
  decrease_percentage = missing * 100 / core_number

  if coreNumberExploded(core_number, deviated_core_number):
    logger.info(f'> Exploded {increase_percentage:.2f}%\nConsider updating CoreNumber to {deviated_core_number:.6f}')

  elif coreNumberIncreased(core_number, deviated_core_number):
    logger.info(f'Increased {increase_percentage:.2f}% - excess of {excess:.6f} {core_number_currency} denominated in {base_currency}')
    tx_result = excess * buy_price
    logger.info(f'\n\n>>> Selling: {tx_result:.6f} {base_currency} at {buy_price} to park an excess of {excess:.6f} {core_number_currency}\n')
    # Sell excess BTC => Buy ETH
    if (not safe_mode_on):
      await account.buy_market(pair, excess)

  elif coreNumberDecreased(core_number, deviated_core_number):
    logger.info(f'Decreased {decrease_percentage:.2f}% - missing {missing:.6f} {core_number_currency} denominated in {base_currency}')
    tx_result = missing * sell_price
    logger.info(f'\n\n>>> Buying: {tx_result:.6f} {base_currency} at {buy_price} taking {missing:.6f} {core_number_currency} from reserves\n')
    # Buy missing BTC => Sell ETH
    if (not safe_mode_on):
      await account.sell_market(pair, missing)

  elif coreNumberPlummeted(core_number, deviated_core_number):
    logger.info(f'> Plummeted {decrease_percentage:.2f}%\nConsider updating CoreNumber to {deviated_core_number:.6f}')

  else:
    logger.info(f'> Price is rock-solid stable')

  # Update balances after adjusting to core number
  balances = await account.get_balance()
  logger.info(f'Final BTC available:{balances[cro.coins.BTC].available} - ETH available:{balances[cro.coins.ETH].available}\n')





def coreNumberIncreased(core_number, deviated_core_number):
  min_core_number_increase = core_number * 1.03 # >3% increase
  max_core_number_increase = core_number * 1.10 # <10% increase
  return deviated_core_number >= min_core_number_increase and deviated_core_number <= max_core_number_increase

def coreNumberExploded(core_number, deviated_core_number):
  max_core_number_increase = core_number * 1.10 # >10% increase
  return deviated_core_number > max_core_number_increase

def coreNumberDecreased(core_number, deviated_core_number):
  min_core_number_decrease = core_number * 0.97 # >3% decrease
  max_core_number_decrease = core_number * 0.90 # <10% decrease
  return deviated_core_number <= min_core_number_decrease and deviated_core_number >= max_core_number_decrease

def coreNumberPlummeted(core_number, deviated_core_number):
  max_core_number_decrease = core_number * 0.90 # >10% decrease
  return deviated_core_number < max_core_number_decrease

def setupLogger(log_filename):
  logger = logging.getLogger('CN')
  
  file_log_handler = logging.FileHandler(log_filename)
  logger.addHandler(file_log_handler)

  stderr_log_handler = logging.StreamHandler()
  logger.addHandler(stderr_log_handler)

  # nice output format
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_log_handler.setFormatter(formatter)
  stderr_log_handler.setFormatter(formatter)

  logger.setLevel('DEBUG')
  return logger



asyncio.get_event_loop().run_until_complete(main())