# Rigol_USBTMC

A simple PyUSBTMC-based interface for the Rigol DS1102E Oscilloscope.

## Overview and Installation

This module provides a simple to use python interface developed
specifically for the Rigol DS1102E.  The chief feature of this module
is that it wraps the oscilloscope interface in a class, automatically
identifies the oscilloscope upon instantiation,  and simplifies calls
made by PyUSBTMC to methods of that class.

This module is based on PyUSB, and so in turn on
[libusb](http://www.libusb.org).  Because of this foundation, this
utility may be used on both Linux and Windows platforms with relative
ease.  On linux, the standard current branch of the libusb project may
be used (e.g. install with, `sudo apt-get install libusb-1.0-0`.)  On
Windows, a
[32-bit build of version 0.1](http://www.libusb.org/wiki/libusb-win32)
has been ported, allowing Windows users to make use of the utility
offered by PyUSB.

This utility makes use of the PyUSB and PyUSBTMC modules.  (These are
imported by slightly different names than their names in `pip`: PyUSB
(version 1.0.0b2 as of this document) is installed with
`pip install pyusb` but imported by `import usb`;  PyUSBTMC
(version 0.1dev15 as of this document) is installed with
`pip install pyusbtmc` but is imported by `import usbtmc`.)

This project has been developed to support the automated interaction of
the Rigol DS1102E and the Hantek 1025G DDS function generator, and as
such (as of 20150419), not all interfaces ofered by the Rigol 1102 have
been implemented in this module.  While other Rigol Oscilloscope models
are likely to be supported to varying degrees, such support has neither
been designed or verified.

This module was developed using Python 3.4.

## Basic usage

The rigol_usbtmc.py module must be on your python path.  This can be
accomplished either by having the module in your working directory, or
by adding the directory containing the module to your python path using
the sys module:

    import sys
    sys.path.append('/path/to/module/directory')

### Instantiation:

    import rigol_usbtmc
    scope = rigol_usbtmc.Scope()

### Measurement:
Sampling frequency is specified for the entire device, while voltage
sampling is specified per channel.  The channels are instances of
`Channel` classes, named `ch1` and `ch2`, belonging to the `Scope`
instance.

    # Specify a specific sampling frequency and voltage levels
    scope.timescale = 0.001  # seconds per division
    scope.ch1.verticalGain = 1  # Volts per division
    scope.ch1.verticalOffset = 0  # Offset in volts
    
    # or have the oscilloscope automatically detect the appropriate sampling parameters
    scope.ch1.auto()
    
    # Make a measurement
    scope.ch1.meas_Vpp()  # Measure the peak to peak voltage

### Implemented measurement methods:

* meas_Vpp()
* meas_Vmax()
* meas_Vmin()
* meas_Vamp()
* meas_Vtop()
* meas_Vbase()
* meas_Vavg()
* meas_Vrms()
* meas_over()
* meas_pre()
* meas_freq()
* meas_rise()
* meas_fall()
* meas_period()
* meas_posWidth()
* meas_negWidth()
* meas_posDuty()
* meas_negDuty()
* meas_posDelay()
* meas_negDelay()

## License
The MIT License (MIT)

Copyright (c) 2015, Atlanta Instrumentation and Measurement, LLC

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Author
Kevin D. Nielson (2015.04.19)

[AIM - Atlanta Instrumentation and Measurement, LLC](http://www.aimatlanta.com)
