import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz
import json

# Constants for IP and port
IP_ADDRESS = "191.235.241.244"
PORT_STH = 8666
DASH_HOST = "0.0.0.0"  # Set this to "0.0.0.0" to allow access from any IP

# API URL for sending commands
API_URL = f"http://{IP_ADDRESS}:1026/v2/entities/urn:ngsi-ld:Lamp:002/attrs"

# Function to send on/off commands to the API
def send_command(command):
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    body = {
        command: {
            "type": "command",
            "value": ""
        }
    }
    # Sends the PATCH request to the API to change the device state
    response = requests.patch(API_URL, headers=headers, data=json.dumps(body))
    if response.status_code == 204:
        print("Command sent successfully.")
    else:
        print(f"Error sending command: {response.status_code}, {response.text}")

# Function to get luminosity data from the API
def get_luminosity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:002/attributes/luminosity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []

# Function to get temperature data from the API
def get_temperature_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:002/attributes/temperature?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []

# Function to get humidity data from the API
def get_humidity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:002/attributes/humidity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []

# Function to convert UTC timestamps to Brazil (Sao Paulo) timezone
def convert_to_Brazil_time(timestamps):
    utc = pytz.utc
    lisbon = pytz.timezone('America/Sao_Paulo')
    converted_timestamps = []
    for timestamp in timestamps:
        try:
            timestamp = timestamp.replace('T', ' ').replace('Z', '')
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')).astimezone(lisbon)
        except ValueError:
            # Handles cases without milliseconds
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).astimezone(lisbon)
        converted_timestamps.append(converted_time)
    return converted_timestamps

# Set lastN value to retrieve the two most recent data points
lastN = 2

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout with title, graph, data store, and interval component
app.layout = html.Div([
    html.H1('Luminosity, Temperature, and Humidity Data Viewer'),
    html.Div(id='alert-message', style={'color': 'red', 'font-weight': 'bold'}),
    dcc.Graph(id='data-graph'),
    # Store component to save historical data between updates
    dcc.Store(id='data-store', data={'timestamps': [], 'luminosity_values': [], 'temperature_values': [], 'humidity_values': []}),
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # 30-second interval in milliseconds
        n_intervals=0
    )
])

# Callback to update data store and generate alerts
@app.callback(
    [Output('data-store', 'data'), Output('alert-message', 'children')],
    Input('interval-component', 'n_intervals'),
    State('data-store', 'data')
)
def update_data_store(n, stored_data):
    alert_messages = []  # List to accumulate alert messages
    send_on_command = False  # Determines if the "on" command should be sent

    # Retrieve data from API
    data_luminosity = get_luminosity_data(lastN)
    data_temperature = get_temperature_data(lastN)
    data_humidity = get_humidity_data(lastN)

    if data_luminosity and data_temperature and data_humidity:
        # Extract data values
        luminosity_values = [float(entry['attrValue']) for entry in data_luminosity]
        temperature_values = [float(entry['attrValue']) for entry in data_temperature]
        humidity_values = [float(entry['attrValue']) for entry in data_humidity]
        timestamps = [entry['recvTime'] for entry in data_luminosity]

        # Convert timestamps to Brazil timezone
        timestamps = convert_to_Brazil_time(timestamps)

        # Add new data to stored_data
        stored_data['timestamps'].extend(timestamps)
        stored_data['luminosity_values'].extend(luminosity_values)
        stored_data['temperature_values'].extend(temperature_values)
        stored_data['humidity_values'].extend(humidity_values)

        # Check conditions for triggers and add alert messages
        if temperature_values[-1] < 15 or temperature_values[-1] > 25:
            send_on_command = True
            alert_messages.append(f"Temperature out of range: {temperature_values[-1]} °C.")

        if luminosity_values[-1] < 0 or luminosity_values[-1] > 30:
            send_on_command = True
            alert_messages.append(f"Luminosity out of range: {luminosity_values[-1]}%.")

        if humidity_values[-1] < 30 or humidity_values[-1] > 50:
            send_on_command = True
            alert_messages.append(f"Humidity out of range: {humidity_values[-1]}%.")

        # Send command based on trigger checks
        if send_on_command:
            send_command("on")  # Send "on" command if any condition is out of range
        else:
            send_command("off")  # Send "off" command if all conditions are within range

    # Combine alert messages into a single output string
    alert_message = [html.P(msg) for msg in alert_messages] if alert_messages else [html.P("All values are within acceptable ranges.")]

    return stored_data, alert_message

# Callback to update the graph with data from the store
@app.callback(
    Output('data-graph', 'figure'),
    Input('data-store', 'data')
)
def update_graph(stored_data):
    if stored_data['timestamps']:
        # Create traces for each data type
        trace_luminosity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['luminosity_values'],
            mode='lines+markers',
            name='Luminosity',
            line=dict(color='orange')
        )
        trace_temperature = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['temperature_values'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='red')
        )
        trace_humidity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['humidity_values'],
            mode='lines+markers',
            name='Humidity',
            line=dict(color='blue')
        )

        # Create figure with layout
        fig = go.Figure(data=[trace_luminosity, trace_temperature, trace_humidity])

        fig.update_layout(
            title='Luminosity, Temperature, and Humidity Over Time',
            xaxis_title='Timestamp',
            yaxis_title='Values',
            hovermode='closest'
        )

        return fig

    return {}

# Run the app server
if __name__ == '__main__':
    app.run_server(debug=True, host=DASH_HOST, port=8050)
