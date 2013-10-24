import datetime
import sys
import struct
import json

PACKET_SIZE = 4096     # maximum UDP packet size for listener to receive
APP_PORT = 8080        # Application port to run front end web server
FLUSH_RATE = 250       # backend to frontend update frequency, in ms


# debugging
BAD_DEBUG_ONLY = False  # Show only debug information for bad cases
DEBUG = (sys.argv[1:] == ['-d'])
PRINT_CHAR_FOR_ARRIVING_PACKETS = False
PRINT_CHAR_FOR_BACK_TO_FRONT_UPDATE = False


# log filename format
PACKET_LOG_FILENAME = datetime.datetime.now().strftime(
    "log/log_%Y.%m.%d_%H-%M-%S")
VALIDATION_LOG_FILENAME = datetime.datetime.now().strftime(
    "log/data_validation_%Y.%m.%d_%H-%M-%S.txt")
MESSAGES_LOG_FILENAME = datetime.datetime.now().strftime(
    "log/messages_%Y.%m.%d_%H-%M-%S.json")


# this line must be in the end of this file
#import debug
