@echo off
start "sub_0" "python.exe" "split_subscriber_and_trading_0.py"
timeout /t 1 /nobreak
start "sub_1" "python.exe" "split_subscriber_and_trading_1.py"
timeout /t 1 /nobreak
start "sub_2" "python.exe" "split_subscriber_and_trading_2.py"
timeout /t 1 /nobreak
start "sub_3" "python.exe" "split_subscriber_and_trading_3.py"
timeout /t 1 /nobreak
start "sub_4" "python.exe" "split_subscriber_and_trading_4.py"
timeout /t 1 /nobreak
pause