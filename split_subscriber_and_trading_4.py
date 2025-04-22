from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys
import win32com.client
import pythoncom
from datetime import datetime

import asyncio
import mysql.connector
from datetime import datetime
from collections import deque

import win32com.client
from typing import List, Dict
import json
import time

from zmq.asyncio import Context
import zmq
import random

from datetime import datetime
from collections import defaultdict

# LS open api로 거래
# split_publisher_ls_{num}.py에서 Xing API로 데이터를 수신. 117{num} 포트로 데이터를 PUSH
# 해당 스크립트에서는 위 데이터를 PULL하여 매매판단을 내림.

# @@@@@@@@@@@@@@@@@@@ 공용 변수들 선언 시작 @@@@@@@@@@@@@@@@@@@
from LS_config import USER_ID, APP_KEY, APP_SECRET_KEY, REST_URL, WEBSOCKET_URL
from trading_mechanism import *


if __name__ == "__main__":
    port = "1174"
    with open(rf"kor_split_codes.json", "r") as f:
        data =json.load(f)
        kospi_codes = data['kospi_split_4']
        kosdaq_codes = data['kosdaq_split_4']
    codes_dict = {}
    for code in kospi_codes + kosdaq_codes:
        codes_dict[code] = True

    asyncio.run(main(port=port, codes_dict=codes_dict))