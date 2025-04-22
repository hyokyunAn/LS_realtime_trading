import json
import pandas as pd
import time
from datetime import datetime, timedelta
import numpy as np
from fractional_diff import apply_fractional_diff
import requests


def dummy_func():
    return


def subtract_n_seconds(time_str, n=10.0):
    # 입력된 시간 문자열 파싱
    try:
        dt = datetime.strptime(time_str, "%H:%M:%S %f")
    except ValueError:
        return "Invalid time format. Please use 'HH:MM:SS mmm'"

    # 10분 뺀 새로운 시간 계산
    new_time = dt - timedelta(seconds=n)

    # 결과를 원래 형식의 문자열로 반환
    return new_time.strftime("%H:%M:%S %f")[:12]


def add_n_seconds(time_str, n=10.0):
    # 입력된 시간 문자열 파싱
    try:
        dt = datetime.strptime(time_str, "%H:%M:%S %f")
    except ValueError:
        return "Invalid time format. Please use 'HH:MM:SS mmm'"

    # 10분 뺀 새로운 시간 계산
    new_time = dt + timedelta(seconds=n)

    # 결과를 원래 형식의 문자열로 반환
    return new_time.strftime("%H:%M:%S %f")[:12]

    

def get_timestamp_float(time1):

    '''
    time: {HH:MM:SS fff}
    '''
    t1, t1_f = time1.split()
    t1_f = int(t1_f)
    t1_h, t1_m, t1_s = [int(i) for i in t1.split(":")]

    time1_stamp = t1_h * 3600 + t1_m * 60 + t1_s + t1_f * 0.001
    return time1_stamp


def subtract_n_minutes(time_str, n=10.0):
    # 입력된 시간 문자열 파싱
    try:
        dt = datetime.strptime(time_str, "%H:%M:%S %f")
    except ValueError:
        return "Invalid time format. Please use 'HH:MM:SS mmm'"

    # 10분 뺀 새로운 시간 계산
    new_time = dt - timedelta(minutes=n)

    # 결과를 원래 형식의 문자열로 반환
    return new_time.strftime("%H:%M:%S %f")[:12]


def buy_CLS_투표(predictions, 투표전략, 구매라벨=2):
    '''
    투표전략: ["한표이상", "다수결", "만장일치"]
    '''
    if 투표전략 == "만장일치":
        for pred in predictions:
            if pred != 구매라벨:
                return False
        return True
    
    elif 투표전략 == "한표이상":
        for pred in predictions:
            if pred == 구매라벨:
                return True
        return False

    elif 투표전략 == "다수결":
        vote_count = 0
        for pred in predictions:
            if pred == 구매라벨:
                vote_count += 1
        if vote_count > len(predictions)/2:
            return True
        else:
            return False
        

def buy_REG_투표(predictions, 투표전략, threshold=0.2):
    '''
    투표전략: ["평균", "최댓값", "최솟값"]
    '''
    if 투표전략 == "평균":
        pred = sum(predictions)/len(predictions)
    elif 투표전략 == "최댓값":
        pred = max(predictions)
    elif 투표전략 == "최솟값":
        pred = min(predictions)

    if pred > threshold:
        return True
    else:
        return False


def buy_or_투표(predictions, thresholds):
    for pred, threshold in zip(predictions, thresholds):
        if pred > threshold:
            return True
    return False


def sell_CLS_투표(predictions, 투표전략, 판매라벨=2, threshold=0.8):
    '''
    투표전략: ["한표이상", "다수결", "만장일치"]
    '''
    if 투표전략 == "만장일치":
        for prob in predictions:
            if prob[판매라벨] < threshold:
                return False
        return True
    
    elif 투표전략 == "한표이상":
        for prob in predictions:
            if prob[판매라벨] > threshold:
                return True
        return False

    elif 투표전략 == "다수결":
        vote_count = 0
        for prob in predictions:
            if prob[판매라벨] > threshold:
                vote_count += 1
        if vote_count > len(predictions)/2:
            return True
        else:
            return False


def get_current_time_formatted():
    now = datetime.now()
    return now.strftime("%H:%M:%S %f")[:-3]


def convert_체결시간(HHMMSS:str):
    '''
    HHMMSS를 "HH:MM:SS 000"으로 변환
    '''
    # HHMMSS = f"{체결시간:06d}"
    return f"{HHMMSS[:2]}:{HHMMSS[2:4]}:{HHMMSS[4:6]} 000"


