# BASIC Language

*Ken Guyton<br />*
*Tue 2018-10-30 15:24:34 -0400*

This will be a BASIC compiler and execution module written in Python.
It will work on a very primative version of BASIC similar to a very
early version of Dartmouth BASIC.

Here's a simple program.

    10 FOR I = 1 TO 10
    20 LET X = I * I
    30 PRINT X,
    40 PRINT "HELLO"
    50 NEXT I


## Set up to test

You need python3.  This program was written using Python 3.6.

You'll also need pipenv.

    pip install pipenv

Untar a distribution file, e.g., 

    tar xvzf basic_lang-1.0.4.tar.gz
    cd basic_lang-1.0.4

If you want to run tests, install the testing dependencies.

    pipenv install -d

Install the pipenv virtual environment.

    pipenv shell

Setup the basic_lang installation in the virtual environment.

    python3 setup.py install

## Run programs

    cd bas_pro

    basic_run.py --basic_file HELLO.BAS --run
    basic_run.py --basic_file IFTHEN.BAS --run
    basic_run.py --basic_file FOR_LOOP.BAS --run

## Run tests

    pytest

## Possible future work

A classic BASIC interactive "shell" should be straightforward.  I've
already written something similar several times and have a shell
library.

## References

[Fifty Years of BASIC, the Programming Language That Made Computers Personal by Harry McCracken, April 29, 2014, Time.com"](http://time.com/69316/basic/)


## Copyright

All the files, documentation, and program code here are copyright
2018, 2019 by Ken Guyton.  All rights reserved.  Licenses for use are
available only by request.
