import requests
import json


def order_stock(
    isu_no, ord_qty, ord_prc, bns_tp_code="2", ordprc_ptn_code="00",
    mgn_trn_code="000", loan_dt="", ord_cndi_tp_code="1",
    access_token="YOUR_ACCESS_TOKEN", mac_address=""
):
    '''
      -IsuNo	종목번호	String	Y	12	주식/ETF : 종목코드 or A+종목코드(모의투자는 A+종목코드)
                                                    ELW : J+종목코드
                                                    ETN : Q+종목코드
        -OrdQty	주문수량	Number	Y	16	
        -OrdPrc	주문가	Number	Y	13.2	
        -BnsTpCode	매매구분	String	Y	1	1:매도, 2:매수
     -OrdprcPtnCode	호가유형코드	String	Y	2	00@지정가
                                                03@시장가
                                                05@조건부지정가
                                                06@최유리지정가
                                                07@최우선지정가
                                                61@장개시전시간외종가
                                                81@시간외종가
                                                82@시간외단일가
     -OrdCndiTpCode	주문조건구분	String	Y	1	0:없음,1:IOC,2:FOK
    '''
    url = "https://openapi.ls-sec.co.kr:8080/stock/order"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "tr_cd": "CSPAT00601",
        "tr_cont": "N",
        "tr_cont_key": "",
        "mac_address": mac_address
    }
    data = {
        "CSPAT00601InBlock1": {
            "IsuNo": isu_no,
            "OrdQty": ord_qty,
            "OrdPrc": ord_prc,
            "BnsTpCode": bns_tp_code,
            "OrdprcPtnCode": ordprc_ptn_code,
            "MgntrnCode": mgn_trn_code,
            "LoanDt": loan_dt,
            "OrdCndiTpCode": ord_cndi_tp_code
        }
    }

    try:
        print("order_stock 호출")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 응답 상태 코드가 200 이외인 경우 예외 발생

        result = response.json()
        if result["rsp_cd"] == "00000":
            print(f"result:{result}")
            print(result["rsp_msg"])
            return result
        elif result["rsp_cd"] == "02711":
            print(f"result:{result}")
            print(result["rsp_msg"])
            return result
        else:
            print(f"result:{result}")
            print(result["rsp_msg"])
            return result

    except requests.exceptions.RequestException as e:
        print("order_stock 요청 실패:", e)
        return result
    

def buy_order(access_token:str, stock_code:str, order_quan:int=1, order_price:int=0, order_type:str="03", order_condition:str="0"):
    '''
    order_type (str): 00@지정가
                03@시장가
                05@조건부지정가
                06@최유리지정가
                07@최우선지정가
                61@장개시전시간외종가
                81@시간외종가
                82@시간외단일가
    order_condition (str): [0:없음,1:IOC,2:FOK]
    '''
    try:
        result = order_stock(access_token=access_token, isu_no=stock_code, ord_qty=order_quan, ord_prc=order_price, bns_tp_code="2", ordprc_ptn_code=order_type, ord_cndi_tp_code=order_condition)
        order_num = result['CSPAT00601OutBlock2']['OrdNo']
        return order_num
    except Exception as e:
        print("buy_order 에러: ", e)
        return


def sell_order(access_token:str, stock_code:str, order_quan:int=1, order_price:int=0, order_type:str="03", order_condition:str="0"):
    '''
    order_type: 00@지정가
                03@시장가
                05@조건부지정가
                06@최유리지정가
                07@최우선지정가
                61@장개시전시간외종가
                81@시간외종가
                82@시간외단일가
    order_condition: [0:없음,1:IOC,2:FOK]
    '''
    try:
        result = order_stock(access_token=access_token, isu_no=stock_code, ord_qty=order_quan, ord_prc=order_price, bns_tp_code="1", ordprc_ptn_code=order_type, ord_cndi_tp_code=order_condition)
        return result
    except Exception as e:
        print("sell_order 에러: ", e)
        return
         

