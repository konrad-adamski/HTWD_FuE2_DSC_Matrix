import pandas as pd

def process_and_merge_data(df_main, df_dsc):
    """
    Diese Funktion verarbeitet die Daten von `df_main` und `df_dsc`,
    um die Indizes zu transformieren, die Daten zu mergen und bereinigen.

    Parameter:
        df_main (pd.DataFrame): Die Haupt-DataFrame mit zu transformierenden Indizes.
        df_dsc (pd.DataFrame): Die DataFrame mit den Spalten 'dHm_J/g' und 'Tm_C', die gemerged werden sollen.

    Rückgabe:
        pd.DataFrame: Die bereinigte und gemergte DataFrame.
    """
    # Entferne den Suffix '_S5' aus den Indizes von df_main
    df_main.index = df_main.index.str.replace('_S5', '', regex=False)

    # Stelle sicher, dass die Indizes als String vorliegen
    df_main.index = df_main.index.astype(str)
    df_dsc.index = df_dsc.index.astype(str)

    # Führe einen Left Merge basierend auf den transformierten Indizes durch
    df_merged = df_main.merge(
        df_dsc[['dHm_J/g', 'Tm_C']],
        left_index=True,
        right_index=True,
        how='left'
    )

    # Entferne alle Zeilen mit NaN-Werten
    df_merged = df_merged.dropna()

    # Konvertiere alle Spaltennamen in Strings
    df_merged.columns = df_merged.columns.astype(str)

    # Füge den Suffix '_S5' zurück zu den Indizes hinzu
    df_merged.index = df_merged.index + '_S5'

    return df_merged