
"""
3-Clause BSD License

Copyright 2022 <Jiachen Xu>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its
       contributors may be used to endorse or promote products derived from
       this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE



This file containts four classes with diamond inheritance as shown below:

                               BaseDriver
                                   |
                        -----------------------
                        |                     |
                      VISA                 USBTMC
                        |                     |
                        -----------------------
                                   |
                             SignalGenerator
"""

import os
import time
import numpy as np
import platform


class BaseDriver(object):
    # A base class for different types of drivers
    def __init__(self, dev=None):
        super(BaseDriver, self).__init__()
        pass

    def set_cmd(self, scpi_command='', dev_fd=None):
        pass

    def read_cmd(self, length, dev_fd=None):
        pass

    def query_cmd(self, scpi_command, length, dev_fd=None):
        pass


class VISA(BaseDriver):
    """Virtual Instrument Software Architecture (VISA) Driver (Default for Win)

    Advantges: Compatible with various interfaces, e.g., USBTMC, GPIB, TCP/IP
    Disadvantages: Require several installations, e.g., pyvisa, device driver,
                   More details refer to README.md

    Parameters
    ----------
    dev : str | None (default None)
        The string used to index device based on ResourceManager object

    Attributes
    ----------
    dev: str | None (default None)
        The string used to index device based on ResourceManager object
    dev_fd: int
        File descriptor of the device (Not applicable for VISA driver)

    Returns
    -------


    """
    def __init__(self, dev=None, inst=True):
        try:
            print('Attempt to use the VISA driver')
            import pyvisa
            self.rm = pyvisa.ResourceManager()
        except ModuleNotFoundError:
            print('---------------------------------------------------')
            print('Use pip install -U pyvisa to install pyvisa package')
            print('---------------------------------------------------')

            raise ModuleNotFoundError
        if inst:
            print(dev)
            self.__dev_init(dev=dev)

    def __dev_init(self, dev):
        print('init')
        print(dev)
        if dev is None:
            dev_info_list, dev_instance_list = self.dev_list()
            dev_id = input('Available devices are listed above and input ' +
                           'the corresponding id number to select the ' +
                           'desired device.\n')
            self.dev = dev_instance_list[int(dev_id)]
        else:
            self.dev = self.rm.open_resource(dev)

    def dev_list(self):
        # Display all VISA compatible interfaces and indicate whethere they can
        # be controlled via SCPI command

        dev_instance_list = []
        dev_info_list = []

        dev_name_list = self.rm.list_resources()
        for tmp_dev_id, tmp_dev_name in enumerate(dev_name_list):
            try:
                tmp_dev = self.rm.open_resource(tmp_dev_name)
                tmp_msg = tmp_dev.query("*IDN?")
                info = f'Id: {tmp_dev_id}, Device info: {tmp_msg}'
            except:
                tmp_dev = None
                info = f'Id: {tmp_dev_id}, Device info: Uncontrolable via SCPI\
                    commands, not target device'
            finally:
                print(info)
                dev_instance_list.append(tmp_dev_name)
                dev_info_list.append(info)

        return dev_info_list, dev_instance_list

    def set_cmd(self, scpi_command='', dev_fd=None):
        return self.dev.write(scpi_command)

    def read_cmd(self, length, dev_fd=None):
        return self.dev.read()

    def query_cmd(self, scpi_command, length, dev_fd=None):
        return self.dev.query(scpi_command)


