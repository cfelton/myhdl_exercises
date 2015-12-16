

from myhdl import *


def shifty(clock, reset, load, load_value, 
           output_bit, initial_value=0):
    
    shiftreg = Signal(intbv(initial_value, 
                            min=load_value.min, max=load_value.max))
    mb = len(shiftreg)-1

    @always_seq(clock.posedge, reset=reset)
    def beh_shift():
        if load:
            shiftreg.next = load_value
        else:
            shiftreg.next = concat(shiftreg[mb:0], shiftreg[mb]) 

    @always_comb
    def beh_assign():
        output_bit.next = shiftreg[mb]

    shifty.shiftreg = shiftreg

    return beh_shift, beh_assign
