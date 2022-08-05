from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from config import bot, dp
from keyboards import client_kb
from database.bot_db import sql_command_random


# @dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.full_name}!',
                           reply_markup=client_kb.start_markup)


# @dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await bot.send_message(message.chat.id, '/start - start the bot\n/help - information about bot commands\n\
Any number -> number^2\n/quiz -> answer the questions and win\n/mem - bot sends a meme')


# @dp.message_handler(commands=['mem'])
async def mem_handler(message: types.Message):
    photo = open('media/meme.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo)


# @dp.message_handler(commands=['quiz'])
async def quiz_handler(message: types.Message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Next', callback_data='button_call_1')
    markup.add(button)

    question = "Why are you gay?"
    answers = [
        'Just because',
        "I'm not",
        "Who says I'm gay",
        'haha'
    ]
    video = open('media/gay.mp4', 'rb')
    await bot.send_video(message.chat.id, video)

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=2,
        explanation='watch the video',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


async def show_random(message: types.Message):
    await sql_command_random(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(help_handler, commands=['help'])
    dp.register_message_handler(quiz_handler, commands=['quiz'])
    dp.register_message_handler(mem_handler, commands=['mem'])
    dp.register_message_handler(show_random, commands=['random'])