def subtract_n_seconds(time_str, n=10.0):
    # 입력된 시간 문자열 파싱
    try:
        dt = datetime.strptime(time_str, "%H:%M:%S %f")
    except ValueError:
        return "Invalid time format. Please use 'HH:MM:SS mmm'"

    # 10분 뺀 새로운 시간 계산
    new_time = dt - timedelta(seconds=n)

    # 결과를 원래 형식의 문자열로 반환
    return new_time.strftime("%H:%M:%S %f")[:12]


def generate_time_list():
    start_time = datetime(2023, 1, 1, 9, 7, 0)  # 2023년 1월 1일 09:05:00
    end_time = datetime(2023, 1, 1, 16, 0, 0)  # 2023년 1월 1일 16:00:00
    time_interval = timedelta(minutes=5)  # 

    time_list = []
    current_time = start_time

    now_time = str(datetime.now().strftime("%H%M%S"))

    while current_time <= end_time:
        time_str = current_time.strftime("%H%M%S")
        if time_str > now_time:
            time_list.append(time_str)
        current_time += time_interval

    return time_list


def format_time_string(time_string):
    '''
    HH:MM:SS fff 형태로 변환
    '''
    # 문자열의 길이가 9자리인지 확인
    if len(time_string) != 9:
        return "Invalid input: string must be 9 digits long"
    
    # 시간, 분, 초, 밀리초로 분리
    hours = time_string[:2]
    minutes = time_string[2:4]
    seconds = time_string[4:6]
    milliseconds = time_string[6:]
    
    # 포맷된 문자열 반환
    return f"{hours}:{minutes}:{seconds} {milliseconds}"


def get_time_diff(time1, time2):
    '''
    time: {HH:MM:SS fff}
    '''
    t1, t1_f = time1.split()
    t2, t2_f = time2.split()
    t1_f = int(t1_f)
    t2_f = int(t2_f)
    t1_h, t1_m, t1_s = [int(i) for i in t1.split(":")]
    t2_h, t2_m, t2_s = [int(i) for i in t2.split(":")]

    time1_stamp = t1_h * 3600 + t1_m * 60 + t1_s + t1_f * 0.001
    time2_stamp = t2_h * 3600 + t2_m * 60 + t2_s + t2_f * 0.001

    diff = abs(time1_stamp - time2_stamp)
    return diff


def get_time_diff_순서고려(time1, time2):
    '''
    time: {HH:MM:SS fff}
    time2가 느리면 음수 반환
    '''
    t1, t1_f = time1.split()
    t2, t2_f = time2.split()
    t1_f = int(t1_f)
    t2_f = int(t2_f)
    t1_h, t1_m, t1_s = [int(i) for i in t1.split(":")]
    t2_h, t2_m, t2_s = [int(i) for i in t2.split(":")]

    time1_stamp = t1_h * 3600 + t1_m * 60 + t1_s + t1_f * 0.001
    time2_stamp = t2_h * 3600 + t2_m * 60 + t2_s + t2_f * 0.001

    diff = time1_stamp - time2_stamp
    return diff


