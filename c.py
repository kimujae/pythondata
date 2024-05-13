# selenium의 webdriver를 사용하기 위한 import
import urllib

import oracledb
from PIL import Image
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
from selenium.webdriver.common.keys import Keys


class Card_Benefit :
    def __init__(self):
        self.__id = 0
        self.__cardId = 0
        self.__benefit_code = 0
        self.__benfit_detail = [] ## len 만큼 card_b 삽입되어야함

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_cardId(self, cardId):
        self.__cardId = cardId

    def get_cardId(self):
        return self.__cardId

    def set_benfit_code(self, code):
        self.__benefit_code = code

    def get_benefit_code(self):
        return self.__benefit_code

    def set_benefit_d(self, bd):
        self.__benfit_detail.append(bd)

    def get_benefit_d(self):
        return self.__benfit_detail

class Card:
    def __init__(self):
        self.__link = ""
        self.__company = ""
        self.__name = ""
        self.__fee = ""
        #self.__benefits = [] #코드로 저장

    def set_link(self, link):
        self.__link = link

    def get_link(self):
        return self.__link

    def set_company(self, company):
        self.__company = company

    def get_company(self):
        return self.__company

    def set_fee(self, fee):
        self.__fee = fee

    def set_name(self, name):
        self.__name = name

    def add_benefit(self, benefit):
        self.__benefits.append(benefit)

    def get_name(self):
        return self.__name

    def get_benfits(self):
        return self.__benefits

    def get_fee(self):
        return self.__fee


class Card_Detail:
    def __init__(self):
        self.__baseRecord = "" #기준실적
        #self.__benefits_detail = []
        self.__benefits_sum = "" #프론트에서 엔터를 기준으로 스플릿해줘야함

    def set_baseRecord(self, baseRecord):
        self.__baseRecord = baseRecord

    def get_baseRecord(self):
        return self.__baseRecord

    def add_benefits_sum(self, benefit_sum):
        self.__benefits_sum += benefit_sum
        self.__benefits_sum += '\n'

    def get_benefits_sum(self):
        return self.__benefits_sum


##### 리스트에 접근 가능한 개별신용카드가 있으면 0~2 반복
##### 개별신용카드에 모두 접근했다면 다음 페이지네이션으로 클릭하여 다음 리스트를 접근한다.
##### 0. 신용카드 리스트 중 개별 신용카드를 클릭한다.
##### 1. 신용카드 세부 정보를 크롤링 한다.
##### 2. 뒤로가기 클릭을 한다.


# 크롬드라이버 실행
driver = webdriver.Chrome()
#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://card-search.naver.com/list?sortMethod=ri&isRefetch=true&bizType=CPC')
# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)


# 카드사 탭을 통해서 alt정보를 통해 card사 추가 해줘야한다.
def is_element_present(tag_name):
    try:
        driver.find_element(By.CSS_SELECTOR, tag_name)
        return True
    except NoSuchElementException:
        return False


company_arr = driver.find_elements(By.CSS_SELECTOR, '.agent > picture > .logo')
btn_arr = driver.find_elements(By.CSS_SELECTOR, '._btnContainer > .item > .agent > picture > .logo')
btn_len = len(company_arr) -1
print(btn_len, len(btn_arr) - 1)

#"MT1", "CS2", "AC5",  "OL7", "CT1", "FD6", "CE7", "HP8"
#### 혜택코드 영속화
rewards_code = {"주유" : 4 , "쇼핑" : 2, "대형마트" : 1, "편의점" : 2, "외식" : 6, "카페/베이커리" : 7, "영화" : 13, "대중교통" : 19,
           "관리비" : 9, "통신" : 10, "교육" : 3, "육아" : 12, "문화" : 5, "레저" : 14, "항공마일리지" : 15, "Priority Pass" : 11,
           "프리미엄" : 16, "하이패스" : 17, "오토" : 18, "의료" : 8, "뷰티" : 20, "금융" : 21, "체크카드겸용" : 22, "포인트/캐시백":23,
           "바우처" : 24, "언제나할인" : 25, "간편결제" : 26, "렌탈" : 27, "경차유류환급" : 28, "연회비지원":29, "국민행복카드" : 30,
           "그린카드": 31, "THE CJ 카드" : 32, "납부 혜택" : 33, "반려동물" : 34}

oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
con = oracledb.connect(user="admin", password="Rladnwo8938!", dsn="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.ap-chuncheon-1.oraclecloud.com))(connect_data=(service_name=ga538a15a6a32a0_nux2_medium.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))")   # DB에 연결 (호스트이름 대신 IP주소 가능)
cursor = con.cursor()   # 연결된 DB 지시자(커서) 생성

# for key in rewards_code :
#     id = rewards_code[key]
#     str = repr(id) + ",'" + key + "'"
#     cursor.execute("insert into benefit_code(benefit_code_id, benefit_name) values(" + str +")")
#
#     cursor.execute('commit')
#
#
cards = []
cards_details = []
cards_benfits = []

