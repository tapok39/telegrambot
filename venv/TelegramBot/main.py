import asyncio
import time
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import logging
import markups as nav
from db import Database
import sqlite3

#Назначаем переменные и вводим токен с @BotFather
bot = Bot(token='5744098377:AAFJRs8AHf07ZHJy1H1uVoRC883Ny6XjuW0')
YOOTOKEN = '381764678:TEST:42248'
dp = Dispatcher(bot)
db = Database('Database.db')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    loop = asyncio.get_event_loop()
    loop.create_task(run_notify())
def days_to_seconds(days):
    return days * 24 * 60 * 60

def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace('days', 'дней')
        dt = dt.replace('day', 'день')
        return dt

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Укажите ваш ник: ")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=nav.mainMenu)

@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 997979287:  # вставить сюда id админа
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)

                await bot.send_message(message.from_user.id, 'Успешная рассылка')
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'ПРОФИЛЬ':
            user_nickname = 'Ваш ник: ' + db.get_nickname(message.from_user.id)
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if user_sub == False:
                 user_sub = 'Нет'
            user_sub = '\nПодписка: ' + user_sub
            await bot.send_message(message.from_user.id, user_nickname + user_sub)
        elif message.text == 'ПОДПИСКА':
            await bot.send_message(message.from_user.id, 'Описание подписки', reply_markup=nav.sub_inline_markup)
        elif message.text == 'СПИСОК ПОЛЬЗОВАТЕЛЕЙ':
            if db.get_sub_status(message.from_user.id):
                await bot.send_message(message.from_user.id, 'Список пользователей')
            else:
                await bot.send_message(message.from_user.id, 'Купите подписку!')
        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if(len(message.text) > 15):
                    await bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно!", reply_markup=nav.mainMenu)
            else:
                await bot.send_message(message.from_user.id, "Что?")

logging.basicConfig(level=logging.INFO)
@dp.callback_query_handler(text='submonth')
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id,
                           title="Оформление подписки на Test",
                           description="Тест описание",
                           payload="month_sub",
                           provider_token=YOOTOKEN,
                           currency="RUB",
                           start_parameter='test1',
                           prices=[{"label": "Руб", "amount": 15000}])
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
@dp.message_handler(content_types= ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_sub':
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, 'Вам выдана подписка на месяц')
         #подписка
@dp.callback_query_handler(text='notification')
async def run_notify():
    while True:
            base = sqlite3.connect("Database.db")
            cursor = base.cursor()
            all_data = cur.execute("SELECT time_sub FROM users").fetchall
            delta = timedelta(days=1)
            for each_train in all_data:
                each_train = int(each_train)
                each_train = re.sub("[(|)|'|,", "", each_train)
                data_info = datetime.strptime(each_train, "%d %m %Y %H:%M")
                today = datetime.now()
                if today == (data_info - delta):
                    await bot.send_message(chat_id=5744098377, text=f"Reminder {data_info}")
            await asyncio.sleep(1)


async def inifinite_task():
    while True:
        await do_something_useful() #выполняем один цикл работы
        await asyncio.sleep(60)

# @dp.message_handler(commands=["start"])
# async def not_sub(self, message):
#         with self.connection:
#             result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()[2] == 0
#             now = datetime.datetime.now()
#             if now.strftime("%d-%m-%Y") > self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()[3]):
#                 await bot.send_message(message.from_user.id, )





