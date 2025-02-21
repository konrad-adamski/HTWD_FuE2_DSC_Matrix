from io import StringIO
import pandas as pd
import re


# Measurement Dataframe ----------------------------------------------------------
def get_measurement_df(measurements_text, info_df):
    # Dataframe
    measurements_df = pd.read_csv(StringIO(measurements_text), sep=';', index_col=0)

    measurements_df.rename_axis(index=lambda idx: re.sub(r'Temp.*C', 'Temp./°C', idx), inplace=True)

    dsc_type = "unknown"
    if "mW/mg" in measurements_df.columns[0]:
        dsc_type = "mW/mg"
    elif "mW" in measurements_df.columns[0]:
        dsc_type = "mW"

    # 1) Anpassung der Spaltennamen
    num_cols = len(info_df)
    new_columns = [info_df.at[i, 'sample'] + '_' + info_df.at[i, 'segment'] for i in range(num_cols)]
    new_columns = [col.replace("/5", "") for col in new_columns]
    measurements_df.columns = new_columns

    # 2) Entfernung des Rauschens (Anfangs- und End-Werte)

    # ersten und letzten 25 Abschneiden
    measurements_df = measurements_df.iloc[25:-25]

    # 3) Entfernung des Initialisierungssegments (S1)
    columns_s1 = measurements_df.filter(like='_S1').columns

    measurements_df.drop(columns=columns_s1, inplace=True)

    # 4) Anpassung der Werte in mW

    measurements_df = measurements_df.apply(pd.to_numeric, errors='coerce')

    try:
        if dsc_type == "mW/mg":
            for column in measurements_df.columns:
                sample, _ = column.split('_')  # Sample und Segment ID extrahieren
                mass_mg_value = info_df.loc[info_df["sample"] == sample, "sample mass_mg"].iloc[0]
                measurements_df.loc[:, column] *= mass_mg_value
            dsc_type = "mW"

    except Exception as e:
        print(f"Error: {e}")
        

    # 5) Zeit-Spalte einfügen
    heating_rate_per_minute = info_df["heat_rate"][0]
    measurements_df['Time [sec]'] = get_time_from_temperatures(measurements_df, heating_rate_per_minute)
    
    print(f"DSC Type: {dsc_type}")
    return measurements_df



# Hilfsfunktionen ----------------------------------------------------

def get_time_from_temperatures(df, heating_rate_per_minute):
    heating_rate_per_second = heating_rate_per_minute / 60
    start_temp = df.index[0]
    time_seconds = [(temp - start_temp) / heating_rate_per_second for temp in df.index]
    return time_seconds