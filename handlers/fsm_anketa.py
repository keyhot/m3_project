from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, ADMIN
from keyboards import client_kb
from database import bot_db


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.photo.set()
        await message.answer(f"Салам {message.from_user.full_name} скинь фотку блюда", reply_markup=client_kb.cancel_markup)
    else:
        await message.reply("Пиши в личку!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Как называется?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Опиши из чего сделано. Веганы могут хавать и тд...")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("Канча сом?")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await bot.send_photo(message.from_user.id, data['photo'],
                         caption=f"Name: {data['name']}\n"
                                 f"Description: {data['description']}\n"
                                 f"Price: {data['price']}\n")
    await bot_db.sql_command_insert(state)
    await state.finish()
    await message.answer("Все свободен)")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Регистрация отменена!")


async def delelete_data(message: types.Message):
    if message.from_user.id in ADMIN and message.chat.type == "private":
        users = await bot_db.sql_command_all()
        for user in users:
            await bot.send_photo(message.from_user.id, user[1],
                                 caption=f"Name: {user[2]}\n"
                                         f"Description: {user[3]}\n"
                                         f"Price: {user[4]}\n",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"delete {user[2]}",
                                         callback_data=f"delete {user[0]}"
                                     )
                                 ))
    else:
        await message.reply("Ты не админ!")


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Пользователь удален!", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['anketa'], state=None)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delelete_data, commands=['delete'])
    dp.register_callback_query_handler(complete_delete, lambda call: call.data and call.data.startswith('delete '))
