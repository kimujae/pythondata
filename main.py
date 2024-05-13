# This is a sample Python script.
import oracledb
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from PyKakao import Local
import random
from datetime import datetime, timedelta
#import oracledb         # oracledb 라이브러리 임포트(불러오기)



# drop table transaction_history;
# CREATE TABLE transaction_history (
#     transaction_id NUMBER PRIMARY KEY,
#     transaction_code VARCHAR2(12),
#     transaction_datetime VARCHAR2(25),
#     transaction_amount NUMBER,
#     card_company VARCHAR2(25),
#     card_number VARCHAR2(25),
#     store_name VARCHAR2(200),
#     industry_code VARCHAR2(20)
# );
# commit;
# --CREATE SEQUENCE transaction_id_seq START WITH 1 INCREMENT BY 1;
# --
# --CREATE OR REPLACE TRIGGER transaction_history_trigger
# --BEFORE INSERT ON transaction_history
# --FOR EACH ROW
# --BEGIN
# --    SELECT transaction_id_seq.NEXTVAL INTO :NEW.transaction_id FROM DUAL;
# --END;
#
#
# desc transaction_history;
#
# select * from transaction_history;


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
class Expenditure_detail:
    def __init__(self):
        self.__address = "" #지도 api
        self.__category = "" #지도 api
        self.__store_name = "" #지도 api
        self.__date = "" #yyyy-mm-dd #랜덤
        self.__amount = "" # 랜덤
        self.__company = ""
        self.__card_num = "" #
        self.__tran_code = "결제승인" # 현재 데이터 더미는 모두 결제승인


    def get_tran_code(self):
        return self.__tran_code



    def set_comapany(self, company):
        self.__company = company

    def get_company(self):
        return self.__company

    def set_card_num(self, card_num):
        self.__card_num = card_num

    def get_card_num(self):
        return self.__card_num



    def set_address(self, address):
        self.__address = address

    def set_category(self, category):
        self.__category = category

    def set_store_name(self, store_name):
        self.__store_name = store_name

    def get_address(self):
        return self.__address

    def get_category(self):
        return self.__category

    def get_store_name(self):
        return self.__store_name

    def set_date(self, date):
        self.__date = date

    def get_date(self):
        return self.__date

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

# ex = Expenditure_detail()
# ex.set_store_name("이마트24")
# print(ex.get_store_name())

##### 변수
# 하루 소비횟수 (랜덤 : 0 ~ 15회)
# 오프라인 소비 vs 온라인 소비(랜덤)
# 업종
# 시간대
##### 카테고리 변수 범위 제한? #####
##### 대형마트 : 하루 0-2회 1000~ 300000
##### 학원 : 하루 0-2회 20000~100000 # 학원도 주기를 가져야한다.
##### 병원 : 하루 0-1 회 3000~30000
##### 음식점 : 하루 0-4회 7500 ~ 40000
##### 카페 : 하루 0-2회 1500 ~ 25000
##### 편의점 : 하루 0-6회 500 ~ 30000
##### 문화시설 : 하루 0-2회 10000 ~ 100000
##### 지하철역 -> 교통 대체
##### 온라인 코드 추가 : 온라인 : 하루 0-10회
##### 주유소 : 하루 0-1회 10000~90000 #주유소도 주기를 갖는다.

user_addrs = ["금낭화로 24가길"]
user_cardnum = ['5654338751249986']
card_company = ['하나카드']
category = ["MT1", "CS2", "AC5",  "OL7", "CT1", "FD6", "CE7", "HP8"] #온라인도 추가해야된다.

# 변수 제약 설정
amount_range = [(1000, 20000), (1000, 15000), (20000, 100000), (10000, 90000), (10000, 100000),  (13000, 35000), (1500, 15000), (6000, 30000)]
hour_range = [(9, 22),(0, 23),(9, 20),(0, 23),(9, 18), (9, 21),(9, 23),(9, 18)]
MAX_EXPENDITURE_CNT = 5
cnt = [1, 6, 0, 0, 2, 4, 2, 1]
month_cnt = [100000, 100000, 0, 0, 100000, 100000, 100000, 3]
week_cnt = [1000, 1000, 0, 0, 3, 1000, 1000, 1000, 3]


date = datetime(year= 2024, month= 5, day=1)
LOCAL = Local(service_key = "90dc29e2693b1374b551ca88ff65413c")

oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
con = oracledb.connect(user="admin", password="Rladnwo8938!", dsn="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.ap-chuncheon-1.oraclecloud.com))(connect_data=(service_name=ga538a15a6a32a0_nux2_medium.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))")   # DB에 연결 (호스트이름 대신 IP주소 가능)
cursor = con.cursor()   # 연결된 DB 지시자(커서) 생성



res = []
input = 0
for useridx in range(0, len(user_addrs)) :
    month_cnt = [100000, 100000, 1, 0, 100000, 100000, 100000, 3]
    week_cnt = [1000, 1000, 1, 0, 1000, 1000, 1000, 1000, 3]


    # 총 생성 일 입력
    for i in range (0, 50) :
        if(i % 30 == 0) :
            month_cnt = [100000, 100000, 1, 4, 100000, 100000, 100000, 3]
        if(i % 7 == 0) :
            week_cnt = [1000, 1000, 1, 1, 1000, 1000, 1000, 1000, 3]

        cnt = [2, 6, 2, 1, 2, 4, 2, 1]
        print(i)
        coord = LOCAL.search_address(user_addrs[useridx], dataframe=False)
        x = coord["documents"][0]["road_address"]["x"]
        y = coord["documents"][0]["road_address"]["y"]

        rand_range = random.randint(0, MAX_EXPENDITURE_CNT)
        for i in range(rand_range) :
            idx = len(category) - 1
            rand_int = 0
            input += 1

            while(True) :
                rand_int =  random.randint(0, idx)
                if month_cnt[rand_int] == 0 or week_cnt[rand_int] == 0 or cnt[rand_int] == 0 :
                    continue

                cnt[rand_int] -= 1
                month_cnt[rand_int] -= 1
                week_cnt[rand_int] -= 1
                break


            categ = category[rand_int]
            amount = random.randint(amount_range[rand_int][0], amount_range[rand_int][1]) // 100 * 100

            rand_range = random.randint(500, 5000)
            expenditure_target_store = LOCAL.search_category(categ, x=x, y=y, radius=2000, dataframe=False)["documents"]

            idx = random.randint(0, len(expenditure_target_store) - 1)
            st_addr = expenditure_target_store[idx]["address_name"]
            st_name = expenditure_target_store[idx]["place_name"]


            rand_hour = random.randint(hour_range[rand_int][0], hour_range[rand_int][1])
            rand_minute = random.randint(0, 59)
            date = date.replace(hour= rand_hour, minute=rand_minute)
            print(date.strftime('%Y-%m-%d %H:%M:%S'))
            exp_d = Expenditure_detail()

            exp_d.set_category(categ)
            exp_d.set_address(st_addr)
            exp_d.set_store_name(st_name)
            exp_d.set_date(date)
            exp_d.set_amount(amount)
            exp_d.set_card_num(user_cardnum[useridx])
            exp_d.set_comapany(card_company[useridx])
            # 2. 레코드를 삽입 후 승인

            str = repr(input) + ",'" + exp_d.get_tran_code() +"', " + "TO_DATE( '"+ exp_d.get_date().strftime('%Y-%m-%d %H:%M:%S') + "', 'YYYY-MM-DD HH24:MI:SS')" +"," + repr(exp_d.get_amount())+ ",'" + exp_d.get_company() +"'," + "'" + exp_d.get_card_num() +"'," + "'" + exp_d.get_store_name() +"'," + "'" + exp_d.get_address() +"',"  + "'" + exp_d.get_category() +"'"
            print(str)

            cursor.execute("insert into my_data_transactions(transaction_id, transaction_code, transaction_datetime,transaction_amount,card_company,card_number,store_name, store_address, industry_code) values(" + str + ")")

            cursor.execute('commit')  # sqldeveloper에 커밋
            res.append(exp_d)
        date = date + timedelta(days=1)

# for exp_d in res :
#     print("가맹점명 : ", exp_d.get_store_name(), "소비카테고리 : ", exp_d.get_category(), "가맹점주소 : ", exp_d.get_address(), "소비금액 : " , repr(exp_d.get_amount()), "소비날짜 : ", exp_d.get_date(),
#           "카드번호 : ", exp_d.get_card_num(
#           , "카드회사 : ", exp_d.get_company())