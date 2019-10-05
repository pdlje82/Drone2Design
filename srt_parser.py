import pandas as pd
import re

with open('./data/input/DJI_0007.SRT') as file:
    file_contents = file.read()
    print(file_contents)