# This Python file uses the following encoding: utf-8
import os
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State


token_bot = '5513704134:AAHHhDifPfWCCJzvkIEK4vUFv6WjYF9myL4'


bot = Bot(token=token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())


class Start(StatesGroup):  # Создаём класс.
    start_name = State()


@dp.message_handler(commands="start")
async def bot_start(message: types.Message):
    start_buttons = ["Поиск человека по ФИО", "Поддержка"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Бот создан для поиска людей на сайте избирательной комиссии Санкт-Петербурга", reply_markup=keyboard)


@dp.message_handler(Text(equals="Поддержка"))
async def aid(message: types.Message):
    await message.answer(f"Автор - Пустынский Александр Максимович\n"
                         f"Номер группы - 4933")


@dp.message_handler(Text(equals="Поиск человека по ФИО"))
async def search_message(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите ФИО человека для поиска')
    await Start.start_name.set()


@dp.message_handler(state=Start.start_name)
async def get_human(message: types.Message, state: FSMContext):
    name = message.text

    with open("people.json") as file:
        new_dict = json.load(file)
    z = 0
    for x in new_dict:
        if x["name"].lower() == name.lower():
            information = f"{x['commission_name']}\n" \
                          f"{x['name']}\n" \
                          f"Номер в таблице - {x['num_in_table']}\n" \
                          f"Ссылка - {x['commission_url']}"
            z = z + 1
            await message.answer(information)

    if z == 0:
        await bot.send_message(message.from_user.id, "Человек не найден")

    await bot.send_message(message.from_user.id, "Выход в главное меню")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
