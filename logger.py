#!/usr/bin/env python3
import logging

class Logger:
  """Handles everything that has to do with logging, telegram notifications, etc"""
  def __init__(self, exchange=''):
    exchange_str = '_'
    if exchange:
      exchange_str += exchange
    self.logger = setupLogger('logfile' + exchange_str + '.log')

  def info(self, msg, *args, **kwargs):
    self.logger.info(msg, *args, **kwargs)

  def logPriceExploded(self, price, max_price_stop, trading_pair, telegram):
    log_message = f'>> {trading_pair} price exploded to {price:.6f}, exceeding the max price to stop corecito {max_price_stop:.6f}'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logPricePlummeted(self, price, min_price_stop, trading_pair, telegram):
    log_message = f'>> {trading_pair} price plummeted to {price:.6f}, below the min price to stop corecito {min_price_stop:.6f}'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logCoreNumberExploded(self, increase_percentage, deviated_core_number, telegram):
    log_message = f'> Exploded {increase_percentage:.2f}%\nConsider updating CoreNumber to {deviated_core_number:.6f}'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logCoreNumberIncreased(self, increase_percentage, excess, core_number_currency, base_currency, telegram):
    log_message = f'Increased {increase_percentage:.2f}% - excess of {excess:.6f} {core_number_currency} denominated in {base_currency}'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logSellExcess(self, tx_result, base_currency, buy_price, excess, core_number_currency, telegram):
    log_message = f'\n\n>>> Selling: {tx_result:.6f} {base_currency} at {buy_price} to park an excess of {excess:.6f} {core_number_currency}\n'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logCoreNumberDecreased(self, decrease_percentage, missing, core_number_currency, base_currency, telegram):
    log_message = f'Decreased {decrease_percentage:.2f}% - missing {missing:.6f} {core_number_currency} denominated in {base_currency}'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logBuyMissing(self, tx_result, base_currency, buy_price, missing, core_number_currency, telegram):
    log_message = f'\n\n>>> Buying: {tx_result:.6f} {base_currency} at {buy_price} taking {missing:.6f} {core_number_currency} from reserves\n'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logCoreNumberPlummeted(self, decrease_percentage, deviated_core_number, telegram):
    log_message = f'> Plummeted {decrease_percentage:.2f}%\nConsider updating CoreNumber to {deviated_core_number:.6f}'
    self.logger.info(log_message)
    if telegram and telegram.notifications_on:
      telegram.send(log_message)

  def logPriceStable(self, increase_percentage):
    log_message = f'> Price is rock-solid stable ({increase_percentage:.2f}%)'
    self.logger.info(log_message)

  def logException(self, exception, config, telegram):
    log_message = "Exception occurred -> '{}'. Waiting for next iteration... ({} seconds)\n\n\n".format(exception, config.get('seconds_between_iterations'))
    self.logger.info(log_message)
    if telegram and telegram.notifications_on and telegram.notify_errors_on:
      telegram.send(log_message)


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
