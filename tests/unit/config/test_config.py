from imports import *

class TestConfig:
  def test_parse_default_configuration(self):
    config = Config()

    assert len(config.data) == 26
    assert config.get("corecito_exchange") == "crypto.com"
    assert config.get("api_key") == "<your Crypto.com Exchange or Binance API key here>"
    assert config.get("api_secret") == "<your Crypto.com Exchange or Binance API secret here>"
    assert config.get("core_number") == 2
    assert config.get("min_price_stop") == None
    assert config.get("max_price_stop") == None
    assert config.get("min_core_number_increase_percentage") == 3
    assert config.get("max_core_number_increase_percentage") == 10
    assert config.get("min_core_number_decrease_percentage") == 3
    assert config.get("max_core_number_decrease_percentage") == 10
    assert config.get("cryptocom_trading_pair") == "ETH_BTC"
    assert config.get("cryptocom_core_number_currency") == "ETH"
    assert config.get("cryptocom_base_currency") == "BTC"
    assert config.get("cryptocom_max_decimals_buy") == 6
    assert config.get("cryptocom_max_decimals_sell") == 3
    assert config.get("binance_trading_pair") == "ETHBTC"
    assert config.get("binance_core_number_currency") == "ETH"
    assert config.get("binance_base_currency") == "BTC"
    assert config.get("binance_max_decimals_buy") == 6
    assert config.get("binance_max_decimals_sell") == 6
    assert config.get("is_fiat") == False
    assert config.get("safe_mode_on") == True
    assert config.get("test_mode_on") == True
    assert config.get("seconds_between_iterations") == 5
    assert config.get("telegram_notifications_on") == False
    assert config.get("telegram_notify_errors") == False
    assert config.get("telegram_bot_token") == "<bot token>"
    assert config.get("telegram_user_id") == "<your user id>"

  def test_parse_user_configuration(self, monkeypatch):
    monkeypatch.setattr(Config, "DEFAULT_USER_CONFIG_PATH", "tests/fixtures/config/user_config.yaml")
    config = Config()

    assert len(config.data) == 28
    for key in config.data:
      value = "test_" + key
      assert config.get(key) == value
