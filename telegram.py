#!/usr/bin/env python3
import asyncio
import requests

class Telegram:
  """Configures Telegram object with info from the provided config"""
  def __init__(self, config=None):
    self.url = 'https://api.telegram.org/bot'
    self.action = '/sendMessage?chat_id='
    self.params = '&parse_mode=Markdown&text='
    self.bot_token = config['telegram_bot_token']
    self.bot_chatId = config['telegram_user_id']
    self.notifications_on = config['telegram_notifications_on']
    self.notify_errors_on = config['telegram_notify_errors']


  def send(self, bot_message):
    send_text = self.url + self.bot_token + self.action + str(self.bot_chatId) + self.params + bot_message
    response = requests.get(send_text)

    return response.json()
