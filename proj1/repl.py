#!/usr/bin/env python3

import sys
import doctest

# Local module
import server

Acknowledgement = 'A'
EndOfSession    = 'E'
Request         = 'R'
WayPoint        = 'W'
Unknown         = 'U'

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
        return self.__stdin.readline()

    def evaluate(self, data):
        parsed = preprocess_line(data)
        if not parsed:
            return EndOfSession, ['']
        head, *rest = parsed
        if head == EndOfSession:
            self.__eos = True
        elif head == Request:
            self.parse_request(parsed)

        return head, rest

    def parse_request(self, data):
        head, *rest = data
        least_cost_path_ids = self.parse_least_cost_path(*rest)

        self.writeline('N %d'%(len(least_cost_path_ids)))
        for way_id in least_cost_path_ids:
            self.send_way_point(way_id)

        self.send_eos()

    def send_eos(self):
        self.writeline(EndOfSession)

    def send_way_point(self, way_id):
        while True:
            _, ok = self.parse_ack()
            if ok:
                retr = self.__vertex_map.get(way_id, None)
                if retr is None:
                    return False
                self.writeline('%s %d %d'%(WayPoint, retr['lat'], retr['lon']))
                return True

    def parse_ack(self):
        symlist = preprocess_line(self.readline())
        symbol = Unknown
        if len(symlist) >= 1:
            symbol = symlist[0]

        return symbol, symbol == Acknowledgement

    def read_evaluate(self):
        return self.evaluate(self.readline())

    def __is_eos(self, expr):
        return expr == EndOfSession

    def eos(self, v):
        return self.__is_eos(v)

    def parse_least_cost_path(self, *fields):
        x_lat, x_lon, y_lat, y_lon = fields
        start_min_dist, start_min_point = self.closest_point(float(x_lat), float(x_lon))
        end_min_dist, end_min_point     = self.closest_point(float(y_lat), float(y_lon))
        start_id, end_id = start_min_point.get('id', -1), end_min_point.get('id', -1)

        return self.__server.least_cost_path_internal(start_id, end_id)

    def closest_point(self, lat, lon):
        min_point, min_dist = (0, 0), float('inf')
        for v_id, v_map in self.__vertex_map.items():
            v_lat, v_lon = float(v_map['lat']), float(v_map['lon'])
            dist = server.cost(lat, lon, v_lat, v_lon)
            if dist < min_dist:
                min_dist = dist
                min_point = v_map

        return min_dist, min_point

def main():
    srv, vmap = server.create_server()
    repl = Repl(srv, vmap)
    while 1:
        head, *rest = repl.read_evaluate()
        if repl.eos(head):
            break

def tester():
    doctest.testmod()

if __name__ == '__main__':
    main()
    # tester()
