

# Introduction
This repository contains a collection of IPython notebooks
with MyHDL exercises (mex).  These exercises can be used as 
a learning tool to learn hardware description and MyHDL.

## Getting Started
First, clone the repository and run the ipython notebook in the 
cloned workspace:

    >> git clone https://bitbucket.org/cfelton/mex
    >> cd mex
    >> ipython notebook
    
Next, to run the exercises the *myhdl* and *myhdl_tools* packages 
are required.  If the above cell did not execute without error the 
packages need to be retrieved and the notebook kernel restarted.  
Both packages can be installed via *pypi*:

    >> pip install myhdl
    >> pip install myhdl_tools
    
Or the latest can be retrieved from:

    >> git clone https://github.com/jandecaluwe/myhdl
    >> hg clone https://bitbucket.org/cfelton/myhdl_tools
    
To start IPython see the [directions here]()

Once the packages are installed open the first notebook and 
verify all the cells can run.

## Exercises
Other than the first exercise, each requires an HDL module to be
defined and an existing test will verify if the HDL module is 
working correctly or not.

0. Getting started [00_mex_start_here]

0. Defining a hardware module.  This exercise defines a basic
   shift register  [01_mex_shifty]

0. GCD

0. Interfaces (small example)

0. Tests

0. More tests

0. Gearbox (solve problem once)

0. Mandelbrot


