import pandas as pd
import plotly.graph_objs as go
import numpy as np
import os
from plotly.subplots import make_subplots
import re

folder_path = 'data_plots_opt_logs'  # Replace with the path to your folder

files_list = []  # List variable to store the filenames

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    files_list.append(filename)

#files_list = ['AAC_PPT V1.3.9_CTM_Limits_Test_Zala.xlsx', 'AAC_PPT V1.3.9.xlsx', 'Manual_Optimizer2_G4_CTPM_ver2.xlsx']





for index, filename in enumerate(files_list):
    # Read the text file line by line and extract the values using regex
    data = []
    with open(os.path.join(folder_path, filename), 'r') as file:
        for line in file:
            # Extract the date and time, if present
            datetime_match = re.match(r"\d{2}/\d{2}/\d{4},\d{1,2}:\d{2}:\d{2} (AM|PM)", line)
            if datetime_match:
                date_time = datetime_match.group(0)
                line = line.replace(date_time, "").strip()

            values = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            values = [float(val) for val in values]
            
            # Append the date and time (if available) to the values
            if datetime_match:
                values = [date_time] + values
            
            try:
                print(values[1])
                data.append(values)
            except:
                True
    print(data)
    # Create a DataFrame from the extracted data
    try:
        columns = ["Time", "Vo", "Vi", "Il", "Iin", "Temp", "Mode"]
        df = pd.DataFrame(data, columns=columns)
    except:
        columns = ["Vo", "Vi", "Il", "Iin", "Temp", "Mode"]
        df = pd.DataFrame(data, columns=columns)
    
    
    print(df.head())
    
    # Create a new figure
    variable_name = f"fig_{index}"
    # Create a layout for the plot
    layout = go.Layout(xaxis=dict(
        #tick0 = 10,
        #dtick = 1,
        #tickformat="%b\n%Y",
        #ticklabelmode="period",
        #dtick="s1",
        #dtick="0.1",
        title=filename),
        yaxis=dict(title='Voltage/Current/Power'))
    #globals()[variable_name] = go.Figure(layout=layout)
    globals()[variable_name] = make_subplots(rows=4, cols=1, shared_xaxes=True)
    # ------------------------------- Scatter Plotting ------------------------------
    #plot_url = plot(fig, filename= path + 'cols_plot.html', auto_open=True)
    # Create a histogram trace for each set of data
    #globals()[variable_name].add_trace(go.Scatter(x=df['Time'], y=df['V (V)'], mode='lines', name='String Voltage (V)'), row=1, col=1)
    #globals()[variable_name].add_trace(go.Scatter(x=df['Time'], y=df['P (W)'], mode='lines', name='Inverter Power (W)'), row=2, col=1)
    #globals()[variable_name].add_trace(go.Scatter(x=df['Time'], y=df['I (A)'], mode='lines', name='Inverter Current(A)'), row=3, col=1)
    print(df.head(100))
    globals()[variable_name].add_trace(go.Scatter(x=(df.iloc[:, 0] if df.columns[0]=='Time' else df.index), y=(df.iloc[:, 1] if df.columns[0]=='Time' else df.iloc[:, 0]), mode='lines', name='Vout'), row=1, col=1)
    #globals()[variable_name].add_trace(go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 3], mode='lines', name='Voltage Limit (V)'), row=2, col=1)
    globals()[variable_name].add_trace(go.Scatter(x=(df.iloc[:, 0] if df.columns[0]=='Time' else df.index), y=(df.iloc[:, 2] if df.columns[0]=='Time' else df.iloc[:, 1]), mode='lines', name='Vin'), row=1, col=1)
    globals()[variable_name].add_trace(go.Scatter(x=(df.iloc[:, 0] if df.columns[0]=='Time' else df.index), y=(df.iloc[:, 3] if df.columns[0]=='Time' else df.iloc[:, 2]), mode='lines', name='IL'), row=2, col=1)
    globals()[variable_name].add_trace(go.Scatter(x=(df.iloc[:, 0] if df.columns[0]=='Time' else df.index), y=(df.iloc[:, 4] if df.columns[0]=='Time' else df.iloc[:, 3]), mode='lines', name='Iin'), row=2, col=1)
    globals()[variable_name].add_trace(go.Scatter(x=(df.iloc[:, 0] if df.columns[0]=='Time' else df.index), y=(df.iloc[:, 5] if df.columns[0]=='Time' else df.iloc[:, 4]), mode='lines', name='Temperature'), row=3, col=1)
    globals()[variable_name].add_trace(go.Scatter(x=(df.iloc[:, 0] if df.columns[0]=='Time' else df.index), y=(df.iloc[:, 6] if df.columns[0]=='Time' else df.iloc[:, 5]), mode='lines', name='Mode'), row=4, col=1)
    # Update layout of the chart
    globals()[variable_name].update_layout(
    title=filename,
    xaxis=dict(title='Samples'),
    yaxis1=dict(title='Voltage (V)'),
    yaxis2=dict(title='Current (A)'),
    yaxis3=dict(title='Temperature (C)'),
    yaxis4=dict(title='Mode (Buck/Boost/BB/Safety)'),
    )
    globals()[variable_name].show()

