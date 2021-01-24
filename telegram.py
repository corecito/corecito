#!/usr/bin/env python3
import asyncio
import requests

class Telegram:
  """Configures Telegram object with info from the provided config"""
  def __init__(self, config):
    self.url = 'https://api.telegram.org/bot'
    self.action = '/sendMessage?chat_id='
    self.params = '&parse_mode=Markdown&text='
    self.bot_token = config.get('telegram_bot_token')
    self.bot_chatId = config.get('telegram_user_id')
    self.notifications_on = config.get('telegram_notifications_on')
    self.notify_errors_on = config.get('telegram_notify_errors')


  def send(self, bot_message):
    send_text = self.url + self.bot_token + self.action + str(self.bot_chatId) + self.params + bot_message
    response = requests.get(send_text)

    return response.json()
