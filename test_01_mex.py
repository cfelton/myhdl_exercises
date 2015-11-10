
from __future__ import division
from __future__ import print_function

import os
from random import randint
from myhdl import *
from support import Clock, Reset
from support import shifty


def test(mod):
    clock = Clock(0)
    reset = Reset(0, active=0, async=True)
    load = Signal(bool(0))
    lval = Signal(intbv(0, max=256, min=0))
    obit = Signal(bool(0))
    ival = randint(0, lval.max-1)

    def _test():
        tbdut = mod(clock, reset, load, lval, obit, ival=ival)
        tbclk = clock.gen()

        log = [(-1, 0, 0, 0, 0,) for _ in range(20)]
        isht = Signal(intbv(0, max=256, min=0))

        @always(clock.posedge)
        def tbmon():
            log.append((now(), load, lval, obit, mod.y,))
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
                    for ii in xrange(1000):
                        assert isht[7] == obit
                        isht.next = concat(isht[6:0], isht[7])
                        yield clock.posedge
                        
                print("Test Successful")
            except Exception as err:
                yield delay(10)
                print("Test Error")
                print("Last %d clock cycles" % (len(log)))
                print(" time    | load | lval | obit | shift (y)")
                for ee in log:
                    print("%8d | %4d | %04X | %4d | %04X" % ee)
                print(err)

            raise StopSimulation

        return tbclk, tbdut, tbstim, tbmon

    if not os.path.isdir('vcd'):
        os.makedirs('vcd')

    traceSignals.name = 'vcd/01_mex'
    if os.path.isfile(traceSignals.name+'.vcd'):
        os.remove(traceSignals.name+'.vcd')
    
    Simulation(traceSignals(_test)).run()
    toVHDL(mod, clock, reset, load, lval, obit, ival=ival)
    toVerilog(mod, clock, reset, load, lval, obit, ival=ival)


if __name__ == '__main__':
    test(shifty)