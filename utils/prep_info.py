import os
import re
import pandas as pd

# Information Dataframe ----------------------------------------------------------
def get_info_df(info_text):
    # 1) Aufteilung des Inhalts auf Key-List (Value) Paare
    raw_info_dict = key_entry_split(info_text)
    info_dict = entries_split(raw_info_dict)

    # 2) Allgemeine Bestimmung der Zeilen
    series_numb = len(info_dict["SAMPLE"])  # alternativ über IDENTITY

    # 3) Ausschluss der Keys mit wenig keys als series_numb
    key_value_count = count_entries_pro_key(info_dict)
    excluded_keys = [key for key, value in key_value_count.items() if value != series_numb]
    # 4) Dataframe bilden
    info_df = dict_to_dataframe(info_dict, ignore_keys=excluded_keys)

  
    # 5 Anpassung der Spaltennamen
    info_df.columns = info_df.columns.str.lower()
    info_df = info_df.rename(columns=replace_slash)
    
    # Entferne Leerzeichen vor "/" aus allen Spaltennamen
    info_df.columns = info_df.columns.str.replace(" /", "/")
    
    # 6 Dataframe auf das Relevante Columns reduzieren
    relevant_columns = ["file", "sample", "segment", "range", "sample mass_mg"]
    info_df = info_df[relevant_columns]


    # 7 Anpassung von sample
    info_df["sample"] = info_df["sample"].str.replace("_", "-")
    

    # Konvertiere 'sample mass_mg' zu numerischen Werten, ignoriere Fehler
    try:
        info_df['sample mass_mg'] = pd.to_numeric(info_df['sample mass_mg'], errors='coerce')
    except Exception as e:
        print(f"sample mass_mg nicht gefunden")

    # Extrahieren der Heizrate
    info_df['heat_rate'] = info_df['range'].apply(extract_heat_rate)

    return info_df



# Information Dataframe - Subfunktionen ------------------------------------------
# 1a) Einfache Key-Value Paare ----------------------------------
def key_entry_split(text):
    data = {}
    sections = text.strip().split("#")
    sections = sections[1:]  # erstes Element wird entfernt da leer (# ist am Anfang)
    for section in sections:
        key = section.split(":")[0]
        value_string = section.split(":")[1]
        data[key] = value_string.strip()
    return data


# 1b) Key-List Paare --------------------------------------------
# Aufteilung der Value-Strings in Value-Listen
def single_entry_split(text):
    return re.split(r'\s{2,}', text.strip())  # 2 oder mehrere Leerzeichen hintereinander


def entries_split(data):
    result = {}
    for key, value in data.items():
        result[key] = single_entry_split(value)
    return result


# 3) -------------------------------------------------------------
def count_entries_pro_key(dictionary):
    result = {}
    for key, values in dictionary.items():
        anzahl_der_values = len(values)
        result[key] = anzahl_der_values
    return result


# 4) Dataframe ---------------------------------------------------
def dict_to_dataframe(dictionary, ignore_keys=None):
    if ignore_keys is None:
        ignore_keys = []
    # Filtern der Schlüssel, die ignoriert werden sollen
    filtered_dict = {key: values for key, values in dictionary.items() if key not in ignore_keys}
    try:
        dframe = pd.DataFrame(filtered_dict)
        return dframe
    except Exception as e:
        print(f"Error: {e}")
        return None

# Hilfsfunktionen ----------------------------------------------------

def replace_slash(column_name):
    return re.sub(r'\s*/\s*', '_', column_name.lower())

def extract_heat_rate(text):
    match = re.search(r'(\d+\.?\d*)(?=\(K/min\))', text)
    return float(match.group(1)) if match else None


def get_time_from_temperatures(df, heating_rate_per_minute=20):
    heating_rate_per_second = heating_rate_per_minute / 60
    start_temp = df.index[0]
    time_seconds = [(temp - start_temp) / heating_rate_per_second for temp in df.index]
    return time_seconds
