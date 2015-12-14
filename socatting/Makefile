.PHONY: deps-or-die open-drone-server

SERVER_ADDR := localhost

default: open-drone-server

open-drone-server: deps-or-die
	socat tcp-l:54321,reuseaddr,fork file:/dev/ttyACM0,nonblock,waitlock=/tmp/ttyACM0.lock

ttyACM: deps-or-die
	socat -x pty,link=ttyACM0,waitslave tcp:$(SERVER_ADDR):54321 2> log

deps-or-die:
	@which socat &>/dev/null || (echo "Please install socat" ; exit 1)
