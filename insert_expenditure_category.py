import oracledb

category = ["MT1", "CS2", "AC5",  "OL7", "CT1", "FD6", "CE7", "HP8"]
category_name = ["대형마트", "편의점", "학원", "주유", "문화", "외식", "카페/베이커리", "의료"]


oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
con = oracledb.connect(user="admin", password="Rladnwo8938!", dsn="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.ap-chuncheon-1.oraclecloud.com))(connect_data=(service_name=ga538a15a6a32a0_nux2_medium.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))")   # DB에 연결 (호스트이름 대신 IP주소 가능)
cursor = con.cursor()


for idx in range(0, 8) :
    str = "'" + category[idx] +"', '" + category_name[idx]  + "'"
    cursor.execute("insert into expenditure_category(expenditure_category_id, expenditure_category_name) values(" + str + ")")
    cursor.execute('commit')