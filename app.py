import os
from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import re

app = Flask(__name__)

# Custom function to parse the log file and extract data for plotting
# Replace this with your actual custom function to process the log file data
def parse_log_file(file_path, filename):
    # Read the text file line by line and extract the values using regex
    data = []
    with open(os.path.join(file_path), 'r') as file:
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
    
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file has a filename and it has the .log extension
        if file.filename == '' or not file.filename.lower().endswith('.log'):
            return redirect(request.url)

        # Save the uploaded file to a temporary location
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Call the custom function to parse the log file and extract data
        parse_log_file(file_path, file.filename)

        # Generate the plot using Plotly
        # Replace the code below with your actual plot creation code
        #fig = go.Figure()
        # Add your plot traces and layout here based on the 'data'

        # Remove the temporary file after processing
        os.remove(file_path)

        #return render_template('plot.html', plot=fig.to_html())

    return render_template('index.html')

if __name__ == '__main__':
    #app.run(port=5001,debug=True)
    app.run(host="0.0.0.0", port=5001)