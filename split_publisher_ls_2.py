from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys
import win32com.client
import pythoncom
from xa_class_kor import XAReal_KOR, XASession, XAQueryEventHandler_T1102, StockDataManager, StockDataManager_rq_symbol_combine
# from get_nasdaq_tickers import get_nd_tickers
from zmq.asyncio import Context
import zmq
import json

from get_kor_tickers import *
import time
from datetime import datetime
import gc
gc.collect() 

ID = ""
PW = ""
PI = ""

data_port = "1172"


def get_current_time_hhmmss():
    now = datetime.now()
    return now.strftime("%H%M%S")


with open(rf"kor_split_codes.json", "r") as f:
    data =json.load(f)
    kospi_codes = data['kospi_split_2']
    kosdaq_codes = data['kosdaq_split_2']


import pandas as pd


class Main():
    '''
    메인 클래스. 증권 프로그램(Xing Api) 초기 세팅
    Session: 증권서버 연동, 로그인 등을 처리함
    XAQuery: 단발성 요청 (계좌 정보, 일봉 데이터, 등등 ..)
    XAReal : 지속 요청 (Tick봉, ..)
    '''
    def __init__(self):
        print("kor_data_publisher 클래스 실행")
        session = win32com.client.DispatchWithEvents("XA_session.XASession", XASession)

        ## 로그인
        # ConnectServer -> 실제/모의 서버에 접속한다. 모의서버: "demo.ebestsec.co.kr". 실제서버: "hts.ebestsec.co.kr"
        session.ConnectServer("hts.ebestsec.co.kr", 20001) # 모의투자:  ("demo.ebestsec.co.kr", 포트번호)
        session.Login(ID,PW, PI, 0, False)

        while XASession.is_login is False:
            pythoncom.PumpWaitingMessages()

        ## 계좌번호 조회
        print("---------------------------------")
        print("계좌번호 조회")
        count = session.GetAccountListCount()
        for i in range(count):
            szAcct = session.GetAccountList(i)
            print("계좌번호: ", szAcct)
        print("---------------------------------")


        
        ## 데이터 Query
        instXAQuery_T1102 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandler_T1102)
        instXAQuery_T1102.ResFileName = r"C:\LS_SEC\xingAPI\Res\t1102.res"
        instXAQuery_T1102.SetFieldData("t1102InBlock", "shcode", 0, "005930") # (tr코드, shcode, 단일데이터조회:0, 코드)
        instXAQuery_T1102.Request(0)
        while XAQueryEventHandler_T1102.query_state == 0:
            pythoncom.PumpWaitingMessages()

        name = instXAQuery_T1102.GetFieldData("t1102OutBlock", "hname", 0)
        price = instXAQuery_T1102.GetFieldData("t1102OutBlock", "price", 0)
        print("###테스트###")
        print(name)
        print(price)

        print("###테스트###")



        stockDataManager1 = StockDataManager_rq_symbol_combine()
        ## 실시간 체결 데이터 요청
        # 한국주식 체결
        rq_ids = []
        codes = []
        for code in kospi_codes:
            rq_ids.append("S3_")
            codes.append(code)
            rq_ids.append("H1_")
            codes.append(code)
        for code in kosdaq_codes:
            rq_ids.append("K3_")
            codes.append(code)
            rq_ids.append("HA_")
            codes.append(code)
            
        print(f"{len(rq_ids)}. {len(codes)}")
        zmq_context = zmq.Context()
        stockDataManager1.create_instances(rq_ids, codes, XAReal_KOR, port=data_port, zmq_context=zmq_context)

        for rq_id, stock_code in zip(rq_ids, codes):
            instance_name = f"inst{rq_id}_Event_{stock_code}"
            stockDataManager1.instances[instance_name].ResFileName = rf"C:\LS_SEC\xingAPI\Res\{rq_id}.res"
            stockDataManager1.instances[instance_name].SetFieldData("InBlock", "shcode", f"{stock_code}")
            stockDataManager1.instances[instance_name].AdviseRealData()

       
        
        while True:
            pythoncom.PumpWaitingMessages()
     
if __name__ == "__main__":
    Main()