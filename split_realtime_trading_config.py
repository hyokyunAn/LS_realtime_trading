
from zmq.asyncio import Context
import zmq
import sys
import os
import pickle
import pandas as pd
import time
import requests
import json
import asyncio
import json
import websockets
from datetime import datetime, timedelta

from real_trading_utils import *
from order_utils import *

from collections import defaultdict, deque
import numpy as np
# split_subscriber_and_trading 에서 사용할 공용 변수, 함수들 선언
from joblib import load
import multiprocessing
import threading
import queue as Queue


# @@@@@@@@@@@@@@@@@@@ 공용 변수들 선언 시작 @@@@@@@@@@@@@@@@@@@
from LS_config import USER_ID, APP_KEY, APP_SECRET_KEY, REST_URL, WEBSOCKET_URL



테스트모드 = False

BUY_MODEL_DIRS = [
                 
                  ]
BUY_MODEL_TYPE = "REG"  # ['CLS', 'REG']
BUY_THRESHOLDs = [0.6, 0.6, 0.6, 0.6]
BUY_FEATURE_FUNC = dummy_func
BUY_SIGNAL_FUNC = dummy_func
BUY_VOTING_FUNC = dummy_func
# BUY_VOTING_STRATEGY = "최댓값"



# 모델매도
# SELL_MODEL_DIRS = [rf""]
# SELL_CLS_THRESHOLD = 0.8
# SELL_MODEL_TYPE = "CLS"
# 주식최대보유시간 = 600
# SELL_FEATURE_FUNC = dummy_func
# SELL_SIGNAL_FUNC = dummy_func
# SELL_VOTING_FUNC = dummy_func
# SELL_VOTING_STRATEGY = "한표이상"


# 자동매도
# 1,2,3,4,5분에 1/5씩 자동 매도
SELL_MODEL_DIRS = []
SELL_CLS_THRESHOLD = 0
SELL_MODEL_TYPE = "자동매도"
주식최대보유시간 = 600
SELL_SIGNAL_FUNC = None
SELL_FEATURE_FUNC = None
SELL_VOTING_FUNC = None
SELL_VOTING_STRATEGY = None





TRANSACTION_COMPRESS_FUNC = dummy_func
TRANSACTION_CUT_THRESHOLD = 50 * 10000

TRANSACTION_DF_MAX_LEN = 600 # TRANSACTION_DF_PER_CODE의 최대 행 길이
HOGA_LIST_MAX_LEN = 5 # HOGA_PER_CODE에 보관할 hoga 개수



BUY_END_TIME = "15:19:00 000"  # 해당 시간이 지나면 매수하지 않음
ALL_SELL_TIME = "18:00:00 000" # 해당 시간이 지나면 보유 중인 종목 전부 처분

MAX_ORDER_PRICE = 5 * 10000
MAX_HOLD_STOCK_NUM = 4 # 각 script에서 보유할 수 있는 최대 종목 수. 해당 변수가 X라면 총 5*X개의 종목을 보유 가능

LIST_체결대기 = {}
MY_ACCOUNT = {}
판매예약시간과개수 = defaultdict(list)
중복주문방지시간 = {}
ALL_LOG = [] 
# 로그: 1) prediction 결과. 2) 매수/매도 주문. 3) 주문 체결 완료 통보
TRANSACTION_PER_CODE = defaultdict(list)
HOGA_PER_CODE = defaultdict(list)

TRANSACTION_DF_PER_CODE = defaultdict(pd.DataFrame)

with open(rf"kor_split_codes.json", "r") as f:
    data = json.load(f)
    ACCESS_TOKEN = data['ACCESS_TOKEN']

YYYY_DD_HH_MM = datetime.now().strftime('%Y_%d_%H_%M')


테스트주문완료했나요 = False


데이터예열시간 = 80
주문준비완료 = False
코드시작시간 = get_current_time_formatted()
print("코드시작시간: ", 코드시작시간)
if 코드시작시간 < "08:59:50 000":
    주문준비완료 = True
