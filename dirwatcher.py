#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Wesley Salesberry with help from JT"

import sys
import argparse
import logging
import signal
import time
import os

exit_flag = False


def search_for_magic(filename, start_line, magic_string, path):
    line_number = start_line
    with open(f'{path}/{filename}') as f:
        lines = f.readlines()
    num_of_lines = len(lines)
    for index in range(start_line, num_of_lines):
        if magic_string in lines[index]:
            print(f'word found in {filename} {index + 1}!')
            # logging moment here
        line_number = index + 1
    return line_number



def watch_directory(path, magic_string, extension, interval):
    file_holder = {}
    exit = False
    while not exit:
        time.sleep(interval)
        if os.path.isdir(path):
            file_list = os.listdir(path)
            for files in file_list:
                if files.endswith(extension) and files not in file_holder:
                    file_holder[files] = 0
                    print(f'file added {files}')
            key = list(file_holder.keys())
            for k in key:
                if k not in file_list:
                    print(f'this file was removed {k}')
                    file_holder.pop(k)
            for key, value in file_holder.items():
                file_holder[key] = search_for_magic(path, key, value, magic_string)
            print(file_holder)

        else:
            print("path not found")
            file_holder = {}
        
  


def create_parser():
    parser = argparse.ArgumentParser(description="Watches specified directory for magic word.")
    parser.add_argument('directory', help='directory to watch')
    parser.add_argument('word', help='word to scan directory for')
    parser.add_argument('-e', '--extension', help='file extension to search',
                        default='.txt')
    parser.add_argument('-i', '--integer', help='poll int, defaults to 1 sec',
                        type=float, default=1.0)
    return parser




def signal_handler(sig_num, frame):

    global exit_flag
    exit_flag = True
    logging.warning('Received ' + signal.Signals(sig_num).name)


def main(args):
    # Your code here
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage(args)
        sys.exit(1)

    path = ns.directory
    magic = ns.magic
    ext = ns.extension
    integer = ns.integer

    while not exit_flag:
        try:
            print('something')
            watch_directory(path, magic, ext, integer)
        except FileNotFoundError as err:
            print('Sorry, this file does not exist')
            logging.error(err)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
