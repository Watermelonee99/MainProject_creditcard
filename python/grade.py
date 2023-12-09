import sys
import mysql.connector
import pandas as pd
import numpy as np
import json
sys.stdout.reconfigure(encoding='utf-8')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'credit',
    'charset': 'utf8',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# 문자 인코딩 설정
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# 첫 번째 쿼리 실행
sql_query = "SELECT * FROM card_info"
cursor.execute(sql_query)
result_card_info = cursor.fetchall()

# 두 번째 쿼리 실행
sql_query2 = "SELECT * FROM transaction ORDER BY idx DESC LIMIT 1"
cursor.execute(sql_query2)
result_transaction = cursor.fetchall()

# 데이터프레임 생성
df_card_info = pd.DataFrame(result_card_info)
df_transaction = pd.DataFrame(result_transaction)