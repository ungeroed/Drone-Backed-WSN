import termios, sys, os

def read_key():
        fd = sys.stdin.fileno()

        old = termios.tcgetattr(fd)

        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0

        termios.tcsetattr(fd, termios.TCSANOW, new)

        c = None
        try:
                c = os.read(fd, 1)
        finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        return c
