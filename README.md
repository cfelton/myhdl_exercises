

# Introduction
This repository contains a collection of IPython notebooks
with MyHDL exercises (mex).  These exercises can be used as 
a learning tool to learn hardware description and MyHDL.

## Getting Started
First, clone the repository and run the ipython notebook in the 
cloned workspace:

    >> git clone https://github.com/cfelton/myhdl_exercises
    >> cd myhdl_exercises
    >> ipython notebook

or

    >> jupyter notebook
    
Next, to run the exercises the *myhdl* pacakge is required.  
MyHDL can be installed via *pypi*:

    >> pip install myhdl

Or the latest can be retrieved from:

    >> git clone https://github.com/jandecaluwe/myhdl
    
To start IPython see the [directions here](http://jupyter-notebook-beginner-guide.readthedocs.org/en/latest/)

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


