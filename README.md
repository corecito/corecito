# Corecito

## Setting up

*Tested on python 3.8.2 and 3.7.8
*To run this project, you may need to install the following python modules:

```
pip3 install cryptocom.exchange
pip3 install python-binance
pip3 install pyyaml
```

For Telegram notifications, you'll also need to enable it in the config (set 'telegram_notifications_on' to True) and provide 'telegram_bot_token' and 'telegram_user_id' ([how to create your Telegram bot](https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e)

## Config

1. Duplicate "config/default_config.yaml" file
2. Rename it as "user_config.yaml" and add there your API keys and set the other values as you wish

Be careful! -> Do not set your API keys in default_config.yaml and push the file to git!

## Known issues

* INVALID_NONCE On All Requests: the issue occurs when the system clock of the client machine is greater than 1 second in the future, or 30 seconds in the past. Usually, re-syncing with the NTP time server on the client machine will correct the issue.
