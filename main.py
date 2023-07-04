# Первый Научный Либертарианский Телеграм Бот

import logging
import asyncio

from config import TOKEN, QUOTE_MARK
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from quotes import quote_randomizer, check_fraction

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
quote = quote_randomizer()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите вариант")
    reply_button1 = KeyboardButton(text = "Угадать по цитате")
    keyboard.clean()
    keyboard.add(reply_button1)
    await message.answer("Как будем унижать этатистов сегодня?", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.ANY)
async def quote_guessing(message: types.Message):
    
    if message.text == "Угадать по цитате":
        inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True, 
                                             input_field_placeholder="Предположите вариант")
        inl_button1 = KeyboardButton(text="Либертарианец",
                                     callback_data=f"libertarian")
        inl_button2 = InlineKeyboardButton(text="Этатист",
                                     callback_data=f"etatist")
        inline_keyboard.clean()
        inline_keyboard.add(inl_button1, inl_button2)
        global quote
        quote = quote_randomizer()
        await message.answer(f'Кто автор этой цитаты?\n"{quote}"', reply_markup=inline_keyboard)
               

@dp.callback_query_handler()
async def vote_for_quote(callback: types.CallbackQuery):

    if callback.data == "libertarian":
        fraction, author = check_fraction(quote)
        if fraction == "libertarian":
            await callback.message.answer(f"✅Верно! Этот тезис сформулировал либертарианец {author}")
        elif fraction == "etatist":
            await callback.message.answer(f"❌Вы не угадали! Этот тезис сформулировал этатист {author}")

    if callback.data == "etatist":
        fraction, author = check_fraction(quote)
        if fraction == "etatist":
            await callback.message.answer(f"✅Верно! Этот тезис сформулировал этатист {author}")
        elif fraction == "libertarian":
            await callback.message.answer(f"❌Вы не угадали! Этот тезис сформулировал либертарианец {author}")

    else:
        await callback.answer()
        


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
