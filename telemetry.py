#!/usr/bin/env python

import config
import processing
import parsing
import server
from time import time

stats = parsing.Stats()
packet_log = open(config.PACKET_LOG_FILENAME, "a")

# global objects for data processing
def main():
    config.debug.open_logs()
    server.thread.start_new_thread(server.tornado_thread, (0, 0))
    receive_packets()

def receive_packets():
    sock = parsing.init_socket()

    # listen socket
    while True:
        new_timeout = data_sync()
        sock.settimeout(new_timeout)
        message = parsing.receive_packet(sock)
        if message == '':  # timeout - no packets received during TIMEOUT
            continue  # get the next packet
        if parsing.PRINT_CHAR_FOR_ARRIVING_PACKETS:
            debug.print_char('.')  # packet received successfully --> print a dot
        seq = parsing.parse_sequence(message)
        stats.new_packet_received(seq)
        dump_packet_to_log_file(message, seq)

        # parse messages from the packet
        message = message[config.SEQUENCE_LENGTH:]
        while len(message) > config.HEADER_LENGTH:  # end of data or truncated header
            message_id, timestamp, length = parsing.parse_message_header(message)
            stats.recent_timestamp(timestamp)
            length = parsing.overwrite_length(message_id, length)
            if parsing.data_is_truncated(message, length):
                break  # skip this message and read the next packet
            data = message[config.HEADER_LENGTH:length + config.HEADER_LENGTH]  # data bytes
            # debug.message_header(message_id, length, timestamp) # debug message
            parsing.parse_data(message_id, timestamp, length, data)
            message = message[config.HEADER_LENGTH + length:]  # go to next message


def dump_packet_to_log_file(message, seq):
    # dump packet to log file
    packet_log.write(config.delimiter.pack('SEQN', seq, len(message)))  # add delimiter
    packet_log.write(message)
    # TODO: need to figure out (define) delimiter format


def data_sync():
    now_time = time()  # in seconds, floating
    if now_time < data_sync.next_update_time:  # not time for an update yet
        # adjust timeout to wait until the next scheduled update time
        return data_sync.next_update_time - now_time
    # otherwise, the update time has just passed, so send an update now.

    if config.PRINT_CHAR_FOR_BACK_TO_FRONT_UPDATE:
        config.debug.print_char('U')  # sending JSON data to front-end

    # Sending data update
    send_data_to_front_end_v2()

    data_sync.next_update_time += config.TIMEOUT  # set new next time for data update
    return max(0, data_sync.next_update_time - time())
    # prevent rare case of negative timeout

# initialize static variables at program start:
data_sync.next_update_time = time() + config.TIMEOUT


def send_data_to_front_end_v2():
    config.debug.clear_screen()
    send_ADIS()
    send_ROLL()
    send_GPS1()
    send_stats()
    reset_processing()
    print "\n", "time:  " + stats.get_current_time_string()

def send_ADIS():
    # ADIS, prepare and send
    if parsing.Messages.adis.counter > 0:
        parsing.Messages.adis.add_other_fields()
        server.send_json_obj(parsing.Messages.adis.data)
        config.debug.print_ADIS(parsing.Messages.adis.data)
    else:
        print "ADIS:  no data\n\n\n\n\n"

def send_ROLL():
    # ROLL, prepare and send
    if parsing.Messages.roll.counter > 0:
        parsing.Messages.roll.add_other_fields()
        server.send_json_obj(parsing.Messages.roll.data)
        debug.print_ROLL(parsing.Messages.roll.data)
    else:
        print "ROLL:  no data\n"
        
def send_GPS1():
    # GPS1, prepare and send
    if parsing.Messages.gps1.counter > 0:
        parsing.Messages.gps1.add_other_fields()
        server.send_json_obj(parsing.Messages.gps1.data)
        debug.print_GPS1(parsing,Messages.gps1.data)
    else:
        print "GPS1:  no data\n\n\n\n\n\n\n\n\n"

def send_stats():
    global stats
    # Send statistics
    obj = stats.get()
    config.debug.print_stats(obj)
    server.send_json_obj(obj)

def reset_processing():
    global stats
    # reset data for the next time chunk
    parsing.Messages.adis.reset()
    parsing.Messages.roll.reset()
    parsing.Messages.gps1.reset()
    stats.reset()
        
if __name__ == "__main__":
    main()
