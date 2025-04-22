import requests
import json
from datetime import datetime, timedelta
import os
from tqdm import tqdm
import time
from LS_config import USER_ID, APP_KEY, APP_SECRET_KEY, REST_URL, WEBSOCKET_URL




REST_URL = "https://openapi.ls-sec.co.kr:8080"
WEBSOCKET_URL = "wss://openapi.ls-sec.co.kr:9443/websocket" 


def LS_get_access_token(APP_KEY, APP_SECRET_KEY):
    # 토큰 발급에 필요한 정보
    url = "https://openapi.ls-sec.co.kr:8080/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecretkey": APP_SECRET_KEY,
        "scope": "oob"
    }

    # 토큰 발급 요청
    response = requests.post(url, headers=headers, data=data)

    # 응답 확인
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        expires_in = token_data["expires_in"]
        print("Access Token:", access_token)
        print("Expires In:", expires_in)
    else:
        print("토큰 발급 실패")
        print("상태 코드:", response.status_code)
        print("응답 내용:", response.text)
    return token_data['access_token']


ACCESS_TOKEN = LS_get_access_token(APP_KEY, APP_SECRET_KEY)



def get_condition_list(user_id, access_token, gb="0", group_name="", cont="", cont_key=""):
    url = f"{REST_URL}/stock/item-search"
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "authorization": f"Bearer {access_token}",
        "tr_cd": "t1866",
        "tr_cont": "N",
        "tr_cont_key": "",
        "mac_address": ""  # 예시 MAC 주소, 실제 사용 시 변경 필요
    }
    data = {
        "t1866InBlock": {
            "user_id": user_id,
            "gb": gb,
            "group_name": group_name,
            "cont": cont,
            "cont_key": cont_key
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def perform_condition_search(query_index, access_token):
    url = f"{REST_URL}/stock/item-search"
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "authorization": f"Bearer {access_token}",
        "tr_cd": "t1859",
        "tr_cont": "N",
        "tr_cont_key": "",
        "mac_address": ""  # 예시 MAC 주소, 실제 사용 시 변경 필요
    }
    data = {
        "t1859InBlock": {
            "query_index": query_index
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()



def get_condition_list_and_sAlertNum(user_id, access_token, condition_num=0):
    '''
    1. 조건검색 조건 불러오기
    '''
    # 1. 조건검색 리스트 불러오기
    condition_list = get_condition_list(user_id, access_token)
    print("condition_list: ", condition_list)
    
    if condition_list["rsp_cd"] == "00000" and len(condition_list.get("t1866OutBlock1", [])) > 0:
        first_condition = condition_list["t1866OutBlock1"][condition_num]
        query_index = first_condition["query_index"]
        
        # 2. 첫 번째 조건에 대해 조건 검색 수행
        condition_search_result = perform_condition_search(query_index, access_token)
        print(type(condition_search_result))
        print("조건 검색 결과:")
        results = json.dumps(condition_search_result, indent=2, ensure_ascii=False)
        print(len(condition_search_result['t1859OutBlock1']))
        print("condition_search_result: ", condition_search_result)
     

        result_codes = []
        for data in condition_search_result['t1859OutBlock1']:
            result_codes.append(data['shcode'])

        return result_codes
    else:
        print("조건검색 리스트를 가져오는데 실패했거나 조건이 없습니다.")
        return None
    

    