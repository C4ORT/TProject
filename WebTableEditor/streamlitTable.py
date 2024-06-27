import streamlit as st
import pandas as pd
import os
import sqlite3 
import glob
import base64
from PIL import Image
from io import BytesIO
from pathlib import Path
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from streamlit_modal import Modal


def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

BASE_DIR = Path(__file__).resolve().parent.parent


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


# Подключение к базе данных sqlite3
# ----------------------------------------
# connection = sqlite3.connect("db.sqlite3")
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM appTP_customer")
# ----------------------------------------

# Подключение к базе данных sql

conn=st.connection("mydb", type='sql')

# Получение результатов запроса sqlite3
# ----------------------------------------
# rows = cursor.fetchall()
# ----------------------------------------

# Получение результатов запроса sql

rows = conn.query('SELECT * from view_personals;', ttl=600)

st.html("""
  <style>
    [alt=Logo] {
      height: 5rem;
    }
  </style>
        """)

st.write("")

st.logo(image=f"{BASE_DIR}/templates/image/logo.jpg")

text_search = st.text_input("",placeholder="Поиск...", value="")


# обработка фото по пути из бд и запись в другую ячейку в формате BLOB sqlite3
# ----------------------------------------
# increment=0

# for row in rows:
    # cursor_temp = connection.cursor()
    # cursor_temp.execute("SELECT photo FROM appTP_customer")
    # path=cursor_temp.fetchall()

    # print(str(path[increment])[2:-3], "\n")
    # print(row, "\n")

#     if str(path[increment])[2:-3]!='':
#         with open(f"{BASE_DIR}/{str(path[increment])[2:-3]}", "rb") as photo:
#             temp=photo.read()

#             # Преобразование BLOB-данных в строку Base64

#             image_base64 = base64.b64encode(temp).decode('utf-8')
#             # Отображение изображения на сайте

#             html = f'data:image/png;base64,{image_base64}'



#             # cursor_temp.execute("INSERT INTO appTP_customer(blob_photo) VALUES(?)", [temp])
#             cursor_temp.execute(f"UPDATE appTP_customer SET blob_photo = (?)", (html,))
            

#         cursor_temp.close()
#     increment+=1
# connection.commit()
# cursor.close()
# connection.close()
#------------------------

pd.set_option('display.max_columns', None)
df = pd.DataFrame(rows, columns=["direction_name", "department_name", "position_name","surname", "firstname", "patronymic","office", "phone", "cellphone","email"])
df = df.rename(columns={"direction_name" : "Дирекция", "department_name" : "Департамент", "position_name" : "Должность","surname" : "Фамилия", "firstname" : "Имя", "patronymic" : "Отчество","office" : "Кабинет", "phone" : "Тел.", "cellphone" : "Личный тел.","email" : "E-mail"})
# Отображение таблицы на Streamlit


m = rows["search"].str.contains(text_search.lower())



df_search = df[m]

if text_search:
    event = st.dataframe(df_search, use_container_width=True, column_config={"photo_blob": st.column_config.ImageColumn()}, hide_index=True, width=2000 #,key="data", on_select="rerun", selection_mode="single-row"
                         )
    
    # people = event.selection.rows
    # print(df.iloc[people])

    @st.experimental_dialog("Личная карточка", width="large")
    def vote(people_id):
        st.write(f"Фамилия: {str(df.filter(regex='surname').iloc[people_id]).split()[-1]}  \n",
                 f"Имя: {str(df.filter(regex='firstname').iloc[people_id]).split()[-1]}  \n", 
                 f"Отчество: {str(df.filter(regex='patronymic').iloc[people_id]).split()[-1]}  \n",
                 f"Кабинет: {str(df.filter(regex='office').iloc[people_id]).split()[-1]}  \n",
                 f"Внутренний тел.: {str(df.filter(regex='phone').iloc[people_id]).split()[-1]}  \n",
                 f"Личный тел.: {str(df.filter(regex='cellphone').iloc[people_id]).split()[-1]}  \n",
                 f"E-mail: {str(df.filter(regex='email').iloc[people_id]).split()[-1]}  \n",
                 f"DirectionName: {str(df.filter(regex='direction_name').iloc[people_id]).split()[-1]}  \n",
                 f"Департамент: {str(df.filter(regex='department_name').iloc[people_id]).split()[-1]}  \n",
                 f"Должность: {str(df.filter(regex='position_name').iloc[people_id]).split()[-1]}  \n",
                #  f"{str(df.filter(regex='patronymic').iloc[people]).split()[-1]}  \n", фото добавить
                #  ИСПРАВИТЬ ID АБСОЛЮТНЫЙ НА ID фрейма 
                 
                 )
        

    # if people:
    #     vote(people)

    




