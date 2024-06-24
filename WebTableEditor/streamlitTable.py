import streamlit as st
import pandas as pd
import os
import sqlite3 
import glob
import base64
from PIL import Image
from io import BytesIO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

def get_thumbnail(path: str) -> Image:
    img = Image.open(path)
    img.thumbnail((200, 200))
    return img

def image_to_base64(img_path: str) -> str:
    img = get_thumbnail(img_path)
    with BytesIO() as buffer:
        img.save(buffer, 'png') # or 'jpeg'
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(img_path: str) -> str:
    return f'<img src="data:image/png;base64,{image_to_base64(img_path)}">'


# Подключение к базе данных

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

cursor.execute("SELECT * FROM appTP_customer")
# Получение результатов запроса

rows = cursor.fetchall()

text_search = st.text_input("Search...", value="")




increment=0

for row in rows:
    cursor_temp = connection.cursor()
    cursor_temp.execute("SELECT photo FROM appTP_customer")
    path=cursor_temp.fetchall()
    print(str(path[increment])[2:-3], "\n")
    print(row, "\n")

    if str(path[increment])[2:-3]!='':
        with open(f"{BASE_DIR}/{str(path[increment])[2:-3]}", "rb") as photo:
            temp=photo.read()

            # Преобразование BLOB-данных в строку Base64

            image_base64 = base64.b64encode(temp).decode('utf-8')
            # Отображение изображения на сайте

            html = f'data:image/png;base64,{image_base64}'



            # cursor_temp.execute("INSERT INTO appTP_customer(blob_photo) VALUES(?)", [temp])
            cursor_temp.execute(f"UPDATE appTP_customer SET blob_photo = (?)", (html,))
            

        cursor_temp.close()
    increment+=1
connection.commit()
cursor.close()
connection.close()


#------------------------
df = pd.DataFrame(rows, columns=["id", "name", "surname","lastname", "gender","status", "office","work_phone", "cellphone", "position","photo", "created", "photo_blob"])
# Отображение таблицы на Streamlit

m1 = df["id"].astype(str).str.contains(text_search)
m2 = df["name"].str.contains(text_search)
m3 = df["surname"].str.contains(text_search)
m4 = df["lastname"].str.contains(text_search)
m5 = df["gender"].str.contains(text_search)
m6 = df["status"].str.contains(text_search)
m7 = df["office"].str.contains(text_search)
m8 = df["work_phone"].str.contains(text_search)
m9 = df["cellphone"].str.contains(text_search)
m10 = df["position"].str.contains(text_search)
m11 = df["created"].str.contains(text_search)





df_search = df[m1 | m2 | m3 | m4 | m5 | m6 | m7 | m8 | m9 | m10 | m11]

if text_search:
    st.dataframe(df_search, column_config={"photo_blob": st.column_config.ImageColumn()})

# st.dataframe(df, column_config={"photo_blob": st.column_config.ImageColumn()})

