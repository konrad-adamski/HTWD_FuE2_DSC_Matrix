import matplotlib.pyplot as plt
import pandas as pd


def plot_dsc_signal(df, column):

    # Plot the selected column against the index (Temperature)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[column], label=f'DSC Signal ({column})', linewidth=2)

    # Add labels and title specific to DSC
    plt.xlabel('Temperature [°C]')
    plt.ylabel('mW/mg')
    plt.title(f'DSC for {column}')
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()
    

def plot_dsc(df, column, df_peak):
    """
    Plots a DSC signal against temperature and includes peak information.

    Parameters:
        df (DataFrame): The pandas DataFrame containing the DSC data with temperature as index.
        column (str): The name of the column to plot on the y-axis.
        df_peak (DataFrame): A DataFrame containing peak information with columns including
                             'Series', 'T_melt [°C]', 'T1 (Onset) [°C]', and 'T2 (Offset) [°C]'.

    Returns:
        None: Displays the plot.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in the DataFrame.")
    
    # Filter peaks for the specified series (column)
    peaks = df_peak[df_peak['Series'] == column]

    # Plot the DSC signal
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[column], label=f'DSC Signal ({column})', linewidth=2)

    # Add vertical dashed lines for T_melt, T1 (Onset), and T2 (Offset)
    for _, peak in peaks.iterrows():
        plt.axvline(x=peak['T_melt [°C]'], color='red', linestyle='--', label='T_melt [°C]' if _ == 0 else "")
        plt.axvline(x=peak['T1 (Onset) [°C]'], color='green', linestyle='--', label='T1 (Onset) [°C]' if _ == 0 else "")
        plt.axvline(x=peak['T2 (Offset) [°C]'], color='blue', linestyle='--', label='T2 (Offset) [°C]' if _ == 0 else "")

    # Add labels and title specific to DSC
    plt.xlabel('Temperature [°C]')
    plt.ylabel('mW/mg')
    plt.title(f'DSC for {column}')
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()