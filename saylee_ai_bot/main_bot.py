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
    # Register the user
    try:
        response = register_user(user_id, "defaultpassword")  # Use a default password or generate one
        if 'detail' in response and response['detail'] == 'User already exists.':
            bot.send_message(user_id, "Welcome back! You are already registered.")
        else:
            bot.send_message(user_id, "You have been successfully registered!")
    except Exception as e:
        bot.send_message(user_id, f"An error occurred during registration: {str(e)}")
        return

    # Send welcome message
    bot.send_message(
        user_id,
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

@bot.message_handler(func=lambda message: message.text == 'Humanize 👤')
def prompt_humanize(message: Message):
    bot.send_message(
        message.chat.id,
        "📝 Send me the text you'd like to humanize. You can send multiple messages. Tap 'Done' when you're finished.",
        parse_mode='Markdown'
    )

    # Initialize a session to collect text
    user_id = message.chat.id
    bot_data[user_id] = {"text": "", "collecting": True}

    # Create reply markup with "Done" and "Cancel" buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton('Done'), KeyboardButton('Cancel'))
    bot.send_message(message.chat.id, "Waiting for your text...", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in bot_data and bot_data[message.chat.id]["collecting"])
def collect_text(message: Message):
    user_id = message.chat.id
    if user_id in bot_data:
        # Handle 'Done' and 'Cancel' commands
        if message.text == 'Done':
            finish_text_collection(message)
            return
        elif message.text == 'Cancel':
            cancel_text_collection(message)
            return

        bot_data[user_id]["text"] += " " + message.text
        # Calculate the current word count
        word_count = len(bot_data[user_id]["text"].split())

        # Notify the user that the text has been saved and show the word count
        bot.send_message(
            message.chat.id,
            f"📝 Your text has been saved. Current word count: {word_count}. You can continue sending messages or tap 'Done' when finished.",
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda message: message.text == 'Done')
def finish_text_collection(message: Message):
    user_id = message.chat.id
    if user_id in bot_data and bot_data[user_id]["collecting"]:
        bot_data[user_id]["collecting"] = False
        collected_text = bot_data[user_id]["text"]

        # Check if the collected text contains at least 100 words
        if len(collected_text.split()) < 100:
            bot.send_message(message.chat.id, "The input text must contain at least 100 words. Please continue sending your text.")
            bot_data[user_id]["collecting"] = True  # Allow user to continue sending text
            return

        # Proceed to humanize the collected text
        humanize_text(message, collected_text)
    else:
        bot.send_message(message.chat.id, "No text collected. Please start again.")
        # Proceed to humanize the collected text
        humanize_text(message, collected_text)
    # else:
    #     bot.send_message(message.chat.id, "No text collected. Please start again.")

@bot.message_handler(func=lambda message: message.text == 'Cancel')
def cancel_text_collection(message: Message):
    user_id = message.chat.id
    if user_id in bot_data:
        bot_data[user_id]["collecting"] = False
        bot_data[user_id]["text"] = ""  # Clear any collected text
        bot.send_message(message.chat.id, "Text collection has been canceled.", reply_markup=main_menu_markup())

def humanize_text(message: Message, text: str):
    # user_id = message.chat.id
    # user_data = get_user_data(user_id)

    # if not user_data:
    #     bot.send_message(message.chat.id, "Please use /start to register first.")
    #     return

    # trial_balance = int(user_data['trial_balance'])
    # balance = int(user_data['balance'])
    trial_balance = 1000
    balance = 1000

    total_balance = trial_balance + balance
    required_words = len(text.split())

    if total_balance <= 0:
        bot.send_message(message.chat.id, "You have no remaining trials or balance. Please contact support for more access.")
        return

    if required_words > total_balance:
        bot.send_message(
            message.chat.id,
            f"You need {required_words} words but only have {total_balance} words available in your balance. Please top up or contact support for more access.",
            reply_markup=main_menu_markup()
        )
        return

    if len(text.split()) < 100:
        bot.send_message(message.chat.id, "The input text must contain at least 100 words.")
        return

    try:
        # Submit the humanization task
        task_id = submit_humanization_task(text, USER_MODE)
        if not task_id:
            bot.send_message(
                message.chat.id,
                "🔧 Oops! We've encountered a small hiccup in our text processing system. Our developers have been notified and are already working their magic to fix it! ✨\n\n🙏 Please try again in a few moments. We appreciate your patience! 🌟",
                reply_markup=main_menu_markup()
            )
            return
        status_message = bot.send_message(message.chat.id, "🔄 Your text is being humanized. Please wait...", parse_mode='Markdown')

        # Simulate loading with periodic updates
        loading_messages = [
            "Processing your text... 🔄",
            "Analyzing text patterns 📊",
            "Enhancing readability ✨",
            "Optimizing word choices 📝",
            "Refining sentence structure 🔄",
            "Improving flow and rhythm 🎵",
            "Adding human touch 🎯",
            "Polishing the content ✨",
            "Making it shine ✨",
            "Finalizing edits ✏️"
        ]

        # duration
        loading_duration = 10  # Adjust this duration as needed

        # Simulate typing and change messages
        for i in range(loading_duration+1):
            bot.send_chat_action(message.chat.id, 'typing')
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=status_message.message_id,  # Use the status message ID
                    text=f"{loading_messages[i % len(loading_messages)]} {i}/{loading_duration}"
                )
            except Exception as e:
                print(f"Failed to edit message: {e}")
            time.sleep(1)  # Ensure this line is not commented out

        # Obtain the humanized text
        humanized_text = obtain_humanized_text(task_id)

        bot.reply_to(message, f"Humanized text (Mode: {USER_MODE}):\n\n{humanized_text}")
        # Save the humanized text as a .txt file with the task ID as the filename
        with open(f"{task_id}.txt", "w") as file:
            file.write(humanized_text)
        # Send the humanized text as a .txt file to the user
        with open(f"{task_id}.txt", "rb") as file:
            bot.send_document(message.chat.id, file)
        # Deduct words used from trial balance first, then balance
        words_used = len(humanized_text.split())
        if trial_balance >= words_used:
            ...
            # update_user_data(user_id, trial_balance=trial_balance - words_used)
        elif trial_balance + balance >= words_used:
            remaining_words = words_used - trial_balance
            # update_user_data(user_id, trial_balance=0, balance=balance - remaining_words)
        else:
            bot.send_message(message.chat.id, "You have insufficient balance. Please top up your balance.")
            return

        # Add main menu reply markup
        bot.send_message(message.chat.id, "Main menu:", reply_markup=main_menu_markup())

    except Exception as e:
        for dev_id in DEVELOPERS_ID:
            bot.send_message(dev_id, f"An error occurred: {str(e)}. Errored user: {message.chat.id}")
