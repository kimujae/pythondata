import oracledb
import copy

def run() :

    response = []
    # 1. 커넥션 객체 획득
    oracledb.init_oracle_client(lib_dir="C:/hyosungedu/DevUtils/instantclient_21_13")
    con = oracledb.connect(user="admin", password="Rladnwo8938!", dsn="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.ap-chuncheon-1.oraclecloud.com))(connect_data=(service_name=ga538a15a6a32a0_nux2_medium.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))")   # DB에 연결 (호스트이름 대신 IP주소 가능)
    cursor = con.cursor()  # 연결된 DB 지시자(커서) 생성

    # 2. 레코드를 삽입 후 승인
    cursor.execute("select expenditure_datetime, expenditure_amount, expenditurecategory_id from expenditure_history where reg_card_id = '5654338751249986' and expenditure_datetime BETWEEN TO_DATE('2024-05-01', 'YYYY-MM-DD') AND TO_DATE('2024-06-01', 'YYYY-MM-DD')")
    column_names = [d[0] for d in cursor.description]

    history = []

    # 결과 가져오기
    for row in cursor:
        #print(row)

        date, amount, code = row
        h = []
        h.append(date)
        h.append(amount)
        h.append(code)

        history.append(h)

    #### 1. 통합할인한도가 존재하는지 체크
    #### 2. 하위 카테고리 별 조건 체크 [할인율, 1회 최대 할인한도, 한달 최대 할인한도]
    ## ["MT1", "CS2", "AC5",  "OL7", "CT1", "FD6", "CE7", "HP8" ,"OS9" ##

    {"전월실적" : 300000, "언제나할인" : [] , "쇼핑" : [], "대형마트" : [0.1, 5000, 50000], "편의점" : [], "외식" : [], "카페/베이커리": [], "의료" :[]}

    card_benefits = [
        {"전월실적" : 300000, "MT1" : [0.1, 5000, 50000]},
        {"전월실적" : 300000, "언제나할인" : [0.07, 99999999, 99999999], "CS2" : [0.7, 9999999,10000]},
        {"전월실적" : 400000, "FD6" : [1000, 1000, 5000]},
        {"전월실적" : 300000, "CS2" : [0.1, 1000, 5000], "CE7" : [0.1, 1000, 5000] ,"MT1" : [0.05, 2500, 20000],"HP8" : [0.1, 1000, 5000] , "통합한도" : 10000},
        {"전월실적" : 300000, "OL7" : [0.1, 150000, 150000], "CE7" : [0.05, 150000, 150000], "CS2" : [0.05, 150000, 150000], "통합한도" : 150000},
        {"전월실적" : 300000, "HP8" : [0.05, 5000, 10000], "OS9" : [0.05, 5000, 10000], "AC5" : [0.1, 5000, 10000], "FD6" : [0.1, 5000, 10000], "통합한도" : 10000},
        {"전월실적" : 500000},
        {"전월실적" : 500000, "MT1" : [0.02, 50000, 50000], "OS9" : [0.02, 50000, 50000]},
        {"전월실적" : 300000},
        {"전월실적" : 500000},
        {"전월실적" : 300000, "CS2" :[0.05, 7000, 7000], "CE7" : [0.05, 7000, 7000], "HP8" : [0.05, 7000, 7000], "통합한도" : 7000},
        {"전월실적" : 0, "CE7" : [0.007,9999999, 9999999 ], "CS2" : [0.007,9999999, 9999999] , "MT1" : [0.007,9999999, 9999999 ], "OS9" :[0.007, 9999999, 9999999] , "FD6" : [0.007, 9999999, 9999999], "HP8" : [0.007, 9999999, 9999999], "OL7" : [0.007,9999999, 9999999]},
        {"전월실적" : 500000, "AC5" : [0.05, 15000, 15000], "HP8" : [0.01, 2000, 2000], "MT1" : [0.01, 2000 , 2000]}, #Edu
        {"전월실적" : 300000}, # air plat
        {"전월실적" : 500000},
        {"전월실적" : 500000},
        {"전월실적" : 300000, "CS2" : [0.2, 10000, 10000]},
        {"전월실적" : 300000},
        {"전월실적" : 400000, "CE7" : [500, 500, 2000]},
        {"전월실적" : 500000, "MT1" : [0.024, 10000, 10000], "CE7" : [0.024, 10000, 10000], "CS2" : [0.024, 10000, 10000], "통합한도" : 10000},
        {"전월실적" : 400000},
        {"전월실적" : 500000, "CE7" : [0.1, 1000, 10000], "MT1" : [0.1, 5000, 5000]}, # SHOPPING
        {"전월실적" : 400000}, # ?? 뭐하면 3000포인트
        {"전월실적" : 300000, "CS2" : [0.2, 7000, 7000], "CE7" : [0.2, 7000, 7000], "통합한도" : 7000},
        {"전월실적" : 300000, "언제나할인" : [0.007, 999999, 999999]}, #Globus
        {"전월실적" : 200000},
        {"전월실적" : 300000, "CS2" : [0.05, 500, 2500], "CE7" : [0.1 , 1000, 8000], "통합한도" : 5000}, #BBig
        {"전월실적" : 500000, "MT1" : [0.02, 9999999, 9999999], "CS2" : [0.02, 9999999, 9999999], "통합한도" : 50000},
        {"전월실적" : 400000},
        {"전월실적" : 400000, "CE7" : [0.05, 7000, 7000], "CS2" : [0.05, 7000, 7000], "MT1" : [0.05, 7000, 7000], "AC5" : [0.05, 7000, 7000], "HP8" : [0.05, 7000, 7000], "통합한도" : 10000},
        {"전월실적" : 500000, "CE7" : [0.05, 1000, 10000]},
        {"전월실적" : 300000, "CS2" : [0.05, 500, 2500]},# bbig
        {"전월실적" : 500000, "언제나할인" : [0.011, 10000, 10000] , "CE7" : [0.024, 10000, 10000], "CS2" : [0.024, 10000, 10000], "MT1" : [0.024, 10000, 10000], "통합한도" : 10000},
        {"전월실적" : 400000, "MT1" : [0.1, 10000, 10000], "CS2" : [0.1, 10000, 10000], "통합한도" : 10000},
        {"전월실적" : 400000, "CS2" : [0.1, 2000, 2000]},
        {"전월실적" : 400000, "언제나할인" : [0.005, 999999, 999999]}, # 신한카드 플리
        {"전월실적" : 400000, "CS2" : [0.002, 10000, 10000], "OL7"  : [0.002, 10000, 10000], "AC5" : [0.002, 10000, 10000], "HP8" : [0.002, 10000, 10000], "통합한도" : 10000},
        {"전월실적" : 400000, "CS2" : [0.002, 10000, 10000], "OL7"  : [0.002, 10000, 10000], "AC5" : [0.002, 10000, 10000], "HP8" : [0.002, 10000, 10000], "통합한도" : 10000},
        {"전월실적" : 300000, "MT1" : [0.1, 5000, 15000], "CE7" : [0.1, 5000, 15000], "통합한도" : 15000},
        {"전월실적" : 300000, "MT1" : [0.005, 2500, 30000], "CS2" : [0.005, 30000, 30000], "통합한도" : 30000},
        {"전월실적" : 400000, "AC5" : [0.1, 10000, 10000]},
        {"전월실적" : 300000, "CS2" : [0.05, 500, 2500], "CE7" : [0.05, 500, 4000], "통합한도" : 7000},
        {"전월실적" : 400000, "언제나할인" : [0.009, 9999999, 9999999]},
        {"전월실적" : 400000, "CS2" : [0.05, 5000, 5000]},
        {"전월실적" : 500000},
        {"전월실적" : 300000, "언제나할인" : [0.001, 999999, 999999]}



        # {"전월실적" : 400000, "언제나할인" : [0.07, 99999999, 99999999], 'FD6' : [1000, 1000, 5000]},
        # {"전월실적" : 300000, "CE7": [0.1, 1000, 5000]},
        # {"전월실적" : 300000, "CS2" : [0.05,99999999,7500]}
    ]

    res = {"MT1" : 0, "언제나할인" : 0, "FD6" : 0, "CE7" : 0 , "CS2" : 0, "HP8" : 0, "CS2" : 0, "AC5" : 0, "CT1" : 0, "OL7" :0, "통합할인액" : 0}
    one_day_res = {"MT1": 0, "언제나할인": 0, "FD6": 0, "CE7": 0, "CS2": 0, "HP8": 0, "CS2": 0, "AC5": 0, "CT1": 0, "OL7": 0}

    for card_benefit in card_benefits :
        discounts = 0
        today  = 1
        for h in history :
        # 소비내역을 순회

            # 일일 혜택 초기화
            if(today is not int(h[0].day)) :
                one_day_res = {"MT1" : 0, "언제나할인" : 0, "FD6" : 0, "CE7" : 0 , "CS2" : 0, "HP8" : 0, "CS2" : 0, "AC5" : 0, "CT1" : 0, "OL7" :0, "통합할인액" : 0}
                today = int(h[0].day)

            # h[0] : 날짜 h[1] : 가격 h[2] : 키

            if "통합한도" in card_benefit :
                if res["통합할인액"] >= card_benefit["통합한도"] :
                    continue

            final_dc_amount = 0
            # 소비내역의 소비카테고리의 혜택을 제공하는 카드인지 판단한다.
            if str(h[2]) in card_benefit:
                # 혜택을 제공하는 카드라면
                # 월최대 혜택 한도와 현재까지 받은 혜택액을 비교한다. -> 한도가 남아있다면 분기문 pass
                if card_benefit[h[2]][2] > res[h[2]] :
                    # 일최대 혜택 한도와 today에 받은 혜택액을 비교한다. -> 한도가 남아있다면 분기문 pass
                    if card_benefit[h[2]][1]  > one_day_res[h[2]]:

                        #할인액 계산
                        dc = int(h[1]) * float(card_benefit[h[2]][0])

                        # 통합한도액의 차이도 계산해야함
                        if card_benefit[h[2]][1] - one_day_res[h[2]] > dc:
                            final_dc_amount = dc

                        else:
                            final_dc_amount = card_benefit[h[2]][1] - one_day_res[h[2]]

                        # # 월 할인 한도
                        # if card_benefit[h[2]][2] < final_dc_amount :
                        #     final_dc_amount = final_dc_amount - (res[h[2]] - card_benefit[h[2]][2])
                        #
                        # # 일 할인 한도
                        # if card_benefit[h[2]][1] < res[h[2]]:
                        #     final_dc_amount = final_dc_amount - (res[h[2]] - card_benefit[h[2]][1])

                        print(final_dc_amount)

                if "통합한도" in card_benefit:
                    if res["통합할인액"] + final_dc_amount > card_benefit["통합한도"]:
                        res["통합할인액"] = card_benefit["통합한도"]

                        final_dc_amount = res["통합할인액"] + final_dc_amount - card_benefit["통합한도"]

                res["통합할인액"] += final_dc_amount
                res[h[2]] += final_dc_amount
                one_day_res[h[2]] += final_dc_amount

            else:
                # 모든 기타 카테고리에 할인이 적용 가능한 언제나 할인 ㅎㅖ택을 제공한다면 분기문 pass
                if "언제나할인" in card_benefit:
                    if card_benefit["언제나할인"][2] > res["언제나할인"] :
                        if card_benefit["언제나할인"][1] > one_day_res["언제나할인"] :
                            dc = int(h[1]) * float(card_benefit["언제나할인"][0])

                            # 통합한도액의 차이도 계산해야함
                            if card_benefit["언제나할인"][1] - one_day_res[h[2]] > dc:
                                final_dc_amount = dc

                            else:
                                final_dc_amount = card_benefit["언제나할인"][1] - one_day_res[h[2]]

                            # # 월 할인 한도
                            # if card_benefit["언제나할인"][2] < final_dc_amount :
                            #     final_dc_amount = final_dc_amount - (res["언제나할인"] - card_benefit["언제나할인"][2])
                            #
                            #
                            # # 일 할인 한도
                            # if card_benefit["언제나할인"][1] < res[h[2]]:
                            #     final_dc_amount = final_dc_amount - (res["언제나할인"] - card_benefit["언제나할인"][1])



                if "통합한도" in card_benefit :
                    if res["통합할인액"] + final_dc_amount > card_benefit["통합한도"] :
                        res["통합할인액"] = card_benefit["통합한도"]

                        final_dc_amount = res["통합할인액"] + final_dc_amount - card_benefit["통합한도"]



                res["통합할인액"] += final_dc_amount
                res["언제나할인"] += final_dc_amount
                one_day_res["언제나할인"] += final_dc_amount

        d = 0
        response.append(copy.deepcopy(res))
        for key in res :
            d = d + res[key]
        #print(d)


    return response


run()