class USBTMC(BaseDriver):
    """USB Test & Measurement Class (USBTMC) Driver (Default for Linux)

    Advantges: Easy usage and installation for Linux system
    Disadvantages: Only available for USBTMC interfaces on Linux system, where
                   devices can be treated as file nodes


    Parameters
    ----------
    dev : str | None (default None)
        The location of usbtmc device

    Attributes
    ----------
    dev: str | None (default None)
        The location of usbtmc device
    dev_fd: int
        File descriptor of the device

    Returns
    -------

    """

    def __init__(self, dev=None, inst=True):
        if inst:
            self.__dev_init(dev)
            self.dev_fd = self.device_open()
            self.__info(dev_fd=self.dev_fd)

    def __dev_init(self, dev):
        """ Initialize the devices based on given device path

        Parameters
        ----------
        dev : str | None (default None)
            If None, then list all available USBTMC devices and select one
            If a string is given, then check its correctness

        Returns
        -------

        """

        if dev is None:
            # List all avaiable devices
            dev_path_dict = {i: i_dev for i, i_dev in enumerate(
                self.available_port_list())}
            print(dev_path_dict)

            # Retrieve the devices info
            for tmp_dev_id, tmp_dev_loc in dev_path_dict.items():
                tmp_dev_fd = self.device_open(tmp_dev_loc)
                tmp_msg = self.__info(dev_fd=tmp_dev_fd)
                print(f'Id: {tmp_dev_id}, Device info: {tmp_msg}')

            dev_id = input('Available devices are listed above and input ' +
                           'the corresponding id number to select the ' +
                           'desired device.\n')
            self.dev = dev_path_dict[int(dev_id)]
        else:
            assert os.path.exists(dev), 'Input device path does not exist, \
                please double-check your input of parameter dev'
            self.dev = dev

    def device_open(self, dev=None):
        """ Open the device node

        Parameters
        ----------
        dev : str | None (default None)
            If None, then list all available USBTMC devices and select one
            If a string is given, then check its correctness

        Attributes
        ----------
        dev: str | None (default None)
            The location of usbtmc device
        dev_fd: int
            File descriptor of the device

        Returns
        -------

        """
        if dev is None:
            dev = self.dev
        try:
            # Only read and write access are needed to open the device
            dev_fd = os.open(dev, os.O_RDWR)
        except OSError:
            print('run the script with sudo')
            # Check the current access of dev port and what is the current user
            self.port_access(dev)
            pwd = input('Please input the password for root accesss:\n')
            # For convenience, give all users with read and write permission,
            # the minimum permission should be 006
            os.system(f'echo {pwd} | sudo -S chmod 666 {dev}')
            dev_fd = os.open(dev, os.O_RDWR)
        finally:
            # Use os.fstat to detect file is opened or not
            dup_check = [os.fstat(i) == os.fstat(dev_fd) for i in range(
                dev_fd)]
            if any(dup_check):
                print('The device is already opened, use the first opened fd')
                dev_fd = dup_check.index(True)
            print(f'Device is opened with file descriptor {dev_fd}')

            return dev_fd

    def port_access(self, dev=None):
        # Check current access of given port/dev/address
        if dev is None:
            self.dev = dev
        access = os.stat(dev)
        print(f'\nThe current access permission is: {oct(access.st_mode)}')

    def available_port_list(self, port_root='/dev'):
        # List all available USBTMC devices that can be found under given root
        target_fd = os.popen(f'ls {port_root} |grep "usbtmc"')
        port_list = target_fd.readlines()
        # remove white space character '\n' and concatenate with port root
        port_list = [f'{port_root}/{x.strip()}' for x in port_list]
        return port_list

    def dev_list(self):
        dev_path_dict = {i: i_dev
                         for i, i_dev in enumerate(self.available_port_list())}

        # Retrieve the devices info
        dev_instance_list, dev_info_list = [], []
        for tmp_dev_id, tmp_dev_loc in dev_path_dict.items():
            tmp_dev_fd = self.device_open(tmp_dev_loc)
            tmp_msg = self.__info(dev_fd=tmp_dev_fd)
            info = f'Id: {tmp_dev_id}, Device info: {tmp_msg}'
            dev_instance_list.append(tmp_dev_loc)
            dev_info_list.append(info)

        return dev_info_list, dev_instance_list

    def set_cmd(self, scpi_command, dev_fd=None):
        # Low level I/O to send data stream to device
        if dev_fd is None:
            dev_fd = self.dev_fd
        assert type(scpi_command) == str, 'SCPI command MUST be written \
            in string'
        os.write(dev_fd, scpi_command.encode(encoding='utf8'))

    def read_cmd(self, length=100, dev_fd=None):
        # Low level I/O to receive data stream from to device
        if dev_fd is None:
            dev_fd = self.dev_fd
        return os.read(dev_fd, length)

    def query_cmd(self, cmd, length=100, dev_fd=None):
        self.set_cmd(cmd, dev_fd=dev_fd)
        # time.sleep(0.2)
        res = self.read_cmd(length=length, dev_fd=dev_fd)
        return res

    def __info(self, dev_fd=None):
        # Retrieve the device information
        self.set_cmd("*IDN?", dev_fd=dev_fd)
        return self.read_cmd(100, dev_fd=dev_fd)

    def reset(self):
        # Reset the device
        self.set_cmd('*RST;*CLS;*OPC?')
        time.sleep(2.0)
        self.read_cmd()
        print("Reset is done!")


