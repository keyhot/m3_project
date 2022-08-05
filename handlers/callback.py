from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, dp
from aiogram import types, Dispatcher





@dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Next', callback_data='button_call_2')
    markup.add(button)

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
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='watch the video',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


@dp.callback_query_handler(lambda call: call.data == "button_call_2")
async def quiz_3(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Next', callback_data='button_call_3')
    markup.add(button)

    question = "DEEZ NUTS"
    answers = [
        'аххпапахпахахах',
        'Эмне?',
        'Чиво?',
        'GOT \'EM'
    ]
    video = open('media\deeznuts.mp4', 'rb')
    await bot.send_video(call.message.chat.id, video)
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='watch the video',
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


@dp.callback_query_handler(lambda call: call.data == "button_call_3")
async def quiz_4(call: types.CallbackQuery):
    question = "Who is this?"
    answers = [
        'Sooronbai Zheenbekov',
        'Ricardo Milos',
        'Ким бул?',
        'Это я'
    ]
    video = open('media\\ricardo.mp4', 'rb')
    await bot.send_video(call.message.chat.id, video)
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
        explanation='watch the video',
        explanation_parse_mode=ParseMode.MARKDOWN_V2
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
