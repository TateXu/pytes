  PyTES Documentation
========================================

PyTES is a Python-based, 3-clause BSD licensed toolbox to facilitate the remote control of transcranial electric stimulation and ease deploying a closed-loop TES system. PyTES supports two communication protocols to control the hardware: VISA and USBTMC.
![PyTES GUI](./pytes/Figures/toolbox_1.png)
 
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
    * [GUI](#GUI) 
    * [In Psychopy](#Psychopy)
    * [In OpenVibe](#OpenVibe)
    * [Live Demo](#Demo)
* [Known Issues](#Issues)

## Installation
-----

### Prerequiste
Different operating system and communication protocol has diverse prerequisites for installing and using the PyTES package. A brief summary is listed below:
|           |   USBTMC   |    VISA    |
|:---------:|:----------:|:----------:|
|   Linux   |    None    |[pyvisa](#Pyvisa)|
|  Windows  |    N/A     |[pyvisa](#Pyvisa) + [driver](#Driver)|

#### Pyvisa
More details about the installation of pyvisa can be found [here][pyvisa_link] 

#### Driver 
Driver installation depends on the chosen hardware(s). For example, the Rigol arbitrary waveform generator requires the type-specific IVI driver, as listed [here][rigoldriver]. Users of PyTES are suggested to install the driver according to the official documentation of their own device(s).

### PyTES
You can either clone this repo or install pytes via pip:
```bash
pip install git+https://github.com/TateXu/pytes.git
```

## Features 
-----
### Plug-in-play
This feature leverages the default USBTMC driver of the Linux system such that the USBTMC interface can be opened as a file node. Please note that this feature is only available for Linux users using the USBTMC protocol.

### Closed-loop application
PyTES can be seamlessly combined with other online experiment frameworks to constitute a closed-loop TES system, e.g., OpenVibe and Psychopy. More details for the usage can be referred to [OpenVibe](#OpenVibe) and [Psychopy](#Psychopy)

### PyTES with arbitrary signal
Some advanced TES require a non-regular shape of the stimulation signal, e.g., AM-tACS, etc. To better support such studies, PyTES provides such function to output a user-defined signal. 
* In the GUI version, the signal should be first used to create a dictionary, as shown below. Next, this dictionary should be saved as a pickle file. Finally, input the path of the pickle file into the corresponding entry.

```Python
data_to_save = {'sps': sampling_rate_in_Hz,
                'data': a_list_of_all_data_points}
```
* In the command line version, you can use the function `SignalGenerator().arb_func()` to output the arbitrary signal.

### Timer for stimulation and fade in/out duration (GUI version only)
For the GUI version of PyTES, the timers for stimulation and fade in/out can be set separately for different output channels. No input for these entries will indicate either indefinite stimulation or no fade in/out for the corresponding channel.

## Usage
-----

### Command Line 

The usage via the command-line version is just as same as the other Python packages. One example of outputing a tACS signal with 1V ampltiude, 25Hz frequency and 45 degree phase shift is as shown below: 
```Python
from pytes.signal_generator import SignalGenerator as SG
control = SG()
control.amp(value=1, chn=1, stim_mode='tACS')  # Adjust the tACS amplitude of channel 1 to 1V
control.freq(value=25, chn=1, stim_mode='tACS')  # Adjust the tACS freuqency of channel 1 to 25Hz
control.phase(value=45, chn=1, stim_mode='tACS')  # Adjust the tACS phase shift of channel 1 to 45 degree
control.on(chn=1)  # Turn on the output of channel 1

```

PyTES also provides many other functions to adjust the stimulation parameters conveniently, e.g., frequency, offset, phase, etc. More functions can be found at [here](./signal_generator.py#L475).

In addition to the provided functions, it is also possible and convenient to directly send SCPI command via PyTES to communicate with the hardware with the function [`SG().set_cmd()`](./signal_generator.py#L383).


### GUI 
* __Step 1__: You can eithe directly run the GUI python script from command line - `path_to_pytes_pkg/pytes_gui.py` or  call the GUI function from the package
```Python
from pytes.pytes_gui import PyTESWindow
``` 
* __Step 2__: Driver selection, USBTMC or VISA (Note: USBTMC is not applicable for Windows; For USBTMC protocol, the root access is required)
![pwdinput](./pytes/Figures/toolbox_2.png)
* __Step 3__: Device selection from the option menu
* __Step 4__: Connection test via clicking "Connect" button
* __Step 5__: Parameter setup
    * tDCS/tACS/tRNS - Fill in the value in the allowable entry
    * Arbitraty signal stimulation - Input the absolute path to the data file (in .pkl format, more details refer to [Features](#Features) )
* __Step 6__: Stimulation signal check via clicking "Update Parameters" button
* __Step 7__: Timer setup for stimulation duration and fade in/out duration.
    * `None` value for stimulation duration means a indefinite stimulation
    * `None` value for fade duration means no fade in/out will be applied
* __Step 8__: Output stimulation signal via clicking "Output" of target channel

Step 1 - 6:

https://user-images.githubusercontent.com/27919893/167694285-08fd13ac-9ce1-4704-9b3f-1793c79d7791.mp4

Step 7 - 8:

https://user-images.githubusercontent.com/27919893/167694322-c0be0b92-31af-499b-8efa-535c65c14e07.mp4

### Psychopy
To integrate the real-time stimulation signal control code into the experimental paradigm written by PsychoPy, you can leverage the [Code Component][psychopy] function of PsychoPy, in which the snippets of PyTES control commands can be inserted into the experimental paradigm code.

### OpenVibe 
For OpenVibe users, you can use [The Python Scripting box][openvibe] to integrate the PyTES command to control the stimulation signal based on the online decoding results.

### Demo
A live demo for controlling the stimulation signal on Windows is as shown below:

https://user-images.githubusercontent.com/27919893/168045550-190f09b7-c675-46e8-9f39-fe7202f3662b.mp4



## Issues 
-----
1. __Font issues of the GUI version__:
The PyTES GUI is based on the package Tkinter. It is known that the Tkinter font cannot be correctly rendered under Anaconda Python on the Ubuntu system. For better visualization, it is suggested to switch to a non-conda Python installation. More discussion about this issue can be found [here][condaissue]

      
2. __USBTMC driver cannot be selected after using the VISA driver__:
Devices that are already opened by the VISA protocol cannot be opened by USBTMC drivers. Restarting the hardware devices can fix the issue.
    
-----
[pyvisa_link]: https://pyvisa.readthedocs.io/en/latest/introduction/getting.html
[condaissue]: https://github.com/ContinuumIO/anaconda-issues/issues/6833#issuecomment-351363320
[rigoldriver]: https://www.rigolna.com/download
[psychopy]: https://www.psychopy.org/builder/components/code.html
[openvibe]: http://openvibe.inria.fr/tutorial-using-python-with-openvibe/#The+Python+Scripting+box
[pytesfunction]: https://github.com/TateXu/pytes/blob/cb66334b7d7131cd4810b9c9db1c80861fc94695/signal_generator.py#L475








