# LS_realtime_trading

- **`XAReal_KOR`**  
  `xa_class_kor` 모듈에 클래스. 주식의 실시간 체결/호가 데이터 + 주문 완료 데이터를 수신합니다.

- **`split_publisher_ls_0.py` ~ `split_publisher_ls_4.py`**  
  여러 개의 publisher 스크립트가 `XAReal_KOR`을 각각 호출하여 데이터를 수신합니다.  

- **`split_subscriber_and_trading_0.py` ~ `split_subscriber_and_trading_4.py`**  
  publisher로부터 데이터를 수신하고, **매매 알고리즘**에 따라 **주문 여부를 판단**합니다.  
  주문이 체결되면, `XAReal_KOR`이 체결 정보를 수신하여 해당 subscriber에 다시 전달합니다.

![Image](https://github.com/user-attachments/assets/b9e32c2b-c1f3-497a-aa99-562909c9d51d)




# Run
```bash
   run split_pub_ls.bat
   run split_sub_ls.bat
