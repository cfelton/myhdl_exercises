
#
# This work was originally completed by ...
#
# This is a manual translation, from perl to python, of :
# http://cpansearch.perl.org/src/GSULLIVAN/Verilog-VCD-0.03/lib/Verilog/VCD.pm 
#
# been modified

from __future__ import print_function

import re
import copy

# import the plotting utilities and setup the plot
try:
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    PlotOk = True
except:
    PlotOk = False

timescale = 0
endtime = 0


def parse_and_plot(filename):
    """ parse the VCD and plot
    """
    data, timescale, endtime = parse(filename)
    t, w = toarray(data, timescale, endtime)
    return plot(t, w, timescale, endtime)


def plot(timearray, waveforms, timescale, endtime):
    """ plot the arrays extracted from the VCD
    """
    fig, ax = None, None
    if PlotOk:    
        fig, ax = plt.subplots(1, figsize=(12, 4,))
        names = []
        for ii, kv in enumerate(waveforms.items()):
            nm, x = kv
            names.append(nm)
            offset = -2*ii
            ax.plot(timearray, np.array(x)+offset, 
                    color='k', linewidth=2.5)
            ax.text(1, offset+.5, nm, fontsize=14)
            
        ax.set_ylim(-1*((len(waveforms)*2)-1), 2)
        
        labels = [item.get_text() for item in ax.get_yticklabels()]
        # print(labels)
        for ii, ll in enumerate(labels):
            # print(ll)
            if ll.isdigit() and int(ll) % 2:
                idx = int(ll)/2
                labels[ii] = names[idx]
            else:
                labels[ii] = ''
        ax.set_yticklabels(labels)
        # ax.set_yticklabels([])
        ax.grid(True)

    return fig,ax


def toarray(vcd, timescale, endtime):
    """conver to simple arrays for plotting
    """

    vcdp = {}
    # @todo: make sure each entry has a 'tv' and 'net' key, if
    #   not don't process
    for k, v in vcd.items():
        if 'tv' in v and 'nets' in v:
            vcdp[k] = v

    max_length = 0
    for k, v in vcdp.items():
        max_length = max(max_length, 
                         v['tv'][-1][0]-v['tv'][0][0])
    # print(max_length)
    # @todo - this is a very simplistic VCD viewer, limit
    # @todo:  to a small number of points
    # print(max_length, endtime)
    max_length = max(max_length, endtime)
    waveforms = {}
    timex = range(max_length)
    for k, v in vcdp.items():
        b = [0 for _ in range(max_length)]
 
        # get the type, only binary and ints for now
        val = int(v['tv'][0][1])
        tv = copy.copy(v['tv'])
        for ii, _ in enumerate(b):
            # print(ii, tv[0])
            if len(tv) > 0 and ii == tv[0][0]:
                val = int(tv[0][1])
                tv.pop(0)
            b[ii] = val
 
        # print(type(v),v)
        nn = v['nets'][0]['name']
        waveforms[nn] = b
 
    return timex, waveforms


