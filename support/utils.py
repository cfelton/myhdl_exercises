
import os

import myhdl
from myhdl import (Simulation, traceSignals, SignalType, always, now)


# reference to the last monitor log
_log = None


def run_testbench(tbfunc, mexname='', dutmod=None, portmap=None):
    """
    Arguments:
      tbfunc: testbench function
      dutmod: design under test module (function)
      mexname: name of the exercise (name of the VCD file)
      portmap: dictionary with the top-level port map for conversion
    """
    
    if not os.path.isdir('vcd'):
        os.makedirs('vcd')

    traceSignals.name = 'vcd/{}'.format(mexname)
    if os.path.isfile(traceSignals.name+'.vcd'):
        os.remove(traceSignals.name+'.vcd')

    Simulation(traceSignals(tbfunc)).run()
    
    noerror = hasattr(tbfunc, 'error') and not tbfunc.error
    if dutmod is not None and portmap is not None and noerror:
        if not os.path.isdir('output'):
            os.makedirs('output')
        myhdl.toVHDL.directory = 'output'
        myhdl.toVerilog.directory = 'output'
        myhdl.toVerilog.no_testbench = True
        myhdl.toVHDL(dutmod, **portmap)
        myhdl.toVerilog(dutmod, **portmap)


def monitor(clock, **sigs):
    global _log
    logmap = sigs
    for name, sig in sigs.items():
      assert isinstance(sig, SignalType)  

    log = [(-1, 0, 0, 0, 0,) for _ in range(20)]

    @always(clock.posedge)
    def monlog():
        log.append((now(),) + tuple(map(int, sigs.values() )) )
        log.pop(0)

    _log = log
    return monlog


def dump_monitor_log():
    global _log
    log = _log
    print("Last {} clock cycles".format(len(log)))
    