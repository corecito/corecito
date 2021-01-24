#!/usr/bin/env python3
import asyncio
import traceback
import cryptocom.exchange as cro
from config import Config
from corecito_account import CorecitoAccount
from telegram import Telegram
from logger import Logger

async def main():
  config = Config()

  logger = Logger(config.get('corecito_exchange'))

  account = CorecitoAccount(config=config)
  logger.logger.info(f'Working on {account.exchange.capitalize()} Exchange\n')

  telegram = Telegram(config=config)

  iteration = 0

  fiat = config.get('is_fiat')

  tx_price = 0

  while True:
    try:
      iteration += 1
      print(f'------------ Iteration {iteration} ------------')
      # Get pair ticker info. i.e. BTC/ETH, BTC/EUR, etc...
      ticker = await account.get_tickers()
      buy_price = float(ticker["buy_price"])
      sell_price = float(ticker["sell_price"])
      logger.info(f'\nMarket {account.pair}\nbuy price: {buy_price} - sell price: {sell_price}\n')

      # Get my base and Core Number currency balances
      balances = await account.get_balances()

      logger.info(f"Balances\n(Base) {account.base_currency} balance:{balances['base_currency_balance']} \n(Core) {account.core_number_currency} balance:{balances['core_number_currency_balance']}\n")

      ###########################
      # Core Number Adjustments #
      ###########################

      # if 'fiat', balances are calculated by multiplying buy_price
      if fiat:
        deviated_core_number = balances['base_currency_available'] * buy_price
      else:
        deviated_core_number = balances['base_currency_available'] / buy_price

      logger.info(f'Core number adjustments')
      logger.info(f'Core number: {account.core_number} {account.core_number_currency}')
      logger.info(f'Deviated Core number:{deviated_core_number:.6f} {account.core_number_currency}')

      excess = round(deviated_core_number - account.core_number, account.max_decimals_buy)
      increase_percentage = excess * 100 / account.core_number
      missing = round(account.core_number - deviated_core_number, account.max_decimals_sell)
      decrease_percentage = missing * 100 / account.core_number

      if pricePlummeted(buy_price, account.min_price_stop):
        logger.logPricePlummeted(buy_price, account.min_price_stop, account.pair_name, telegram)

      elif priceExploded(buy_price, account.max_price_stop):
        logger.logPriceExploded(buy_price, account.max_price_stop, account.pair_name, telegram)

      elif coreNumberExploded(account.core_number, deviated_core_number, account.max_core_number_increase_percentage):
        logger.logCoreNumberExploded(increase_percentage, deviated_core_number, telegram)


      elif coreNumberIncreased(account.core_number, deviated_core_number, account.min_core_number_increase_percentage, account.max_core_number_increase_percentage):
        logger.logCoreNumberIncreased(increase_percentage, excess, account.core_number_currency, account.base_currency, telegram)
        #Check if 'fiat' is True to adjust messages format and tx_result var and 'excess' has to be divided by the buy_price
        if fiat:
          tx_result = round(excess / buy_price, account.max_decimals_buy)
          tx_price = buy_price
        else:
          tx_result = round(excess * sell_price, account.max_decimals_buy)
          tx_price = sell_price
        logger.logSellExcess(tx_result, account.base_currency, tx_price, excess, account.core_number_currency, telegram)

        # Sell excess of base currency ie. => in ETH_BTC pair, sell excess BTC => Buy ETH
        # If fiat, we sell the value previously calculated and stored on tx_result
        if (not config.get('safe_mode_on')):
          if fiat:
            await account.order_market_sell(tx_result)
          else:
            await account.order_market_buy(tx_result, excess)


      elif coreNumberDecreased(account.core_number, deviated_core_number, account.min_core_number_decrease_percentage, account.max_core_number_decrease_percentage):
        logger.logCoreNumberDecreased(decrease_percentage, missing, account.core_number_currency, account.base_currency, telegram)
        #Check is fiat is True to adjust messages format and tx_result var and 'missing' has to be divided by the sell_price
        if fiat:
          tx_result = round(missing / sell_price, account.max_decimals_sell)
          tx_price = sell_price
        else:
          tx_result = missing * buy_price
          tx_price = buy_price
        logger.logBuyMissing(tx_result, account.base_currency, tx_price, missing, account.core_number_currency, telegram)

        # Buy missing base currency; ie. => in ETH_BTC pair, buy missing BTC => Sell ETH
        if (not config.get('safe_mode_on')):
          if fiat:
            await account.order_market_buy(missing, tx_result)
          else:
            await account.order_market_sell(missing)


      elif coreNumberPlummeted(account.core_number, deviated_core_number, account.max_core_number_decrease_percentage):
        logger.logCoreNumberPlummeted(decrease_percentage, deviated_core_number, telegram)

      else:
        logger.logPriceStable(increase_percentage)

      # Update balances after adjusting to core number
      balances = await account.get_balances()
      logger.info(f"Final {account.base_currency} available:{balances['base_currency_available']} - {account.core_number_currency} available:{balances['core_number_currency_available']}")

      # Loop end
      print(f'------------ Iteration {iteration} ------------\n')
      if config.get('test_mode_on'):
        await asyncio.sleep(1)
        break
      else:
        # Wait given seconds until next poll
        logger.info("Waiting for next iteration... ({} seconds)\n\n\n".format(config.get('seconds_between_iterations')))
        await asyncio.sleep(config.get('seconds_between_iterations'))

    except Exception as e:
      # Network issue(s) occurred (most probably). Jumping to next iteration
      if config.get('test_mode_on'):
        logger.info("Exception occurred -> '{}'.\n\n\n".format(e))
        print(traceback.format_exc())
        await asyncio.sleep(1)
        break
      else:
        logger.logException(e, config, telegram)
        print(traceback.format_exc())
        await asyncio.sleep(config.get('seconds_between_iterations'))

def pricePlummeted(price, min_price_stop):
  if min_price_stop is None:
    return False
  return price < min_price_stop

def priceExploded(price, max_price_stop):
  if max_price_stop is None:
    return False
  return price > max_price_stop

def coreNumberIncreased(core_number, deviated_core_number, min_core_number_increase_percentage, max_core_number_increase_percentage):
  min_core_number_increase = core_number * (1 + (min_core_number_increase_percentage/100))
  max_core_number_increase = core_number * (1 + (max_core_number_increase_percentage/100))
  return deviated_core_number >= min_core_number_increase and deviated_core_number <= max_core_number_increase

def coreNumberExploded(core_number, deviated_core_number, max_core_number_increase_percentage):
  max_core_number_increase = core_number * (1 + (max_core_number_increase_percentage/100))
  return deviated_core_number > max_core_number_increase

def coreNumberDecreased(core_number, deviated_core_number, min_core_number_decrease_percentage, max_core_number_decrease_percentage):
  min_core_number_decrease = core_number * (1 - (min_core_number_decrease_percentage/100))
  max_core_number_decrease = core_number * (1 - (max_core_number_decrease_percentage/100))
  return deviated_core_number <= min_core_number_decrease and deviated_core_number >= max_core_number_decrease

def coreNumberPlummeted(core_number, deviated_core_number, max_core_number_decrease_percentage):
  max_core_number_decrease = core_number * (1 - (max_core_number_decrease_percentage/100))
  return deviated_core_number < max_core_number_decrease



loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(main())
except KeyboardInterrupt:
  pass
finally:
  print("Stopping Corecito...")
  loop.close()
