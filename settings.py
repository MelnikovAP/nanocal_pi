import json

from daq_device import DaqParams
from ai_device import AiParams
from ao_device import AoParams
from utils import is_int_or_raise, list_bitwise_or
from constants import *


class Settings:
    """Reads a JSON configuration file."""

    def __init__(self, path: str):
        """Initializes dictionary.

        Args:
            path: A string path to JSON file.

        Raises:
            ValueError if file doesn't exist or has invalid extension or is empty.
        """
        self._json = dict()
        if not os.path.exists(path):
            raise ValueError("Settings file doesn't exist.")
        if not os.path.splitext(path)[-1] != JSON_EXTENSION:
            raise ValueError("Settings file doesn't have '{}' extension.".format(JSON_EXTENSION))
        with open(path, 'r') as f:
            self._json = json.load(f)
        if not self._json:
            raise ValueError("Empty settings file defined.")

    def json(self):
        """Provides access to the read dictionary."""
        return self._json


class SettingsParser:
    """Parses configuration file with all necessary acquisition parameters."""

    def __init__(self, path: str):
        """Initializes dictionary and checks that all needed fields exist.

        After correct parsing it is possible to obtain DaqParams, AiParams and AoParams.

        Args:
            path: A string path to JSON file.

        Raises:
            ValueError if any field doesn't exist.
        """
        json_dict = Settings(path).json()
        if SETTINGS_FIELD not in json_dict:
            raise ValueError("No '{}' field found in the settings file.".format(SETTINGS_FIELD))
        else:
            self._settings_dict = json_dict[SETTINGS_FIELD]
            for field in [DAQ_FIELD, AI_FIELD, AO_FIELD]:
                if field not in self._settings_dict:
                    raise ValueError("No '{}' field found in the settings file.".format(field))

        self._invalid_fields = []
        # only in that order
        self._parse_daq_params()
        self._parse_ai_params()
        self._parse_ao_params()
        self._check_invalid_fields()

    def get_daq_params(self) -> DaqParams:
        """Provides explicit access to the read DaqParams."""
        return self._daq_params

    def get_ai_params(self) -> AiParams:
        """Provides explicit access to the read AiParams."""
        return self._ai_params

    def get_ao_params(self) -> AoParams:
        """Provides explicit access to the read AoParams."""
        return self._ao_params

    def _parse_daq_params(self):
        """Parses all necessary DAQ parameters and fills DaqParams instance."""
        self._daq_params = DaqParams()
        daq_dict = self._settings_dict[DAQ_FIELD]

        if INTERFACE_TYPE_FIELD in daq_dict:
            interface_types = daq_dict[INTERFACE_TYPE_FIELD]
            if isinstance(interface_types, list):
                self._daq_params.interface_type = list_bitwise_or(interface_types)
            elif is_int_or_raise(interface_types):
                self._daq_params.interface_type = int(interface_types)
        else:
            self._invalid_fields.append(INTERFACE_TYPE_FIELD)

        if CONNECTION_CODE_FIELD in daq_dict:
            connection_code = daq_dict[CONNECTION_CODE_FIELD]
            if is_int_or_raise(connection_code):
                self._daq_params.connection_code = int(connection_code)
        else:
            self._invalid_fields.append(CONNECTION_CODE_FIELD)

    def _parse_ai_params(self):
        """Parses all necessary analog-input parameters and fills AiParams instance."""
        self._ai_params = AiParams()
        ai_dict = self._settings_dict[AI_FIELD]

        if SAMPLE_RATE_FIELD in ai_dict:
            sample_rate = ai_dict[SAMPLE_RATE_FIELD]
            if is_int_or_raise(sample_rate):
                self._ai_params.sample_rate = min(int(sample_rate), MAX_SCAN_SAMPLE_RATE)
        else:
            self._invalid_fields.append(SAMPLE_RATE_FIELD)

        if RANGE_ID_FIELD in ai_dict:
            range_id = ai_dict[RANGE_ID_FIELD]
            if is_int_or_raise(range_id):
                self._ai_params.range_id = int(range_id)
        else:
            self._invalid_fields.append(RANGE_ID_FIELD)

        if LOW_CHANNEL_FIELD in ai_dict:
            low_channel = ai_dict[LOW_CHANNEL_FIELD]
            if is_int_or_raise(low_channel):
                self._ai_params.low_channel = int(low_channel)
        else:
            self._invalid_fields.append(LOW_CHANNEL_FIELD)

        if HIGH_CHANNEL_FIELD in ai_dict:
            high_channel = ai_dict[HIGH_CHANNEL_FIELD]
            if is_int_or_raise(high_channel):
                self._ai_params.high_channel = int(high_channel)
        else:
            self._invalid_fields.append(HIGH_CHANNEL_FIELD)

        if INPUT_MODE_FIELD in ai_dict:
            input_mode = ai_dict[INPUT_MODE_FIELD]
            if is_int_or_raise(input_mode):
                self._ai_params.input_mode = int(input_mode)
        else:
            self._invalid_fields.append(INPUT_MODE_FIELD)

        if SCAN_FLAGS_FIELD in ai_dict:
            scan_flags = ai_dict[SCAN_FLAGS_FIELD]
            if isinstance(scan_flags, list):
                self._ai_params.scan_flags = list_bitwise_or(scan_flags)
            elif is_int_or_raise(scan_flags):
                self._ai_params.scan_flags = int(scan_flags)
        else:
            self._invalid_fields.append(SCAN_FLAGS_FIELD)

    def _parse_ao_params(self):
        """Parses all necessary analog-output parameters and fills AoParams instance."""
        self._ao_params = AoParams()
        ao_dict = self._settings_dict[AO_FIELD]

        if SAMPLE_RATE_FIELD in ao_dict:
            sample_rate = ao_dict[SAMPLE_RATE_FIELD]
            if is_int_or_raise(sample_rate):
                self._ao_params.sample_rate = min(int(sample_rate), MAX_SCAN_SAMPLE_RATE)
        else:
            self._invalid_fields.append(SAMPLE_RATE_FIELD)
            
        if RANGE_ID_FIELD in ao_dict:
            range_id = ao_dict[RANGE_ID_FIELD]
            if is_int_or_raise(range_id):
                self._ao_params.range_id = int(range_id)
        else:
            self._invalid_fields.append(RANGE_ID_FIELD)

        if LOW_CHANNEL_FIELD in ao_dict:
            low_channel = ao_dict[LOW_CHANNEL_FIELD]
            if is_int_or_raise(low_channel):
                self._ao_params.low_channel = int(low_channel)
        else:
            self._invalid_fields.append(LOW_CHANNEL_FIELD)

        if HIGH_CHANNEL_FIELD in ao_dict:
            high_channel = ao_dict[HIGH_CHANNEL_FIELD]
            if is_int_or_raise(high_channel):
                self._ao_params.high_channel = int(high_channel)
        else:
            self._invalid_fields.append(HIGH_CHANNEL_FIELD)

        if SCAN_FLAGS_FIELD in ao_dict:
            scan_flags = ao_dict[SCAN_FLAGS_FIELD]
            if isinstance(scan_flags, list):
                self._ao_params.scan_flags = list_bitwise_or(scan_flags)
            elif is_int_or_raise(scan_flags):
                self._ao_params.scan_flags = int(scan_flags)
        else:
            self._invalid_fields.append(SCAN_FLAGS_FIELD)

    def _check_invalid_fields(self):
        """Raises ValueError if at least one required field is missing in the settings."""
        if self._invalid_fields:
            invalid_fields_str = ", ".join(self._invalid_fields)
            raise ValueError("No fields found in the settings file: {}.".format(invalid_fields_str))


if __name__ == '__main__':
    try:
        _path = "./settings.json"
        parser = SettingsParser(_path)

        _daq_params = parser.get_daq_params()
        print(_daq_params)
        _ai_params = parser.get_ai_params()
        print(_ai_params)
        _ao_params = parser.get_ao_params()
        print(_ao_params)

    except BaseException as e:
        print(e)
