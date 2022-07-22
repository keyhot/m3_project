from aiogram import types, Dispatcher
from config import bot, ADMIN


async def ban(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMIN:
            await message.answer("Ты не админ!")
        elif not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение")
        else:
            await message.bot.kick_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id
            )
            await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был кикнут!")
    else:
        await message.answer("Это работает только в чатах!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='.!')