def compress_df(data, cut_threshold):
    '''
    * 시가, 고가, 저가 대비 가격 추가
    current_group 으로 알고리즘 개선한 버전
    '''
    if len(data) == 0:
        return None

    # Initialize variables
    filtered_data = []
    current_group = None

    # Iterate over the DataFrame
    for idx, row in data.iterrows():
        time = row['체결시간']
        price = row['체결가']
        volume = row['체결량']
        price_pct_change = row['전일대비체결가']
        시가 = row['시가']
        고가 = row['고가']
        저가 = row['저가']
        시가시간 = row['시가시간']
        고가시간 = row['고가시간']
        저가시간 = row['저가시간']


        # Start a new group if there is no current group
        if current_group is None:
            current_group = {
                'start_time': time,
                'last_time': time,
                'price': price,
                'total_volume': volume,
                '체결대금': price * volume,
                'sign': 1 if volume > 0 else -1,
                '전일대비체결가': price_pct_change,
                '시가': 시가,
                '고가': 고가,
                '저가': 저가,
                '시가시간': 시가시간,
                '고가시간': 고가시간,
                '저가시간': 저가시간
            }
            continue
        
        time_diff = get_time_diff(time, current_group['last_time'])

        # Check if the current row can be grouped with the current group
        if time_diff < 0.01 and (volume > 0) == (current_group['sign'] > 0):
            current_group['last_time'] = time
            current_group['price'] = price  # Update to the latest price
            current_group['total_volume'] += volume
            current_group['체결대금'] += price * volume
        else:
            # Check if the group meets the cut_threshold
            if abs(current_group['체결대금']) >= cut_threshold:
                filtered_data.append([
                    current_group['last_time'],
                    current_group['price'],
                    current_group['total_volume'],
                    current_group['전일대비체결가'],
                    current_group['체결대금'],
                    current_group['시가'],
                    current_group['저가'],
                    current_group['고가'],
                    current_group['시가시간'],
                    current_group['저가시간'],
                    current_group['고가시간']
                ])
                
            # Start a new group
            current_group = {
                'start_time': time,
                'last_time': time,
                'price': price,
                'total_volume': volume,
                '체결대금': price * volume,
                'sign': 1 if volume > 0 else -1,
                '전일대비체결가':price_pct_change,
                '시가':시가,
                '저가':저가,
                '고가':고가,
                '시가시간':시가시간,
                '저가시간':저가시간,
                '고가시간':고가시간
            }

    # Handle the last group
    if current_group and abs(current_group['체결대금']) >= cut_threshold:
        filtered_data.append([
            current_group['last_time'],
            current_group['price'],
            current_group['total_volume'],
            current_group['전일대비체결가'],
            current_group['체결대금'],
            current_group['시가'],
            current_group['저가'],
            current_group['고가'],
            current_group['시가시간'],
            current_group['저가시간'],
            current_group['고가시간']
        ])
        
    
    filtered_data = pd.DataFrame(filtered_data, columns=['체결시간', '체결가', '체결량', '전일대비체결가', '체결대금', '시가', '저가', '고가', '시가시간', '저가시간', '고가시간'])
    # filtered_data['시가대비'] = filtered_data['체결가']/filtered_data['시가']
    # filtered_data['저가대비'] = filtered_data['체결가']/filtered_data['저가']
    # filtered_data['고가대비'] = filtered_data['체결가']/filtered_data['고가']
    return filtered_data


