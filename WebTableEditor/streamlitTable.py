import streamlit as st
import pandas as pd
import os
import sqlite3 
import glob
import base64
from PIL import Image
from io import BytesIO


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

increment=0

for row in rows:
    cursor_temp = connection.cursor()
    cursor_temp.execute("SELECT photo FROM appTP_customer")
    path=cursor_temp.fetchall()
    print(str(path[increment])[2:-3], "\n")
    print(row, "\n")

    if str(path[increment])[2:-3]!='':
        with open(f"C:/Users/4ORT/Desktop/TProject/{str(path[increment])[2:-3]}", "rb") as photo:
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
st.dataframe(df, column_config={"photo_blob": st.column_config.ImageColumn()})

