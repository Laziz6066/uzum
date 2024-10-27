import http.client
import json
import time
from datetime import datetime
from aiogram.types import Message
from aiogram import Router

router = Router()


async def get_products(page, size, shop_id, headers, file_name, update_message_callback):
    total_products_fetched = 0
    all_products = []
    status_message = None
    while True:

        # Создаем новое соединение на каждой итерации
        conn = http.client.HTTPSConnection("api-seller.uzum.uz")
        conn.request("GET", f"/api/seller-openapi/v1/product/shop/{shop_id}?size={size}&page={page}",
                     headers=headers)
        res = conn.getresponse()

        if res.status == 429:
            await update_message_callback("Ошибка 429: Слишком много запросов. Ожидание 60 секунд...")
            time.sleep(60)
            conn.close()  # Закрываем соединение и начинаем заново
            continue

        if res.status != 200:
            await update_message_callback(f"Ошибка {res.status}: {res.reason}")
            conn.close()  # Закрываем соединение при ошибке
            break

        data = res.read()
        conn.close()  # Закрываем соединение после получения ответа

        if not data:
            await update_message_callback("Получен пустой ответ от сервера.")
            break

        decoded_data = data.decode("utf-8")

        try:
            json_data = json.loads(decoded_data)
        except json.JSONDecodeError as e:
            await update_message_callback(f"Ошибка при декодировании JSON: {e}")
            break

        products_on_page = json_data.get('productList', [])
        all_products.extend(products_on_page)
        total_products_fetched += len(products_on_page)

        total_products_amount = json_data.get('totalProductsAmount', 0)
        message_text = f"Загружено товаров: {total_products_fetched} из {total_products_amount}"
        if status_message is None:
            status_message = await update_message_callback(message_text)
        else:
            await status_message.edit_text(message_text)

        if len(products_on_page) == 0:
            await update_message_callback("Нет больше товаров для загрузки.")
            break

        if total_products_fetched >= total_products_amount:
            await update_message_callback("Все товары были загружены.")
            break

        page += 1
        time.sleep(1)  # Небольшая пауза между запросами

    current_date = datetime.now().date()
    if all_products:
        with open(f"C:/Users/Lazik/Desktop/{file_name}_{current_date}.json", 'w', encoding='utf-8') as json_file:
            json.dump(all_products, json_file, ensure_ascii=False, indent=4)
    else:
        await update_message_callback("Данные не были загружены.")