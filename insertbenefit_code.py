import oracledb

rewards_code = {"주유" : 4 , "쇼핑" : 2, "대형마트" : 1, "편의점" : 2, "외식" : 6, "카페/베이커리" : 7, "영화" : 13, "대중교통" : 19,
           "관리비" : 9, "통신" : 10, "교육" : 3, "육아" : 12, "문화" : 5, "레저" : 14, "항공마일리지" : 15, "Priority Pass" : 11,
           "프리미엄" : 16, "하이패스" : 17, "오토" : 18, "의료" : 8, "뷰티" : 20, "금융" : 21, "체크카드겸용" : 22, "포인트/캐시백":23,
           "바우차" : 24, "언제나할인" : 25, "간편결제" : 26, "렌탈" : 27, "경차유류환급" : 28, "연회비지원":29, "국민행복카드" : 30,
           "그린카드": 31, "THE CJ 카드" : 32, "납부 혜택" : 33, "반려동물" : 34}

oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
con = oracledb.connect(user="admin", password="Rladnwo8938!", dsn="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.ap-chuncheon-1.oraclecloud.com))(connect_data=(service_name=ga538a15a6a32a0_nux2_medium.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))")   # DB에 연결 (호스트이름 대신 IP주소 가능)
cursor = con.cursor()   # 연결된 DB 지시자(커서) 생성

for key in rewards_code :
    id = rewards_code[key]
    str = repr(id) + ",'" + key + "'"
    cursor.execute("insert into benefit_code(benefit_code_id, benefit_name) values(" + str +")")

    cursor.execute('commit')