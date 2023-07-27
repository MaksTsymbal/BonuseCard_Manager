import logging
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
django.setup()
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from urllib.request import urlopen
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '6577173919:AAG8nyAWhLgAapO8ROXFC3MaPTnshWoGHIg'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
user_auth = {}
user_now = list()

def _get_users_() -> dict:
    url = 'http://127.0.0.1:8000/accounts/view-users/'
    response = urlopen(url)
    return json.load(response)


def _get_cards_() -> list:
    url = 'http://127.0.0.1:8000/card/view-cards/'
    response = urlopen(url)
    return json.load(response)

@dp.message_handler(commands=['cards'])
async def show_cards(message: types.Message):
    card_list = _get_cards_()
    filtered_cards = [card for card in card_list if card.get("created_by_id") == int(user_now[0])]

    if filtered_cards:
        await message.answer("Cards created by you: ")
        for card in filtered_cards:
            card_info = f"ID: {card['card_number']}\nTitle: {card['title']}\nDescription: {card['description']}\nDate Created: {card['date_created']}\nStatus: {card['card_status']}"
            await message.answer(card_info)
    else:
        await message.answer("You haven't created any cards yet.")

@dp.message_handler(commands=['login'])
async def login(message: types.Message):
    user_auth[message.from_user.id] = True
    await message.answer("Enter a username:")

@dp.message_handler(commands=['logout'])
async def logout(message: types.Message):
    if len(user_now) > 0:
        user_auth[message.from_user.id] = False
        user_now.clear()
        await message.answer("You are logged out of your account!")
    else:
        await message.answer("To log out of your account, you must first log in!)")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"I'm your personal-card telegram bot, Hi {message.from_user.first_name}!")

@dp.message_handler(lambda message: user_auth.get(message.from_user.id) == True)
async def process_username(message: types.Message):
    username = message.text
    users = _get_users_()
    user_id = None
    for user in users:
        if user['username'] == username:
            user_id = user['id']
            break

    if user_id is not None:
        user_now.append(user_id)
        await message.answer("Successful authorization!")
        user_auth[message.from_user.id] = False
    else:
        await message.answer("No user found with this name. Enter the username again:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
