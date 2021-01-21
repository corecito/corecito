class Mocked:
  config = {
    "corecito_exchange": "binance",
    "api_key": "binance-api-key",
    "api_secret": "binance-api-secret",
    "core_number": 1000,
    "min_price_stop": 5000,
    "max_price_stop": 11500,
    "min_core_number_increase_percentage": 10,
    "max_core_number_increase_percentage": 20,
    "min_core_number_decrease_percentage": 10,
    "max_core_number_decrease_percentage": 20,
    "binance_trading_pair": "BTCEUR",
    "binance_core_number_currency": "EUR",
    "binance_base_currency": "BTC",
    "binance_max_decimals_buy": 6,
    "binance_max_decimals_sell": 6,
    "is_fiat": True,
    "safe_mode_on": False,
    "test_mode_on": True,
    "telegram_notifications_on": False,
    "telegram_notify_errors": False,
    "telegram_bot_token": "telegram-token",
    "telegram_user_id": "telegram-user"
  }

  balances = {
    "base_currency_balance": 0.1,
    "base_currency_available": 0.1,
    "core_number_currency_balance": 0,
    "core_number_currency_available": 0
  }

  def config_for_test_core_deviated_sell_excess():
    return Mocked.config

  def config_for_test_price_rock_solid_do_not_sell():
    return Mocked.config

  def config_for_test_exceeded_max_price_do_not_sell():
    return Mocked.config

  def config_for_test_exceeded_max_core_number_increase_percentage_do_not_sell():
    config = Mocked.config
    config["max_price_stop"] = 13000
    return config

  async def get_tickers_for_test_core_deviated_sell_excess(self):
    return {"buy_price": 11000, "sell_price": 11000}

  async def get_tickers_for_test_price_rock_solid_do_not_sell(self):
    return {"buy_price": 10500, "sell_price": 10500}

  async def get_tickers_for_test_exceeded_max_price_do_not_sell(self):
    return {"buy_price": 11501, "sell_price": 11501}

  async def get_tickers_for_test_exceeded_max_core_number_increase_percentage_do_not_sell(self):
    return {"buy_price": 12001, "sell_price": 12001}

  async def get_balances_for_test_core_deviated_sell_excess(self):
    return Mocked.balances

  async def get_balances_for_test_price_rock_solid_do_not_sell(self):
    return Mocked.balances

  async def get_balances_for_test_exceeded_max_price_do_not_sell(self):
    return Mocked.balances

  async def get_balances_for_test_exceeded_max_core_number_increase_percentage_do_not_sell(self):
    return Mocked.balances
