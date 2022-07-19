from config import bot, dp
from aiogram import types, Dispatcher
from random import choice


@dp.message_handler()
async def echo(message: types.Message):
    bad = ['java', 'bitch', 'lox', 'kotlin', 'плохой мальчик']
    text = int(message.text) ** 2 if message.text.isnumeric() else message.text
    for word in bad:
        if word in str(text):
            await bot.send_message(message.chat.id, f"Не матерись, {message.from_user.full_name}! Сам ты {word}!")
            await bot.delete_message(message.chat.id, message.message_id)
            return

    if message.text.startswith('!pin'):
        if not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение")
        else:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        return

    if message.text.startswith('game'):
        emoji_list = ['⚽️', '🏀', '🎳', '🎯', '🎰', '🎲']
        a = await bot.send_dice(message.chat.id, emoji=choice(emoji_list))
        return

    await bot.send_message(message.chat.id, text)


def register_handlers_extra(dp: Dispatcher):
    dp.message_handler(echo)
