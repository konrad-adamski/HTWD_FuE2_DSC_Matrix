from io import StringIO
import pandas as pd
import re


# Measurement Dataframe ----------------------------------------------------------
def get_measurement_df(measurements_text, info_df, trim = 25):
    # Dataframe
    measurements_df = pd.read_csv(StringIO(measurements_text), sep=';', index_col=0)

    measurements_df.rename_axis(index=lambda idx: re.sub(r'Temp.*C', 'Temp./°C', idx), inplace=True)

    # 1) Anpassung der Spaltennamen
    num_cols = len(info_df)
    new_columns = [info_df.at[i, 'sample'] + '_' + info_df.at[i, 'segment'] for i in range(num_cols)]
    new_columns = [col.replace("/5", "") for col in new_columns]
    measurements_df.columns = new_columns

    # 2) Entfernung des Rauschens (Anfangs- und End-Werte)

    # ersten und letzten 25 Abschneiden
    measurements_df = measurements_df.iloc[trim:-trim]

    # 3) Entfernung des Initialisierungssegments (S1)
    columns_s1 = measurements_df.filter(like='_S1').columns

    measurements_df.drop(columns=columns_s1, inplace=True)
    
    return measurements_df