
import os
import sys
import time
import platform
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import tkinter.font as tkFont
from tkinter import (Label, Entry, Button, Checkbutton, OptionMenu,
                     StringVar, messagebox, simpledialog)

from pytes.signal_generator import SignalGenerator as SG

matplotlib.use('TkAgg')


class PyTESWindow():
    def __init__(self, window, fontsize=20):

        is_conda = os.path.exists(os.path.join(sys.prefix, 'conda-meta'))
        if is_conda:
            messagebox.showwarning('Warning', 'The font of GUI cannot be \
                                   rendered by Anaconda Python. For better \
                                   visulization, please use other version \
                                   of Python')
        self.window = window
        self.dev_available = False

        self.window_geometry()
        self.fontStyle = tkFont.Font(family="Lucida Grande",
                                     size=self.fontsize)
        self.button_place()
        self.wave_display()
        self.window.mainloop()

    def button_place(self):
        # Allocating the spaces for the GUI widgets based on the grid
        self.fig_root = os.path.dirname(os.path.abspath(__file__))

        im_on = f'{self.fig_root}/Figures/button_on.png'
        im_off = f'{self.fig_root}/Figures/button_off.png'
        im_update = f'{self.fig_root}/Figures/button_update.png'
        im_refresh = f'{self.fig_root}/Figures/button_refresh.png'
        im_connect = f'{self.fig_root}/Figures/button_connect.png'
        self.window.fig_on = tk.PhotoImage(file=im_on).subsample(3)
        self.window.fig_off = tk.PhotoImage(file=im_off).subsample(3)
        self.window.fig_update = tk.PhotoImage(file=im_update).subsample(3)
        self.window.fig_refresh = tk.PhotoImage(file=im_refresh).subsample(3)
        self.window.fig_connect = tk.PhotoImage(file=im_connect).subsample(3)

        """
        Data type of element in the mat - Type of the widgets
        None  - Empty
        Dict  - Checkbutton
        Str   - Label
        List  - Option Menu
        Tuple - Clickable Button
        Int/Float - Entry of value
        """
        self.para_widgets_mat = np.asarray(
            [[{'VISA': self.dev_list}, {'USBTMC': self.dev_list}, None,
              'CH1', 'CH2'],
             ['Device List', [''], 'Stimulation Type',
              ['tACS', 'tDCS', 'tRNS', 'Arb'],
              ['tACS', 'tDCS', 'tRNS', 'Arb']],
             [(self.window.fig_connect, lambda: self.dev_connect()), None,
              'Arbitrary Data', 0, 0],
             [None, None, 'Voltage', 1, 1],
             [None, None, 'Frequency', 10, 10],
             [None, None, 'Phase', 0, 0],
             [None, None, 'Offset', 0, 0],
             [None, None, 'Fade In/Out', 5, 5],
             [None, None, 'Stim. Duration', 5, 5],
             [(self.window.fig_update, self.para_update),
              (self.window.fig_refresh, self.refresh),
              'Output',
              (self.window.fig_off, lambda: self.signal_out(chn=1), 'bt_out'),
              (self.window.fig_off, lambda: self.signal_out(chn=2), 'bt_out')],
             [None, None, 'Timer', '', '']],
            dtype='object')

        # Images for the labels
        self.para_label = {'Device List': 'label_ch1.png',
                           'CH1': 'label_ch1.png',
                           'CH2': 'label_ch2.png',
                           'Arbitrary Data': 'label_stim_type.png',
                           'Stimulation Type': 'label_stim_type.png',
                           'Voltage': 'label_amp.png',
                           'Frequency': 'label_freq.png',
                           'Phase': 'label_phase.png',
                           'Offset': 'label_offset.png',
                           'Fade In/Out': 'label_fade_dur.png',
                           'Stim. Duration': 'label_stim_dur.png',
                           'Output': 'label_output.png',
                           'Timer': 'label_output.png',
                           }
        self.para_widgets_mat_obj = np.empty(self.para_widgets_mat.shape,
                                             dtype='object')

        self.entry_row_start, self.entry_col_start = 2, 3
        row_start, col_start = 0, 0
        self.click_list, self.bt_out, self.check_list = [], [], []
        for (row, col), grid_val in np.ndenumerate(self.para_widgets_mat):
            if grid_val is None:
                # None value means no button neither entry
                continue
            grid_type = type(grid_val)
            if grid_type == int or grid_type == float:
                tmp_obj = Entry(self.window, font=self.fontStyle)
                tmp_obj.insert(0, str(grid_val))
                tmp_obj.grid(row=row+row_start, column=col+col_start)
            elif grid_type == str:
                tmp_obj = Label(self.window, font=self.fontStyle)
                tmp_obj = Label(self.window, text=grid_val,
                                font=self.fontStyle, bg="white")
                tmp_obj.grid(row=row+row_start, column=col+col_start)
            elif grid_type == list:
                tmp_click = StringVar()
                tmp_click.set(grid_val[0])
                tmp_stim_menu = OptionMenu(self.window, tmp_click, *grid_val,
                                           command=self.entry_state_update)
                tmp_stim_menu.grid(row=row+row_start, column=col+col_start,
                                   ipadx=90, sticky='ew')
                tmp_stim_menu.configure(font=self.fontStyle)

                tmp_menu_opt = self.window.nametowidget(tmp_stim_menu.menuname)
                tmp_menu_opt.config(font=self.fontStyle)
                tmp_obj = [tmp_stim_menu, tmp_menu_opt]
                if 'tACS' in grid_val:
                    self.click_list.append(tmp_click)
                else:
                    self.dev_click = tmp_click
                del tmp_click
            elif grid_type == tuple:
                tmp_obj = Button(self.window, image=grid_val[0], bg="white",
                                 command=grid_val[1])
                tmp_obj.image = grid_val[0]
                tmp_obj.grid(row=row+row_start, column=col+col_start)
                if len(grid_val) == 3:
                    self.bt_out.append(tmp_obj)
            elif grid_type == dict:
                tmp_check = tk.IntVar()
                tmp_obj = Checkbutton(self.window, variable=tmp_check,
                                      text=list(grid_val.keys())[0], onvalue=1,
                                      offvalue=0, bg="white",
                                      command=list(grid_val.values())[0],
                                      font=self.fontStyle)
                tmp_obj.grid(row=row+row_start, column=col+col_start)
                self.check_list.append(tmp_check)
            else:
                raise ValueError('Unsupported Variable Value')

            self.para_widgets_mat_obj[row, col] = tmp_obj
            del tmp_obj

    def entry_state_update(self, event):
        """Update the status of each entry

        Note:
        After selecting the stimualtion mode in the option menu, certain
        entries will be activated or deactivated. E.g., in tDCS mode, the entry
        for frequency is deactivated because a direct current signal has no
        frequency.
        """
        for id_click, click in enumerate(self.click_list):
            click_val = click.get()

            if click_val == 'tACS':
                state_list = ['disable', 'normal', 'normal', 'normal',
                              'normal', 'normal', 'normal', 'normal']
            elif click_val == 'tDCS':
                state_list = ['disable', 'normal', 'disable', 'disable',
                              'disable', 'normal', 'normal', 'normal']
            elif click_val == 'tRNS':
                state_list = ['disable', 'normal', 'disable', 'disable',
                              'normal', 'normal', 'normal', 'normal']
            elif click_val == 'Arb':
                state_list = ['normal', 'disable', 'disable', 'disable',
                              'disable', 'disable', 'disable', 'normal']
            for id_entry, entry_state in enumerate(state_list):
                self.para_widgets_mat_obj[
                    id_entry+self.entry_row_start,
                    id_click+self.entry_col_start].config(state=entry_state)

    def dev_list(self):
        """Display the list of clickable devices corresponding to chosen driver

        """
        visa_status = self.check_list[0].get()
        usbtmc_status = self.check_list[1].get()
        self.os_ver = platform.platform()
        if 'Windows' in self.os_ver and usbtmc_status:
            messagebox.showerror(title='Warning', message='USBTMC protocol' +
                                 ' is not available on Windows system. Use ' +
                                 'the default VISA protocol')
            # click yes in msg box, should toggle a button which disable usbtmc
            usbtmc_status = 0

        if visa_status and usbtmc_status:
            messagebox.showwarning(
                title='Warning', message='Please select only one protocol!')
            return None
        elif not visa_status and usbtmc_status:
            from signal_generator import USBTMC

            tmp = USBTMC(inst=False)
            for i, i_dev in enumerate(tmp.available_port_list()):
                try:
                    _ = os.open(i_dev, os.O_RDWR)
                except OSError:
                    pwd = simpledialog.askstring(
                        title="Test",
                        prompt='Enter your root pwd to change port access')
                    os.system(f'echo {pwd} | sudo -S chmod 666 {i_dev}')

            self.all_devices, self.dev_inst_list = \
                USBTMC(inst=False).dev_list()
            self.protocol = 'USBTMC'
        elif visa_status and not usbtmc_status:
            from signal_generator import VISA
            try:
                self.all_devices, self.dev_inst_list = VISA(inst=False).dev_list()
            except ModuleNotFoundError:
                messagebox.showerror(title='Error', message='VISA driver is \
                                     not available. Check installation of \
                                     pyvisa')
            self.protocol = 'VISA'
        else:
            return None

        self.dev_click.set('')
        menu = self.para_widgets_mat_obj[1, 1][0]['menu']
        menu.delete(0, 'end')
        for choice in self.all_devices:
            menu.add_command(label=choice,
                             command=tk._setit(self.dev_click, choice))

        self.refresh()

    def dev_connect(self):
        """Try to connect the selected devices

        """
        click_val = self.dev_click.get()
        if click_val == '':
            messagebox.showwarning('Warning', 'No selected device! \
                                   Please try another driver or check the' +
                                   ' connection')
        else:
            ind_ = self.all_devices.index(click_val)

            dev = self.dev_inst_list[ind_]
            if dev is None:
                messagebox.showwarning('Warning', 'No available devices!')
            print(ind_)
            try:
                self.sig_gen = SG(dev=dev, protocol=self.protocol)
                self.dev_available = True
                messagebox.showinfo('Connection Status', 'Connection succeeded!')
            except Exception as e:
                self.dev_available = False
                messagebox.showinfo('Connection Status', f'Connection failed!\n{e}')

    def wave_display(self):
        """Plot the signal in the left panel based on the input entries of
        the right panels

        E.g., if stimulation is chosen as tACS for Channel 1, the corresponding
        plots for CH1 will show a sinusoid curve based on input frequency,
        amplitude, offset and phase.

        """
        self.fig, self.ax = plt.subplots(2, 1, facecolor=(1, 1, 1))
        self.curve_color_list = ['xkcd:yellow green', 'xkcd:sky blue']
        self.title_list = ['CH1', 'CH2']

        self.ax[0].set_title('CH1')
        self.ax[0].set_facecolor('xkcd:black')
        self.ax[0].grid(True)
        self.ax[0].set_xlabel('Time/sec')
        self.ax[0].set_ylabel('Voltage/V')

        self.ax[1].set_title('CH2')
        self.ax[1].set_facecolor('xkcd:black')
        self.ax[1].grid(True)
        self.ax[1].set_xlabel('Time/sec')
        self.ax[1].set_ylabel('Voltage/V')

        plt.ion()
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(np.pi*t)
        self.ax[0].plot(t, s)
        self.fig.tight_layout()

        canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        plot_widget = canvas.get_tk_widget()

        def update():
            s = np.cos(np.pi*t)
            self.ax[0].plot(t, s, color='xkcd:yellow green')
            self.ax[1].plot(t, s, color='xkcd:sky blue')
            self.fig.tight_layout()
            self.fig.canvas.draw()

        plot_widget.grid(row=3, column=0, rowspan=6, columnspan=2,
                         sticky='nsew')

    def ax_plt(self, xs, ys, chn):

        self.ax[chn-1].clear()
        self.ax[chn-1].plot(xs, ys, color=self.curve_color_list[chn-1])
        self.ax[chn-1].set_title(self.title_list[chn-1])
        self.ax[chn-1].set_facecolor('xkcd:black')
        self.ax[chn-1].grid(True)
        self.ax[chn-1].set_xlabel('Time/sec')
        self.ax[chn-1].set_ylabel('Voltage/V')
        self.fig.tight_layout()
        self.fig.canvas.draw()

    def para_update(self):
        """Update the plots of the left panel based on the current parameters
        of the right panel

        """
        for id_click, click in enumerate(self.click_list):
            click_val = click.get()
            if click_val == 'tACS':
                self.sin_update(chn=id_click+1)
            elif click_val == 'tDCS':
                self.dc_update(chn=id_click+1)
            elif click_val == 'tRNS':
                self.noise_update(chn=id_click+1)
            elif click_val == 'Arb':
                self.arb_update(chn=id_click+1)

    def load_entry(self):
        """Load the current values for all entries on the right panel

        """
        def customize_float(string_val):
            try:
                return float(string_val)
            except ValueError:
                return string_val

        # arb, amp, freq, phase, offset, fade, stim dur
        self.entry_data = np.empty((7, 2), dtype='object')
        for (i, j), _ in np.ndenumerate(self.entry_data):
            self.entry_data[i, j] = customize_float(
                self.para_widgets_mat_obj[i+self.entry_row_start,
                                          j+self.entry_col_start].get())

    def sin_update(self, chn):
        self.load_entry()
        amp, freq, phase, offset = self.entry_data[1:5, chn-1]

        t = np.arange(0.0, 1.0, 0.001)
        ch_signal = offset + amp * np.sin(2*np.pi*freq*t + phase / 180 * np.pi)
        self.ax_plt(t, ch_signal, chn)

        self.scpi_cmd_ch = {'sin': [freq, amp, offset, phase]}
        if self.dev_available:
            self.sig_gen.para_set(self.scpi_cmd_ch, chn=chn)

    def dc_update(self, chn):
        self.load_entry()
        amp = self.entry_data[1, chn-1]

        t = np.arange(0.0, 1.0, 0.001)
        ch_signal = amp * np.ones(t.shape)

        self.ax_plt(t, ch_signal, chn)
        self.scpi_cmd_ch = {'dc': amp}

        if self.dev_available:
            self.sig_gen.para_set(self.scpi_cmd_ch, chn=chn)

    def noise_update(self, chn):
        self.load_entry()
        amp, offset = self.entry_data[[1, 4], chn-1]

        t = np.arange(0.0, 1.0, 0.001)
        ch_signal = np.random.normal(loc=offset, scale=amp, size=t.shape)

        self.ax_plt(t, ch_signal, chn)
        self.scpi_cmd_ch = {'noise': [amp, offset]}

        if self.dev_available:
            self.sig_gen.para_set(self.scpi_cmd_ch, chn=chn)

    def arb_update(self, chn):
        # read file
        import pickle
        self.load_entry()
        arb_data_path = self.entry_data[0, chn-1]
        with open(arb_data_path, 'rb') as f:
            arb_data = pickle.load(f)

        len_data = len(arb_data['data'])
        t = np.linspace(0.0, len_data/arb_data['sps'], len_data)
        self.ax_plt(t, arb_data['data'], chn)

        if self.dev_available:
            self.sig_gen.sps = arb_data['sps']
            self.sig_gen.arb_func(data=arb_data['data'], chn=chn,
                                  sps=arb_data['sps'])

    def signal_out(self, chn):
        """Control the output of the stimulation signal and switch the status
        button accordingly.

        In addition, once the output is turned on and a stimulation timer is
        set, a counting down window will indicate the residual stimulation time

        """
        self.load_entry()
        self.para_update()

        def state_switch(button, channel, forced=None):
            if forced is None:
                if button["state"] == "normal":
                    button["state"] = "active"
                    if self.dev_available:
                        self.sig_gen.on(chn=channel)
                    button.configure(image=self.window.fig_on)
                    # vlabel.configure(image=self.window.photo1)
                    # print('active')
                else:
                    button["state"] = "normal"
                    if self.dev_available:
                        self.sig_gen.off(chn=channel)
                    button.configure(image=self.window.fig_off)
                    # vlabel.configure(image=self.window.photo)
                    # print('normal')
            elif forced == 'on':
                if self.dev_available:
                    self.sig_gen.on(chn=channel)
                button.configure(image=self.window.fig_on)
                button["state"] = "active"
                time.sleep(0.1)
            elif forced == 'off':
                if self.dev_available:
                    self.sig_gen.off(chn=channel)
                button.configure(image=self.window.fig_off)
                button["state"] = "normal"
                time.sleep(0.1)
            self.window.update()

        def amp_adjust(val, chn):
            click_list = self.click_list.copy()
            click = click_list[chn-1]
            click_val = click.get()

            if self.dev_available:
                if click_val == 'tACS':
                    self.sig_gen.amp(value=val, chn=chn)
                elif click_val == 'tDCS':
                    self.sig_gen.para_set({'offset': val}, chn=chn)
                elif click_val == 'tRNS':
                    if chn == 1:
                        offset = self.offset_val_ch1
                    else:
                        offset = self.offset_val_ch2
                    self.sig_gen.para_set({'noise': [val, offset]}, chn=chn)

        def fade(amp, fade_dur, chn, step_per_sec=2, status='start'):
            print('fade start')
            sleep_dur = 1 / step_per_sec
            step_list = np.linspace(0.002, amp, int(fade_dur*step_per_sec))
            if status == 'start':
                # self.sig_gen.amp(0.002, chn=chn)
                amp_adjust(0.002, chn=chn)
                for stim_val in step_list:
                    time.sleep(sleep_dur)
                    amp_adjust(val=stim_val, chn=chn)
                    print(stim_val)
            elif status == 'finish':
                for stim_val in step_list[::-1]:
                    amp_adjust(val=stim_val, chn=chn)
                    # self.sig_gen.amp(stim_val, chn=chn)
                    time.sleep(sleep_dur)
                print('off output')

            print('fade end')

        def stim_timer(chn, duration):
            print('Timer start')
            # Note: tried to use self.window.after, but it does not work as
            # after is a callback function and cannot block the thread
            while duration > 0:
                duration -= 1
                self.para_widgets_mat_obj[
                    10, chn+self.entry_col_start-1]['text'] = duration
                self.window.update()
                time.sleep(1)
            print('Timer end')

        amp, fade_dur, stim_dur = self.entry_data[[1, -2, -1], chn-1]
        button_out = self.bt_out[chn-1]

        if stim_dur == '' and fade_dur == '':
            # No fade in/out nor limited stimulation duration,
            # Indefinitely switch the output status
            state_switch(button_out, channel=chn)
        elif fade_dur != '':
            # Valid input for fade duration
            assert stim_dur != '', 'When fade is non-empty, duration also \
                must be non-empty. Otherwise, the fade out will start right \
                after the fade in done'
            state_switch(button_out, channel=chn, forced='on')
            fade(amp=amp, chn=chn, status='start', fade_dur=float(fade_dur))
            stim_timer(chn=chn, duration=float(stim_dur))
            fade(amp=amp, chn=chn, status='finish', fade_dur=float(fade_dur))
            state_switch(button_out, channel=chn, forced='off')
        else:
            # No fade in/out but has limited stimulation duration
            state_switch(button_out, channel=chn, forced='on')
            stim_timer(chn=chn, duration=float(stim_dur))
            state_switch(button_out, channel=chn, forced='off')

    def refresh(self):
        self.para_widgets_mat_obj[1, 1][0].config(width=2)
        self.window_ratio()
        self.window.update()

    # The three functions below are about properly setting up the toolbox
    # window based on the current monitor.

    def window_ratio(self):
        for id_row, row in enumerate([1]*7):
            self.window.grid_rowconfigure(id_row, weight=row)
        for id_col, col in enumerate([2, 2, 2, 2, 2]):
            self.window.grid_columnconfigure(id_col, weight=col)

    def window_geometry(self):
        self.window_ratio()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self. window.winfo_screenheight()

        ratio = (screen_width*9) / (screen_height*16)
        self.window_width = screen_width * .5 / ratio
        self.window_height = screen_height * .5
        self.window_start_x = screen_width * .2
        self.window_start_y = screen_height * .2
        window.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height,
                                         self.window_start_x,
                                         self.window_start_y))
        self.window.configure(bg=self._from_rgb((255, 255, 255)))

        self.fontsize = np.amin([self.window_width/80,
                                 self.window_height/80]).astype(int)

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb


window = tk.Tk()
window.title('PyTES Toolbox')
mywin = PyTESWindow(window)
