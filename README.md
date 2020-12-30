# Corecito

## Setting up

*python3
*To run this project, you may need to install the following python modules:

```
pip3 install cryptocom.exchange
pip3 install python-binance
pip3 install yaml
```

## Config

1. Duplicate "config/default_config.yaml" file
2. Rename it as "user_config.yaml" and add there your API keys and set the other values as you wish

Be careful! -> Do not set your API keys in default_config.yaml and push the file to git!

## Known issues

* INVALID_NONCE On All Requests: the issue occurs when the system clock of the client machine is greater than 1 second in the future, or 30 seconds in the past. Usually, re-syncing with the NTP time server on the client machine will correct the issue.
