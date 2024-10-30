import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz

# Constants for IP and port
IP_ADDRESS = "191.235.241.244"
PORT_STH = 8666
DASH_HOST = "0.0.0.0"  # Set this to "0.0.0.0" to allow access from any IP

# Function to get luminosity, temperature, and humidity data from the API
def get_luminosity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:02x/attributes/luminosity?lastN={lastN}"
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

def get_temperature_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:02x/attributes/temperature?lastN={lastN}"
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

def get_humidity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:02x/attributes/umity?lastN={lastN}"
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

# Function to convert UTC timestamps to Lisbon time
def convert_to_lisbon_time(timestamps):
    utc = pytz.utc
    lisbon = pytz.timezone('Europe/Lisbon')
    converted_timestamps = []
    for timestamp in timestamps:
        try:
            timestamp = timestamp.replace('T', ' ').replace('Z', '')
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')).astimezone(lisbon)
        except ValueError:
            # Handle case where milliseconds are not present
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).astimezone(lisbon)
        converted_timestamps.append(converted_time)
    return converted_timestamps

# Set lastN value
lastN = 10  # Get 10 most recent points at each interval

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Luminosity, Temperature, and Humidity Data Viewer'),
    dcc.Graph(id='data-graph'),
    # Store to hold historical data
    dcc.Store(id='data-store', data={'timestamps': [], 'luminosity_values': [], 'temperature_values': [], 'humidity_values': []}),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds (10 seconds)
        n_intervals=0
    )
])

@app.callback(
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('data-store', 'data')
)
def update_data_store(n, stored_data):
    # Obter dados
    data_luminosity = get_luminosity_data(lastN)
    data_temperature = get_temperature_data(lastN)
    data_humidity = get_humidity_data(lastN)

    if data_luminosity and data_temperature and data_humidity:
        # Extrair valores
        luminosity_values = [float(entry['attrValue']) for entry in data_luminosity]
        temperature_values = [float(entry['attrValue']) for entry in data_temperature]
        humidity_values = [float(entry['attrValue']) for entry in data_humidity]
        timestamps = [entry['recvTime'] for entry in data_luminosity]

        # Converter timestamps para o fuso horário de Lisboa
        timestamps = convert_to_lisbon_time(timestamps)

        # Verificar se temos pelo menos 10 valores para calcular a média
        if len(luminosity_values) >= 10:
            avg_luminosity = sum(luminosity_values[-10:]) / 10
            avg_temperature = sum(temperature_values[-10:]) / 10
            avg_humidity = sum(humidity_values[-10:]) / 10

            # Adicionar a média dos últimos 10 valores ao stored_data
            stored_data['timestamps'].append(timestamps[-1])  # Usar o timestamp mais recente
            stored_data['luminosity_values'].append(avg_luminosity)
            stored_data['temperature_values'].append(avg_temperature)
            stored_data['humidity_values'].append(avg_humidity)

        return stored_data

    return stored_data


@app.callback(
    Output('data-graph', 'figure'),
    Input('data-store', 'data')
)
def update_graph(stored_data):
    if stored_data['timestamps']:
        # Create traces for the plot
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

        # Create figure
        fig = go.Figure(data=[trace_luminosity, trace_temperature, trace_humidity])

        # Update layout
        fig.update_layout(
            title='Luminosity, Temperature, and Humidity Over Time',
            xaxis_title='Timestamp',
            yaxis_title='Values',
            hovermode='closest'
        )

        return fig

    return {}

if __name__ == '__main__':
    app.run_server(debug=True, host=DASH_HOST, port=8050)
