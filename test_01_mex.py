
from __future__ import division
from __future__ import print_function

from random import randint
from collections import OrderedDict as odict

from myhdl import (Signal, intbv, always, instance, concat, 
                   now, delay, StopSimulation)

from support import Clock, Reset
from support import run_testbench, monitor, dump_monitor_log
from support import shifty


def test(mod=None):
    if mod is None:
        mod = shifty

    clock = Clock(0)
    reset = Reset(0, active=0, async=True)
    load = Signal(bool(0))
    lval = Signal(intbv(0, max=256, min=0))
    obit = Signal(bool(0))
    ival = randint(0, lval.max-1)
    
    sigs = odict()
    sigs['load'], sigs['load_value'] = load, lval
    sigs['output_bit'] = obit

    def _bench():
        _bench.error = True
        tbdut = mod(clock, reset, load, lval, obit, 
                    initial_value=ival)
        sigs['shiftreg'] = mod.shiftreg
        tbclk = clock.gen()
        tbmon = monitor(clock, sigs)

        isht = Signal(intbv(0, max=256, min=0))
            
        @instance
        def tbstim():
            try:
                isht.next = ival
                yield reset.pulse(10)
                yield clock.posedge

                for ii in range(1000):
                    assert isht[7] == obit
                    isht.next = concat(isht[6:0], isht[7])
                    yield clock.posedge

                for ii in range(33):
                    rr = randint(1, lval.max-1)
                    lval.next = rr
                    load.next = True
                    isht.next = rr
                    yield clock.posedge
                    load.next = False  
                    yield clock.posedge                  
                    for ii in range(1000):
                        assert isht[7] == obit
                        isht.next = concat(isht[6:0], isht[7])
                        yield clock.posedge
                        
                _bench.error = False
                print("Test Successful")
            except Exception as err:
                yield delay(10)
                print("Test Error")
                dump_monitor_log(format='hex')
                _bench.error = True
                print(err)

            raise StopSimulation

        return tbclk, tbdut, tbstim, tbmon

    portmap = {"clock": clock, "reset": reset, "load": load,
               "load_value": lval, "output_bit": obit, 
               "initial_value": ival}
    run_testbench(_bench, "01_mex", mod, portmap)


if __name__ == '__main__':
    test(shifty)