def extract_static_features_(filtered_row, base_price=None):
    '''
    특정 시점의 호가 정보를 feature로 나타냄
    '''
    if base_price is None:
        base_price = (filtered_row['매도호가1']+filtered_row['매수호가1'])/2
    for i in range(1,11):
        filtered_row[f'매도호가_기준가대비_{i}'] = filtered_row[f'매도호가{i}'] / base_price
        filtered_row[f'매수호가_기준가대비_{i}'] = filtered_row[f'매수호가{i}'] / base_price
    for i in range(1,11):
        filtered_row[f'매도호가잔량_금액_{i}'] = 0
        filtered_row[f'매수호가잔량_금액_{i}'] = 0
        filtered_row[f'매도_{i}호가_비율'] = 0
        filtered_row[f'매수_{i}호가_비율'] = 0
    filtered_row[[f'매도호가잔량_금액_{i}' for i in range(1,11)]] = filtered_row[[f'매도호가{i}' for i in range(1, 11)]].values * filtered_row[[f'매도호가잔량{i}' for i in range(1, 11)]].values
    filtered_row[[f'매수호가잔량_금액_{i}' for i in range(1,11)]] = filtered_row[[f'매수호가{i}' for i in range(1, 11)]].values * filtered_row[[f'매수호가잔량{i}' for i in range(1, 11)]].values

    # 1. VWAP (가중평균가격) 계산
    매수_vwap = (filtered_row[[f'매수호가{i}' for i in range(1, 11)]].values * 
                filtered_row[[f'매수호가잔량{i}' for i in range(1, 11)]].values).sum() / filtered_row[[f'매수호가잔량{i}' for i in range(1, 11)]].values.sum()

    매도_vwap = (filtered_row[[f'매도호가{i}' for i in range(1, 11)]].values * 
                filtered_row[[f'매도호가잔량{i}' for i in range(1, 11)]].values).sum() / filtered_row[[f'매도호가잔량{i}' for i in range(1, 11)]].values.sum()
    

    # 2. 상위 1, 2, 3위 물량이 많은 호가 번호
    매수_volumes = {f'매수호가잔량{i}': filtered_row[f'매수호가잔량{i}'] for i in range(1, 11)}
    매도_volumes = {f'매도호가잔량{i}': filtered_row[f'매도호가잔량{i}'] for i in range(1, 11)}

    top_매수_volumes = sorted(매수_volumes, key=매수_volumes.get, reverse=True)[0]
    매수최대호가번호 = int(top_매수_volumes.replace("매수호가잔량", ""))
    top_매도_volumes = sorted(매도_volumes, key=매도_volumes.get, reverse=True)[0]
    매도최대호가번호 = int(top_매도_volumes.replace("매도호가잔량", ""))

    # 3. 매수/매도 총량 비율
    total_매수량 = sum(filtered_row[f'매수호가잔량{i}'] for i in range(1, 11))
    total_매도량 = sum(filtered_row[f'매도호가잔량{i}'] for i in range(1, 11))
    매수매도_잔량비율 = total_매수량 / (total_매도량 + 1e-9) # 매도/매수

    # 4. 매수/매도 잔량의 대금 합
    total_매도대금 = sum(filtered_row[f'매도호가{i}'] * filtered_row[f'매도호가잔량{i}'] for i in range(1, 11))
    total_매수대금 = sum(filtered_row[f'매수호가{i}'] * filtered_row[f'매수호가잔량{i}'] for i in range(1, 11))

    # 5. 매수/매도 1,2,3호가 잔량
    매수_1호가_잔량 = filtered_row['매수호가1'] * filtered_row['매수호가잔량1']
    매도_1호가_잔량 = filtered_row['매도호가1'] * filtered_row['매도호가잔량1']
    매수_2호가_잔량 = filtered_row['매수호가2'] * filtered_row['매수호가잔량2']
    매도_2호가_잔량 = filtered_row['매도호가2'] * filtered_row['매도호가잔량2']
    매수_3호가_잔량 = filtered_row['매수호가3'] * filtered_row['매수호가잔량3']
    매도_3호가_잔량 = filtered_row['매도호가3'] * filtered_row['매도호가잔량3']

    # 6. 각 전체호가에서 비율매수/매도 각 호가의 비율
    filtered_row[[f'매수_{i}호가_비율' for i in range(1,11)]] = filtered_row[[f'매수호가잔량_금액_{i}' for i in range(1,11)]] / total_매수대금
    filtered_row[[f'매도_{i}호가_비율' for i in range(1,11)]] = filtered_row[[f'매도호가잔량_금액_{i}' for i in range(1,11)]] / total_매도대금

    

    mid_price = (filtered_row['매도호가1']+filtered_row['매수호가1'])/2
    # try:
    return {
        "매수매도_격차": (filtered_row['매도호가1']-filtered_row['매수호가1'])/filtered_row['매수호가1'] * 100,
        "매도중심가": 매도_vwap/filtered_row['매도호가1'],
        "매수중심가": 매수_vwap/filtered_row['매수호가1'],

        "매도잔량최대호가": 매도최대호가번호,
        "매도최대호가_금액": filtered_row[f'매도호가{매도최대호가번호}'] * filtered_row[f'매도호가잔량{매도최대호가번호}'],
        "매도최대호가_가격": filtered_row[f'매도호가{매도최대호가번호}'] / filtered_row[f'매도호가1'],
        "매도최대호가_가격_중간가대비": filtered_row[f'매도호가{매도최대호가번호}'] / mid_price,

        "매수잔량최대호가": 매수최대호가번호,
        "매수최대호가_금액": filtered_row[f'매수호가{매수최대호가번호}'] * filtered_row[f'매수호가잔량{매수최대호가번호}'],
        "매수최대호가_가격": filtered_row[f'매수호가{매수최대호가번호}'] / filtered_row[f'매수호가1'],
        "매수최대호가_가격_중간가대비": filtered_row[f'매수호가{매수최대호가번호}'] / mid_price,

        "매도/매수": 매수매도_잔량비율,
        "매도대금합": total_매도대금,
        "매수대금합": total_매수대금,
        "매수1호가_금액": 매수_1호가_잔량,
        "매도1호가_금액": 매도_1호가_잔량,
        "매수2호가_금액": 매수_2호가_잔량,
        "매도2호가_금액": 매도_2호가_잔량,
        "매수3호가_금액": 매수_3호가_잔량,
        "매도3호가_금액": 매도_3호가_잔량,

        "매수_1호가_비율": filtered_row["매수_1호가_비율"],
        "매도_1호가_비율": filtered_row["매도_1호가_비율"],
        "매수_2호가_비율": filtered_row["매수_2호가_비율"],
        "매도_2호가_비율": filtered_row["매도_2호가_비율"],
        "매수_3호가_비율": filtered_row["매수_3호가_비율"],
        "매도_3호가_비율": filtered_row["매도_3호가_비율"],
        "매수_4호가_비율": filtered_row["매수_4호가_비율"],
        "매도_4호가_비율": filtered_row["매도_4호가_비율"],
        "매수_5호가_비율": filtered_row["매수_5호가_비율"],
        "매도_5호가_비율": filtered_row["매도_5호가_비율"],
        "매수_6호가_비율": filtered_row["매수_6호가_비율"],
        "매도_6호가_비율": filtered_row["매도_6호가_비율"],
        "매수_7호가_비율": filtered_row["매수_7호가_비율"],
        "매도_7호가_비율": filtered_row["매도_7호가_비율"],
        "매수_8호가_비율": filtered_row["매수_8호가_비율"],
        "매도_8호가_비율": filtered_row["매도_8호가_비율"],
        "매수_9호가_비율": filtered_row["매수_9호가_비율"],
        "매도_9호가_비율": filtered_row["매도_9호가_비율"],
        "매수_10호가_비율": filtered_row["매수_10호가_비율"],
        "매도_10호가_비율": filtered_row["매도_10호가_비율"],
        
        "매수_1호가_기준가대비": filtered_row[f'매수호가_기준가대비_1'],
        "매수_2호가_기준가대비": filtered_row[f'매수호가_기준가대비_2'],
        "매수_3호가_기준가대비": filtered_row[f'매수호가_기준가대비_3'],
        "매수_4호가_기준가대비": filtered_row[f'매수호가_기준가대비_4'],
        "매수_5호가_기준가대비": filtered_row[f'매수호가_기준가대비_5'],
        "매수_6호가_기준가대비": filtered_row[f'매수호가_기준가대비_6'],
        "매수_7호가_기준가대비": filtered_row[f'매수호가_기준가대비_7'],
        "매수_8호가_기준가대비": filtered_row[f'매수호가_기준가대비_8'],
        "매수_9호가_기준가대비": filtered_row[f'매수호가_기준가대비_9'],
        "매수_10호가_기준가대비": filtered_row[f'매수호가_기준가대비_10'],
        "매도_1호가_기준가대비": filtered_row[f'매도호가_기준가대비_1'],
        "매도_2호가_기준가대비": filtered_row[f'매도호가_기준가대비_2'],
        "매도_3호가_기준가대비": filtered_row[f'매도호가_기준가대비_3'],
        "매도_4호가_기준가대비": filtered_row[f'매도호가_기준가대비_4'],
        "매도_5호가_기준가대비": filtered_row[f'매도호가_기준가대비_5'],
        "매도_6호가_기준가대비": filtered_row[f'매도호가_기준가대비_6'],
        "매도_7호가_기준가대비": filtered_row[f'매도호가_기준가대비_7'],
        "매도_8호가_기준가대비": filtered_row[f'매도호가_기준가대비_8'],
        "매도_9호가_기준가대비": filtered_row[f'매도호가_기준가대비_9'],
        "매도_10호가_기준가대비": filtered_row[f'매도호가_기준가대비_10'],
    }
    # except:
    #     print("extract_static_feature_ Error: ")
    #     print(f"매도최대호가_가격: {filtered_row[f'매도호가{매도최대호가번호}']}. filtered_row[f'매도호가1']:{filtered_row[f'매도호가1']}")


