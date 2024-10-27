from aiogram import F, Router
from aiogram.filters import CommandStart, Command
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
    id = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Вас приветстувет бот по поиску товаров на меркетплейсе "
                        "Uzum перед началом работы ознакомьтесь с руководством.", reply_markup=kb.main)


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


@router.message(F.text.in_(['Поиск по id TCL', 'Поиск по id Roison']))
async def input_id(message: Message, state: FSMContext):
    if message.text == 'Поиск по id TCL':
        await state.update_data(search_type='tcl')
    elif message.text == 'Поиск по id Roison':
        await state.update_data(search_type='roison')

    await state.set_state(Reg.id)
    await message.answer('Введите id товара:')


@router.message(Reg.id)
async def search_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()

    try:
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        search_type = data.get('search_type', 'TCL')  # Default to 'TCL' if not set
        file_name = f'C:/Users/Lazik/Desktop/SKU_{search_type}_{current_date}.xlsx'

        excel_data = pd.read_excel(file_name)

        product_info = excel_data[excel_data['ID Продукта'] == int(data['id'])]

        if not product_info.empty:
            response_text = (
                f"ID Продукта: {product_info['ID Продукта'].values[0]}\n"
                f"Название продукта: {product_info['Название продукта'].values[0]}\n"
                f"Остаток Продукта: {product_info['Остаток Продукта'].values[0]}"
            )
        else:
            response_text = "Продукт с таким ID не найден."

    except FileNotFoundError:
        response_text = "Данные не найдены, попробуйте обновить базу."

    except ValueError:
        response_text = "ID должен быть числом. Попробуйте ещё раз."

    await message.answer(response_text)
    await state.clear()


@router.message(F.text == "Руководство")
async def get_info(message: Message):
    response_text = ("Этот бот предназначен для отображения остатков товаров на маркетплейсе Uzum по магазинам: "
                     "<b>TCL Ssmart.Online</b> и <b>Roison.Uz</b> также в боте присутствует функция поиска товара по "
                     "его <b>id</b>. Перед началом работы чтобы получить точные данные рекомендуется обновить базу "
                     "(каждый день) так как данные динамичны и значение остатка товаров изменяются по мере их продажи.")
    await message.answer(f"{response_text}", parse_mode="HTML")
