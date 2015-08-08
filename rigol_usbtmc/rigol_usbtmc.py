# -*- coding: utf-8 -*-
"""
Module providing USBTMC interface to the Rigol DS1000 series oscilloscope.

Provides convenient interfaces for frequency sweep operations.
"""
import usbtmc
from usb import USBError
import usb.util
import time
import numpy

class Scope(object):

    """ Class for Rigol oscilloscope. """

    VID = '1AB1'
    PID = '0588'

    def __init__(self):
        """Open a connection to the oscilloscope and create interfaces for both channels."""
        try:
            self.handle = usbtmc.Instrument(int(self.VID, 16), int(self.PID, 16))
            self.handle.timeout = 5000
        except USBError:
            devlist = usbtmc.list_devices()
            for dev in devlist:
                if dev.idProduct == int(self.PID, 16) and dev.idVendor == int(self.VID, 16):
                    dev.reset()
                    self.handle = usbtmc.Instrument(int(self.VID, 16), int(self.PID, 16))
                    break
            raise USBError('Unable to establish connection with oscilloscope.')

        print('Connected to Rigol oscilloscope as ' + repr(self.handle.device))
        self.ch1 = self.Channel(1, self)
        self.ch2 = self.Channel(2, self)

    def __del__(self):
        self.close()

    def close(self):
        """(Attempt to) explicitly release the interface claimed by this class on the device."""
        try:
            self.handle.device.reset()
        except USBError:
            pass
        
    def ask(self, command):
        """Send a command and read the subsequent response as a string."""
        return (self.handle.ask(command))

    def write(self, command):
        """Send a command."""
        self.handle.write(command)
        time.sleep(0.01)
        return

    def read(self, n=-1):
        """Read data from device as raw bytes."""
        data = self.handle.read_raw(n)
        return data

    @property
    def timemode(self):
        self._timemode = self.ask(':TIM:MODE?')
        return self._timemode

    @timemode.setter
    def timemode(self, tmode):
        val = str(tmode).upper()
        if val in ['MAIN', 'DELAYED']:
            self.write(':TIM:MODE {:s}'.format(val))
            self._timemode = self.timemode

    @property
    def timescale(self):
        self._timescale = float(self.ask(':TIM:SCAL?'))
        return self._timescale

    @timescale.setter
    def timescale(self, secondsPerDiv):
        self.write(':TIM:SCAL {:11.9f}'.format(secondsPerDiv))
        self._timescale = self.timescale

    @property
    def timeoffset(self):
        self._timeoffset = self.ask(':TIM:DEL?')
        return self._timeoffset

    @timeoffset.setter
    def timeoffset(self, delay):
        self.write(':TIM:DEL {:11.9f}'.format(delay))
        self._timeoffset = self._timeoffset

    def run(self):
        """Command the device to resume sampling."""
        self.write(':RUN')

    def auto(self):
        """Command the device to automatically select gain and frequency settings."""
        self.write(':AUTO')

    @property
    def keyslocked(self):
        """Query the key lock status.

        Locked is remote operation (indicated on the oscilloscope display by 'Rmt'.
        Unlocked allows control of the oscilloscope by the front panel keys.
        """
        self._keyslocked = [True if self.ask(':KEY:LOCK?') == 'ENAB' else False]
        return self._keyslocked

    @keyslocked.setter
    def keyslocked(self, lock):
        """Set the key lock status.

        Valid options arguments for `lock` are:
        'ENAB' (control over USB connection only)
        'DIS' (local control via oscilloscope front panel keys)
        """
        val = ['ENAB' if lock else 'DIS']
        self.write(':KEY:LOCK {:s}'.format(val))
        self._keyslocked = self.keyslocked

    @property
    def acquireMode(self):
        self._acquireMode = self.ask(':ACQ:MODE ?')
        return self._acquireMode

    @acquireMode.setter
    def acquireMode(self, mode):
        val = str(mode).upper()
        if val in ['NORM, AVER, PEAK']:
            self.write(':ACQ:MODE {:4s}'.format(val))
            self._acquireMode = self.acquireMode

    @property
    def averages(self):
        self._averages = int(self.ask(':ACQ:AVER?'))
        return self._averages

    @averages.setter
    def averages(self, n_averages):
        if n_averages in [2 ** p for p in range(1, 8)]:
            self.write(':ACQ:AVER {:d}'.format(n_averages))
            self._averages = self.averages

    @property
    def memDepth(self):
        self._memDepth = int(self.ask(':ACQ:MEM?'))
        return self._memDepth

    @memDepth.setter
    def memDepth(self, depth):
        val = str(depth).upper()
        if val in ['NORM', 'LONG']:
            self.write(':ACQ:MEM {:4s}'.format(val))
            self._memDepth = self.memDepth

    @property
    def time_data(self):
        time = np.arange(-300. / 50 * self._timescale,
                         300. / 50 * self._timescale,
                         self._timescale / 50)
        return time

    class Channel(object):
        """Create channel objects for channel specific queries."""
        def __init__(self, channel_number, parent):
            """

            :rtype : object
            """
            self.p = parent
            self.chn = channel_number

        # Channel settings
        @property
        def verticalOffset(self):
            self._verticalOffset = float(self.p.ask(':CHAN{:d}:OFFS?'.format(self.chn)))
            return self._verticalOffset

        @verticalOffset.setter
        def verticalOffset(self, volts):
            self.p.write(':CHAN{:d}:OFFS {:11.9f}'.format(self.chn, volts))
            self._verticalOffset = self.verticalOffset

        @property
        def verticalGain(self):
            self._verticalGain = float(self.p.ask(':CHAN{:d}:SCAL?'.format(self.chn)))
            return self._verticalGain

        @verticalGain.setter
        def verticalGain(self, voltsPerDiv):
            self.p.write(':CHAN{:d}:SCAL {:11.9f}'.format(self.chn, voltsPerDiv))
            self._verticalGain = self.verticalGain

        @property
        def data(self):
            self.p.write(':WAV:DATA? CHAN{:d}'.format(self.chn))
            raw_data = self.p.read()[10:]
            data = numpy.frombuffer(raw_data, 'B')
            return self.scale_data(data)

        @property
        def chMemDepth(self):
            self._chMemDepth = self.p.ask(':CHAN{:d}:MEM?'.format(self.chn))
            return self._chMemDepth

        @chMemDepth.setter
        def chMemDepth(self, depth):
            self.p.write(':CHAN{:d}:MEM {:d}'.format(self.chn, depth))
            self._chMemDepth = self.chMemDepth

        def scale_data(self, data):
            """ Recover physical quantities from scope digitization.
            Values taken from Cibo Mahto, www.cibomahto.com/2010/04/
            controlling-a-rigol-oscilloscope-using-linux-and-python"""
            vs = self.verticalGain
            vo = self.verticalOffset
            data = 255 - data  # Invert data
            data = (data - 130.0 - vo / vs * 25) / 25 * vs
            return data

        # Measurements
        def meas_Vpp(self):
            return float(self.p.ask(':MEAS:VPP? CHAN{:d}'.format(self.chn)))

        def meas_Vmax(self):
            return float(self.p.ask(':MEAS:VMAX? CHAN{:d}'.format(self.chn)))

        def meas_Vmin(self):
            return float(self.p.ask(':MEAS:VMIN? CHAN{:d}'.format(self.chn)))

        def meas_Vamp(self):
            return float(self.p.ask(':MEAS:VAMP? CHAN{:d}'.format(self.chn)))

        def meas_Vtop(self):
            return float(self.p.ask(':MEAS:VTOP? CHAN{:d}'.format(self.chn)))

        def meas_Vbase(self):
            return float(self.p.ask(':MEAS:VBAS? CHAN{:d}'.format(self.chn)))

        def meas_Vavg(self):
            return float(self.p.ask(':MEAS:VAV? CHAN{:d}'.format(self.chn)))

        def meas_Vrms(self):
            return float(self.p.ask(':MEAS:VRMS? CHAN{:d}'.format(self.chn)))

        def meas_over(self):
            return float(self.p.ask(':MEAS:OVER? CHAN{:d}'.format(self.chn)))

        def meas_pre(self):
            return float(self.p.ask(':MEAS:PRE? CHAN{:d}'.format(self.chn)))

        def meas_freq(self):
            return float(self.p.ask(':MEAS:FREQ? CHAN{:d}'.format(self.chn)))

        def meas_rise(self):
            return float(self.p.ask(':MEAS:RIS? CHAN{:d}'.format(self.chn)))

        def meas_fall(self):
            return float(self.p.ask(':MEAS:FALL? CHAN{:d}'.format(self.chn)))

        def meas_period(self):
            return float(self.p.ask(':MEAS:PER? CHAN{:d}'.format(self.chn)))

        def meas_posWidth(self):
            return float(self.p.ask(':MEAS:PWID? CHAN{:d}'.format(self.chn)))

        def meas_negWidth(self):
            return float(self.p.ask(':MEAS:NWID? CHAN{:d}'.format(self.chn)))

        def meas_posDuty(self):
            return float(self.p.ask(':MEAS:PDUT? CHAN{:d}'.format(self.chn)))

        def meas_negDuty(self):
            return float(self.p.ask(':MEAS:NDUT? CHAN{:d}'.format(self.chn)))

        def meas_posDelay(self):
            return float(self.p.ask(':MEAS:PDE? CHAN{:d}'.format(self.chn)))

        def meas_negDelay(self):
            return float(self.p.ask(':MEAS:NDE? CHAN{:d}'.format(self.chn)))