class SignalGenerator():
    """Convert the python command into low level I/O command (SCPI) and use
    selected driver to communicate with the target hardware

    Parameters
    ----------
    dev : str | None (default None)
        The location of usbtmc device
    protocol : 'USBTMC' | 'VISA' | None (default None)
        The driver for communicate with target hardwares. If None, a default
        driver will be chosen based on the operating system.
        USBTMC - Linux, VISA - Windows/MacOS
    out_chn : 1 | 2 (default 1)
        Output channel to configure
    mode : 'sin' | 'sweep?'
        !!! should be checked one by one and filling in
    amp : float (default 0.5)
        Amplitude of signal in the unit of Volt

    Attributes
    ----------
    dev: str | None (default None)
        The location of usbtmc device
    dev_fd: int
        File descriptor of the device

    Returns
    -------

    """
    def __init__(self, dev='/dev/usbtmc1', protocol=None, out_chn=1,
                 mode='sin', amp=0.5):
        self.os_ver = platform.platform()
        if protocol is None:
            if 'Linux' in self.os_ver:
                protocol = 'USBTMC'
            elif 'Windows' in self.os_ver:
                protocol = 'VISA'
            else:
                raise ValueError('Unsupported Operating System')

        # Diamond inheritance
        if protocol == 'USBTMC':
            # use super to call base and to avoid call VISA
            # self.protocol = super()
            self.protocol = USBTMC(dev=dev)
        elif protocol == 'VISA':
            # use super to call base and to avoid call USBTMC
            # self.protocol = super(USBTMC, self)
            self.protocol = VISA(dev=dev)
        else:
            raise ValueError('Unsupported protocol.')
        # self.protocol.__init__(dev=dev)

        self.out_chn = out_chn

    def set_cmd(self, scpi_command, dev_fd=None):
        self.protocol.set_cmd(scpi_command=scpi_command, dev_fd=dev_fd)

    def read_cmd(self, length=100, dev_fd=None):
        self.protocol.read_cmd(length=length, dev_fd=dev_fd)

    def query_cmd(self, scpi_command, length=100, dev_fd=None):
        res = self.protocol.query_cmd(cmd=scpi_command, length=length,
                                      dev_fd=dev_fd)
        return res

    def chn_check(self, chn):
        # To ensure the output channel is not None
        if chn is None:
            chn = self.out_chn
        self.prefix = f':SOUR{chn}'
        return chn

    def status(self):
        # Get current configurations of both channels
        # For sine mode, the parameters are in the order of frequency,
        # amplitude, offset and phase
        for i in [1, 2]:
            self.set_cmd(':SOURce' + str(i) + ':APPLy?')
            time.sleep(0.2)
            print(f'CHN{str(i)}:')
            print(self.query_cmd())

    def para_set(self, para_dict, chn=None):
        # To conveniently configure multiple parameters in one python command
        chn = self.chn_check(chn)
        special_dict = {'offset': 'VOLT:OFFS',
                        'sin': ['APPL:SIN', '', '', '', ''],
                        'dc': 'APPL:DC 1,1,',
                        'noise': ['APPL:NOIS', '']}
        for key, val in para_dict.items():
            if key not in special_dict.keys():
                self.set_cmd(self.prefix + ':' + key[:4].upper() + ' ' +
                             str(val).upper())
            else:
                if type(special_dict[key]) == list:
                    suffix = ''
                    for i, j in zip(special_dict[key], val):
                        suffix += f'{i} {str(j).upper()},'
                    self.set_cmd(self.prefix + ':' + suffix[:-1])
                    print(self.prefix + ':' + suffix[:-1])
                else:
                    self.set_cmd(self.prefix + ':' + special_dict[key] + ' ' +
                                 str(val).upper())
            time.sleep(0.05)

    def on(self, chn=None):
        # Turn on the output channel
        chn = self.chn_check(chn)
        self.set_cmd(f':OUTPut{chn} ON')

    def off(self, chn=None):
        # Turn off the output channel
        chn = self.chn_check(chn)
        self.set_cmd(':OUTPut' + str(chn) + ' OFF')

    def _single_para_set(self, para='amp', value=None, query=False, chn=None):
        """ Configure the single paramter or get the current configuration

        Parameters
        ----------
        para : 'amp' | 'offset' | 'frequency' | 'phase' (default 'amp')
            Selected parameter to set or get
        value : float | None (default None)
            Value of amplitude to set
        query: bool (default False)
            If True, get the current value of parameter.
            If False, set the current value of parameter.
        chn : 1 | 2 (default 1)
            Output channel to configure

        """
        assert value is not None or query, 'When query is False, valid \
            value must be given'
        chn = self.chn_check(chn)

        para_dict = {'amp': ':VOLT',
                     'offset': ':VOLT:OFFS',
                     'frequency': ':FREQ',
                     'phase': ':PHAS',
                     }

        if query:
            print(self.query_cmd(f':SOUR{str(chn)}{para_dict[para]}?'))
        else:
            self.set_cmd(f':SOUR{str(chn)}{para_dict[para]} {str(value)}')

    def amp(self, value=None, query=False, chn=None):
        self._single_para_set(para='amp', value=value, query=query, chn=chn)

    def offset(self, value=None, query=False, chn=None):
        self._single_para_set(para='offset', value=value, query=query, chn=chn)

    def frequency(self, value=None, query=False, chn=None):
        self._single_para_set(para='frequency', value=value, query=query,
                              chn=chn)

    def phase(self, value=None, query=False, chn=None):
        self._single_para_set(para='phase', value=value, query=query, chn=chn)

    def arb_func(self, data, sps=None, chn=None):
        """ Output a predefined 1-D signal with arbitrary shape.

        Parameters
        ----------
        data : 1-D array
            Discretized float data points of the input signal within the
            range -2.5v to 2.5V
        sps: int
            Samples per seconds, i.e., the sampling rate of input signal
        chn : 1 | 2 (default 1)
            Output channel to configure

        Return
        ---------
        data : 1-D array
            The adjusted int data points which are sent to the interfaces

        """
        if sps is not None:
            self.sps = sps

        # 0 - 16383 : -2.5V - 2.5V
        chn = self.chn_check(chn)
        data = np.asarray(data)
        assert len(data.shape) == 1, 'The input data must be 1-D data array'

        if np.amin(data) < -2.5 or np.amax(data) > 2.5:
            raise ValueError('Input must be between -2.5V to 2.5V')
        data = (data + 2.5) * 16383 / 5
        data = data.astype('int')  # The data sent via SCPI must be INT
        n_data = len(data)
        self.set_cmd(':SOUR' + str(chn) + ':APPL:ARB ' + str(self.sps))
        time.sleep(0.1)
        self.set_cmd(':SOUR' + str(chn) +
                     ':DATA:POIN VOLATILE, ' + str(n_data))
        time.sleep(0.1)
        for ind in range(len(data)):
            data_str = ':SOUR' + str(chn) + \
                ':DATA:VALue VOLATILE,' + str(ind+1) + ', ' + str(data[ind])
            self.set_cmd(data_str)
            time.sleep(2/self.sps)

        return data

    def fade(self, amp=0.5, fade_dur=5, chn=1, step_per_sec=2, mode='fadein'):
        """ Control the fade in/out of the current signal

        Parameters
        ----------
        amp : float (default 0.5)
            When in mode 'fadein', it is the goal amplitude to reach
            When in mode 'fadeout', it is the amplitude to start fading out
        fade_dur : int or float (default 5)
            Duration of the fade in/out signal in seconds
        chn : 1 | 2 (default 1)
            Output channel to configure
        step_per_sec : int (default 2)
            The frequency of updating amplitude in one second.
            A larger number indicates a more frequent update and vice versa.
        mode : 'fadein' | 'fadeout' (default 'fadein')
            'fadein' indicates the amplitude of signal increases
            'fadeout' indicates the amplitude of signal decreases

        """

        sleep_dur = 1 / step_per_sec
        # 0.002V is the minimum input voltage of the authors' hardware setup
        # step list is the list of amplitudes to update
        step_list = np.linspace(0.002, amp, int(fade_dur*step_per_sec))
        if mode == 'fadein':
            self.fade_amp(0.002, chn=chn)
            for stim_val in step_list:
                time.sleep(sleep_dur)
                self.fade_amp(val=stim_val, chn=chn)
                print(stim_val)
        elif mode == 'fadeout':
            for stim_val in step_list[::-1]:
                self.fade_amp(val=stim_val, chn=chn)
                time.sleep(sleep_dur)
            print('off output')

    def fade_amp(self, val, chn, stim_mode='tACS'):
        """ Adjust the
        """
        if stim_mode == 'tACS':
            self.sig_gen.amp(value=val, chn=chn)
        elif stim_mode == 'tDCS':
            self.sig_gen.para_set({'offset': val}, chn=chn)
        elif stim_mode == 'tRNS':
            offset = self.offset_val_ch1 if chn == 1 else self.offset_val_ch2
            self.sig_gen.para_set({'noise': [val, offset]}, chn=chn)
