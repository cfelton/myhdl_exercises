
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

    0 Getting started [00_mex_start_here][00_mex]

    1 Defining a hardware module.  This exercise defines a basic
      shift register  [01_mex_shifty][00_mex]

    2 Greatest common divisor [02_mex_gcd][02_mex]

    3 Interfaces (small example) [03_mex_interfaces][03_mex] 

    4 Tests [04_mex_tests][04_mex]

    5 More tests [05_mex_more_tests][05_mex]
    
    6 Modeling [06_mex_modeling][06_mex]

    7 Music Box [07_mex_music_box][07_mex]


[00_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/00_mex_start_here.ipynb
[01_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/01_mex_shifty.ipynb
[02_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/02_mex_gcd.ipynb
[03_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/03_mex_interfaces.ipynb
[04_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/04_mex_tests.ipynb
[05_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/05_mex_more_tests.ipynb
[06_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/06_mex_modeling.ipynb
[07_mex]: https://github.com/cfelton/myhdl_exercises/blob/master/07_mex_music_box.ipynb
