# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from PyKakao import Local
import random
from datetime import datetime, timedelta
import oracledb         # oracledb 라이브러리 임포트(불러오기)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
class Expenditure_detail:
    def __init__(self):
        self.__address = "" #지도 api
        self.__category = "" #지도 api
        self.__store_name = "" #지도 api
        self.__date = "" #yyyy-mm-dd #랜덤
        self.__amount = 0 # 랜덤
        self.__company = ""
        self.__card_num = ""
        self.__tran_code = ""

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
user_cardnum = ['3053513933283477', '4948924115781567']
card_company = ['하나카드', '신한카드']


category = ["MT1", "CS2", "AC5",  "OL7", "CT1", "FD6", "CE7", "HP8"]
amount_range = [(1000, 200000), (1000, 15000), (20000, 100000), (10000, 90000), (10000, 100000),  (13000, 35000), (1500, 15000), (6000, 30000)]
hour_range = [(9, 22),(0, 23),(9, 20),(0, 23),(9, 18), (9, 21),(9, 23),(9, 18)]
cnt = [1, 6, 2, 1, 2, 4, 2, 1]

res = []
MAX_EXPENDITURE_CNT = 5
date = datetime(year= 2023, month= 5, day=2)
LOCAL = Local(service_key = "90dc29e2693b1374b551ca88ff65413c")

for user in user_addrs :
    month_cnt = [100000, 100000, 1, 4, 100000, 100000, 100000, 3]
    week_cnt = [1000, 1000, 1, 1, 1000, 1000, 1000, 1000, 3]
    for i in range (0, 23) :
        if(i % 30 == 0) :
            month_cnt = [100000, 100000, 1, 4, 100000, 100000, 100000, 3]
        if(i % 7 == 0) :
            week_cnt = [1000, 1000, 1, 1, 1000, 1000, 1000, 1000, 3]

        cnt = [2, 6, 2, 1, 2, 4, 2, 1]
        print(i)
        coord = LOCAL.search_address(user, dataframe=False)
        x = coord["documents"][0]["road_address"]["x"]
        y = coord["documents"][0]["road_address"]["y"]

        rand_range = random.randint(0, MAX_EXPENDITURE_CNT)
        for i in range(rand_range) :
            idx = len(category) - 1
            rand_int = 0

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

            exp_d = Expenditure_detail()

            exp_d.set_category(categ)
            exp_d.set_address(st_addr)
            exp_d.set_store_name(st_name)
            exp_d.set_date(date)
            exp_d.set_amount(amount)


            res.append(exp_d)
        date = date + timedelta(days=1)

for exp_d in res :
    print("가맹점명 : ", exp_d.get_store_name(), "소비카테고리 : ", exp_d.get_category(), "가맹점주소 : ", exp_d.get_address(), "소비금액 : " , exp_d.get_amount(), "소비날짜 : ", exp_d.get_date())


# # 1. 커넥션 객체 획득
# con = oracledb.connect(user="kosa", password="5176", dsn="호스트이름:port/SID")   # DB에 연결 (호스트이름 대신 IP주소 가능)
# cursor = con.cursor()   # 연결된 DB 지시자(커서) 생성
#
# # 2. 레코드를 삽입 후 승인
# cursor.execute("insert into dept values(50, 'DEVELOPER','LA')")
# cursor.execute('commit') # sqldeveloper에 커밋

##### 변수
# 하루 소비횟수 (랜덤 : 0 ~ 15회)
# 오프라인 소비 vs 온라인 소비(랜덤)
# 업종
# 시간대