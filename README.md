  PyTES README
========================================

PyTES is a Python-based, 3-clause BSD licensed toolbox to facilitate the remote control of transcranial electric stimulation and ease the deployment of a closed-loop TES system. PyTES supports two types of communication protocols to control the hardware: VISA and USBTMC. More detailed about there differences can be refered to the paper:
 
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

|           |   USBTMC   |    VISA    |
|:---------:|:----------:|:----------:|
|   Linux   |    None    |[pyvisa](#Pyvisa)|
|  Windows  |    N/A     |[pyvisa](#Pyvisa) + [driver](#Driver)|

#### Pyvisa
More details obout the installation of pyvisa can be found [here][pyvisa_link] 

#### Driver 
Driver installation can be found here

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
    * __Step 1__: Driver selection, USBTMC or VISA (Note: USBTMC is not applicable for Windows)
    * __Step 2__: Device selection from the option menu
    * __Step 3__: Connection test via clicking "Connect" button
    * __Step 4__: Parameter setup
        * tDCS/tACS/tRNS - Fill in the value in the allowable entry
        * Arbitraty signal stimulation - Input the absolute path to the data file (in .pkl format, more details refer to [Features](#Features) )
    * __Step 5__: Stimulation signal check via clicking "Update Parameters" button
    * __Step 6__: Timer setup for stimulation duration and fade in/out duration.
        * `None` value for stimulation duration means a indefinite stimulation
        * `None` value for fade duration means no fade in/out will be applied
    * __Step 7__: Output stimulation signal via clicking "Output" of target channel

### In Psychopy

### In OpenVibe 


## Known Issues 
    1. __Font issues of the GUI version__
    The PyTES GUI is based on the package tkinter. It is known that the tkinter font cannot be correctly rendered under Anaconda Python on Ubuntu system. For better visualization, it is suggested to switch to non-conda Python installation. More discussion about this issue can be found [here][https://github.com/ContinuumIO/anaconda-issues/issues/6833#issuecomment-351363320]

         
    2. __USBTMC driver cannot be selected after using the VISA driver__
    
    Devices which are already opened by VISA protocol cannot be opened by USBTMC drivers. Restarting the hardware devices can fix the issue.
        
-----
[pyvisa_link]: https://pyvisa.readthedocs.io/en/latest/introduction/getting.html
