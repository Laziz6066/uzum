import pandas as pd

file_path = 'C:/Users/Lazik/Desktop/SKU_tcl_2024-10-25.xlsx'
data = pd.read_excel(file_path)

product_id = int(input("Введите ID продукта: "))

product_info = data[data['ID Продукта'] == product_id]

if not product_info.empty:
    print("ID Продукта:", product_info['ID Продукта'].values[0])
    print("Название продукта:", product_info['Название продукта'].values[0])
    print("Остаток Продукта:", product_info['Остаток Продукта'].values[0])
else:
    print("Продукт с таким ID не найден.")
