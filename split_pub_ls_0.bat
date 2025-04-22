@echo on
start "pub_0" "python.exe" "split_publisher_ls_0.py"
timeout /t 1 /nobreak
start "pub_1" "python.exe" "split_publisher_ls_1.py"
timeout /t 1 /nobreak
start "pub_2" "python.exe" "split_publisher_ls_2.py"
timeout /t 1 /nobreak
start "pub_3" "python.exe" "split_publisher_ls_3.py"
timeout /t 1 /nobreak
start "pub_4" "python.exe" "split_publisher_ls_4.py"
timeout /t 1 /nobreak

pause