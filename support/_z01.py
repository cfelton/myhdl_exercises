

from myhdl import *

def shifty(clock, reset, load, lval, obit, ival=0):
    
    y = Signal(intbv(ival, min=lval.min, max=lval.max))
    mb = len(y)-1

    @always_seq(clock.posedge, reset=reset)
    def rtl():
        if load:
            y.next = lval
        else:
            y.next = concat(y[mb-1:0], y[mb]) 

    @always_comb
    def rtl_assign():
        obit.next = y[mb]

    shifty.y = y

    return rtl, rtl_assign