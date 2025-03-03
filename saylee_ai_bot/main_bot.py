import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import requests
from datetime import datetime
import time
from db_manage import *
from parce_uzs_rate import get_uzs_rate, round_uzs
import os
import random
import json

# Load the JSON file
with open('saylee_ai_bot/constants.json', 'r') as file:
    config = json.load(file)

# Access the necessary values
BOT_API_KEY = config['telegram'][0]['bot_api_key']
CHANNEL_ID = config['telegram'][0]['channel_id']
DEVELOPERS_ID = config['telegram'][0]['developers_id']
HUMANIZATION_API_KEY = config['ai']['humanization']['api_key']
HUMANIZATION_ENDPOINT_SUBMIT = config['ai']['humanization']['endpoint_submit']
HUMANIZATION_ENDPOINT_OBTAIN = config['ai']['humanization']['endpoint_obtain']
USER_MODE = config['ai']['humanization']['mode']
bot = telebot.TeleBot(BOT_API_KEY)

# Example of accessing package details
packages = config['packages']
for package in packages:
    package_id = package['id']
    words = package['words']
    price_usd = package['price_usd']
    print(f"Package ID: {package_id}, Words: {words}, Price (USD): {price_usd}")

PENDING_PROOFS = {}
bot_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user_id = message.chat.id
    # TODO: Check if user already registered / if not got to registration options
    bot.send_message(
    message.chat.id,
    "👋 **Welcome to HumanizeBot!**\n\n"
    "🎯 I can help you humanize text to bypass AI detection.\n\n"
    "🔽 Use the buttons below to:\n"
    "• **Humanize your text** 🤖➡️👤\n"
    "• **Check your balance** 💰\n"
    "• **View top-up history** 📜",
    reply_markup=main_menu_markup(),
    parse_mode='Markdown'
    )

def main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('Humanize 👤'),
        KeyboardButton('Detector 🔍')
    )
    markup.add(
        KeyboardButton('Courses 📚')
    )
    markup.add(
        KeyboardButton('Ask4Help 🧑‍💻'),
        KeyboardButton('Profile 🏠')
    )
    return markup

