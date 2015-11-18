
from myhdl import Signal, intbv, always_seq


def gcd(clock, reset, a, b, c, start, finished):
    # force the default state of `finished` to True
    finished._val = True
    x, y = [Signal(intbv(0)[len(a):]) for _ in range(2)]

    @always_seq(clock.posedge, reset=reset)
    def beh():
        if start:
            finished.next = False
            x.next = a
            y.next = b
        else:
            if y == 0:
                finished.next = True
                c.next = x
            elif x > y:
                x.next = x - y
            else:
                y.next = y - x

    return beh
    