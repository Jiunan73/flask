#!/bin/sh
while true
do
	ps -ef | grep "app.py" | grep -v "grep"
if [ "$?" -eq 1 ]
then
	./autostart.sh #啟動應用，修改成使用者啟動應用指令碼或命令
	echo "process has been restarted!"
else
	echo "process already started!"
fi
	sleep 1000
done
