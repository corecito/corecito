from imports import *
from mocked import Mocked

class TestSell:
  def setup_logger_variable_handler(self):
    logger = logging.getLogger('CN')
    log_capture_string = StringIO()
    log_handler = logging.StreamHandler(log_capture_string)
    logger.addHandler(log_handler)
    return log_capture_string


  def test_core_deviated_sell_excess(self, monkeypatch):
    monkeypatch.setattr(corecito, "get_config", Mocked.config_for_test_core_deviated_sell_excess)
    monkeypatch.setattr(CorecitoAccount, "get_tickers", Mocked.get_tickers_for_test_core_deviated_sell_excess)
    monkeypatch.setattr(CorecitoAccount, "get_balances", Mocked.get_balances_for_test_core_deviated_sell_excess)

    log_capture_string = self.setup_logger_variable_handler()

    asyncio.run(corecito.main())

    log_output = log_capture_string.getvalue()
    log_capture_string.close()

    assert "Working on Binance Exchange" in log_output
    assert "Market BTCEUR" in log_output
    assert "buy price: 11000.0" in log_output
    assert "sell price: 11000.0" in log_output
    assert "(Base) BTC balance:0.1" in log_output
    assert "(Core) EUR balance:0" in log_output
    assert "Core number adjustments" in log_output
    assert "Core number: 1000 EUR" in log_output
    assert "Deviated Core number:1100.000000 EUR" in log_output
    assert "Increased 10.00% - excess of 100.000000 EUR denominated in BTC" in log_output
    assert "Selling: 0.009091 BTC at 11000.0 to park an excess of 100.000000 EUR" in log_output

    assert "Price is rock-solid stable" not in log_output


  def test_price_rock_solid_do_not_sell(self, monkeypatch):
    monkeypatch.setattr(corecito, "get_config", Mocked.config_for_test_price_rock_solid_do_not_sell)
    monkeypatch.setattr(CorecitoAccount, "get_tickers", Mocked.get_tickers_for_test_price_rock_solid_do_not_sell)
    monkeypatch.setattr(CorecitoAccount, "get_balances", Mocked.get_balances_for_test_price_rock_solid_do_not_sell)

    log_capture_string = self.setup_logger_variable_handler()

    asyncio.run(corecito.main())

    log_output = log_capture_string.getvalue()
    log_capture_string.close()

    assert "Working on Binance Exchange" in log_output
    assert "Market BTCEUR" in log_output
    assert "buy price: 10500.0" in log_output
    assert "sell price: 10500.0" in log_output
    assert "(Base) BTC balance:0.1" in log_output
    assert "(Core) EUR balance:0" in log_output
    assert "Core number adjustments" in log_output
    assert "Core number: 1000 EUR" in log_output
    assert "Deviated Core number:1050.000000 EUR" in log_output
    assert "Price is rock-solid stable (5.00%)" in log_output
    assert "Increased 5.00% - excess of 50.000000 EUR denominated in BTC" not in log_output

    assert "Selling:" not in log_output


  def test_exceeded_max_price_do_not_sell(self, monkeypatch):
    monkeypatch.setattr(corecito, "get_config", Mocked.config_for_test_exceeded_max_price_do_not_sell)
    monkeypatch.setattr(CorecitoAccount, "get_tickers", Mocked.get_tickers_for_test_exceeded_max_price_do_not_sell)
    monkeypatch.setattr(CorecitoAccount, "get_balances", Mocked.get_balances_for_test_exceeded_max_price_do_not_sell)

    log_capture_string = self.setup_logger_variable_handler()

    asyncio.run(corecito.main())

    log_output = log_capture_string.getvalue()
    log_capture_string.close()

    assert "Working on Binance Exchange" in log_output
    assert "Market BTCEUR" in log_output
    assert "buy price: 11501.0" in log_output
    assert "sell price: 11501.0" in log_output
    assert "(Base) BTC balance:0.1" in log_output
    assert "(Core) EUR balance:0" in log_output
    assert "Core number adjustments" in log_output
    assert "Core number: 1000 EUR" in log_output
    assert "Deviated Core number:1150.100000 EUR" in log_output
    assert "BTCEUR price exploded to 11501.000000, exceeding the max price to stop corecito 11500.000000" in log_output

    assert "Selling:" not in log_output

  def test_exceeded_max_core_number_increase_percentage_do_not_sell(self, monkeypatch):
    monkeypatch.setattr(corecito, "get_config", Mocked.config_for_test_exceeded_max_core_number_increase_percentage_do_not_sell)
    monkeypatch.setattr(CorecitoAccount, "get_tickers", Mocked.get_tickers_for_test_exceeded_max_core_number_increase_percentage_do_not_sell)
    monkeypatch.setattr(CorecitoAccount, "get_balances", Mocked.get_balances_for_test_exceeded_max_core_number_increase_percentage_do_not_sell)

    log_capture_string = self.setup_logger_variable_handler()

    asyncio.run(corecito.main())

    log_output = log_capture_string.getvalue()
    log_capture_string.close()

    assert "Working on Binance Exchange" in log_output
    assert "Market BTCEUR" in log_output
    assert "buy price: 12001.0" in log_output
    assert "sell price: 12001.0" in log_output
    assert "(Base) BTC balance:0.1" in log_output
    assert "(Core) EUR balance:0" in log_output
    assert "Core number adjustments" in log_output
    assert "Core number: 1000 EUR" in log_output
    assert "Deviated Core number:1200.100000 EUR" in log_output
    assert "Exploded 20.01%" in log_output
    assert "Consider updating CoreNumber to 1200.100000" in log_output

    assert "Selling:" not in log_output
