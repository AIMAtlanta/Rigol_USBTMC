import numpy
import matplotlib.pyplot as plot
from rigol_usbtmc import rigol_usbtmc

def main():
    scope = rigol_usbtmc.Scope()
    scope.auto()
    scope.run()

    data = scope.ch1.data

    data_size = len(scope.ch1.data)

    # get metadata
    sample_rate = float(scope.ask(':ACQ:SAMP?'))
    timescale = float(scope.ask(":TIM:SCAL?"))
    timeoffset = float(scope.ask(":TIM:OFFS?"))
    voltscale = float(scope.ask(':CHAN1:SCAL?'))
    voltoffset = float(scope.ask(":CHAN1:OFFS?"))

    # show metadata
    print("Data size:      ", data_size)
    print("Sample rate:    ", sample_rate)
    print("Time scale:     ", timescale)
    print("Time offset:    ", timeoffset)
    print("Voltage offset: ", voltoffset)
    print("Voltage scale:  ", voltscale)

    # convert data from (inverted) bytes to an array of scaled floats
    # this magic from Matthew Mets
    data = data * -1 + 255
    data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale

    # creat array of matching timestamps
    time = numpy.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale,
                          num=len(data))

    # scale time series and label accordingly
    if (time[-1] < 1e-3):
        time = time * 1e6
        tUnit = "uS"
    elif (time[-1] < 1):
        time = time * 1e3
        tUnit = "mS"
    else:
        tUnit = "S"

    # Plot the data
    plot.plot(time, data)
    plot.title("Oscilloscope Channel 1")
    plot.ylabel("Voltage (V)")
    plot.xlabel("Time (" + tUnit + ")")
    plot.xlim(time[0], time[-1])
    plot.show()

if __name__ == '__main__':
    main()