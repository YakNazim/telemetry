"""A set of configurations for diffecent possible feeds into the telemety
system. A feed will define the way the system is expected to listen on the
network to the data, and the different messages sent by the feed.
"""

import struct

# Flight Computer
fc = {
    'port_type': "UDP",
    'ip': "",
    'port': "35001",
    'message_type': "messages",
    'messages': {
        'ADIS': {
            'struct': struct.Struct("<12h"),
            'members': [
                {'key': "VCC",     'units': {'mks': "volt", 'scale': 2.418}},
                {'key': "Gryo_X",  'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Y",  'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Z",  'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Acc_X",   'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Acc_Y",   'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Acc_Z",   'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Magn_X",  'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Temp",    'units': {'mks': "kelvin", 'scale': 0.14}},
                {'key': "Aux_ADC", 'units': {'mks': "volt", 'scale': 806}},
            ],
        },
        'ROLL': {
            'struct': struct.Struct("<HB"),
            'members': [
                {'key': "PWM", 'units': {'mks': "seconds", 'scale': 0}},
                {'key': "Disable"},
            ],
        },
    },
}

# List all active feeds
FEEDS = {
    'fc': fc,
}
