import logging

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


# btnMain = KeyboardButton('Главное меню')
# ГЛАВНОЕ МЕНЮ
btnSub = KeyboardButton('ПОДПИСКА')
btnList = KeyboardButton('СПИСОК ПОЛЬЗОВАТЕЛЕЙ')
btnProfile = KeyboardButton('ПРОФИЛЬ')
btnNotification = KeyboardButton('Напоминание о подписке')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnSub, btnProfile, btnList, btnNotification)

#Другое меню
sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubMonth = InlineKeyboardButton(text='Месяц - 150 рублей', callback_data='submonth')
btnNotification = InlineKeyboardMarkup(text='Включить оповещение о подписке', callback_data='Notification')
sub_inline_markup.insert(btnSubMonth)
# btnInfo = KeyboardButton('Информация')
# btnMoney = KeyboardButton('Курсы валют')
# otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMoney, btnMain)
# btnsub = KeyboardButton('Подписка')
# btnSettings = ReplyKeyboardMarkup(resize_keyboard=True)
# mainMenu.add(btnsub)
# mainMenu.add(btnSettings)
#
# sub_inline_markup = InlineKeyboardMarkup(row_width=1)
#
# btnSubMonth = InlineKeyboardButton(text='Месяц подписки - None рублей', callback_data='submonth')
#
# sub_inline_markup.insert(btnSubMonth)