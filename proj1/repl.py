#!/usr/bin/env python3

import sys
import base64
import doctest

# Local module
from .server import (
    cost,
    create_server,
)

Acknowledgement = 'A'
StartOfSession  = 'starting'
EndOfSession    = 'E'
Request         = 'R'
WayPoint        = 'W'
Unknown         = 'U'
Comment         = '#'

def is_callable_attr(obj, attr):
    """
    >>> class F:
    ...    def __init__(self):
    ...       self.foo = 'bar'
    ...    def get(self): 
    ...       return self.foo
    >>> obj = F()
    >>> is_callable_attr(obj, 'get')
    True
    >>> is_callable_attr(obj, 'pop')
    False
    >>> is_callable_attr(1, 'foo')
    False
    """
    retr = getattr(obj, attr, None)
    if retr is None:
        return False
    return hasattr(retr, '__call__')

def preprocess_line(line):
    return non_empty_fields(line.strip().split(' '))

def non_empty_fields(splits):
    return [field for field in splits if field]

class Repl:
    def __init__(self, server, vertex_map, stdin=None, stdout=None):
        self.__server = server
        self.__vertex_map = vertex_map

        self.__eos = False
        self.__stdin = stdin or sys.stdin
        self.__stdout = stdout or sys.stdout

        assert(is_callable_attr(self.__stdin, 'readline'))
        assert(is_callable_attr(self.__stdout, 'write'))

    def writeline(self, content):
        return self.__stdout.write(content+'\n')

    def readline(self):
        try:
            df = self.__stdin.readline()
        except Exception as e:
            print(e)
            return ''
        else:
            if df and df[0] == Comment:
                print(df)
                return self.readline()

            #print(df)
            return df

    def evaluate(self, data):
        parsed = preprocess_line(data)
        if not parsed:
            return EndOfSession, ['']
        head, *rest = parsed
        # print(head, rest)
        if head == EndOfSession:
            self.__eos = True
        elif head == Request:
            self.parse_request(parsed)

        return head, rest

    def parse_request(self, data):
        head, *rest = data
        least_cost_path_ids = self.parse_least_cost_path(*rest)
        # print("\033[47midsLen\033[00m", len(least_cost_path_ids))

        fmt = 'N %d'%(len(least_cost_path_ids))
        self.writeline(fmt)

        for way_id in least_cost_path_ids:
            if not self.send_way_point(way_id):
                print("Failed to get a response", way_id)
                break

            print(way_id)

        self.send_eos()

    def send_eos(self):
        self.writeline(EndOfSession)

    def send_way_point(self, way_id):
        retr = self.__vertex_map.get(way_id, None)
        if retr is None:
            return False
        lat, lon = retr['lat'], retr['lon']
        outLine = '%s %d %d'%(WayPoint, lat, lon)
        print(outLine, self.writeline(outLine))

        _, ok = self.parse_ack()
        print(_, ok)
        return ok

    def parse_ack(self):
        symlist = preprocess_line(self.readline())
        symbol = Unknown
        if len(symlist) >= 1:
            symbol = symlist[0]

        # print(symbol, "symlist", symlist)
        return symbol, symbol == Acknowledgement
        # return symbol, True

    def read_evaluate(self):
        return self.evaluate(self.readline())

    def __is_eos(self, expr):
        return expr == EndOfSession

    def eos(self, v):
        return self.__is_eos(v)

    def bos(self, v):
        return v.lower().find(StartOfSession) == 0

    def parse_least_cost_path(self, *fields):
        x_lat, x_lon, y_lat, y_lon = fields
        start_min_dist, start_min_point =\
                        self.closest_point(float(x_lat), float(x_lon))
        end_min_dist, end_min_point  =\
                        self.closest_point(float(y_lat), float(y_lon))
        start_id, end_id =\
                     start_min_point.get('id', -1), end_min_point.get('id', -1)

        return self.__server.least_cost_path_internal(start_id, end_id)

    def closest_point(self, lat, lon):
        min_point, min_dist = (0, 0), float('inf')
        for v_id, v_map in self.__vertex_map.items():
            v_lat, v_lon = float(v_map['lat']), float(v_map['lon'])
            dist = cost(lat, lon, v_lat, v_lon)
            if dist < min_dist:
                min_dist = dist
                min_point = v_map

        return min_dist, min_point

def fresh_repl(stdin=None, stdout=None):
    srv, vmap = create_server()
    return Repl(srv, vmap, stdin=stdin, stdout=stdout)

def main():
    repl = fresh_repl()
    while 1:
        head, *rest = repl.read_evaluate()
        if repl.eos(head):
            break

def tester():
    doctest.testmod()

if __name__ == '__main__':
    main()
    # tester()
