import pandas as pd
import re


def load_srt(path):
    with open(path) as file:
        file_contents = file.read()
        return file_contents


def frame_to_coordinates_dict(path):
    file_contents = load_srt(path)
    srt_dict = {}
    myarray = file_contents.split("\n\n")  # split the file at each empty line
    myarray = myarray[:-1]  # skip newline at the end of the srt file
    for e in myarray:
        subarray = e.split('\n')
        srt_dict[subarray[0]] = {'lat': subarray[4].split(']')[7][12:],
                                 'lon': subarray[4].split(']')[8][14:]}
    return srt_dict


