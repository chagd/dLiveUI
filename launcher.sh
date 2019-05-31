
#!/bin/bash

roscore &
/usr/bin/python ./main.py &
/usr/bin/python ./listener.py &
 

function finish
{
	sudo killall roscore
	sudo killall listener
}

trap finish EXIT
