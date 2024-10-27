import json
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime


def get_products_excel(file_name):
    current_date = datetime.now().date()
    with open(f'C:/Users/Lazik/Desktop/{file_name}_{current_date}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    products_data = []
    for product in data:
        product_id = product.get('productId')
        title = product.get('title')
        quantity_active = product.get('quantityActive')

        products_data.append({
            'ID Продукта': product_id,
            'Название продукта': title,
            'Остаток Продукта': quantity_active
        })

    df = pd.DataFrame(products_data)

    excel_file = f'C:/Users/Lazik/Desktop/{file_name}_{current_date}.xlsx'
    df.to_excel(excel_file, index=False)

    wb = load_workbook(excel_file)
    ws = wb.active

    # Step 3: Auto-adjust column width
    for column_cells in ws.columns:
        max_length = 0
        column = column_cells[0].column_letter  # Get the column letter
        for cell in column_cells:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))  # Find the max length in the column
            except:
                pass
        adjusted_width = (max_length + 2)  # Slightly increase width for better visibility
        ws.column_dimensions[column].width = adjusted_width

    # Save changes
    wb.save(excel_file)

    print(f"Файл сохранен с подогнанными полями: '{excel_file}'")
