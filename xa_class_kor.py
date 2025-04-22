from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys
import win32com.client
import pythoncom
from datetime import datetime
import time
import asyncio
import mysql.connector
from datetime import datetime
from collections import deque

import win32com.client
from typing import List, Dict

from zmq.asyncio import Context
import zmq
import json
import random
from real_trading_utils import get_current_time_formatted


STAND_BY = 0
RECEIVED = 1


class XASession:
    is_login = False
    login_state = STAND_BY
    def OnLogin(self, code, msg):
        XASession.login_state = RECEIVED
        print('로그인 결과: ',msg)
        print('로그인 결과 code: ',code)

        if code == "0000":
            XASession.is_login = True
        else:
            XASession.is_login = False
        
        return

class XAQuery:
    SC0_Event = None
    SC1_Event = None


class XAReal_KOR:
    S3_Event = None
    K3_Event = None
    GSC_Event = None
    port = 6667  # 기본값 설정
    context = None

    동시호가체크 = {}


    with open(rf"kor_split_codes.json", "r") as f:
        data =json.load(f)
        kospi_codes = data['kospi_split_0']
        kosdaq_codes = data['kosdaq_split_0']
    codes0 = kospi_codes + kosdaq_codes
    codes0 = {code:True for code in codes0}

    with open(rf"kor_split_codes.json", "r") as f:
        data =json.load(f)
        kospi_codes = data['kospi_split_1']
        kosdaq_codes = data['kosdaq_split_1']
    codes1 = kospi_codes + kosdaq_codes
    codes1 = {code:True for code in codes1}

    with open(rf"kor_split_codes.json", "r") as f:
        data =json.load(f)
        kospi_codes = data['kospi_split_2']
        kosdaq_codes = data['kosdaq_split_2']
    codes2 = kospi_codes + kosdaq_codes
    codes2 = {code:True for code in codes2}

    with open(rf"kor_split_codes.json", "r") as f:
        data =json.load(f)
        kospi_codes = data['kospi_split_3']
        kosdaq_codes = data['kosdaq_split_3']
    codes3 = kospi_codes + kosdaq_codes
    codes3 = {code:True for code in codes3}

    with open(rf"kor_split_codes.json", "r") as f:
        data =json.load(f)
        kospi_codes = data['kospi_split_4']
        kosdaq_codes = data['kosdaq_split_4']
    codes4 = kospi_codes + kosdaq_codes
    codes4 = {code:True for code in codes4} 

    print("codes0: ", codes0)
    print("codes1: ", codes1)
    print("codes2: ", codes2)
    print("codes3: ", codes3)
    print("codes4: ", codes4)

    context_SC1 = zmq.Context()
    socket0 = context_SC1.socket(zmq.PUSH)
    socket0.connect(f"tcp://localhost:1170")

    socket1 = context_SC1.socket(zmq.PUSH)
    socket1.connect(f"tcp://localhost:1171")

    socket2 = context_SC1.socket(zmq.PUSH)
    socket2.connect(f"tcp://localhost:1172")

    socket3 = context_SC1.socket(zmq.PUSH)
    socket3.connect(f"tcp://localhost:1173")

    socket4 = context_SC1.socket(zmq.PUSH)
    socket4.connect(f"tcp://localhost:1174")

    def __init__(self):
        # self.context = zmq.Context()
        
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(f"tcp://localhost:{self.port}")
        self.hoga_collected_check = {}
    
        
    def OnReceiveRealData(self, szTrCode):        
        if get_current_time_formatted() < "09:00:00 000":
            return
        if szTrCode == "K1_": # KOSPI 거래원
            클라이언트시간 = get_current_time_formatted()
            매도증권사코드1 = self.GetFieldData("OutBlock", "offerno1")
            매수증권사코드1 = self.GetFieldData("OutBlock", "bidno1")
            매도회원사명1 = self.GetFieldData("OutBlock", "offertrad1")
            매수회원사명1 = self.GetFieldData("OutBlock", "bidtrad1")
            매도거래량1 = self.GetFieldData("OutBlock", "tradmdvol1")
            매수거래량1 = self.GetFieldData("OutBlock", "tradmsvol1")
            매도거래량비중1 = self.GetFieldData("OutBlock", "tradmdrate1")
            매수거래량비중1 = self.GetFieldData("OutBlock", "tradmsrate1")
            매도거래량직전대비1 = self.GetFieldData("OutBlock", "tradmdcha1")
            매수거래량직전대비1 = self.GetFieldData("OutBlock", "tradmscha1")

            매도증권사코드2 = self.GetFieldData("OutBlock", "offerno2")
            매수증권사코드2 = self.GetFieldData("OutBlock", "bidno2")
            매도회원사명2 = self.GetFieldData("OutBlock", "offertrad2")
            매수회원사명2 = self.GetFieldData("OutBlock", "bidtrad2")
            매도거래량2 = self.GetFieldData("OutBlock", "tradmdvol2")
            매수거래량2 = self.GetFieldData("OutBlock", "tradmsvol2")
            매도거래량비중2 = self.GetFieldData("OutBlock", "tradmdrate2")
            매수거래량비중2 = self.GetFieldData("OutBlock", "tradmsrate2")
            매도거래량직전대비2 = self.GetFieldData("OutBlock", "tradmdcha2")
            매수거래량직전대비2 = self.GetFieldData("OutBlock", "tradmscha2")

            매도증권사코드3 = self.GetFieldData("OutBlock", "offerno3")
            매수증권사코드3 = self.GetFieldData("OutBlock", "bidno3")
            매도회원사명3 = self.GetFieldData("OutBlock", "offertrad3")
            매수회원사명3 = self.GetFieldData("OutBlock", "bidtrad3")
            매도거래량3 = self.GetFieldData("OutBlock", "tradmdvol3")
            매수거래량3 = self.GetFieldData("OutBlock", "tradmsvol3")
            매도거래량비중3 = self.GetFieldData("OutBlock", "tradmdrate3")
            매수거래량비중3 = self.GetFieldData("OutBlock", "tradmsrate3")
            매도거래량직전대비3 = self.GetFieldData("OutBlock", "tradmdcha3")
            매수거래량직전대비3 = self.GetFieldData("OutBlock", "tradmscha3")

            매도증권사코드4 = self.GetFieldData("OutBlock", "offerno4")
            매수증권사코드4 = self.GetFieldData("OutBlock", "bidno4")
            매도회원사명4 = self.GetFieldData("OutBlock", "offertrad4")
            매수회원사명4 = self.GetFieldData("OutBlock", "bidtrad4")
            매도거래량4 = self.GetFieldData("OutBlock", "tradmdvol4")
            매수거래량4 = self.GetFieldData("OutBlock", "tradmsvol4")
            매도거래량비중4 = self.GetFieldData("OutBlock", "tradmdrate4")
            매수거래량비중4 = self.GetFieldData("OutBlock", "tradmsrate4")
            매도거래량직전대비4 = self.GetFieldData("OutBlock", "tradmdcha4")
            매수거래량직전대비4 = self.GetFieldData("OutBlock", "tradmscha4")

            매도증권사코드5 = self.GetFieldData("OutBlock", "offerno5")
            매수증권사코드5 = self.GetFieldData("OutBlock", "bidno5")
            매도회원사명5 = self.GetFieldData("OutBlock", "offertrad5")
            매수회원사명5 = self.GetFieldData("OutBlock", "bidtrad5")
            매도거래량5 = self.GetFieldData("OutBlock", "tradmdvol5")
            매수거래량5 = self.GetFieldData("OutBlock", "tradmsvol5")
            매도거래량비중5 = self.GetFieldData("OutBlock", "tradmdrate5")
            매수거래량비중5 = self.GetFieldData("OutBlock", "tradmsrate5")
            매도거래량직전대비5 = self.GetFieldData("OutBlock", "tradmdcha5")
            매수거래량직전대비5 = self.GetFieldData("OutBlock", "tradmscha5")

            외국계증권사매도합계 = self.GetFieldData("OutBlock", "ftradmdvol")
            외국계증권사매수합계 = self.GetFieldData("OutBlock", "ftradmsvol")
            외국계증권사매도거래량비중 = self.GetFieldData("OutBlock", "ftradmdrate")
            외국계증권사매수거래량비중 = self.GetFieldData("OutBlock", "ftradmsrate")
            외국계증권사매도거래량직전대비 = self.GetFieldData("OutBlock", "ftradmdcha")
            외국계증권사매수거래량직전대비 = self.GetFieldData("OutBlock", "ftradmscha")
            단축코드 = self.GetFieldData("OutBlock", "shcode")

            매도거래대금1 = self.GetFieldData("OutBlock", "tradmdval1")
            매수거래대금1 = self.GetFieldData("OutBlock", "tradmsval1")
            매도평균단가1 = self.GetFieldData("OutBlock", "tradmdavg1")
            매수평균단가1 = self.GetFieldData("OutBlock", "tradmsavg1")

            매도거래대금2 = self.GetFieldData("OutBlock", "tradmdval2")
            매수거래대금2 = self.GetFieldData("OutBlock", "tradmsval2")
            매도평균단가2 = self.GetFieldData("OutBlock", "tradmdavg2")
            매수평균단가2 = self.GetFieldData("OutBlock", "tradmsavg2")

            매도거래대금3 = self.GetFieldData("OutBlock", "tradmdval3")
            매수거래대금3 = self.GetFieldData("OutBlock", "tradmsval3")
            매도평균단가3 = self.GetFieldData("OutBlock", "tradmdavg3")
            매수평균단가3 = self.GetFieldData("OutBlock", "tradmsavg3")

            매도거래대금4 = self.GetFieldData("OutBlock", "tradmdval4")
            매수거래대금4 = self.GetFieldData("OutBlock", "tradmsval4")
            매도평균단가4 = self.GetFieldData("OutBlock", "tradmdavg4")
            매수평균단가4 = self.GetFieldData("OutBlock", "tradmsavg4")

            매도거래대금5 = self.GetFieldData("OutBlock", "tradmdval5")
            매수거래대금5 = self.GetFieldData("OutBlock", "tradmsval5")
            매도평균단가5 = self.GetFieldData("OutBlock", "tradmdavg5")
            매수평균단가5 = self.GetFieldData("OutBlock", "tradmsavg5")

            외국계증권사매도거래대금 = self.GetFieldData("OutBlock", "ftradmdval")
            외국계증권사매수거래대금 = self.GetFieldData("OutBlock", "ftradmsval")
            외국계증권사매도평균단가 = self.GetFieldData("OutBlock", "ftradmdavg")
            외국계증권사매수평균단가 = self.GetFieldData("OutBlock", "ftradmsavg")

            data = {
                '클라이언트시간': 클라이언트시간,
                '단축코드': 단축코드,

                '매도증권사코드1': 매도증권사코드1,
                '매수증권사코드1': 매수증권사코드1,
                '매도회원사명1': 매도회원사명1,
                '매수회원사명1': 매수회원사명1,
                '매도거래량1': 매도거래량1,
                '매수거래량1': 매수거래량1,
                '매도거래량비중1': 매도거래량비중1,
                '매수거래량비중1': 매수거래량비중1,
                '매도거래량직전대비1': 매도거래량직전대비1,
                '매수거래량직전대비1': 매수거래량직전대비1,

                '매도증권사코드2': 매도증권사코드2,
                '매수증권사코드2': 매수증권사코드2,
                '매도회원사명2': 매도회원사명2,
                '매수회원사명2': 매수회원사명2,
                '매도거래량2': 매도거래량2,
                '매수거래량2': 매수거래량2,
                '매도거래량비중2': 매도거래량비중2,
                '매수거래량비중2': 매수거래량비중2,
                '매도거래량직전대비2': 매도거래량직전대비2,
                '매수거래량직전대비2': 매수거래량직전대비2,

                '매도증권사코드3': 매도증권사코드3,
                '매수증권사코드3': 매수증권사코드3,
                '매도회원사명3': 매도회원사명3,
                '매수회원사명3': 매수회원사명3,
                '매도거래량3': 매도거래량3,
                '매수거래량3': 매수거래량3,
                '매도거래량비중3': 매도거래량비중3,
                '매수거래량비중3': 매수거래량비중3,
                '매도거래량직전대비3': 매도거래량직전대비3,
                '매수거래량직전대비3': 매수거래량직전대비3,

                '매도증권사코드4': 매도증권사코드4,
                '매수증권사코드4': 매수증권사코드4,
                '매도회원사명4': 매도회원사명4,
                '매수회원사명4': 매수회원사명4,
                '매도거래량4': 매도거래량4,
                '매수거래량4': 매수거래량4,
                '매도거래량비중4': 매도거래량비중4,
                '매수거래량비중4': 매수거래량비중4,
                '매도거래량직전대비4': 매도거래량직전대비4,
                '매수거래량직전대비4': 매수거래량직전대비4,

                '매도증권사코드5': 매도증권사코드5,
                '매수증권사코드5': 매수증권사코드5,
                '매도회원사명5': 매도회원사명5,
                '매수회원사명5': 매수회원사명5,
                '매도거래량5': 매도거래량5,
                '매수거래량5': 매수거래량5,
                '매도거래량비중5': 매도거래량비중5,
                '매수거래량비중5': 매수거래량비중5,
                '매도거래량직전대비5': 매도거래량직전대비5,
                '매수거래량직전대비5': 매수거래량직전대비5,

                '외국계증권사매도합계': 외국계증권사매도합계,
                '외국계증권사매수합계': 외국계증권사매수합계,
                '외국계증권사매도거래량비중': 외국계증권사매도거래량비중,
                '외국계증권사매수거래량비중': 외국계증권사매수거래량비중,
                '외국계증권사매도거래량직전대비': 외국계증권사매도거래량직전대비,
                '외국계증권사매수거래량직전대비': 외국계증권사매수거래량직전대비,

                '매도거래대금1': 매도거래대금1,
                '매수거래대금1': 매수거래대금1,
                '매도평균단가1': 매도평균단가1,
                '매수평균단가1': 매수평균단가1,
                
                '매도거래대금2': 매도거래대금2,
                '매수거래대금2': 매수거래대금2,
                '매도평균단가2': 매도평균단가2,
                '매수평균단가2': 매수평균단가2,

                '매도거래대금3': 매도거래대금3,
                '매수거래대금3': 매수거래대금3,
                '매도평균단가3': 매도평균단가3,
                '매수평균단가3': 매수평균단가3,

                '매도거래대금4': 매도거래대금4,
                '매수거래대금4': 매수거래대금4,
                '매도평균단가4': 매도평균단가4,
                '매수평균단가4': 매수평균단가4,

                '매도거래대금5': 매도거래대금5,
                '매수거래대금5': 매수거래대금5,
                '매도평균단가5': 매도평균단가5,
                '매수평균단가5': 매수평균단가5,


                '외국계증권사매도거래대금': 외국계증권사매도거래대금,
                '외국계증권사매수거래대금': 외국계증권사매수거래대금,
                '외국계증권사매도평균단가': 외국계증권사매도평균단가,
                '외국계증권사매수평균단가': 외국계증권사매수평균단가,
            }
    
            # Send data
            self.send_data(szTrCode, 단축코드, data)

        elif szTrCode == "OK_": # KOSDAQ 거래원
            클라이언트시간 = get_current_time_formatted()
            매도증권사코드1 = self.GetFieldData("OutBlock", "offerno1")
            매수증권사코드1 = self.GetFieldData("OutBlock", "bidno1")
            매도회원사명1 = self.GetFieldData("OutBlock", "offertrad1")
            매수회원사명1 = self.GetFieldData("OutBlock", "bidtrad1")
            매도거래량1 = self.GetFieldData("OutBlock", "tradmdvol1")
            매수거래량1 = self.GetFieldData("OutBlock", "tradmsvol1")
            매도거래량비중1 = self.GetFieldData("OutBlock", "tradmdrate1")
            매수거래량비중1 = self.GetFieldData("OutBlock", "tradmsrate1")
            매도거래량직전대비1 = self.GetFieldData("OutBlock", "tradmdcha1")
            매수거래량직전대비1 = self.GetFieldData("OutBlock", "tradmscha1")

            매도증권사코드2 = self.GetFieldData("OutBlock", "offerno2")
            매수증권사코드2 = self.GetFieldData("OutBlock", "bidno2")
            매도회원사명2 = self.GetFieldData("OutBlock", "offertrad2")
            매수회원사명2 = self.GetFieldData("OutBlock", "bidtrad2")
            매도거래량2 = self.GetFieldData("OutBlock", "tradmdvol2")
            매수거래량2 = self.GetFieldData("OutBlock", "tradmsvol2")
            매도거래량비중2 = self.GetFieldData("OutBlock", "tradmdrate2")
            매수거래량비중2 = self.GetFieldData("OutBlock", "tradmsrate2")
            매도거래량직전대비2 = self.GetFieldData("OutBlock", "tradmdcha2")
            매수거래량직전대비2 = self.GetFieldData("OutBlock", "tradmscha2")

            매도증권사코드3 = self.GetFieldData("OutBlock", "offerno3")
            매수증권사코드3 = self.GetFieldData("OutBlock", "bidno3")
            매도회원사명3 = self.GetFieldData("OutBlock", "offertrad3")
            매수회원사명3 = self.GetFieldData("OutBlock", "bidtrad3")
            매도거래량3 = self.GetFieldData("OutBlock", "tradmdvol3")
            매수거래량3 = self.GetFieldData("OutBlock", "tradmsvol3")
            매도거래량비중3 = self.GetFieldData("OutBlock", "tradmdrate3")
            매수거래량비중3 = self.GetFieldData("OutBlock", "tradmsrate3")
            매도거래량직전대비3 = self.GetFieldData("OutBlock", "tradmdcha3")
            매수거래량직전대비3 = self.GetFieldData("OutBlock", "tradmscha3")

            매도증권사코드4 = self.GetFieldData("OutBlock", "offerno4")
            매수증권사코드4 = self.GetFieldData("OutBlock", "bidno4")
            매도회원사명4 = self.GetFieldData("OutBlock", "offertrad4")
            매수회원사명4 = self.GetFieldData("OutBlock", "bidtrad4")
            매도거래량4 = self.GetFieldData("OutBlock", "tradmdvol4")
            매수거래량4 = self.GetFieldData("OutBlock", "tradmsvol4")
            매도거래량비중4 = self.GetFieldData("OutBlock", "tradmdrate4")
            매수거래량비중4 = self.GetFieldData("OutBlock", "tradmsrate4")
            매도거래량직전대비4 = self.GetFieldData("OutBlock", "tradmdcha4")
            매수거래량직전대비4 = self.GetFieldData("OutBlock", "tradmscha4")

            매도증권사코드5 = self.GetFieldData("OutBlock", "offerno5")
            매수증권사코드5 = self.GetFieldData("OutBlock", "bidno5")
            매도회원사명5 = self.GetFieldData("OutBlock", "offertrad5")
            매수회원사명5 = self.GetFieldData("OutBlock", "bidtrad5")
            매도거래량5 = self.GetFieldData("OutBlock", "tradmdvol5")
            매수거래량5 = self.GetFieldData("OutBlock", "tradmsvol5")
            매도거래량비중5 = self.GetFieldData("OutBlock", "tradmdrate5")
            매수거래량비중5 = self.GetFieldData("OutBlock", "tradmsrate5")
            매도거래량직전대비5 = self.GetFieldData("OutBlock", "tradmdcha5")
            매수거래량직전대비5 = self.GetFieldData("OutBlock", "tradmscha5")

            외국계증권사매도합계 = self.GetFieldData("OutBlock", "ftradmdvol")
            외국계증권사매수합계 = self.GetFieldData("OutBlock", "ftradmsvol")
            외국계증권사매도거래량비중 = self.GetFieldData("OutBlock", "ftradmdrate")
            외국계증권사매수거래량비중 = self.GetFieldData("OutBlock", "ftradmsrate")
            외국계증권사매도거래량직전대비 = self.GetFieldData("OutBlock", "ftradmdcha")
            외국계증권사매수거래량직전대비 = self.GetFieldData("OutBlock", "ftradmscha")
            단축코드 = self.GetFieldData("OutBlock", "shcode")

            매도거래대금1 = self.GetFieldData("OutBlock", "tradmdval1")
            매수거래대금1 = self.GetFieldData("OutBlock", "tradmsval1")
            매도평균단가1 = self.GetFieldData("OutBlock", "tradmdavg1")
            매수평균단가1 = self.GetFieldData("OutBlock", "tradmsavg1")

            매도거래대금2 = self.GetFieldData("OutBlock", "tradmdval2")
            매수거래대금2 = self.GetFieldData("OutBlock", "tradmsval2")
            매도평균단가2 = self.GetFieldData("OutBlock", "tradmdavg2")
            매수평균단가2 = self.GetFieldData("OutBlock", "tradmsavg2")

            매도거래대금3 = self.GetFieldData("OutBlock", "tradmdval3")
            매수거래대금3 = self.GetFieldData("OutBlock", "tradmsval3")
            매도평균단가3 = self.GetFieldData("OutBlock", "tradmdavg3")
            매수평균단가3 = self.GetFieldData("OutBlock", "tradmsavg3")

            매도거래대금4 = self.GetFieldData("OutBlock", "tradmdval4")
            매수거래대금4 = self.GetFieldData("OutBlock", "tradmsval4")
            매도평균단가4 = self.GetFieldData("OutBlock", "tradmdavg4")
            매수평균단가4 = self.GetFieldData("OutBlock", "tradmsavg4")

            매도거래대금5 = self.GetFieldData("OutBlock", "tradmdval5")
            매수거래대금5 = self.GetFieldData("OutBlock", "tradmsval5")
            매도평균단가5 = self.GetFieldData("OutBlock", "tradmdavg5")
            매수평균단가5 = self.GetFieldData("OutBlock", "tradmsavg5")

            외국계증권사매도거래대금 = self.GetFieldData("OutBlock", "ftradmdval")
            외국계증권사매수거래대금 = self.GetFieldData("OutBlock", "ftradmsval")
            외국계증권사매도평균단가 = self.GetFieldData("OutBlock", "ftradmdavg")
            외국계증권사매수평균단가 = self.GetFieldData("OutBlock", "ftradmsavg")

            data = {
                '클라이언트시간': 클라이언트시간,
                '단축코드': 단축코드,

                '매도증권사코드1': 매도증권사코드1,
                '매수증권사코드1': 매수증권사코드1,
                '매도회원사명1': 매도회원사명1,
                '매수회원사명1': 매수회원사명1,
                '매도거래량1': 매도거래량1,
                '매수거래량1': 매수거래량1,
                '매도거래량비중1': 매도거래량비중1,
                '매수거래량비중1': 매수거래량비중1,
                '매도거래량직전대비1': 매도거래량직전대비1,
                '매수거래량직전대비1': 매수거래량직전대비1,

                '매도증권사코드2': 매도증권사코드2,
                '매수증권사코드2': 매수증권사코드2,
                '매도회원사명2': 매도회원사명2,
                '매수회원사명2': 매수회원사명2,
                '매도거래량2': 매도거래량2,
                '매수거래량2': 매수거래량2,
                '매도거래량비중2': 매도거래량비중2,
                '매수거래량비중2': 매수거래량비중2,
                '매도거래량직전대비2': 매도거래량직전대비2,
                '매수거래량직전대비2': 매수거래량직전대비2,

                '매도증권사코드3': 매도증권사코드3,
                '매수증권사코드3': 매수증권사코드3,
                '매도회원사명3': 매도회원사명3,
                '매수회원사명3': 매수회원사명3,
                '매도거래량3': 매도거래량3,
                '매수거래량3': 매수거래량3,
                '매도거래량비중3': 매도거래량비중3,
                '매수거래량비중3': 매수거래량비중3,
                '매도거래량직전대비3': 매도거래량직전대비3,
                '매수거래량직전대비3': 매수거래량직전대비3,

                '매도증권사코드4': 매도증권사코드4,
                '매수증권사코드4': 매수증권사코드4,
                '매도회원사명4': 매도회원사명4,
                '매수회원사명4': 매수회원사명4,
                '매도거래량4': 매도거래량4,
                '매수거래량4': 매수거래량4,
                '매도거래량비중4': 매도거래량비중4,
                '매수거래량비중4': 매수거래량비중4,
                '매도거래량직전대비4': 매도거래량직전대비4,
                '매수거래량직전대비4': 매수거래량직전대비4,

                '매도증권사코드5': 매도증권사코드5,
                '매수증권사코드5': 매수증권사코드5,
                '매도회원사명5': 매도회원사명5,
                '매수회원사명5': 매수회원사명5,
                '매도거래량5': 매도거래량5,
                '매수거래량5': 매수거래량5,
                '매도거래량비중5': 매도거래량비중5,
                '매수거래량비중5': 매수거래량비중5,
                '매도거래량직전대비5': 매도거래량직전대비5,
                '매수거래량직전대비5': 매수거래량직전대비5,

                '외국계증권사매도합계': 외국계증권사매도합계,
                '외국계증권사매수합계': 외국계증권사매수합계,
                '외국계증권사매도거래량비중': 외국계증권사매도거래량비중,
                '외국계증권사매수거래량비중': 외국계증권사매수거래량비중,
                '외국계증권사매도거래량직전대비': 외국계증권사매도거래량직전대비,
                '외국계증권사매수거래량직전대비': 외국계증권사매수거래량직전대비,

                '매도거래대금1': 매도거래대금1,
                '매수거래대금1': 매수거래대금1,
                '매도평균단가1': 매도평균단가1,
                '매수평균단가1': 매수평균단가1,
                
                '매도거래대금2': 매도거래대금2,
                '매수거래대금2': 매수거래대금2,
                '매도평균단가2': 매도평균단가2,
                '매수평균단가2': 매수평균단가2,

                '매도거래대금3': 매도거래대금3,
                '매수거래대금3': 매수거래대금3,
                '매도평균단가3': 매도평균단가3,
                '매수평균단가3': 매수평균단가3,

                '매도거래대금4': 매도거래대금4,
                '매수거래대금4': 매수거래대금4,
                '매도평균단가4': 매도평균단가4,
                '매수평균단가4': 매수평균단가4,

                '매도거래대금5': 매도거래대금5,
                '매수거래대금5': 매수거래대금5,
                '매도평균단가5': 매도평균단가5,
                '매수평균단가5': 매수평균단가5,


                '외국계증권사매도거래대금': 외국계증권사매도거래대금,
                '외국계증권사매수거래대금': 외국계증권사매수거래대금,
                '외국계증권사매도평균단가': 외국계증권사매도평균단가,
                '외국계증권사매수평균단가': 외국계증권사매수평균단가,
            }
    
            # Send data
            self.send_data(szTrCode, 단축코드, data)

        elif szTrCode == "H1_": # KOSPI 호가잔량
            try:
                클라이언트시간 = get_current_time_formatted()
                호가시간 = self.GetFieldData("OutBlock", "hotime")
                매도호가1 = self.GetFieldData("OutBlock", "offerho1")
                매수호가1 = self.GetFieldData("OutBlock", "bidho1")
                매도호가잔량1 = self.GetFieldData("OutBlock", "offerrem1")
                매수호가잔량1 = self.GetFieldData("OutBlock", "bidrem1")
                매도호가2 = self.GetFieldData("OutBlock", "offerho2")
                매수호가2 = self.GetFieldData("OutBlock", "bidho2")
                매도호가잔량2 = self.GetFieldData("OutBlock", "offerrem2")
                매수호가잔량2 = self.GetFieldData("OutBlock", "bidrem2")
                매도호가3 = self.GetFieldData("OutBlock", "offerho3")
                매수호가3 = self.GetFieldData("OutBlock", "bidho3")
                매도호가잔량3 = self.GetFieldData("OutBlock", "offerrem3")
                매수호가잔량3 = self.GetFieldData("OutBlock", "bidrem3")
                매도호가4 = self.GetFieldData("OutBlock", "offerho4")
                매수호가4 = self.GetFieldData("OutBlock", "bidho4")
                매도호가잔량4 = self.GetFieldData("OutBlock", "offerrem4")
                매수호가잔량4 = self.GetFieldData("OutBlock", "bidrem4")
                매도호가5 = self.GetFieldData("OutBlock", "offerho5")
                매수호가5 = self.GetFieldData("OutBlock", "bidho5")
                매도호가잔량5 = self.GetFieldData("OutBlock", "offerrem5")
                매수호가잔량5 = self.GetFieldData("OutBlock", "bidrem5")
                매도호가6 = self.GetFieldData("OutBlock", "offerho6")
                매수호가6 = self.GetFieldData("OutBlock", "bidho6")
                매도호가잔량6 = self.GetFieldData("OutBlock", "offerrem6")
                매수호가잔량6 = self.GetFieldData("OutBlock", "bidrem6")
                매도호가7 = self.GetFieldData("OutBlock", "offerho7")
                매수호가7 = self.GetFieldData("OutBlock", "bidho7")
                매도호가잔량7 = self.GetFieldData("OutBlock", "offerrem7")
                매수호가잔량7 = self.GetFieldData("OutBlock", "bidrem7")
                매도호가8 = self.GetFieldData("OutBlock", "offerho8")
                매수호가8 = self.GetFieldData("OutBlock", "bidho8")
                매도호가잔량8 = self.GetFieldData("OutBlock", "offerrem8")
                매수호가잔량8 = self.GetFieldData("OutBlock", "bidrem8")
                매도호가9 = self.GetFieldData("OutBlock", "offerho9")
                매수호가9 = self.GetFieldData("OutBlock", "bidho9")
                매도호가잔량9 = self.GetFieldData("OutBlock", "offerrem9")
                매수호가잔량9 = self.GetFieldData("OutBlock", "bidrem9")
                매도호가10 = self.GetFieldData("OutBlock", "offerho10")
                매수호가10 = self.GetFieldData("OutBlock", "bidho10")
                매도호가잔량10 = self.GetFieldData("OutBlock", "offerrem10")
                매수호가잔량10 = self.GetFieldData("OutBlock", "bidrem10")
                총매도호가잔량 = self.GetFieldData("OutBlock", "totofferrem")
                총매수호가잔량 = self.GetFieldData("OutBlock", "totbidrem")
                동시호가구분 = self.GetFieldData("OutBlock", "donsigubun")
                단축코드 = self.GetFieldData("OutBlock", "shcode")
                배분적용구분 = self.GetFieldData("OutBlock", "alloc_gubun")
                누적거래량 = self.GetFieldData("OutBlock", "volume")

                data = {
                    '클라이언트시간': 클라이언트시간,
                    '호가시간': 호가시간,
                    '매도호가1': int(매도호가1),
                    '매수호가1': int(매수호가1),
                    '매도호가잔량1': int(매도호가잔량1),
                    '매수호가잔량1': int(매수호가잔량1),
                    '매도호가2': int(매도호가2),
                    '매수호가2': int(매수호가2),
                    '매도호가잔량2': int(매도호가잔량2),
                    '매수호가잔량2': int(매수호가잔량2),
                    '매도호가3': int(매도호가3),
                    '매수호가3': int(매수호가3),
                    '매도호가잔량3': int(매도호가잔량3),
                    '매수호가잔량3': int(매수호가잔량3),
                    '매도호가4': int(매도호가4),
                    '매수호가4': int(매수호가4),
                    '매도호가잔량4': int(매도호가잔량4),
                    '매수호가잔량4': int(매수호가잔량4),
                    '매도호가5': int(매도호가5),
                    '매수호가5': int(매수호가5),
                    '매도호가잔량5': int(매도호가잔량5),
                    '매수호가잔량5': int(매수호가잔량5),
                    '매도호가6': int(매도호가6),
                    '매수호가6': int(매수호가6),
                    '매도호가잔량6': int(매도호가잔량6),
                    '매수호가잔량6': int(매수호가잔량6),
                    '매도호가7': int(매도호가7),
                    '매수호가7': int(매수호가7),
                    '매도호가잔량7': int(매도호가잔량7),
                    '매수호가잔량7': int(매수호가잔량7),
                    '매도호가8': int(매도호가8),
                    '매수호가8': int(매수호가8),
                    '매도호가잔량8': int(매도호가잔량8),
                    '매수호가잔량8': int(매수호가잔량8),
                    '매도호가9': int(매도호가9),
                    '매수호가9': int(매수호가9),
                    '매도호가잔량9': int(매도호가잔량9),
                    '매수호가잔량9': int(매수호가잔량9),
                    '매도호가10': int(매도호가10),
                    '매수호가10': int(매수호가10),
                    '매도호가잔량10': int(매도호가잔량10),
                    '매수호가잔량10': int(매수호가잔량10),
                    '총매도호가잔량': int(총매도호가잔량),
                    '총매수호가잔량': int(총매수호가잔량),
                    '동시호가구분': 동시호가구분,
                    '단축코드': 단축코드,
                    '배분적용구분': 배분적용구분,
                    '누적거래량': 누적거래량
                }

                # self.send_data(szTrCode, 단축코드, data)
                save_time = time.time()
                # 0.n초마다 저장 코드
                if 단축코드 not in self.hoga_collected_check:
                    self.hoga_collected_check[단축코드] = 0 
                    self.send_data(szTrCode, 단축코드, data)

                # 0.n초 이상 지났으면 저장
                elif self.hoga_collected_check[단축코드] + 0.01 < save_time:
                    self.hoga_collected_check[단축코드] = save_time
                    self.send_data(szTrCode, 단축코드, data)
                # 0.n초 이상 지나지 않았으면 저장하지 않고 스킵
                else:
                    pass

            except Exception as e:
                print(f"Error in H1_ (KOSPI 호가잔량): {str(e)}")

        elif szTrCode == "HA_": # KOSDAQ 호가잔량
            try:
                클라이언트시간 = get_current_time_formatted()
                호가시간 = self.GetFieldData("OutBlock", "hotime")
                매도호가1 = self.GetFieldData("OutBlock", "offerho1")
                매수호가1 = self.GetFieldData("OutBlock", "bidho1")
                매도호가잔량1 = self.GetFieldData("OutBlock", "offerrem1")
                매수호가잔량1 = self.GetFieldData("OutBlock", "bidrem1")
                매도호가2 = self.GetFieldData("OutBlock", "offerho2")
                매수호가2 = self.GetFieldData("OutBlock", "bidho2")
                매도호가잔량2 = self.GetFieldData("OutBlock", "offerrem2")
                매수호가잔량2 = self.GetFieldData("OutBlock", "bidrem2")
                매도호가3 = self.GetFieldData("OutBlock", "offerho3")
                매수호가3 = self.GetFieldData("OutBlock", "bidho3")
                매도호가잔량3 = self.GetFieldData("OutBlock", "offerrem3")
                매수호가잔량3 = self.GetFieldData("OutBlock", "bidrem3")
                매도호가4 = self.GetFieldData("OutBlock", "offerho4")
                매수호가4 = self.GetFieldData("OutBlock", "bidho4")
                매도호가잔량4 = self.GetFieldData("OutBlock", "offerrem4")
                매수호가잔량4 = self.GetFieldData("OutBlock", "bidrem4")
                매도호가5 = self.GetFieldData("OutBlock", "offerho5")
                매수호가5 = self.GetFieldData("OutBlock", "bidho5")
                매도호가잔량5 = self.GetFieldData("OutBlock", "offerrem5")
                매수호가잔량5 = self.GetFieldData("OutBlock", "bidrem5")
                매도호가6 = self.GetFieldData("OutBlock", "offerho6")
                매수호가6 = self.GetFieldData("OutBlock", "bidho6")
                매도호가잔량6 = self.GetFieldData("OutBlock", "offerrem6")
                매수호가잔량6 = self.GetFieldData("OutBlock", "bidrem6")
                매도호가7 = self.GetFieldData("OutBlock", "offerho7")
                매수호가7 = self.GetFieldData("OutBlock", "bidho7")
                매도호가잔량7 = self.GetFieldData("OutBlock", "offerrem7")
                매수호가잔량7 = self.GetFieldData("OutBlock", "bidrem7")
                매도호가8 = self.GetFieldData("OutBlock", "offerho8")
                매수호가8 = self.GetFieldData("OutBlock", "bidho8")
                매도호가잔량8 = self.GetFieldData("OutBlock", "offerrem8")
                매수호가잔량8 = self.GetFieldData("OutBlock", "bidrem8")
                매도호가9 = self.GetFieldData("OutBlock", "offerho9")
                매수호가9 = self.GetFieldData("OutBlock", "bidho9")
                매도호가잔량9 = self.GetFieldData("OutBlock", "offerrem9")
                매수호가잔량9 = self.GetFieldData("OutBlock", "bidrem9")
                매도호가10 = self.GetFieldData("OutBlock", "offerho10")
                매수호가10 = self.GetFieldData("OutBlock", "bidho10")
                매도호가잔량10 = self.GetFieldData("OutBlock", "offerrem10")
                매수호가잔량10 = self.GetFieldData("OutBlock", "bidrem10")
                총매도호가잔량 = self.GetFieldData("OutBlock", "totofferrem")
                총매수호가잔량 = self.GetFieldData("OutBlock", "totbidrem")
                동시호가구분 = self.GetFieldData("OutBlock", "donsigubun")
                단축코드 = self.GetFieldData("OutBlock", "shcode")
                배분적용구분 = self.GetFieldData("OutBlock", "alloc_gubun")
                누적거래량 = self.GetFieldData("OutBlock", "volume")

                data = {
                    '클라이언트시간': 클라이언트시간,
                    '호가시간': 호가시간,
                    '매도호가1': int(매도호가1),
                    '매수호가1': int(매수호가1),
                    '매도호가잔량1': int(매도호가잔량1),
                    '매수호가잔량1': int(매수호가잔량1),
                    '매도호가2': int(매도호가2),
                    '매수호가2': int(매수호가2),
                    '매도호가잔량2': int(매도호가잔량2),
                    '매수호가잔량2': int(매수호가잔량2),
                    '매도호가3': int(매도호가3),
                    '매수호가3': int(매수호가3),
                    '매도호가잔량3': int(매도호가잔량3),
                    '매수호가잔량3': int(매수호가잔량3),
                    '매도호가4': int(매도호가4),
                    '매수호가4': int(매수호가4),
                    '매도호가잔량4': int(매도호가잔량4),
                    '매수호가잔량4': int(매수호가잔량4),
                    '매도호가5': int(매도호가5),
                    '매수호가5': int(매수호가5),
                    '매도호가잔량5': int(매도호가잔량5),
                    '매수호가잔량5': int(매수호가잔량5),
                    '매도호가6': int(매도호가6),
                    '매수호가6': int(매수호가6),
                    '매도호가잔량6': int(매도호가잔량6),
                    '매수호가잔량6': int(매수호가잔량6),
                    '매도호가7': int(매도호가7),
                    '매수호가7': int(매수호가7),
                    '매도호가잔량7': int(매도호가잔량7),
                    '매수호가잔량7': int(매수호가잔량7),
                    '매도호가8': int(매도호가8),
                    '매수호가8': int(매수호가8),
                    '매도호가잔량8': int(매도호가잔량8),
                    '매수호가잔량8': int(매수호가잔량8),
                    '매도호가9': int(매도호가9),
                    '매수호가9': int(매수호가9),
                    '매도호가잔량9': int(매도호가잔량9),
                    '매수호가잔량9': int(매수호가잔량9),
                    '매도호가10': int(매도호가10),
                    '매수호가10': int(매수호가10),
                    '매도호가잔량10': int(매도호가잔량10),
                    '매수호가잔량10': int(매수호가잔량10),
                    '총매도호가잔량': int(총매도호가잔량),
                    '총매수호가잔량': int(총매수호가잔량),
                    '동시호가구분': 동시호가구분,
                    '단축코드': 단축코드,
                    '배분적용구분': 배분적용구분,
                    '누적거래량': 누적거래량
                }

                # self.send_data(szTrCode, 단축코드, data)
                save_time = time.time()
                # 0.n초마다 저장 코드
                if 단축코드 not in self.hoga_collected_check:
                    self.hoga_collected_check[단축코드] = 0 
                    self.send_data(szTrCode, 단축코드, data)

                # 0.n초 이상 지났으면 저장
                elif self.hoga_collected_check[단축코드] + 0.05 < save_time:
                    self.hoga_collected_check[단축코드] = save_time
                    self.send_data(szTrCode, 단축코드, data)
                else:
                    pass

                
            except Exception as e:
                print(f"Error in HA_ (KOSDAQ 호가잔량): {str(e)}")

        elif szTrCode == "S3_": # KOSPI 체결
            try:
                클라이언트시간 = get_current_time_formatted()
                체결시각 = self.GetFieldData("OutBlock", "chetime")
                전일대비구분 = self.GetFieldData("OutBlock", "sign")
                전일대비 = self.GetFieldData("OutBlock", "change")
                등락율 = self.GetFieldData("OutBlock", "drate")
                현재가 = self.GetFieldData("OutBlock", "price")
                시가시간 = self.GetFieldData("OutBlock", "opentime")
                시가 = self.GetFieldData("OutBlock", "open")
                고가시간 = self.GetFieldData("OutBlock", "hightime")
                고가 = self.GetFieldData("OutBlock", "high")
                저가시간 = self.GetFieldData("OutBlock", "lowtime")
                저가 = self.GetFieldData("OutBlock", "low")
                체결구분 = self.GetFieldData("OutBlock", "cgubun")
                체결량 = self.GetFieldData("OutBlock", "cvolume")
                누적거래량 = self.GetFieldData("OutBlock", "volume")
                누적거래대금 = self.GetFieldData("OutBlock", "value")
                매도누적체결량 = self.GetFieldData("OutBlock", "mdvolume")
                매도누적체결건수 = self.GetFieldData("OutBlock", "mdchecnt")
                매수누적체결량 = self.GetFieldData("OutBlock", "msvolume")
                매수누적체결건수 = self.GetFieldData("OutBlock", "mschecnt")
                체결강도 = self.GetFieldData("OutBlock", "cpower")
                가중평균가 = self.GetFieldData("OutBlock", "w_avrg")
                매도호가 = self.GetFieldData("OutBlock", "offerho")
                매수호가 = self.GetFieldData("OutBlock", "bidho")
                장정보 = self.GetFieldData("OutBlock", "status")
                전일동시간대거래량 = self.GetFieldData("OutBlock", "jnilvolume")
                단축코드 = self.GetFieldData("OutBlock", "shcode")

                현재가 = int(현재가)
                if 체결구분 == "-":
                    체결량 = int(체결량) * -1
                elif 체결구분 == "+":
                    체결량 = int(체결량)
                else:
                    # 동시호가 데이터 제외
                    return
                data = {
                    '체결시간': 클라이언트시간,
                    '체결시각': 체결시각,
                    '전일대비구분': 전일대비구분,
                    '전일대비': 전일대비,
                    '전일대비체결가': 등락율,
                    '체결가': int(현재가),
                    '시가시간': 시가시간,
                    '시가': int(시가),
                    '고가시간': 고가시간,
                    '고가': int(고가),
                    '저가시간': 저가시간,
                    '저가': int(저가),
                    '체결구분': 체결구분,
                    '체결량': 체결량,
                    '누적거래량': 누적거래량,
                    '누적거래대금': 누적거래대금,
                    '매도누적체결량': 매도누적체결량,
                    '매도누적체결건수': 매도누적체결건수,
                    '매수누적체결량': 매수누적체결량,
                    '매수누적체결건수': 매수누적체결건수,
                    '체결강도': 체결강도,
                    '가중평균가': 가중평균가,
                    '매도호가': 매도호가,
                    '매수호가': 매수호가,
                    '장정보': 장정보,
                    '전일동시간대거래량': 전일동시간대거래량,
                    '단축코드': 단축코드,
                    '체결대금': 현재가*체결량
                }

            # Example function call to send the data
                self.send_data(szTrCode, 단축코드, data)
                # if 단축코드 == "005930" and int(체결량) > 100:
                #     print(f"삼성전자. 체결량: {체결량}. 클라:{클라이언트시간}. 서버:{체결시각}")
            except Exception as e:
                print(f"Error in S3_ (KOSPI 체결): {str(e)}")
        
        elif szTrCode == "K3_": # KOSDAQ 체결
            try:
                클라이언트시간 = get_current_time_formatted()
                체결시각 = self.GetFieldData("OutBlock", "chetime")
                전일대비구분 = self.GetFieldData("OutBlock", "sign")
                전일대비 = self.GetFieldData("OutBlock", "change")
                등락율 = self.GetFieldData("OutBlock", "drate")
                현재가 = self.GetFieldData("OutBlock", "price")
                시가시간 = self.GetFieldData("OutBlock", "opentime")
                시가 = self.GetFieldData("OutBlock", "open")
                고가시간 = self.GetFieldData("OutBlock", "hightime")
                고가 = self.GetFieldData("OutBlock", "high")
                저가시간 = self.GetFieldData("OutBlock", "lowtime")
                저가 = self.GetFieldData("OutBlock", "low")
                체결구분 = self.GetFieldData("OutBlock", "cgubun")
                체결량 = self.GetFieldData("OutBlock", "cvolume")
                누적거래량 = self.GetFieldData("OutBlock", "volume")
                누적거래대금 = self.GetFieldData("OutBlock", "value")
                매도누적체결량 = self.GetFieldData("OutBlock", "mdvolume")
                매도누적체결건수 = self.GetFieldData("OutBlock", "mdchecnt")
                매수누적체결량 = self.GetFieldData("OutBlock", "msvolume")
                매수누적체결건수 = self.GetFieldData("OutBlock", "mschecnt")
                체결강도 = self.GetFieldData("OutBlock", "cpower")
                가중평균가 = self.GetFieldData("OutBlock", "w_avrg")
                매도호가 = self.GetFieldData("OutBlock", "offerho")
                매수호가 = self.GetFieldData("OutBlock", "bidho")
                장정보 = self.GetFieldData("OutBlock", "status")
                전일동시간대거래량 = self.GetFieldData("OutBlock", "jnilvolume")
                단축코드 = self.GetFieldData("OutBlock", "shcode")

                현재가 = int(현재가)
                if 체결구분 == "-":
                    체결량 = int(체결량) * -1
                elif 체결구분 == "+":
                    체결량 = int(체결량)
                else:
                    # 동시호가 데이터 제외
                    return
                
                data = {
                    '체결시간': 클라이언트시간,
                    '체결시각': 체결시각,
                    '전일대비구분': 전일대비구분,
                    '전일대비': 전일대비,
                    '전일대비체결가': 등락율,
                    '체결가': int(현재가),
                    '시가시간': 시가시간,
                    '시가': int(시가),
                    '고가시간': 고가시간,
                    '고가': int(고가),
                    '저가시간': 저가시간,
                    '저가': int(저가),
                    '체결구분': 체결구분,
                    '체결량': 체결량,
                    '누적거래량': 누적거래량,
                    '누적거래대금': 누적거래대금,
                    '매도누적체결량': 매도누적체결량,
                    '매도누적체결건수': 매도누적체결건수,
                    '매수누적체결량': 매수누적체결량,
                    '매수누적체결건수': 매수누적체결건수,
                    '체결강도': 체결강도,
                    '가중평균가': 가중평균가,
                    '매도호가': 매도호가,
                    '매수호가': 매수호가,
                    '장정보': 장정보,
                    '전일동시간대거래량': 전일동시간대거래량,
                    '단축코드': 단축코드,
                    '체결대금': 현재가*체결량
                }

            # Example function call to send the data
                self.send_data(szTrCode, 단축코드, data)
                # if 단축코드 == "005930" and int(체결량) > 100:
                #     print(f"삼성전자. 체결량: {체결량}. 클라:{클라이언트시간}. 서버:{체결시각}")
            
            except Exception as e:
                print(f"Error in K3_ (KOSDAQ 체결): {str(e)}")
                
        elif szTrCode == "PH_": # KOSPI 프로그램매매종목별
            try:
                클라이언트시간 = get_current_time_formatted()
                수신시간 = self.GetFieldData("OutBlock", "time")
                현재가 = self.GetFieldData("OutBlock", "price")
                전일대비구분 = self.GetFieldData("OutBlock", "sign")
                전일대비 = self.GetFieldData("OutBlock", "change")
                누적거래량 = self.GetFieldData("OutBlock", "volume")
                등락율 = self.GetFieldData("OutBlock", "drate")
                차익매도호가잔량 = self.GetFieldData("OutBlock", "cdhrem")
                차익매수호가잔량 = self.GetFieldData("OutBlock", "cshrem")
                비차익매도호가잔량 = self.GetFieldData("OutBlock", "bdhrem")
                비차익매수호가잔량 = self.GetFieldData("OutBlock", "bshrem")
                차익매도호가수량 = self.GetFieldData("OutBlock", "cdhvolume")
                차익매수호가수량 = self.GetFieldData("OutBlock", "cshvolume")
                비차익매도호가수량 = self.GetFieldData("OutBlock", "bdhvolume")
                비차익매수호가수량 = self.GetFieldData("OutBlock", "bshvolume")
                전체매도위탁체결수량 = self.GetFieldData("OutBlock", "dwcvolume")
                전체매수위탁체결수량 = self.GetFieldData("OutBlock", "swcvolume")
                전체매도자기체결수량 = self.GetFieldData("OutBlock", "djcvolume")
                전체매수자기체결수량 = self.GetFieldData("OutBlock", "sjcvolume")
                전체매도체결수량 = self.GetFieldData("OutBlock", "tdvolume")
                전체매수체결수량 = self.GetFieldData("OutBlock", "tsvolume")
                전체순매수수량 = self.GetFieldData("OutBlock", "tvol")
                전체매도위탁체결금액 = self.GetFieldData("OutBlock", "dwcvalue")
                전체매수위탁체결금액 = self.GetFieldData("OutBlock", "swcvalue")
                전체매도자기체결금액 = self.GetFieldData("OutBlock", "djcvalue")
                전체매수자기체결금액 = self.GetFieldData("OutBlock", "sjcvalue")
                전체매도체결금액 = self.GetFieldData("OutBlock", "tdvalue")
                전체매수체결금액 = self.GetFieldData("OutBlock", "tsvalue")
                전체순매수금액 = self.GetFieldData("OutBlock", "tval")
                매도사전공시수량 = self.GetFieldData("OutBlock", "pdgvolume")
                매수사전공시수량 = self.GetFieldData("OutBlock", "psgvolume")
                종목코드 = self.GetFieldData("OutBlock", "shcode")


                data = {
                    '클라이언트시간': 클라이언트시간,
                    '수신시간': 수신시간,
                    '현재가': 현재가,
                    '전일대비구분': 전일대비구분,
                    '전일대비': 전일대비,
                    '누적거래량': 누적거래량,
                    '등락율': 등락율,
                    '차익매도호가잔량': 차익매도호가잔량,
                    '차익매수호가잔량': 차익매수호가잔량,
                    '비차익매도호가잔량': 비차익매도호가잔량,
                    '비차익매수호가잔량': 비차익매수호가잔량,
                    '차익매도호가수량': 차익매도호가수량,
                    '차익매수호가수량': 차익매수호가수량,
                    '비차익매도호가수량': 비차익매도호가수량,
                    '비차익매수호가수량': 비차익매수호가수량,
                    '전체매도위탁체결수량': 전체매도위탁체결수량,
                    '전체매수위탁체결수량': 전체매수위탁체결수량,
                    '전체매도자기체결수량': 전체매도자기체결수량,
                    '전체매수자기체결수량': 전체매수자기체결수량,
                    '전체매도체결수량': 전체매도체결수량,
                    '전체매수체결수량': 전체매수체결수량,
                    '전체순매수수량': 전체순매수수량,
                    '전체매도위탁체결금액': 전체매도위탁체결금액,
                    '전체매수위탁체결금액': 전체매수위탁체결금액,
                    '전체매도자기체결금액': 전체매도자기체결금액,
                    '전체매수자기체결금액': 전체매수자기체결금액,
                    '전체매도체결금액': 전체매도체결금액,
                    '전체매수체결금액': 전체매수체결금액,
                    '전체순매수금액': 전체순매수금액,
                    '매도사전공시수량': 매도사전공시수량,
                    '매수사전공시수량': 매수사전공시수량,
                    '종목코드': 종목코드
                }
                

                # Example function call to send the data
                self.send_data(szTrCode, 종목코드, data)
            except Exception as e:
                print(f"Error in PH_ (KOSPI 프로그램매매종목별): {str(e)}")

        elif szTrCode == "KH_": # KOSDAQ 프로그램매매종목별
            try:
                클라이언트시간 = get_current_time_formatted()
                수신시간 = self.GetFieldData("OutBlock", "time")
                현재가 = self.GetFieldData("OutBlock", "price")
                전일대비구분 = self.GetFieldData("OutBlock", "sign")
                전일대비 = self.GetFieldData("OutBlock", "change")
                누적거래량 = self.GetFieldData("OutBlock", "volume")
                등락율 = self.GetFieldData("OutBlock", "drate")
                차익매도호가잔량 = self.GetFieldData("OutBlock", "cdhrem")
                차익매수호가잔량 = self.GetFieldData("OutBlock", "cshrem")
                비차익매도호가잔량 = self.GetFieldData("OutBlock", "bdhrem")
                비차익매수호가잔량 = self.GetFieldData("OutBlock", "bshrem")
                차익매도호가수량 = self.GetFieldData("OutBlock", "cdhvolume")
                차익매수호가수량 = self.GetFieldData("OutBlock", "cshvolume")
                비차익매도호가수량 = self.GetFieldData("OutBlock", "bdhvolume")
                비차익매수호가수량 = self.GetFieldData("OutBlock", "bshvolume")
                전체매도위탁체결수량 = self.GetFieldData("OutBlock", "dwcvolume")
                전체매수위탁체결수량 = self.GetFieldData("OutBlock", "swcvolume")
                전체매도자기체결수량 = self.GetFieldData("OutBlock", "djcvolume")
                전체매수자기체결수량 = self.GetFieldData("OutBlock", "sjcvolume")
                전체매도체결수량 = self.GetFieldData("OutBlock", "tdvolume")
                전체매수체결수량 = self.GetFieldData("OutBlock", "tsvolume")
                전체순매수수량 = self.GetFieldData("OutBlock", "tvol")
                전체매도위탁체결금액 = self.GetFieldData("OutBlock", "dwcvalue")
                전체매수위탁체결금액 = self.GetFieldData("OutBlock", "swcvalue")
                전체매도자기체결금액 = self.GetFieldData("OutBlock", "djcvalue")
                전체매수자기체결금액 = self.GetFieldData("OutBlock", "sjcvalue")
                전체매도체결금액 = self.GetFieldData("OutBlock", "tdvalue")
                전체매수체결금액 = self.GetFieldData("OutBlock", "tsvalue")
                전체순매수금액 = self.GetFieldData("OutBlock", "tval")
                매도사전공시수량 = self.GetFieldData("OutBlock", "pdgvolume")
                매수사전공시수량 = self.GetFieldData("OutBlock", "psgvolume")
                종목코드 = self.GetFieldData("OutBlock", "shcode")


                data = {
                    '클라이언트시간': 클라이언트시간,
                    '수신시간': 수신시간,
                    '현재가': 현재가,
                    '전일대비구분': 전일대비구분,
                    '전일대비': 전일대비,
                    '누적거래량': 누적거래량,
                    '등락율': 등락율,
                    '차익매도호가잔량': 차익매도호가잔량,
                    '차익매수호가잔량': 차익매수호가잔량,
                    '비차익매도호가잔량': 비차익매도호가잔량,
                    '비차익매수호가잔량': 비차익매수호가잔량,
                    '차익매도호가수량': 차익매도호가수량,
                    '차익매수호가수량': 차익매수호가수량,
                    '비차익매도호가수량': 비차익매도호가수량,
                    '비차익매수호가수량': 비차익매수호가수량,
                    '전체매도위탁체결수량': 전체매도위탁체결수량,
                    '전체매수위탁체결수량': 전체매수위탁체결수량,
                    '전체매도자기체결수량': 전체매도자기체결수량,
                    '전체매수자기체결수량': 전체매수자기체결수량,
                    '전체매도체결수량': 전체매도체결수량,
                    '전체매수체결수량': 전체매수체결수량,
                    '전체순매수수량': 전체순매수수량,
                    '전체매도위탁체결금액': 전체매도위탁체결금액,
                    '전체매수위탁체결금액': 전체매수위탁체결금액,
                    '전체매도자기체결금액': 전체매도자기체결금액,
                    '전체매수자기체결금액': 전체매수자기체결금액,
                    '전체매도체결금액': 전체매도체결금액,
                    '전체매수체결금액': 전체매수체결금액,
                    '전체순매수금액': 전체순매수금액,
                    '매도사전공시수량': 매도사전공시수량,
                    '매수사전공시수량': 매수사전공시수량,
                    '종목코드': 종목코드
                }

                # Example function call to send the data
                self.send_data(szTrCode, 종목코드, data)
            except Exception as e:
                print(f"Error in KH_ (KOSDAQ 프로그램매매종목별): {str(e)}")

        elif szTrCode == "VI_": # 주식VI발동해제
            try:
                클라이언트시간 = get_current_time_formatted()
                구분 = self.GetFieldData("OutBlock", "vi_gubun")
                정적VI발동기준가격 = self.GetFieldData("OutBlock", "svi_recprice")
                동적VI발동기준가격 = self.GetFieldData("OutBlock", "dvi_recprice")
                VI발동가격 = self.GetFieldData("OutBlock", "vi_trgprice")
                단축코드 = self.GetFieldData("OutBlock", "shcode")
                참조코드 = self.GetFieldData("OutBlock", "ref_shcode")
                시간 = self.GetFieldData("OutBlock", "time")

                data = {
                    '클라이언트시간':클라이언트시간,
                    '시간':시간,
                    '구분':구분,
                    '정적VI발동기준가격':정적VI발동기준가격,
                    '동적VI발동기준가격':동적VI발동기준가격,
                    'VI발동가격':VI발동가격,
                    '단축코드':단축코드,
                    '참조코드':참조코드,
                }
                self.send_data(szTrCode, 단축코드, data)
            except Exception as e:
                print(f"Error in VI_ (주식VI발동해제): {str(e)}")
        
        elif szTrCode == "SC1": # 나의 체결 데이터
            클라이언트시간 = get_current_time_formatted()
            평균매입가 = self.GetFieldData("OutBlock", "avrpchsprc") 
            체결시각 = self.GetFieldData("OutBlock", "exectime") 
            체결가격 = self.GetFieldData("OutBlock", "execprc") 
            체결번호 = self.GetFieldData("OutBlock", "execno") 
            주문번호 = self.GetFieldData("OutBlock", "ordno")
            계좌번호 = self.GetFieldData("OutBlock", "accno1") 
            단축코드 = self.GetFieldData("OutBlock", "shtnIsuno")[1:]
            체결수량 = int(self.GetFieldData("OutBlock", "execqty"))
            주문종류구분 = self.GetFieldData("OutBlock", "trcode") # SONAT000:신규주문 SONAT001:정정주문 SONAT002:취소주문 SONAS100:체결확인
            매수매도구분 = self.GetFieldData("OutBlock", "bnstp")    #1:매도 2:매수
            data = {
                    '클라이언트시간': 클라이언트시간,
                    '평균매입가': 평균매입가,
                    '체결시각': 체결시각,
                    '체결가격': 체결가격,
                    '체결번호': 체결번호,
                    '주문번호': 주문번호,
                    '계좌번호': 계좌번호,
                    '단축코드': 단축코드,
                    '체결수량': 체결수량,
                    '주문종류구분': 주문종류구분,
                    '매수매도구분': 매수매도구분,
                }
            print(f"SC1 수신! \n{data}")
            
            if 단축코드 in self.codes0:
                print("socket 0")
                self.send_data_to_socket(szTrCode, 단축코드, data, 0)
            elif 단축코드 in self.codes1:
                print("socket 1")
                self.send_data_to_socket(szTrCode, 단축코드, data, 1)
            elif 단축코드 in self.codes2:
                print("socket 2")
                self.send_data_to_socket(szTrCode, 단축코드, data, 2)
            elif 단축코드 in self.codes3:
                print("socket 3")
                self.send_data_to_socket(szTrCode, 단축코드, data, 3)
            elif 단축코드 in self.codes4:
                print("socket 4")
                self.send_data_to_socket(szTrCode, 단축코드, data, 4)


    def send_data(self, real_type, code, data):
        message = {
            "type": real_type,
            "code": code,
            "data": data
        }
        json_data =json.dumps(message)
        self.socket.send_json(json_data)

    def send_data_to_socket(self, real_type, code, data, socket_num):
        message = {
            "type": real_type,
            "code": code,
            "data": data
        }
        json_data =json.dumps(message)
        if socket_num == 0:
            self.socket0.send_json(json_data)
        if socket_num == 1:
            self.socket1.send_json(json_data)
        if socket_num == 2:
            self.socket2.send_json(json_data)
        if socket_num == 3:
            self.socket3.send_json(json_data)
        if socket_num == 4:
            self.socket4.send_json(json_data)




