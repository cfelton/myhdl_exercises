
from myhdl import *

def test(mod, Nsmp=10, Fs=48e3, Nmax=16, convert=False):
    
    Fclk = 4*48e3
    Ts = 1/Fs
    Timeout = 3*Ts
    xv,tv = [],[]
    nmax = Nmax
    
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    note = Signal(intbv(0, min=-nmax, max=nmax))
    nv = Signal(bool(0))
    
    # clock driver
    @always(delay(10))
    def tbclk():
        clock.next = not clock
        
    # reset driver
    def pulse_reset():
        reset.next = reset.active
        yield delay(100)
        reset.next = not reset.active
        yield clock.posedge
        
    # stimulus driver
    def _test():
        tbdut = mod(clock, reset, note, nv, Fs, Fclk)
                
        @instance
        def tbstim():
            t,scnt = 0,0
            yield pulse_reset()
            
            tocnt = 0
            while scnt < Nsmp:
                if nv:
                    xv.append(int(note.val))
                    tv.append(t)
                    t += Ts
                    scnt += 1
                    tocnt = 0
                else:
                    tocnt += 1

                # make sure the musicbox is output samples
                if tocnt >= Timeout:
                    raise StandardError("No samples")

                yield clock.posedge
                
            raise StopSimulation
            
        return tbclk, tbdut, tbstim
    
    # run the simulation, using _test as the stimulus
    Simulation(traceSignals(_test)).run()

    if convert:
        # convert the design to VHDL
        toVHDL(m_musicbox, clock, reset, note, nv,
               sample_rate=Fs, clock_rate=50e6)    
        
        toVerilog(m_musicbox, clock, reset, note, nv, 
                  sample_rate=Fs, clock_rate=50e6)    
    return tv,xv