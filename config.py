import yaml
import sys
from os.path import exists
from logger import Logger

class Config:
  DEFAULT_CONFIG_PATH = 'config/default_config.yaml'
  DEFAULT_USER_CONFIG_PATH = 'config/user_config.yaml'
  data = {}

  def __init__(self):
    self.data = self.load_config_file(self.get_file_path())
    self.check_config()

  def get(self, key):
    return self.data[key] if key in self.data else None

  def get_file_path(self, file_path=None):
    logger = Logger()
    if file_path is None:
      file_path = self.DEFAULT_USER_CONFIG_PATH
    if exists(file_path):
      logger.info('Found user configuration in "{}"'.format(file_path))
      return file_path
    elif exists(Config.DEFAULT_CONFIG_PATH):
      logger.info('Found default configuration in "{}"'.format(Config.DEFAULT_CONFIG_PATH))
      return Config.DEFAULT_CONFIG_PATH
    else:
      logger.error('Not possible to find any configuration file.')
      sys.exit(1)

  def load_config_file(self, file_path):
    try:
      config_file = open(file_path)
      data = yaml.load(config_file, Loader=yaml.FullLoader)
      config_file.close()
      return data
    except:
      logger.error('Not possible to open and/or parse the YAML configuration file "{}"'.format(file_path))
      logger.error(sys.exc_info()[0])
      sys.exit(1)

  def check_config(self):
    #TODO Move this method inside the class Crypto
    import cryptocom.exchange as cro
    if self.data['corecito_exchange'] == 'crypto.com':
      logger = Logger(self.data['corecito_exchange'])
      try:
        eval('cro.pairs.' + self.data['cryptocom_trading_pair'])
      except AttributeError:
        print('Trading pair "{}" does not exist (check your config_file)'.format(self.data['cryptocom_trading_pair']))
        sys.exit(1)
      try:
        eval('cro.coins.' + self.data['cryptocom_core_number_currency'])
      except AttributeError:
        print('Currency "{}" does not exist (check your config_file)'.format(self.data['cryptocom_core_number_currency']))
        sys.exit(1)
      try:
        eval('cro.coins.' + self.data['cryptocom_base_currency'])
      except AttributeError:
        print('Currency "{}" does not exist (check your config_file)'.format(self.data['cryptocom_base_currency']))
        sys.exit(1)
