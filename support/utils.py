
from __future__ import print_function

import os

import myhdl
from myhdl import (Simulation, traceSignals, SignalType, always, now)


# reference to the last monitor log
_log = None
_logmap = None


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


def monitor(clock, sigs):
    global _log, _logmap    
    assert isinstance(sigs, dict)

    logmap = sigs
    for name, sig in sigs.items():
      assert isinstance(sig, SignalType)  

    log = [(-1, 0, 0, 0, 0,) for _ in range(20)]

    @always(clock.posedge)
    def monlog():
        log.append((now(),) + tuple(map(int, sigs.values() )) )
        log.pop(0)

    _log = log
    _logmap = logmap

    return monlog


def dump_monitor_log(format='int'):
    global _log, _logmap
    assert format in (None, 'hex', 'int')

    log = [entry for entry in (_log) if entry[0] != -1]
    print("Last {} clock cycles".format(len(log)))

    lognames = list(_logmap.keys())
    logsigs = list(_logmap.values())

    print(" sim step |", end="")
    for nm in lognames:
        more = ' ' if len(nm) <= 8 else '~'
        print(" {:<8s}{} |".format(nm[:8], more), end="")
    print(" ")
    
    for en in log:
        for ii, val in enumerate(en):
            if ii == 0:
                print(" {:<8d} |".format(en[0]), end="")
            else:
                if len(logsigs[ii-1]) == 1 or format == 'int':
                    print(" {:8d}  |".format(val), end="")
                else:
                    print(" {:08X}  |".format(val), end="")
        print(" ")
        
    return 