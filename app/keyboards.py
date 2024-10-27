from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить базу TCL'), KeyboardButton(text='Обновить базу Roison')],
    [KeyboardButton(text='Поиск по id TCL'), KeyboardButton(text='Поиск по id Roison')],
    [KeyboardButton(text='Руководство')]
    ], resize_keyboard=True, input_field_placeholder='Select a menu item.')
