import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import seaborn as sns


def compute_mean_curve(df, columns):
    """
    Computes a DataFrame containing only the specified columns and a new column with the mean of these columns for each row.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        columns (list of str): List of column names to compute the mean for.

    Returns:
        pd.DataFrame: A DataFrame containing the specified columns and an additional column named 'Mean'.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if not all(col in df.columns for col in columns):
        missing_columns = [col for col in columns if col not in df.columns]
        raise ValueError(f"The following columns are missing in the DataFrame: {missing_columns}")

    # Compute the row-wise mean for the specified columns
    mean_column = df[columns].mean(axis=1)

    # Create a new DataFrame with the specified columns and the mean column
    result_df = df[columns].copy()
    result_df['Mean'] = mean_column

    return result_df



def plot_dsc_values_with_mean(df, columns, include_individual=True, title="DSC Measurement Values", y_min=None, y_max=None):
    """
    Plots the DSC measurement values for the given columns and the mean curve.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        columns (list of str): List of column names to plot.
        include_individual (bool): Whether to include individual column plots.
        title (str): Title of the plot.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    # Compute mean curve using compute_mean_curve
    mean_df = compute_mean_curve(df, columns)

    plt.figure(figsize=(10, 6))

    # Plot individual columns if enabled
    if include_individual:
        for col in columns:
            plt.plot(mean_df.index, mean_df[col], label=col, alpha=0.5, linestyle='--')

    # Plot the mean column as a bold line
    plt.plot(mean_df.index, mean_df['Mean'], label='Mean', linewidth=2.5, color='black')

    # Set y-axis limits if specified
    if y_min is not None or y_max is not None:
        plt.ylim(bottom=y_min, top=y_max)

    # Add legend with maximum height
    max_legend_entries = 20  # Maximum number of legend entries visible
    handles, labels = plt.gca().get_legend_handles_labels()

    if len(labels) > max_legend_entries:
        displayed_labels = labels[:max_legend_entries - 1] + ['...', 'Mean']
        displayed_handles = handles[:len(displayed_labels) -1] + [handles[labels.index('Mean')]]
    else:
        displayed_labels = labels
        displayed_handles = handles
    
    plt.legend(displayed_handles, displayed_labels, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    plt.xlabel("Temperature (°C)")
    plt.ylabel("mW")
    plt.title(title)
    plt.tight_layout()
    plt.show()
    
    
    
    
def analyze_clusters_with_percentages(cluster_to_samples, df_dsc, column_name="Matrix"):
    """
    Analysiert die Verteilung einer angegebenen Spalte für Cluster in einem DataFrame und berechnet Anteile.
    Fügt 'Nicht vorhanden' hinzu, wenn fehlende Proben in einem Cluster existieren.
    
    Args:
        cluster_to_samples (dict): Dictionary mit Clustern und zugehörigen Proben.
        df_dsc (pd.DataFrame): DataFrame mit den Daten (Index muss die Proben enthalten).
        column_name (str): Name der Spalte, die analysiert werden soll.

    Returns:
        dict: Ergebnisse als Dictionary mit Clusternamen als Schlüssel und DataFrames mit Count und Anteil als Wert.
    """
    results = {}
    
    for cluster, samples in cluster_to_samples.items():
        # Entferne den Suffix "_S5", um die Proben zu matchen
        selected_samples = [s.split('_')[0] for s in samples]

        # Prüfe, welche Werte im Index vorhanden sind
        existing_samples = [s for s in selected_samples if s in df_dsc.index]

        # Finde die fehlenden Werte
        missing_samples = set(selected_samples) - set(existing_samples)

        # Filtere den DataFrame nur für die vorhandenen Proben
        filtered_df = df_dsc.loc[existing_samples]

        # Zähle die Werte in der angegebenen Spalte
        column_counts = filtered_df[column_name].value_counts()

        # Füge fehlende Werte als "Nicht vorhanden" hinzu, wenn es fehlende gibt
        if len(missing_samples) > 0:
            column_counts['Nicht vorhanden'] = len(missing_samples)

        # Berechne die Anteile
        total_samples = column_counts.sum()
        column_percentages = (column_counts / total_samples) * 100

        print(samples)
        print("____")

        # Kombiniere Count und Anteile in einem DataFrame
        result_df = pd.DataFrame({
            'Count': column_counts,
            'Anteil (%)': column_percentages.round(2),
            'von (gesamt)': len(cluster_to_samples)
        })

        # Speichere die Ergebnisse im Dictionary
        results[cluster] = result_df
    
    return results