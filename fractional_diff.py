import numpy as np



'''
원 논문: https://www.ma.imperial.ac.uk/~ejm/M3S8/Problems/hosking81.pdf
'''

def get_weights(d, size):
    """
    프랙셔널 차분을 위한 가중치를 계산합니다.
    
    Parameters:
    d (float): 차분 차수 (0 < d < 1)
    size (int): 계산할 가중치의 개수
    
    Returns:
    np.array: 계산된 가중치 배열
    """
    w = [1.]  # 첫 번째 가중치는 항상 1
    for k in range(1, size):
        # w[k] = w[k-1] * (d - k + 1) / k
        # 위 공식은 다음과 같이 표현될 수 있습니다:
        w.append(-w[-1] * (d - k + 1) / k)
    return np.array(w)


def fractional_diff(series, d, window=None):
    """
    시계열 데이터에 대해 프랙셔널 차분을 계산합니다.
    
    Parameters:
    series (np.array): 입력 시계열 데이터
    d (float): 차분 차수 (0 < d < 1)
    window (int): 사용할 과거 데이터의 윈도우 크기 (None인 경우 전체 시리즈 길이 사용)
    
    Returns:
    np.array: 프랙셔널 차분이 적용된 시계열
    """
    # 입력 데이터를 numpy 배열로 변환
    series = np.array(series)
    
    # 윈도우 크기가 지정되지 않은 경우 전체 시리즈 길이 사용
    if window is None:
        window = len(series)
    
    # 가중치 계산
    weights = get_weights(d, window)
    
    # 결과를 저장할 배열 초기화 (첫 window-1개의 값은 NaN으로 설정)
    res = np.full_like(series, np.nan, dtype=float)
    
    # 각 시점에 대해 프랙셔널 차분 계산
    for t in range(window-1, len(series)):
        # 현재 시점부터 window 크기만큼의 과거 데이터에 가중치를 적용
        res[t] = np.sum(weights * series[t-window+1:t+1][::-1])
    
    return res


def apply_fractional_diff(data, d, window=None, threshold=1e-5):
    """
    프랙셔널 차분을 적용하고 가중치가 특정 임계값 이하인 경우 윈도우 크기를 최적화합니다.
    
    Parameters:
    data (np.array): 입력 시계열 데이터
    d (float): 차분 차수 (0 < d < 1)
    window (int): 사용할 과거 데이터의 윈도우 크기
    threshold (float): 가중치 임계값
    
    Returns:
    np.array: 프랙셔널 차분이 적용된 시계열
    int: 사용된 실제 윈도우 크기
    """
    if window is None:
        # 가중치가 임계값보다 작아질 때까지 윈도우 크기를 찾음
        window = 1
        while True:
            weights = get_weights(d, window)
            if abs(weights[-1]) < threshold:
                break
            window += 1
    
    return fractional_diff(data, d, window), window


if __name__ == "__main__":
    a = [100, 142, 117, 130, 122, 130, 115,92,127,106,143,143,156,147,125,154,155,145,152,186,175,171]

    diff_data, used_window = apply_fractional_diff(a, d=0.2, window=10)

    print(f"Used window size: {used_window}")
    print("Fractional differenced data:", diff_data)


    