class XAQueryEventHandler_T1102:
    query_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData. code: ", code)
        XAQueryEventHandler_T1102.query_state = 1


class XAQueryEventHandler_G3101:
    query_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData. code: ", code)
        XAQueryEventHandler_G3101.query_state = 1


class EventsContainer:
    events_list = []


class StockDataManager:
    def __init__(self):
        self.instances: Dict[str, win32com.client.CDispatch] = {}

    def create_instances(self, rq_id, stock_symbols: List[str], XAReal_class, port: int = 6667):
        # XAReal_class에 port 정보를 전달하기 위해 클래스 속성 설정
        XAReal_class.port = port
        
        for symbol in stock_symbols:
            instance_name = f"inst{rq_id}_Event_{symbol}"
            self.instances[instance_name] = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XAReal_class)


class StockDataManager_rq_symbol_combine:
    '''
    하나의 port에서 모든 데이터를 다루기 위해
    '''
    def __init__(self):
        self.instances: Dict[str, win32com.client.CDispatch] = {}


    def create_instance(self, rq_id, XAReal_class, port: int = 6667, zmq_context=None):
        XAReal_class.port = port
        XAReal_class.context = zmq_context
        instance_name = f"inst{rq_id}_Event"
        self.instances[instance_name] = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XAReal_class)

    def create_instances(self, rq_ids, stock_symbols: List[str], XAReal_class, port: int = 6667, zmq_context=None):
        # XAReal_class에 port 정보를 전달하기 위해 클래스 속성 설정
        XAReal_class.port = port
        XAReal_class.context = zmq_context
        
        for rq_id, symbol in zip(rq_ids, stock_symbols):
            instance_name = f"inst{rq_id}_Event_{symbol}"
            self.instances[instance_name] = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XAReal_class)
