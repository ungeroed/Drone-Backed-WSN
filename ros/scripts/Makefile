default: run

run: run.py init
	python run.py

init: init.py 
	-python init.py mavsys
	-python init.py mavsafety
	-python init.py mavsetp
	-python init.py mavcmd

rc: rc.py
	python rc.py
