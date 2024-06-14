import streamlit as st
import pandas as pd
import os
import sqlite3 

# Подключение к базе данных

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

cursor.execute("SELECT * FROM appTP_customer")
# Получение результатов запроса

rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=["id", "name", "surname","lastname", "gender","status", "office","work_phone", "cellphone", "position","photo", "created"])
# Отображение таблицы на Streamlit

# st.table(df)
st.dataframe(df)

# ----------------------

# df = pd.DataFrame(
#     [

#         {"name": }

#         {"command": "st.selectbox", "rating": 4, "is_widget": True},
#         {"command": "st.balloons", "rating": 5, "is_widget": False},
#         {"command": "st.time_input", "rating": 3, "is_widget": True},
#     ]
# )

# st.dataframe(df, use_container_width=True)

# ----------------------

# name=models.CharField(max_length=15, default='')
# surname=models.CharField(max_length=30, default='')
# lastname=models.CharField(max_length=20, default='')

# status=models.CharField(max_length=40, default='')
# office=models.CharField(max_length=20, default='')
# work_phone=models.CharField(max_length=15, default='')
# cellphone=models.CharField(max_length=15, default='')
# position=models.CharField(max_length=100, default='')
# photo=models.ImageField(upload_to="images/", blank=True, null=True)