def modify_stock_order(access_token, org_order_no, stock_code, quantity, order_type, order_condition, order_price):
    """
    LS증권 API를 사용하여 주식정정주문을 요청하는 함수
    
    Parameters:
    - access_token (str): OAuth 인증 토큰
    - org_order_no (int): 원주문번호
    - stock_code (str): 종목코드 (예: 'A005930' - 삼성전자)
    - quantity (int): 주문수량
    - order_type (str): 호가유형코드 (00: 지정가, 03: 시장가 등)
    - order_condition (str): 주문조건구분 (0: 없음, 1: IOC, 2: FOK)
    - price (float): 주문가격
    
    Returns:
    - dict: API 응답 결과
    """
    # API 엔드포인트 URL
    url = "https://openapi.ls-sec.co.kr:8080/stock/order"
    
    # 요청 헤더 설정
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {access_token}",
        "tr_cd": "CSPAT00701",    # 현물정정주문 거래코드
        "tr_cont": "N",           # 연속거래 여부 (N: 연속 아님)
        "tr_cont_key": "",        # 연속거래 키 (연속거래 아니므로 빈 값)
        "mac_address": "112233445566"  # 법인인 경우 필수 (예시 값)
    }
    
    # 요청 본문 데이터 구성
    payload = {
        "CSPAT00701InBlock1": {
            "OrgOrdNo": org_order_no,      # 원주문번호
            "IsuNo": stock_code,           # 종목번호 (A+종목코드)
            "OrdQty": quantity,            # 주문수량
            "OrdprcPtnCode": order_type,   # 호가유형코드
            "OrdCndiTpCode": order_condition, # 주문조건구분
            "OrdPrc": order_price                # 주문가격
        }
    }
    
    try:
        # API 요청 전송
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # 응답 확인
        if response.status_code == 200:
            result = response.json()
            print("정정주문 result:\n", result)
            order_num, spare_order_num = result['CSPAT00701OutBlock1']['OrgOrdNo'], result['CSPAT00701OutBlock2']['SpareOrdNo']
            return spare_order_num
        else:
            return {
                "status_code": response.status_code,
                "error": f"API 요청 실패: {response.text}"
            }
    except Exception as e:
        return {
            "error": f"예외 발생: {str(e)}"
        }
    

def cancel_stock_order(access_token, org_order_no, stock_code, quantity):
    """
    LS증권 API를 사용하여 주식취소주문을 요청하는 함수
    
    Parameters:
    - access_token (str): OAuth 인증 토큰
    - org_order_no (int): 원주문번호
    - stock_code (str): 종목코드 (예: 'A005930' - 삼성전자)
    - quantity (int): 취소할 주문수량
    
    Returns:
    - dict: API 응답 결과
    """
    # API 엔드포인트 URL
    url = "https://openapi.ls-sec.co.kr:8080/stock/order"
    
    # 요청 헤더 설정
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {access_token}",
        "tr_cd": "CSPAT00801",    # 현물취소주문 거래코드
        "tr_cont": "N",           # 연속거래 여부 (N: 연속 아님)
        "tr_cont_key": "",        # 연속거래 키 (연속거래 아니므로 빈 값)
        "mac_address": "112233445566"  # 법인인 경우 필수 (예시 값)
    }
    
    # 요청 본문 데이터 구성
    payload = {
        "CSPAT00801InBlock1": {
            "OrgOrdNo": org_order_no,  # 원주문번호
            "IsuNo": stock_code,       # 종목번호 (A+종목코드)
            "OrdQty": quantity         # 취소할 주문수량
        }
    }
    
    try:
        # API 요청 전송
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # 응답 확인
        if response.status_code == 200:
            result = response.json()
            print("취소 주문 result:\n", result)
            return result
        else:
            return {
                "status_code": response.status_code,
                "error": f"API 요청 실패: {response.text}"
            }
    except Exception as e:
        return {
            "error": f"예외 발생: {str(e)}"
        }
    