#### 카드 영속화
companys = ["신한카드", "현대카드", "삼성카드", "국민카드","롯데카드", "하나카드", "우리카드", "NH농협카드","IBK기업은행카드"]

cardId = -1
card_benefitId = -1
cnt = 1
for idx in range(0, 8) :
    #print(company_arr[idx].get_attribute('alt'))
    btn_arr[idx].click()
    time.sleep(3)



    while(is_element_present('.more')) :
        btn = driver.find_element(By.CSS_SELECTOR, '.more')
        btn.click()
        time.sleep(2)

    imgs = driver.find_elements(By.CSS_SELECTOR, '.figure > .img')


    name = driver.find_elements(By.CSS_SELECTOR, '.info > .anchor')

    ########### 카드 순회 시작 ###########
    for n in name:
        cardId += 1
        driver.get(n.get_attribute('href'))
        time.sleep(3)
        ## 상세 페이지

        card_entity = Card()
        card_d_entity = Card_Detail()
        card_benefit = Card_Benefit()

        card_name = driver.find_elements(By.CSS_SELECTOR, 'b.txt')
        card_fee = driver.find_elements(By.CSS_SELECTOR, '.desc > .txt')[0]
        benefits = driver.find_elements(By.CSS_SELECTOR, 'button.benefit > span.name')
        link = driver.find_element(By.CSS_SELECTOR, '.apply').get_attribute('href')
        company = companys[idx]
        benefit_sum = driver.find_elements(By.CSS_SELECTOR, '.desc:nth-child(8)')
        base_record = driver.find_element(By.CSS_SELECTOR, '.as_baseRecord > .txt').text
        #print(benefit_sum[0].text, "혜택요약")

        ####### 주요혜택 상세 정보 #######
        benefit_btn = driver.find_elements(By.CSS_SELECTOR, 'button.benefit')


        #주요혜택 클릭 -> 혜택 디테일정보 얻기
        for jdx in range(0, len(benefit_btn)) :
            benefit_btn[jdx].click()
            time.sleep(1)
            benefit_d = driver.find_elements(By.CSS_SELECTOR, '.desc > .item ')

            ######## card_benefit  중간테이블에 객체 삽입을 위한 엔티티 정의 ########
            ######## 카드사도 코드로 관리해야함 ########
            for detail in benefit_d :
                card_benefitId += 1
                card_benefit.set_id(card_benefitId)
                card_benefit.set_cardId(cardId)
                card_benefit.set_benefit_d(detail.text)
                card_benefit.set_benfit_code(rewards_code[benefits[jdx].text])
                cards_benfits.append(card_benefit)
                print(card_benefit.get_id(), card_benefit.get_cardId(), card_benefit.get_benefit_code())

            str = "'" + repr(rewards_code[benefits[jdx].text]) + "'," + repr(card_benefit.get_cardId()) + ",'" + benefits[jdx].text + "'"
            print(str)
            cursor.execute(
                "insert into card_benefit_code(benefit_code_id, card_product_id, benefit_name) values(" + str + ")")
            benefit_btn[jdx].click()


        card_entity.set_name(card_name[0].text)
        card_entity.set_fee(card_fee.text)
        card_entity.set_link(link)
        card_entity.set_company(idx)
        cards.append(card_entity)

        card_d_entity.set_baseRecord(base_record)



        for sum in benefit_sum :
            card_d_entity.add_benefits_sum(sum.text)

        str = repr(cardId) + "," + repr(
            idx) + ",'" + card_entity.get_name() + "'," + "'" + card_entity.get_name() + "','"+ card_entity.get_fee() + "','"+ card_d_entity.get_benefits_sum() + "'"
        cursor.execute(
            "insert into card_product(card_product_id, card_company_id, card_product_name, card_product_image, membership_fee, benefit_summary) values(" + str + ")")

        str = repr(cardId) + ",'" + card_d_entity.get_baseRecord() + "'"
        cursor.execute(
            "insert into card_product_details(card_product_id, base_record) values(" + str + ")")

        cards_details.append(card_d_entity)
        print(card_d_entity.get_benefits_sum(), card_d_entity.get_baseRecord())

        str = repr(card_benefit.get_id()) + "," +repr(card_benefit.get_benefit_code()) + "," + repr(card_benefit.get_cardId()) + ",'" + card_benefit.get_benefit_d() + "'"
        cursor.execute(
            "insert into card_benefit_details(card_benefit_details, benefit_code_id, card_id, benefit_details) values(" + str + ")")

        cursor.execute("commit")
        #print(card.get_name(), card.get_fee(), card.get_link(), card.get_company())



        #
        driver.back()



    btn_arr[idx].click()

#
# # for card in cards :
#
#
#
#
# # len1 = len(summary_arr) - 1
# # print(len1)
# # for idx in range(0, 1) :
# #     names = name_arr[idx]
# #     summaries = summary_arr[idx]
# #     fees = fee_arr[idx]
# #     benefits = benefits_arr[idx]
# #
# #     print(len(names))
# #     for idx in range(0, len(names) - 1) :
# #         print(names[idx].text)
#
#
#
#
#
#
#
