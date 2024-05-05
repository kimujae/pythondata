import oracledb
import os
# 1. 커넥션 객체 획득
oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
con = oracledb.connect(user="kosa", password="5176", dsn="localhost:1521/xe")   # DB에 연결 (호스트이름 대신 IP주소 가능)
cursor = con.cursor()   # 연결된 DB 지시자(커서) 생성

# 2. 레코드를 삽입 후 승인
cursor.execute("insert into dept values(70, 'DEVELOPER','LA')")
cursor.execute('commit') # sqldeveloper에 커밋