def get_hoga_diff_features(filtered_row_before, filtered_row_after, base_price=None):
    '''
    time_before, time_after 두 시각에서의 호가창 상태 비교
    '''
    assert base_price != None
    
    time_before = filtered_row_before['클라이언트시간']
    time_after = filtered_row_after['클라이언트시간']
    static_features_before = extract_static_features_(filtered_row_before.copy(), base_price=base_price)
    static_features_after = extract_static_features_(filtered_row_after.copy(), base_price=base_price)
    diff_features = {
        '매수1호가_가격차이': static_features_after['매수_1호가_기준가대비'] - static_features_before['매수_1호가_기준가대비'],
        '매도1호가_가격차이': static_features_after['매도_1호가_기준가대비'] - static_features_before['매도_1호가_기준가대비'],
        '매수매도1호가_크로스스프레드_1': static_features_after['매도_1호가_기준가대비'] - static_features_before['매수_1호가_기준가대비'],
        '매수매도1호가_크로스스프레드_2': static_features_after['매수_1호가_기준가대비'] - static_features_before['매도_1호가_기준가대비'],
        '호가끼리시간차': get_time_diff(time_after, time_before),
        '매수대금합_Diff':static_features_after['매수대금합'] - static_features_before['매수대금합'],
        '매도대금합_Diff':static_features_after['매도대금합'] - static_features_before['매도대금합'],
        '매수최대호가금액_Diff':static_features_after['매수최대호가_금액'] - static_features_before['매수최대호가_금액'],
        '매도최대호가금액_Diff':static_features_after['매도최대호가_금액'] - static_features_before['매도최대호가_금액'],
    }
    return static_features_before, static_features_after, diff_features



