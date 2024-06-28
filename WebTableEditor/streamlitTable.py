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
from streamlit_js_eval import streamlit_js_eval


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



@st.experimental_fragment
def dataframe_with_selections(df: pd.DataFrame, init_value: bool = False) -> pd.DataFrame:
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", init_value)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=False)},
        disabled=df.columns,
        
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]

    

        # st.experimental_rerun()
    
    return selected_rows.drop('Select', axis=1)


m = rows["search"].str.contains(text_search.lower())



df_search = df[m]

if text_search:
    event = st.dataframe(df_search, use_container_width=True, column_config={"photo_blob": st.column_config.ImageColumn()}, hide_index=True, width=2000 ,key="data", on_select="rerun", selection_mode="single-row"
                         )

    people = event.selection.rows
    # print("EVENT 1 : ",event['selection']['rows'])
    # print("EVENT: ",event)
    print("PEOPLE: ",people)



    @st.experimental_dialog("Личная карточка", width="large")
    def vote(absolut_id):
        # {str(df.filter(regex='surname').iloc[selection[6]]).split()[-1]}          f"Фамилия: {conn.query('SELECT surname from view_personals WHERE id = ?;', (people[0],))}",
        print("ZZZZZ")
        
        col1, col2 = st.columns(2)
        
        surname = conn.query(f'SELECT surname from view_personals WHERE id = {absolut_id};')
        firstname = conn.query(f'SELECT firstname from view_personals WHERE id = {absolut_id};')
        patronymic = conn.query(f'SELECT patronymic from view_personals WHERE id = {absolut_id};')
        office = conn.query(f'SELECT office from view_personals WHERE id = {absolut_id};')
        phone = conn.query(f'SELECT phone from view_personals WHERE id = {absolut_id};')
        cellphone = conn.query(f'SELECT cellphone from view_personals WHERE id = {absolut_id};')
        email = conn.query(f'SELECT email from view_personals WHERE id = {absolut_id};')
        direction_name = conn.query(f'SELECT direction_name from view_personals WHERE id = {absolut_id};')
        department_name = conn.query(f'SELECT department_name from view_personals WHERE id = {absolut_id};')
        position_name = conn.query(f'SELECT position_name from view_personals WHERE id = {absolut_id};')
        # photo = conn.query(f'SELECT surname from view_personals WHERE id = {absolut_id};')
        
        
        # print("ABSOLUTE ID: ",absolut_id)
        # print("SURR: ",str(direction_name).split()[2:])
        with col1:
            st.write(   f"Фамилия: {' '.join(str(surname).split()[2:])}  \n",
                        f"Имя: {' '.join(str(firstname).split()[2:])}  \n", 
                        f"Отчество: {' '.join(str(patronymic).split()[2:])}  \n",
                        f"Кабинет: {' '.join(str(office).split()[2:])}  \n",
                        f"Внутренний тел.: {' '.join(str(phone).split()[2:])}  \n",
                        f"Личный тел.: {' '.join(str(cellphone).split()[2:])}  \n",
                        f"E-mail: {' '.join(str(email).split()[2:])}  \n",
                        f"Дирекция: {' '.join(str(direction_name).split()[2:])}  \n",
                        f"Департамент: {' '.join(str(department_name).split()[2:])}  \n",
                        f"Должность: {' '.join(str(position_name).split()[2:])}  \n",
                    #  фото добавить
                    

                        )
            
        with col2:
            st.write("PHOTO")


    if people:
        absolut_id = df_search.iloc[people].index[0]+1
    
        vote(absolut_id)
    
        

    
    




