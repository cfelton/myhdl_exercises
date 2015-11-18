
from __future__ import division
from __future__ import print_function

from random import randint
from myhdl import (Signal, intbv, always, instance, concat, 
                   now, StopSimulation)
from support import Clock, Reset
from support import run_testbench
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

    def _bench():
        _bench.error = True
        tbdut = mod(clock, reset, load, lval, obit, 
                    initial_value=ival)
        tbclk = clock.gen()

        log = [(-1, 0, 0, 0, 0,) for _ in range(20)]
        isht = Signal(intbv(0, max=256, min=0))

        @always(clock.posedge)
        def tbmon():
            log.append((now(), load, lval, obit, mod.shiftreg,))
            log.pop(0)
            
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
                print("Last %d clock cycles" % (len(log)))
                print(" time    | load | lval | obit | shiftreg")
                for ee in log:
                    print("%8d | %4d | %04X | %4d | %04X" % ee)
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