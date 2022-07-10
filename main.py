from aiogram import types
from aiogram.utils import executor
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, dp
import logging

@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await bot.send_message(message.from_user.id, '/start - start the bot\n/help - information about bot commands\n\
Any number -> number^2\n/quiz -> answer the questions and win\n/meme - bot sends a meme')

@dp.message_handler(commands=['mem'])
async def help_handler(message: types.Message):
    photo = open('media/meme.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)

@dp.message_handler(commands=['quiz'])
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
        chat_id = message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=2,
        explanation='watch the video',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


@dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):
    question = "Boom Bam Bap\nBada Bap Boom Pow"
    answers = [
        'OOOOHHHHHHHHHH',
        'What?',
        'Че он несет?',
        'hehe'
    ]
    video = open('media\hotfire.mp4', 'rb')
    await bot.send_video(call.message.chat.id, video)
    await bot.send_poll(
        chat_id = call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='watch the video',
        explanation_parse_mode=ParseMode.MARKDOWN_V2
    )

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.full_name}!')

@dp.message_handler()
async def echo(message: types.Message):
    text = int(message.text) ** 2 if message.text.isnumeric() else message.text
    await bot.send_message(message.chat.id, text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
