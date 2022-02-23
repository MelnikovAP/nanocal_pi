from daq_params import DaqParams

import uldaq as ul


class DaqDeviceHandler:
    def __init__(self, params: DaqParams):
        self._params = params

        devices = ul.get_daq_device_inventory(self._params.interface_type)
        devices_count = len(devices)
        if not devices_count:
            raise RuntimeError("Error. No DAQ devices found.")

        # by default connecting only to one DAQBoard with index 0
        self._daq_device = ul.DaqDevice(devices[0]) 

    def descriptor(self) -> ul.DaqDeviceDescriptor:
        return self._daq_device.get_descriptor()

    def is_connected(self):
        return self._daq_device.is_connected()

    def connect(self):
        descriptor = self.descriptor()
        print("Connecting to {} - please wait...".format(descriptor.dev_string))
        # For Ethernet devices using a connection_code other than the default
        # value of zero, change the line below to enter the desired code.
        self._daq_device.connect(connection_code=self._params.connection_code)

    def disconnect(self):
        return self._daq_device.disconnect()

    def release(self):
        return self._daq_device.release()

    def get(self):
        return self._daq_device

    def get_ai_device(self):
        return self._daq_device.get_ai_device()

    def get_ao_device(self):
        return self._daq_device.get_ao_device()