else:
    print("데이터 예열 필요. 예열 완료 시간: ", add_n_seconds(코드시작시간, 데이터예열시간))



async def main(port="1170", codes_dict={}):
    global BUY_MODEL_DIRS
    global SELL_MODEL_DIRS
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(f"tcp://*:{port}")

    buy_models = []
    sell_models = []
    for buy_model_dir in BUY_MODEL_DIRS:
        buy_models.append(load(buy_model_dir))
    for sell_model_dir in SELL_MODEL_DIRS:
        sell_models.append(load(sell_model_dir))

    await get_data(socket, buy_models, sell_models, codes_dict, port)


async def get_data(socket, buy_models, sell_models, codes_dict, port):
    '''
    codes_dict: 해당 script에서 관리하는 코드목록
    '''
    global MY_ACCOUNT
    global 주문준비완료
    global 판매예약시간과개수
 

    queue = Queue.Queue()
    thread = threading.Thread(target=prediction_worker, args=(queue,))
    thread.start()

    while True:
        #@@@@@@@@@@ socket에서 실시간 체결 데이터 수신 #@@@@@@@
        data = socket.recv_json()
        data = json.loads(data)
        데이터_타입 = data['type']
        단축코드 = data['code']
        데이터 = data['data']        
        
        # 체결 데이터 수신
        if 데이터_타입 == 'S3_' or 데이터_타입 == 'K3_':
            TRANSACTION_PER_CODE[단축코드].append(데이터)

        # 호가 데이터 수신
        elif 데이터_타입 == 'H1_' or  데이터_타입 == 'HA_':
            # 호가 데이터 추가
            # HOGA_PER_CODE[단축코드].append(데이터)
            # if len(HOGA_PER_CODE[단축코드]) > HOGA_LIST_MAX_LEN:
            #     HOGA_PER_CODE[단축코드].pop(0)

            # Transaction 데이터 정규화
            last_transaction_df = pd.DataFrame(TRANSACTION_PER_CODE[단축코드])
            
            if len(last_transaction_df) != 0:
                compressed_df = TRANSACTION_COMPRESS_FUNC(last_transaction_df, cut_threshold=TRANSACTION_CUT_THRESHOLD)
                if compressed_df is None or len(compressed_df) == 0:
                    continue
                TRANSACTION_DF_PER_CODE[단축코드] = pd.concat([TRANSACTION_DF_PER_CODE[단축코드], compressed_df], ignore_index=True)
                TRANSACTION_PER_CODE[단축코드] = []
                if len(TRANSACTION_DF_PER_CODE[단축코드]) > TRANSACTION_DF_MAX_LEN:
                    TRANSACTION_DF_PER_CODE[단축코드] = TRANSACTION_DF_PER_CODE[단축코드].iloc[-TRANSACTION_DF_MAX_LEN:]
                

                # 중복주문방지시간
                # if 단축코드 in 중복주문방지시간:
                #     # 1. 주문 후 0.4초가 지났음에도 아직 주문 완료되지 않은 경우 -> 주문이 실패했다고 판단
                #     if get_time_diff(중복주문방지시간['단축코드'], get_current_time_formatted()) > 0.4:
                #         del 중복주문방지시간[단축코드]
                #     # 2. 주문을 했는데, 아직 주문 완료가 되지 않은 경우 -> 추가 주문하지 않음
                #     else:
                #         continue
                

                현재시각 = get_current_time_formatted()
                호가시간 = 데이터['호가시간']
                호가시간_변환 = convert_체결시간(호가시간)

                
                # Signal 판별
                if 주문준비완료 == False:
                    if get_time_diff(코드시작시간, 현재시각) > 데이터예열시간:
                        주문준비완료 = True
                        print(f"{코드시작시간} -> {현재시각}. 주문준비완료")
                    continue
                is_매수시그널통과 = False
                is_매도시그널통과 = False

                # 매수 시그널 판별
                if len(MY_ACCOUNT) < MAX_HOLD_STOCK_NUM and 단축코드 not in MY_ACCOUNT and 데이터['클라이언트시간'] < BUY_END_TIME:
                    # 데이터 수신이 밀리는 경우 매수 체크 패스
                    if 테스트모드 is False:
                        if get_time_diff_순서고려(호가시간_변환, 현재시각) < -2:
                            print("시간지연필터링", 호가시간_변환, 현재시각)
                            continue
                    is_매수시그널통과 = BUY_SIGNAL_FUNC(TRANSACTION_DF_PER_CODE[단축코드], compressed_df)
                # 매도 시그널판별
                elif 단축코드 in MY_ACCOUNT:
                    if SELL_MODEL_TYPE == "자동매도" or SELL_SIGNAL_FUNC is None:
                        if 현재시각 > 판매예약시간과개수[단축코드][0][0]:
                            is_매도시그널통과 = True
                        else:
                            is_매도시그널통과 = False
                    else:
                        is_매도시그널통과 = SELL_SIGNAL_FUNC(TRANSACTION_DF_PER_CODE[단축코드], compressed_df)
                
                # Signal 판별 통과했다면 매수/매도 판별
                if is_매수시그널통과:
                    queue_input = {
                        'code':단축코드,
                        'data':{'transaction':TRANSACTION_DF_PER_CODE[단축코드], 'hoga':데이터, '단축코드':단축코드},
                        'buy_feature_func': BUY_FEATURE_FUNC, 
                        'sell_feature_func':SELL_FEATURE_FUNC, 
                        '매수매도구분':"매수",
                        'buy_models':buy_models, 
                        'sell_models':sell_models,
                        '데이터클라이언트시간':데이터['클라이언트시간'],
                        'port':port
                    }
                    queue.put(queue_input)
                    
                    
                elif is_매도시그널통과:
                    queue_input = {
                        'code':단축코드,
                        'data':{'transaction':TRANSACTION_DF_PER_CODE[단축코드], 'hoga':데이터, '단축코드':단축코드},
                        'buy_feature_func': BUY_FEATURE_FUNC, 
                        'sell_feature_func':SELL_FEATURE_FUNC, 
                        '매수매도구분':"매도",
                        'buy_models':buy_models, 
                        'sell_models':sell_models,
                        '데이터클라이언트시간':데이터['클라이언트시간'],
                        'port':port
                    }
                    queue.put(queue_input)
                    
                

        elif 데이터_타입 == "SC1":
            print("@@@@@@@@@@ 주식 체결 @@@@@@@@@@")
            print("단축코드: ", 데이터['단축코드'])
            print("체결 클라이언트시간:", 데이터['클라이언트시간'])
            print("체결시각: ", 데이터['체결시각'])
            print("체결가격: ", 데이터['체결가격'])
            print("주문번호: ", 데이터['주문번호'])
            print("체결수량: ", 데이터['체결수량'])
            print("주문종류구분: ", 데이터['주문종류구분'])
            print("매수매도구분: ", 데이터['매수매도구분'])
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            
            account_info = {
                '체결단가':int(데이터['체결가격']),
                '체결번호':데이터['체결번호'],
                '체결수량':int(데이터['체결수량']),
                '체결시각':데이터['체결시각'],
                '클라이언트시간':데이터['클라이언트시간'],
            }
            단축코드 = 데이터['단축코드']
            #@@@ 매수
            if 데이터['매수매도구분'] == "2" and 단축코드 in codes_dict:
                if 단축코드 not in MY_ACCOUNT or MY_ACCOUNT[단축코드] == []:
                    MY_ACCOUNT[단축코드] = account_info
                
                else:
                    MY_ACCOUNT[단축코드]['체결단가'] = int((MY_ACCOUNT[단축코드]['체결단가']*int(MY_ACCOUNT[단축코드]['체결수량']) + int(데이터['체결가격'])* int(데이터['체결수량']))/(int(MY_ACCOUNT[단축코드]['체결수량']) + int(데이터['체결수량'])))
                    MY_ACCOUNT[단축코드]['체결수량'] += int(데이터['체결수량'])

                if SELL_MODEL_TYPE == "자동매도":
                    체결수량 = int(데이터['체결수량'])
                    판매수량리스트 = divide_into_N(체결수량, 5)
                    for i in range(5):
                        판매예약시간과개수[단축코드].append([add_n_seconds(데이터['클라이언트시간'], 60*(i+1)), 판매수량리스트[i]])
                    판매예약시간과개수[단축코드] = sort_by_timestamp(판매예약시간과개수[단축코드])

            
            #@@@ 매도
            elif 데이터['매수매도구분'] == "1" and 단축코드 in codes_dict and 단축코드 in MY_ACCOUNT:
                MY_ACCOUNT[단축코드]['체결수량'] -= int(데이터['체결수량'])   
                if MY_ACCOUNT[단축코드]['체결수량'] <= 0:
                    del MY_ACCOUNT[단축코드]
                    del 판매예약시간과개수[단축코드]
                # ALL_LOG.append([get_current_time_formatted(), "매도 체결 로그", 데이터])
                
        
