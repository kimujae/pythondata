import oracledb
import os
# 1. 커넥션 객체 획득
oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
con = oracledb.connect(user="kosa", password="5176", dsn="localhost:1521/xe")   # DB에 연결 (호스트이름 대신 IP주소 가능)
cursor = con.cursor()   # 연결된 DB 지시자(커서) 생성

# 2. 레코드를 삽입 후 승인
cursor.execute("select transaction_datetime, transaction_amount, industry_code from transaction_history where card_number = '3053513933283477' and TO_DATE(transaction_datetime, 'YYYY-MM-DD HH24:MI:SS') between TO_DATE('2023-05-01', 'YYYY-MM-DD') and TO_DATE('2023-06-01', 'YYYY-MM-DD')")
column_names = [d[0] for d in cursor.description]

history = []

# 결과 가져오기
for row in cursor:
    #print(row)
    n = str(row).strip("()")
    arr = n.split(",")
    history.append(arr)



{"전월실적" : 300000, "언제나할인" : [] , "쇼핑" : [], "대형마트" : [0.1, 5000, 50000], "편의점" : [], "외식" : [], "카페/베이커리": [], "의료" :[]}

card_benefits = [
    {"전월실적" : 300000, "MT1" : [0.1, 5000, 50000]}
    # {"전월실적" : 300000, "언제나할인" : [0.07, 99999999, 99999999]},
    # {"전월실적" : 400000, "언제나할인" : [0.07, 99999999, 99999999], 'FD6' : [1000, 1000, 5000]},
    # {"전월실적" : 300000, "CE7": [0.1, 1000, 5000]},
    # {"전월실적" : 300000, "CS2" : [0.05,99999999,7500]}
]

res = {"MT1" : 0, "언제나할인" : 0, "FD6" : 0, "CE7" : 0 , "CS2" : 0}



for card_benefit in card_benefits :
    discounts = 0
    today  = 1
    for h in history :
        # h[0] : 날짜 h[1] : 가격 h[2] : 키
        one_day_res =  {"MT1" : 0, "언제나할인" : 0,"FD6" : 0,"CE7" : 0,"CS2" : 0}


        if(today is not int(h[0][9:11])) :
            one_day_res = {"MT1": 0, "언제나할인": 0 ,"FD6": 0 , "CE7": 0 ,"CS2": 0}
            today = int(h[0][9:11])


        #print(h[2].strip("' '"))
        #print(h[2] in card_benefit)
        h[2] = h[2].strip("' '")
        if str(h[2]) in card_benefit:
            #print(1)
            if card_benefit[h[2]][2] > res[h[2]] :
                #print(2)
                if card_benefit[h[2]][1]  > one_day_res[h[2]]:
                    #print(card_benefit[h[2]][0])
                    dc = int(h[1]) * float(card_benefit[h[2]][0])
                    if card_benefit[h[2]][1] - one_day_res[h[2]] > dc :
                        #print(4)
                        one_day_res[h[2]] += dc
                        res[h[2]] += dc
                    else :
                        res[h[2]] += card_benefit[h[2]][1] - one_day_res[h[2]]
                        one_day_res[h[2]] += card_benefit[h[2]][1] - one_day_res[h[2]]

                    if card_benefit[h[2]][2]  < res[h[2]] :
                        res[h[2]] = card_benefit[h[2]][2]
        else:
            if "언제나할인" in card_benefit:
                res["언제나할인"] = int(h[1]) * card_benefit["언제나할인"][0]




for key in res :
    print(res[key])

