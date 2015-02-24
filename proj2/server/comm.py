#!/usr/bin/env python3

import sys

# Local modules
from graphing import repl
from textserial import textserial

def default_port():
    if sys.platform == 'darwin':
        return '/dev/tty.usbmodem1411'

    return '/dev/ttyACM0'


class SerialTalkie:
    def __init__(self, port=None, baud=9600):
        self.__port = port or default_port()
        self.__baud = int(baud)
        self.__talkie = None

    def __start_talkie(self):
        self.__talkie = textserial.TextSerial(self.__port, self.__baud,
                                                    encoding='ISO-8859-1')
                            

    def __enter__(self):
        self.__start_talkie()
        return self.__talkie

    def __exit__(self, *args, **kwargs):
        self.__talkie.__exit__(*args, **kwargs)

def main():
    
    with SerialTalkie() as f:
        rpl = repl.fresh_repl(f, f)
        # First step is to wait for the start of the session
        while 1:
            head, *rest = rpl.read_evaluate()
            if rpl.bos(head):
                break

            print('Started!')
            evaluating = True

            while evaluating:
                head, *rest = rpl.read_evaluate()
                # print(head, rest)
                if rpl.eos(head):
                    evaluating = False

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
