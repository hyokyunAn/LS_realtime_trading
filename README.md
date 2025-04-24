# LS_realtime_trading

- **`XAReal_KOR`**  
  A class in the `xa_class_kor` module. Receives real-time stock data and order completion data.

- **`split_publisher_ls_0.py` ~ `split_publisher_ls_4.py`**  
  Multiple publisher scripts each call `XAReal_KOR` to receive data.

- **`split_subscriber_and_trading_0.py` ~ `split_subscriber_and_trading_4.py`**  
  Receive data from publishers and send it to the Trader.

- **`Trading_mechanism`**  
  Determines whether to place an order according to the **trading algorithm**.  
  Once an order is filled, `XAReal` receives the transaction information and sends it back to the corresponding subscriber.

  

![Image](https://github.com/user-attachments/assets/40d3483f-08bb-45c8-8507-d0a11a73225c)




# Run
```bash
   run split_pub_ls.bat
   run split_sub_ls.bat
