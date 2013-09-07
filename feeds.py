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
            'members': [
                {'key': "VCC",     'struct': "h", 'units': {'mks': "volt", 'scale': 2.418}},
                {'key': "Gryo_X",  'struct': "h", 'untis': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Y",  'struct': "h", 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Z",  'struct': "h", 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Acc_X",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Acc_Y",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Acc_Z",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Temp",    'struct': "h", 'units': {'mks': "kelvin", 'scale': 0.14}},
                {'key': "Aux_ADC", 'struct': "h", 'units': {'mks': "volt", 'scale': 806}},
            ],
        },
        'ROLL': {
            'struct': struct.Struct("<HB"),
            'members': [
                {'key': "PWM", 'struct': "H", 'units': {'mks': "seconds", 'scale': 0}},
                {'key': "Disable", 'struct': "B"},
            ],
        },
    },
}

# List all active feeds
FEEDS = {
    'fc': fc,
}
