PyTES README
========================================

PyTES 

****

## Contents

* [Installation](#Installation)
* [Features](#Features)
    * Plug-in-play
    * Closed-loop application
    * TES with arbitrary signal
    * Timer for stimulation and fade in/out duration (GUI version)

* [Usage](#Usage)
    * Command line 
    * GUI 
    * In Psychopy
    * In OpenVibe 


* [Known Issues](#Known Issues)


## Installation
-----

### Prerequiste
PyTES supports two types of drivers: USBTMC and VISA. 


### PyTES

## Features 
-----
### Plug-in-play
For Linux users, the control of stimulation signal via PyTES is rather straight forward
### Closed-loop application

### PyTES with arbitrary signal
To output via 
### Timer for stimulation and fade in/out duration (GUI version only)
For the GUI version of PyTES, the timers for stimulation and fade in/out can be set seperately for different output channels 

## Usage
-----

### Command line 


### GUI 
    * **Step 1**: Driver selection, USBTMC or VISA (Note: USBTMC is not applicable for Windows)
    * **Step 2**: Device selection from the option menu
    * **Step 3**: Connection test via clicking "Connect" button
    * **Step 4**: Parameter setup
        * tDCS/tACS/tRNS - Fill in the value in the allowable entry
        * Arbitraty signal stimulation - Input the absolute path to the data file (in .pkl format, more details refer to [Features](#Features) )
    * **Step 5**: Stimulation signal check via clicking "Update Parameters" button
    * **Step 6**: Timer setup for stimulation duration and fade in/out duration.
        * `None` value for stimulation duration means a indefinite stimulation
        * `None` value for fade duration means no fade in/out will be applied
    * **Step 7**: Output stimulation signal via clicking "Output" of target channel

### In Psychopy

### In OpenVibe 


## Known Issues 
    1. **Font issues of the GUI version**
    The PyTES GUI is based on the package tkinter. It is known that the tkinter font cannot be correctly rendered under Anaconda Python on Ubuntu system. For better visualization, it is suggested to switch to non-conda Python installation. More discussion about this issue can be found [here](https://github.com/ContinuumIO/anaconda-issues/issues/6833#issuecomment-351363320)

         
    2. **Font issues**
        
-----