def convert_timestr_to_float(time_str:str):
    '''
    time_str: "HH:MM:SS fff" 형식
    '''
    hour, minute, seconds = time_str.split(":")[0], time_str.split(":")[1], time_str.split(":")[2]
    seconds, floats = seconds.split(" ")[0], seconds.split(" ")[1]
    time_float = int(hour) + int(minute) / 60 + int(seconds)/3600 + int(floats)/(3600*1000)
    return time_float


def convert_to_time_format(number):
    '''
    91117 -> "09:11:17 000"
    '''
    # 숫자를 문자열로 변환
    number_str = str(int(number)).zfill(6)
    ### print("number_str: ", number_str)
    
    # 시, 분, 초 추출
    hours = number_str[:2]
    minutes = number_str[2:4]
    seconds = number_str[4:6]
    ### print(f"hours:{hours}. minutes:{minutes}. seconds:{seconds}")
    
    # 포맷팅된 시간 문자열 생성
    formatted_time = f"{hours}:{minutes}:{seconds}.000"
    
    return formatted_time


def convert_HHMMSS_to_float(time_str:str):
    '''
    time_str: "HH:MM:SS" 형식
    '''
    
    hour, minute, seconds = time_str.split(":")[0], time_str.split(":")[1], time_str.split(":")[2]
    time_float = int(hour) + int(minute) / 60 + int(seconds)/3600 
    return time_float



def signal_for_0p25상승_b_highest_eat10000(all_transaction_df, last_transaction_df, hoga_df):
    '''
    all_transaction_df, last_transaction_df: compress된 df

    0. 5호가 전에 비해 0.25%이상 상승
    1. 5호가전 1~5호가 중 최대 호가 잔량이 1억 이상.
    2. 해당 호가 잔량을 75%이상 잡아먹음
    '''
    signal_발견 = False
    if len(all_transaction_df) - len(last_transaction_df) < 31:
        return False
    
    for idx, row in last_transaction_df.iterrows():
        if row['체결대금'] > 5000 * 10000:
            signal_발견 = True
            체결시간 = row['체결시간']
            break
    if signal_발견:
        n초전 = subtract_n_seconds(체결시간, 30)
        if all_transaction_df.iloc[-30-idx]['체결시간'] < n초전:
            return False
        else:
            return True
    return False




def divide_into_N(number, N):
    """
    숫자를 N등분하는 함수
    나누어 떨어지지 않는 경우 뒤에서부터 차례대로 나머지를 분배
    """
    # 기본 몫 계산
    base_value = number // N
    
    # 나머지 계산
    remainder = number % N
    
    # 결과 리스트 초기화 (기본 몫으로)
    result = [base_value] * N
    
    # 나머지가 있다면 뒤에서부터 분배
    # 뒤에서부터 나머지만큼 각 요소에 1씩 추가
    for i in range(remainder):
        result[N- 1 - i] += 1
    
    return result


def sort_by_timestamp(data):
    """
    리스트의 첫 번째 원소(시간 문자열)를 기준으로 정렬하는 함수
    """
    # 첫 번째 원소를 기준으로 정렬
    sorted_data = sorted(data, key=lambda x: x[0])
    return sorted_data