def prediction_worker(queue):
    while True:
        data = queue.get()
        prediction_and_trading(data)
    

def prediction_and_trading(data_dict):
    global MY_ACCOUNT
    global 주식최대보유시간
    global 판매예약시간과개수
    global SELL_MODEL_TYPE
    
    # try:
    port = data_dict['port']
    buy_feature_func = data_dict['buy_feature_func'] 
    sell_feature_func = data_dict['sell_feature_func'] 
    매수매도구분 = data_dict['매수매도구분']
    buy_models = data_dict['buy_models']
    sell_models = data_dict['sell_models']
    data = data_dict['data']
    단축코드 = data['단축코드']
    데이터클라이언트시간 = data_dict['데이터클라이언트시간']
    transaction_df = data['transaction']
    
    #### 매수 판별 ####
    if 매수매도구분 == "매수":
        #@#@

        featured_data = buy_feature_func(transaction_df, 데이터클라이언트시간, data['hoga'])
        if featured_data is None:
            return
        
        # BUY MODEL CLS타입
        buy_predictions = []
        for buy_model in buy_models:
            prediction = buy_model.predict([featured_data])[0]
            if type(prediction) == np.array:
                prediction = prediction[2]
            buy_predictions.append(prediction)
        is_매수 = BUY_VOTING_FUNC(predictions=buy_predictions, thresholds=BUY_THRESHOLDs)
        # 매수판별완료시간 = get_current_time_formatted()
    
        
        
        if is_매수:
            매수호가1 = data['hoga']['매수호가1']
            매도호가1 = data['hoga']['매도호가1']
            주문수량 = MAX_ORDER_PRICE//int(매도호가1)
            if 주문수량 == 0:
                if 매도호가1 < 15*10000:
                    주문수량 = 1
                else:
                    #@@@
                    print("20만원 초과는 구매 X")
                    주문수량 = 0
            ### 주식 주문
            if 테스트모드 is False:
                # 시장가 주문
                buy_order(access_token=ACCESS_TOKEN,
                            stock_code=단축코드,
                            order_quan=주문수량,
                            order_price=0,
                            order_type="03",
                            order_condition="1"
                            )
                # 지정가 주문
                buy_order(access_token=ACCESS_TOKEN,
                            stock_code=단축코드,
                            order_quan=주문수량,
                            order_price=매도호가1,
                            order_type="00",
                            order_condition="0"
                            )
            완료후시간 = get_current_time_formatted()
            print(f"매수 주문. 시간: {완료후시간}. 데이터시간:{데이터클라이언트시간}. 매도호가1:{매도호가1}. 코드: {단축코드}. MY_ACCOUNT:{MY_ACCOUNT}")
            print("#######################\n\n")
            매수주문데이터 = [transaction_df, featured_data, 데이터클라이언트시간, 완료후시간, 단축코드, data['hoga'], buy_predictions, '모델매수']
       
       
            return
            # 중복주문방지시간[단축코드] = get_current_time_formatted()


    #### 매도 판별 ####
    elif 매수매도구분 == "매도":
        try:
            매수체결시간 = MY_ACCOUNT[단축코드]['클라이언트시간']
        except:
            print(f"매수체결시간 존재 X. 코드:{단축코드}. MY_ACCOUNT:{MY_ACCOUNT}") 
            return
        매수호가1 = data['hoga']['매수호가1']
        매도호가1 = data['hoga']['매도호가1']

        if SELL_MODEL_TYPE == "자동매도":
            판매예약시간 = 판매예약시간과개수[단축코드][0][0]
            판매예약개수 = 판매예약시간과개수[단축코드][0][1]
            if 데이터클라이언트시간 > 판매예약시간:
                sell_order(access_token=ACCESS_TOKEN,
                    stock_code=단축코드,
                    order_quan=판매예약개수,
                    order_price=0,
                    order_type="03",
                    order_condition="0"
                    )
                del 판매예약시간과개수[단축코드][0]
                완료후시간 = get_current_time_formatted()
                print(f"자동 매도 주문. 시간: {완료후시간}. 코드: {단축코드}. 매도개수: {판매예약개수}. 판매예약시간과개수:{판매예약시간과개수}. MY_ACCOUNT:{MY_ACCOUNT}.")
            return
            
        else:
            매수매도시간차 = get_time_diff(매수체결시간, 데이터클라이언트시간)
            # 시간초과 매도
            if 매수매도시간차 > 주식최대보유시간:
                sell_order(access_token=ACCESS_TOKEN,
                        stock_code=단축코드,
                        order_quan=MY_ACCOUNT[단축코드]['체결수량'],
                        order_price=0,
                        order_type="03",
                        order_condition="0"
                        )
                완료후시간 = get_current_time_formatted()
                print(f"매도 주문. 시간: {완료후시간}. 코드: {단축코드}. MY_ACCOUNT:{MY_ACCOUNT}")

                return
            
            featured_data = sell_feature_func(transaction_df, 데이터클라이언트시간, data['hoga'])
            if featured_data is None:
                return
            featured_data += [매수매도시간차]
            
            if SELL_MODEL_TYPE == "CLS":
                sell_predictions = []
                for sell_model in sell_models:
                    prediction_probs = sell_model.predict([featured_data])[0]
                    # prediction = np.argmax(prediction_probs, axis=1)[0]
                    sell_predictions.append(prediction_probs)
                is_매도 = SELL_VOTING_FUNC(predictions=sell_predictions, 투표전략=SELL_VOTING_STRATEGY, threshold=SELL_CLS_THRESHOLD)
            elif SELL_MODEL_TYPE == "REG":
                print("SELL_MODEL_TYPE REG 아직 구현 안함")
                return
            
            
            if is_매도:
                sell_order(access_token=ACCESS_TOKEN,
                        stock_code=단축코드,
                        order_quan=MY_ACCOUNT[단축코드]['체결수량'],
                        order_price=0,
                        order_type="03",
                        order_condition="0"
                        )
                완료후시간 = get_current_time_formatted()
                print(f"매도 주문. 시간: {완료후시간}. 코드: {단축코드}. MY_ACCOUNT:{MY_ACCOUNT}")

                return


    # except Exception as e:
    #     print("prediction_and_trading 에러: ", e)
    #     return
    
    
# @@@@@@@@@@@@@@@@@@@ 공용 함수들 선언 끝 @@@@@@@@@@@@@@@@@@

if __name__ == "__main__":
    print("split_realtime_trading_utils main 실행")
    buy_order(access_token=ACCESS_TOKEN, stock_code="004830", order_quan=1, order_price=7100, order_type="00", order_condition="0")
    # sell_order(access_token=ACCESS_TOKEN, stock_code="004830", order_quan=1, order_price=0, order_type="03", order_condition="0")
    