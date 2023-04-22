import asyncio
import json

from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN, user_id
from par import check_news_up

# Создание экземпляра бота
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Функция, которая будет вызываться при запуске бота
async def on_startup(dp):
    await bot.send_message(chat_id='820106141', text='Привет работяга! Для того, чтобы посмотреть статьи на сайте напишите команду: "/start". Также ты должен быть зарегестрирован на сайте.')


# Обработчик команды /start (приветствие)
@dp.message_handler(commands=['start'])
async def send_news(message: types.Message):
    start_buttons = ['Все статьи', 'Последние 5 статьей', 'Новые статьи']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Лента статей', reply_markup=keyboard)

# функция для всех новостей
@dp.message_handler(Text(equals='Все статьи'))
async def get_all_news(message: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
       news = f"{hunderline(v['article_title'])}\n" \
              f"{hbold(v['article_desc'])}\n" \
              f"{hlink(v['article_title'], v['article_url'])}"
       await message.answer(news)


# функция для последних пяти новостей
@dp.message_handler(Text(equals='Последние 5 статьей'))
async def get_last_five_news(message: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[:5]:
        news = f"{hunderline(v['article_title'])}\n" \
               f"{hbold(v['article_desc'])}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)

@dp.message_handler(Text(equals='Новые статьи'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_up()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hunderline(v['article_title'])}\n" \
                   f"{hbold(v['article_desc'])}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)

    else:
        await message.answer("Пока нет новых статей...")




# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    



