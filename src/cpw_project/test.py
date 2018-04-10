import utils
import os
import shutil


def tt(directory):
    directories = utils.get_all_directories(directory)

    i = 0
    for d_base in directories:
        files_base = utils.get_all_files(d_base)
        for d_compare in directories:
            files_compare = utils.get_all_files(d_compare)

            # Check to not compare same directory
            if d_base != d_compare:
                for fb in files_base:
                    for fc in files_compare:
                        i = i + 1
        directories.remove(d_base)
    return i