def submit_humanization_task(text, mode):
    url = HUMANIZATION_ENDPOINT_SUBMIT
    headers = {
        'api-key': HUMANIZATION_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'input': text,
        'mode': mode
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    if response.status_code == 200:
        result = response.json()
        if result['err_code'] == 0:
            return result['data']['task_id']
        else:
            for dev_id in DEVELOPERS_ID:
                bot.send_message(dev_id, f"Error in submission: {result['err_msg']}")
            return False
    else:
        for dev_id in DEVELOPERS_ID:
            bot.send_message(dev_id, f"Failed to submit task: {response.status_code}")
        return False

def obtain_humanized_text(task_id):
    url = HUMANIZATION_ENDPOINT_OBTAIN
    headers = {
        'api-key': HUMANIZATION_API_KEY
    }
    params = {
        'task_id': task_id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['err_code'] == 0:
            return result['data']['output']
        else:
            raise Exception(f"Error in obtaining result: {result['err_msg']}")
    else:
        raise Exception(f"Failed to obtain task result: {response.status_code}")

@bot.message_handler(func=lambda message: message.text == 'Ask4Help 🧑‍💻')
def send_help_info(message: Message):
    faq_text = (
        "📚 <b>Frequently Asked Questions</b> 📚\n\n"
        "1. <b>How do I humanize text?</b>\n"
        "   - Tap 'Humanize 👤' and follow the instructions.\n\n"
        "2. <b>How do I check my balance?</b>\n"
        "   - Tap 'Profile 🏠' to view your balance.\n\n"
        "3. <b>How do I top up my balance?</b>\n"
        "   - Select a package and follow the payment instructions.\n\n"
        "4. <b>What if I encounter an error?</b>\n"
        "   - Contact support for assistance.\n\n"
        "For further assistance, please contact our admin: <a href='https://t.me/admin_username'>@admin_username</a>"
    )

    bot.send_message(
        message.chat.id,
        faq_text,
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda message: message.text == 'Profile 🏠')
def show_profile(message: Message):
    user_id = message.chat.id
    try:
        # Fetch user data from the database
        user_data = get_user(user_id)
        
        if 'detail' in user_data and user_data['detail'] == 'Not found.':
            bot.send_message(message.chat.id, "User profile not found. Please register first.")
            return
        
        # Extract user details
        words = user_data.get('words', 0)
        balance = user_data.get('balance', 0)
        language = user_data.get('language', 'en')
        
        # Create a profile message
        profile_message = (
            f"👤 **Your Profile:**\n\n"
            f"🔹 **User ID:** {user_id}\n"
            f"🔹 **Words:** {words}\n"
            f"🔹 **Balance:** {balance}\n"
            f"🔹 **Language:** {language}\n"
        )
        
        # Send the profile message
        bot.send_message(message.chat.id, profile_message, parse_mode='Markdown')
    
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching your profile: {str(e)}")

bot.polling()