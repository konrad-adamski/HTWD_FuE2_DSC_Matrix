import os
import re
import pandas as pd


def split_text(file_path, encoding=None):
    if encoding == "True":
        with open(file_path, "r", encoding="ISO-8859-1") as datei:
            inhalt = datei.read()
    elif encoding is not None:
        with open(file_path, "r", encoding=encoding) as datei:
            inhalt = datei.read()
    else:
        with open(file_path, 'r') as datei:
            inhalt = datei.read()
    return inhalt.strip().split("##")  # returns info_text and measurement_text



def get_time_from_temperatures(df, heating_rate_per_minute=20):
    heating_rate_per_second = heating_rate_per_minute / 60
    start_temp = df.index[0]
    time_seconds = [(temp - start_temp) / heating_rate_per_second for temp in df.index]
    return time_seconds


