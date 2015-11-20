
from __future__ import division
from __future__ import print_function

from random import randint
import fractions
from collections import OrderedDict as odict

from myhdl import (Signal, intbv, always, instance, 
                   delay, StopSimulation)

from support import Clock, Reset
from support import run_testbench, monitor, dump_monitor_log
from support import gcd


def test(mod=None):
    if mod is None:
        mod = gcd

    nloops = 9
    clock = Clock(0)
    reset = Reset(0, active=0, async=True)
    a, b, c = [Signal(intbv(0)[32:]) for _ in range(3)]
    start = Signal(bool(0))
    finished = Signal(bool(1))
    
    sigs = odict()
    sigs['a'], sigs['b'], sigs['c'] = a, b, c
    sigs['start'] = start
    sigs['finished'] = finished

    def _bench():
        _bench.error = True
        tbdut = mod(clock, reset, a, b, c, start, finished)
        tbclk = clock.gen()
        tbmon = monitor(clock, sigs)

        @instance
        def tbstim():
            try:
                yield reset.pulse(10)
                yield clock.posedge

                for ii in range(nloops):
                    a.next = randint(0, 2**26-1)
                    b.next = randint(0, 2**26-1)

                    start.next = True
                    yield clock.posedge
                    start.next = False
                    yield clock.posedge

                    waitcnt = 0
                    er = fractions.gcd(a, b)
                    while not finished:
                        yield clock.posedge
                        waitcnt += 1
                        if waitcnt > 100000:
                            raise Exception("Timeout error")
                    
                    assert c == er
                    yield delay(100)
                    yield clock.posedge

                _bench.error = False
                print("Test Successful")
            except Exception as err:
                yield delay(10)
                print("Test Error")
                dump_monitor_log()
                _bench.error = True
                print(err)

            raise StopSimulation

        return tbdut, tbclk, tbmon, tbstim

    portmap = {"clock": clock, "reset": reset, 
               "a": a, "b": b, "c": c,
               "start": start, "finished": finished}

    run_testbench(_bench, "02_mex", mod, portmap)


if __name__ == '__main__':
    test(gcd)
