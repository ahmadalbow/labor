import pyvisa
from enum import Enum

# A class representing the DMM6500 instrument.
class DMM6500:
    # Initialize the VISA resource manager as a class-level attribute.
    rm = pyvisa.ResourceManager()

    def __init__(self, ipaddress):
        # Open a VISA resource using the instrument's IP address.
        self.inst = self.rm.open_resource(f'TCPIP::{ipaddress}::INSTR')
        self.ranges = {}

    # Method to measure a specified function and return the result as a float.
    def measure(self, function, bufferName='defbuffer1'):
        return float(self.inst.query(f'MEAS:{function.value}? "{bufferName}"'))

    # Method to send a query command to the instrument.
    def query(self, command):
        self.inst.query(command)

    # Method to send a write command to the instrument.
    def write(self, command):
        self.inst.write(command)

    # Method to reset the trigger configuration to continuous mode.
    def reset_trigger(self):
        self.inst.write("TRIG:CONT REST")

    # Method to set up the initial configuration of the DMM6500.
    def startup(self):
        for func in list(Function_With_Range):
            self.ranges[func.name] = 'AUTO'
            self.write(f'SENS:{func.value}:RANG:AUTO ON')

    # Method to set the range for a specific measurement function.
    def set_Range(self, function, value):
        if function.name in [e.name for e in list(Function_With_Range)]:
            if value in ['auto', 'AUTO', 'Auto']:
                self.write(f'SENS:{function.value}:RANG:AUTO ON')
                self.ranges[function.name] = 'AUTO'
                return
            elif (
                (function.name == 'VOLTDC' and value in [0.1, 1, 10, 100, 1000])
                or (function.name == 'VOLTAC' and value in [0.1, 1, 10, 100, 750])
                or (function.name == 'CURRDC' and value in [0.00001, 0.0001, 0.001, 0.01, 0.1, 1])
                or (function.name == 'CURRAC' and value in [0.0001, 0.001, 0.01, 0.1, 1, 3])
                or (function.name == 'RES' and value in [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000])
                or (function.name == 'CAPACITANCE' and value in [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4])
            ):
                self.write(f'{function.value}:RANGE {value}')
            else:
                print('Incorrect function or range entered')
                return
            self.ranges[function.name] = value

    # Method to get the range setting for a specific measurement function.
    def get_range(self, function):
        if function.name in [e.name for e in list(Function_With_Range)]:
            return self.ranges[function.name]
        return 'This function has no range'

# Enumeration for supported measurement functions.
class Function(Enum):
    VOLTDC = 'VOLT'
    VOLTAC = 'VOLT:AC'
    CURRDC = 'CURR'
    CURRAC = 'CURR:AC'
    RES = 'RES'
    FRES = 'FRES'
    DIOD = 'DIOD'
    CAPACITANCE = 'CAPacitance'
    TEMP = 'TEMP'
    CONT = 'CONT'
    FREQ = 'FREQ'
    PERIOD = 'PERIOD'

# Enumeration for supported measurement functions with range settings.
class Function_With_Range(Enum):
    VOLTDC = 'VOLT'
    VOLTAC = 'VOLT:AC'
    CURRDC = 'CURR'
    CURRAC = 'CURR:AC'
    RES = 'RES'
    CAPACITANCE = 'CAPacitance'
