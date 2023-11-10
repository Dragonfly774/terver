import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from config import TOKEN, tests_1, tests_2, tests_3
import random


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

titles_tests = '''\n1. Законы распределения дискретных случайных величин\n2. Основные понятия теории вероятностей\n3. Распределение Пуассона дискретной случайной величины'''

number_test = random.randint(1, 3)
if number_test == 1:
    title_test = '1. Законы распределения дискретных случайных величин'
    tests = tests_1
if number_test == 2:
    title_test = '2. Основные понятия теории вероятностей'
    tests = tests_2
if number_test == 3:
    title_test = '3. Распределение Пуассона дискретной случайной величины'
    tests = tests_3


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    '''Хэндлер на команду /start'''
    msg = f'Выбери тему тестирования {titles_tests}'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="1", callback_data="title_tests"))
    builder.add(types.InlineKeyboardButton(
        text="2", callback_data="title_tests"))
    builder.add(types.InlineKeyboardButton(
        text="3", callback_data="title_tests"))
    await message.answer(msg, reply_markup=builder.as_markup())


@dp.callback_query(F.data == "title_tests")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(f'{callback.data}')
    await callback.answer()


@dp.message(F.text)
async def answer_msg(message: types.Message):
    msg_user = message.text
    await message.answer(message.text)


async def main():
    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)

    # Удалнеие всех сообщений
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
