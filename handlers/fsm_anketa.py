from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ADMIN, dp
from keyboards import client_kb


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    print("hello")
    if message.chat.type == "private":
        await FSMAdmin.photo.set()
        await message.answer(f"Салам {message.from_user.full_name} скинь фотку блюда", reply_markup=client_kb.cancel_markup)
    else:
        await message.reply("Пиши в личку!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data["username"] = f"@{message.from_user.username}"
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
    if int(message.text) < 1:
        await message.answer("нормально айтчы")
    else:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=f"Name: {data['name']}\n"
                                     f"Description: {data['description']}\n"
                                     f"Price: {data['price']}\n")
        await state.finish()
        await message.answer("Все свободен)")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Регистрация отменена!")


def register_handlers_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['anketa'], commands_prefix='!/')
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
