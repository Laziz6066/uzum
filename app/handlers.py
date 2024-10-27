from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from get_products_json import get_products
from headers import headers_tcl, headers_roison
from aiogram.types import FSInputFile
from get_products_excel import get_products_excel
from datetime import datetime
import pandas as pd

router = Router()


class Reg(StatesGroup):
    name = State()
    number = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Выберите один из магазинов чтобы узнать остаток товаров.", reply_markup=kb.main)


@router.message(F.text == 'Обновить базу TCL')
async def catalog(message: Message):
    current_date = datetime.now().date()
    await message.answer('Подождите немного вычисляю остаток товаров в магазине TCL (UZUM) это может занять '
                         'немного времени! (примерно 120 секунд)')
    await get_products(page=0, size=1, shop_id=772, headers=headers_tcl, file_name="SKU_tcl",
                       update_message_callback=message.answer)
    get_products_excel("SKU_tcl")
    excel = FSInputFile(f"C:/Users/Lazik/Desktop/SKU_tcl_{current_date}.xlsx")
    await message.bot.send_document(chat_id=message.chat.id, document=excel)


@router.message(F.text == 'Обновить базу Roison')
async def catalog(message: Message):
    current_date = datetime.now().date()
    await message.answer('Подождите немного вычисляю остаток товаров в магазине Roison (UZUM) это может занять '
                         'немного времени! (примерно 120 секунд)')
    await get_products(page=0, size=1, shop_id=14511, headers=headers_roison, file_name="SKU_roison",
                       update_message_callback=message.answer)

    get_products_excel("SKU_roison")
    excel = FSInputFile(f"C:/Users/Lazik/Desktop/SKU_roison_{current_date}.xlsx")
    await message.bot.send_document(chat_id=message.chat.id, document=excel)