def parse(file, only_sigs=0, use_stdout=0, siglist=[], opt_timescale=''):
    """Parse input VCD file into data structure.
    Also, print t-v pairs to STDOUT, if requested.
    """
    global timescale, endtime
    usigs = {}
    for i in siglist:
        usigs[i] = 1

    if len(usigs):
        all_sigs = 0
    else :
        all_sigs = 1

    data = {}
    mult = 0
    num_sigs = 0
    hier = []
    time = 0

    re_time = re.compile(r"^#(\d+)")
    re_1b_val = re.compile(r"^([01zxZX])(.+)")
    re_Nb_val = re.compile(r"^[br](\S+)\s+(.+)")

    fh = open(file, 'r')
    while True:
        line = fh.readline()
        if line == '':  # EOF
            break

        # chomp
        # s/ ^ \s+ //x
        line = line.strip()

        if "$enddefinitions" in line:
            num_sigs = len(data)
            if num_sigs == 0:
                if all_sigs:
                    _croak("Error: No signals were found in the VCD file file.",
                          'Check the VCD file for proper var syntax.')
                else:
                    _croak("Error: No matching signals were found in the VCD file file.",
                          ' Use list_sigs to view all signals in the VCD file.')

            if (num_sigs > 1) and use_stdout:
                _croak("Error: There are too many signals (num_sigs) for output ",
                      'to STDOUT.  Use list_sigs to select a single signal.')
            
            if only_sigs:
                break

        elif "$timescale" in line:
            statement = line
            if "$end" not in line:
                while fh:
                    line = fh.readline()
                    statement += line
                    if "$end" in line:
                        break
            
            mult = _calc_mult(statement, opt_timescale)

        elif "$scope" in line:
            # assumes all on one line
            #   $scope module dff end
            hier.append( line.split()[2] ) # just keep scope name
        
        elif "$upscope" in line:
            hier.pop()
        
        elif "$var" in line:
            # assumes all on one line:
            #   $var reg 1 *@ data $end
            #   $var wire 4 ) addr [3:0] $end
            ls = line.split()
            type = ls[1]
            size = ls[2]
            code = ls[3]
            name = "".join(ls[4:-1])
            path = '.'.join(hier)
            full_name = path + name
            if (full_name in usigs) or all_sigs :
                if code not in data :
                    data[code] = {}
                if 'nets' not in data[code]:
                    data[code]['nets'] = []

                var_struct = {'type': type,
                              'name': name,
                              'size': size,
                              'hier': path, }

                if var_struct not in data[code]['nets']:
                    data[code]['nets'].append( var_struct )

        elif line.startswith('#'):
            re_time_match   = re_time.match(line)
            time = mult * int(re_time_match.group(1))
            endtime = time

        elif line.startswith(('0', '1', 'x', 'z', 'b', 'r', 'Z', 'X')):
            re_1b_val_match = re_1b_val.match(line)
            re_Nb_val_match = re_Nb_val.match(line)
            if re_Nb_val_match:
              value = re_Nb_val_match.group(1)
              code  = re_Nb_val_match.group(2)
            elif re_1b_val_match :
              value = re_1b_val_match.group(1)
              code  = re_1b_val_match.group(2)
            if code in data:
                if use_stdout:
                    print(time, value)
                else:
                    if 'tv' not in data[code]:
                        data[code]['tv'] = []
                    data[code]['tv'].append( (time, value) )

    fh.close()

    return data, timescale, endtime


def _calc_mult(statement, opt_timescale=''):
    """ 
    Calculate a new multiplier for time values.
    Input statement is complete timescale, for example:
      timescale 10ns end
    Input new_units is one of s|ms|us|ns|ps|fs.
    Return numeric multiplier.
    Also sets the package timescale variable.
    """ 

    fields = statement.split()
    fields.pop()   # delete end from array
    fields.pop(0)  # delete timescale from array
    tscale = ''.join(fields)

    new_units = ''
    if opt_timescale != '':
        new_units = opt_timescale.lower()
        new_units = re.sub(r"\s", '', new_units)
        timescale = "1"+new_units
    
    else:
        timescale = tscale
        return 1

    mult = 0
    units = 0
    ts_match = re.compile(r"(\d+)([a-z]+)")
    if ts_match.match(tscale):
        mult = ts_match.group(1)
        units = ts_match.group(2).lower()
    else:
        _croak("Error: Unsupported timescale found in VCD file: tscale.  ",
               'Refer to the Verilog LRM.')

    mults = {
        'fs': 1e-15,
        'ps': 1e-12,
        'ns': 1e-09,
        'us': 1e-06,
        'ms': 1e-03,
         's': 1e-00,
    }
    mults_keys = mults.keys()
    mults_keys.sort(key=lambda x : mults[x])
    usage = '|'.join(mults_keys)

    scale = 0
    if units in mults :
        scale = mults[units]
    
    else:
        _croak("Error: Unsupported timescale units found in VCD file: "+units+".  ",
               "Supported values are: "+usage)

    new_scale = 0
    if new_units in mults:
        new_scale = mults[new_units]
    
    else:
        _croak("Error: Illegal user-supplied timescale: "+new_units+".  ",
               "Legal values are: "+usage)

    return (mult * scale) / new_scale


def _croak(*args):
    """ Function similar to Perl's Carp::croak, to simplify porting this code
    """
    a = "".join(args)
    raise Exception(a)



