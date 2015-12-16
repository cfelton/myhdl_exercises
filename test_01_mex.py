
from __future__ import division
from __future__ import print_function

from random import randint
from collections import OrderedDict as odict
import traceback

from myhdl import (Signal, intbv, always, instance, concat, 
                   now, delay, StopSimulation)

from support import Clock, Reset
from support import run_testbench, monitor, dump_monitor_log
from support import shifty

# initial_value check error message
errmsg1 = """initial_value output bit check failed, expected {} got {}
    initial_value    {:X}
    cycle (# shifts) {:d}
"""

# load value shift check error message
errmsg2 = """output bit check failed, expected {} got {}
    load_value       {:X}
    cycle (# shifts) {:d}
"""


def stimulator(mod=None):
    """ Basic stimulus for waveform viewing
    Arguments:
        mod: myhdl module to be stimulated

    This module will exercise a fixed number of clock cycles and
    will not verify for correctness.
    """
    if mod is None:
        mod = shifty

    clock = Clock(0)
    reset = Reset(0, active=0, async=True)
    load = Signal(bool(0))
    load_value = Signal(intbv(0, max=256, min=0))
    output_bit = Signal(bool(0))
    initial_value = 0x80

    sigs = odict()
    sigs['load'], sigs['load_value'] = load, load_value
    sigs['output_bit'] = output_bit

    def _bench():
        tbdut = mod(clock, reset, load, load_value, output_bit,
                    initial_value=initial_value)
        sigs['shiftreg'] = mod.shiftreg
        tbclk = clock.gen()
        tbmon = monitor(clock, sigs)

        @instance
        def tbstim():
            timestart = now()
            try:
                yield reset.pulse(10)
                yield clock.posedge
                for _ in range(8):
                    yield clock.posedge
                load_value.next = 0x01
                load.next = True
                yield clock.posedge
                load.next = False
                for _ in range(17):
                    yield clock.posedge
            except Exception as err:
                print("Error occurred: {}".format(err))
                traceback.print_exc()
                yield delay(now()-270)
            dump_monitor_log(format='hex')
            raise StopSimulation

        return tbdut, tbclk, tbmon, tbstim

    portmap = {"clock": clock, "reset": reset, "load": load,
               "load_value": load_value, "output_bit": output_bit,
               "initial_value": initial_value}
    run_testbench(_bench, "01_mex_stim", mod, portmap)


def test(mod=None):
    """ Verification test
    Arguments:
        mod: myhdl module to be verified
    """
    if mod is None:
        mod = shifty

    clock = Clock(0)
    reset = Reset(0, active=0, async=True)
    load = Signal(bool(0))
    load_value = Signal(intbv(0, max=256, min=0))
    output_bit = Signal(bool(0))
    initial_value = randint(0, load_value.max-1)
    
    sigs = odict()
    sigs['load'], sigs['load_value'] = load, load_value
    sigs['output_bit'] = output_bit

    def _bench():
        _bench.error = True
        tbdut = mod(clock, reset, load, load_value, output_bit, 
                    initial_value=initial_value)
        sigs['shiftreg'] = mod.shiftreg
        tbclk = clock.gen()
        tbmon = monitor(clock, sigs)

        expected_shift = Signal(intbv(0, max=256, min=0))
            
        @instance
        def tbstim():
            try:
                expected_shift.next = initial_value
                yield reset.pulse(10)
                yield clock.posedge

                # check the `initial_value`
                for ii in range(1000):
                    assert expected_shift[7] == output_bit, \
                        errmsg1.format(expected_shift[7], output_bit,
                                       initial_value, ii)
                    expected_shift.next = concat(expected_shift[7:0],
                                                 expected_shift[7])
                    yield clock.posedge

                for ii in range(7):
                    rr = randint(1, load_value.max-1)
                    load_value.next = rr
                    load.next = True
                    expected_shift.next = rr
                    yield clock.posedge
                    load.next = False  
                    yield clock.posedge                  
                    for ii in range(100):
                        assert expected_shift[7] == output_bit, \
                        errmsg2.format(expected_shift[7], output_bit,
                                       load_value, ii)
                        expected_shift.next = concat(expected_shift[7:0],
                                                     expected_shift[7])
                        yield clock.posedge
                        
                _bench.error = False
                print("Test Successful")
            except Exception as err:
                yield delay(10*5)
                print("Test Error")
                dump_monitor_log(format='hex')
                _bench.error = True
                print(err)

            raise StopSimulation

        return tbclk, tbdut, tbstim, tbmon

    portmap = {"clock": clock, "reset": reset, "load": load,
               "load_value": load_value, "output_bit": output_bit, 
               "initial_value": initial_value}
    run_testbench(_bench, "01_mex_test", mod, portmap)


if __name__ == '__main__':
    test(shifty)
