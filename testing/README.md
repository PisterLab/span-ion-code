# code/testing

Code for testing the second iteration of the SPANI chip, taped out 2022/11/16.

* `cfd.ino`: Code for the Teensy 3.6 microcontroller.
* `dac.py`: Measurement and processing on-chip DAC voltages.
* `gpib.py`: GPIB control functions for boxes in the lab.
* `scan.py`: For programming and reading from the on-chip analog scan chain.
* `signal_chains.py`: Low level functions for prompting and measuring the full signal chains on the chip.
* `testing.py`: Functions incorporating control over potentially multiple boxes and the Teensy microcontroller for more nicely packaged automation for testing.
* `run_me.py`: The file for people to _locally_ modify, intended to be run when performing actual measurements. Doubles as a location for working use examples of the code.

## Getting Started
1. Clone the repository
2. If you're running Windows 10, `source .bashrc_win10` in the terminal. Note that this may screw with your Jupyter setup, so I recommend running that from a separate instantiation of the terminal. Windows 10 is notorious for not playing nicely with Python, which can result in infinite hang time when trying to just run `python` in the terminal.

## How to Use the Code
After cloning, go into `run_me.py`---unless you are working on the code base, this is the only file you should go near. Within `run_main()` there are a series of `if True/False` blocks. Each of these is a self-contained module which doubles as a debugging bench and eventually example use case for functions within the code base. Feel free to use them and modify as you like; I ask that if you build up another self-contained testing module like any of these, make a pull request with a detailed description of what you've modified. 