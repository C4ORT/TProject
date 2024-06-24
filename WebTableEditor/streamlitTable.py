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


text_search = st.text_input("Search...", value="")


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

df = pd.DataFrame(rows, columns=[ "direction_name", "department_name", "position_name","surname", "firstname", "patronymic","office", "phone", "cellphone","email"])
# Отображение таблицы на Streamlit

# m1 = df["id"].astype(str).str.contains(text_search)
# m2 = df["direction_id"].astype(str).str.contains(text_search)
m3 = df["direction_name"].str.contains(text_search)
# m4 = df["department_id"].astype(str).str.contains(text_search)
m5 = df["department_name"].str.contains(text_search)
# m6 = df["position_id"].astype(str).str.contains(text_search)
m7 = df["position_name"].str.contains(text_search)
m8 = df["surname"].str.contains(text_search)
m9 = df["firstname"].str.contains(text_search)
m10 = df["patronymic"].str.contains(text_search)
m11 = df["office"].str.contains(text_search)
m12 = df["phone"].str.contains(text_search)
m13 = df["cellphone"].str.contains(text_search)
m14 = df["email"].str.contains(text_search)





df_search = df[m3 | m5 | m7 | m8 | m9 | m10 | m11 | m12 | m13 | m14]

if text_search:
    st.dataframe(df_search, column_config={"photo_blob": st.column_config.ImageColumn()}, hide_index=True)


# def aggrid_interactive_table(df: pd.DataFrame):
#     """Creates an st-aggrid interactive table based on a dataframe.

#     Args:
#         df (pd.DataFrame]): Source dataframe

#     Returns:
#         dict: The selected row
#     """
#     options = GridOptionsBuilder.from_dataframe(
#         df, enableRowGroup=True, enableValue=True, enablePivot=True
#     )

#     options.configure_side_bar()

#     options.configure_selection("single")
#     selection = AgGrid(
#         df,
#         enable_enterprise_modules=True,
#         gridOptions=options.build(),
#         update_mode=GridUpdateMode.MODEL_CHANGED,
#         allow_unsafe_jscode=True,
#     )

#     return selection



# if text_search:
#     selection = aggrid_interactive_table(df=df_search)

#     if selection:
#         st.write("You selected:")
#         st.write(selection["selected_rows"])




# st.dataframe(df, column_config={"photo_blob": st.column_config.ImageColumn()})

