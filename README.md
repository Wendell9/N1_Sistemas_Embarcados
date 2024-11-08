# IoT Dashboard for Monitoring and Controlling Environmental Data

This project is a dashboard built with Python and Dash to monitor environmental data (luminosity, temperature, and humidity) from an IoT device. The dashboard can trigger alerts when data goes out of the acceptable range and send commands to control the device. It connects to an API endpoint to retrieve and display real-time data, and it provides a graphical visualization of the monitored metrics.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Overview](#code-overview)
  - [send_command](#send_command)
  - [get_luminosity_data, get_temperature_data, get_humidity_data](#get_luminosity_data-get_temperature_data-get_humidity_data)
  - [convert_to_Brazil_time](#convert_to_Brazil_time)

## Features
- **Real-time data monitoring** for luminosity, temperature, and humidity.
- **Configurable alert system** to send commands when values go out of range.
- **Time zone conversion** for accurate data timestamps.
- **Interactive graph** to visualize data trends over time.

## Requirements
- Python 3.7+
- Dash
- Plotly
- Requests
- pytz

## Installation
1. Clone the repository:
    ```bash
    https://github.com/Wendell9/PBL_Sistemas_Embarcados.git
    cd IoT-Environmental-Dashboard
    ```
2. Install dependencies:
    ```bash
    pip install dash plotly requests pytz
    ```

3. (Optional) Update IP and Port configurations in the code if necessary:
   ```python
   IP_ADDRESS = "XXX.XXX.XXX.XXX"
   PORT_STH = "XXXX"

# Usage
To start the dashboard, run:
   ```bash
      python app.py
   ```

By default, the app will be available at http://0.0.0.0:8050. Open this URL in your browser to access the dashboard.

The dashboard will display a graph with real-time updates every 30 seconds, showing luminosity, temperature, and humidity data. 

![image](https://github.com/user-attachments/assets/fab93a4e-7f8f-45aa-a546-5afc40e9f87d)


Alerts will display at the top of the page if values fall outside the acceptable range:

- Temperature: 15°C - 25°C
- Luminosity: 0% - 30%
- Humidity: 30% - 50%

Commands are sent to turn the device on or off based on these values:

Turn on if any value is out of range.

Turn off if all values are within the range.

# Code Overview
## send_command
- Sends an "on" or "off" command to the IoT device via a PATCH request to the API.
- Used to control the device based on environmental conditions.
## get_luminosity_data, get_temperature_data, get_humidity_data
- Functions that fetch data from the API for each metric.
- Use the lastN parameter to retrieve recent data points.
## convert_to_Brazil_time
- Converts UTC timestamps to Brazil’s Sao Paulo timezone for display purposes.
# Example Output
The dashboard shows time-series data for luminosity, temperature, and humidity, with dynamic updates every 30 seconds. Alerts are shown if values are outside acceptable ranges.

# IoT Environmental Monitoring and Control System

This project consists of two main components:
1. An ESP32 microcontroller that monitors environmental data (luminosity, temperature, and humidity) and sends it to a server.
2. A Python dashboard built with Dash to visualize and control the ESP32 remotely.

The ESP32 collects data from sensors and communicates with the server, while the dashboard retrieves this data and displays it in an interactive web application. The dashboard also allows sending control commands to the ESP32 based on threshold conditions.

## Table of Contents
- [ESP32 Features](#ESP32-features)
- [ESP32 Requirements](#ESP32-requirements)
- [ESP32 Installation](#ESP32-installation)
- [ESP32 Setup](#esp32-setup)
- [ESP32 Code Overview](#ESP32-code-overview)

## ESP32 Features
- **Real-time monitoring** of environmental data (luminosity, temperature, and humidity).
- **Configurable alert system** to automatically send control commands if values go outside acceptable ranges.
- **Data visualization** on an interactive dashboard with historical data.
- **Remote control** of ESP32 via dashboard commands.

## ESP32 Requirements
- **ESP32 Microcontroller**
- **DHT11/DHT22 Sensor** for temperature and humidity
- **LDR (Light Dependent Resistor)** for luminosity
- **Python 3.7+** (for dashboard)
- Python libraries: `dash`, `plotly`, `requests`, `pytz`

## ESP32 Installation

### ESP32 Setup
1. **ESP32 Code**: Flash the provided ESP32 code (`esp32_code.ino`) to your ESP32 board.
2. **Libraries**: Ensure that the ESP32 environment has the required libraries:
   - `WiFi.h` for connecting to WiFi.
   - `DHT.h` for interfacing with the DHT sensor.
3. **Network and API Configuration**: Update the following values in the ESP32 code:
   ```cpp
   const char* ssid = "your_SSID";         // Your WiFi SSID
   const char* password = "your_password"; // Your WiFi password
   const char* serverName = "http://your_server_ip:port"; // Server URL

Data Transmission: The ESP32 collects sensor readings every 10 seconds and sends them to the server as a JSON object, allowing the dashboard to retrieve and display the latest data.

# ESP32 Code Overview

The ESP32 code is responsible for:

- Reading Sensor Data: Collects temperature, humidity, and luminosity data every 10 seconds.
- Connecting to WiFi: Establishes a WiFi connection using provided credentials.
- Sending Data: Sends sensor data to the server as a JSON object.
- Receiving Commands: Listens for "on" or "off" commands from the dashboard and performs actions accordingly.

# Basic architecture of the project

The web application serves as the visible interface of the system, providing an interactive dashboard for real-time monitoring and control of IoT devices. This front-end, developed with Dash and Plotly, allows users to view luminosity, temperature, and humidity data captured by sensors connected to the ESP32. The application also issues alerts when values fall outside acceptable ranges and sends commands to adjust the device as needed. This dashboard enables continuous environmental monitoring while providing an intuitive experience for interacting with the IoT device.

The back-end supports platform operations by linking the web application with the IoT device. Components such as the Orion Context Broker and STH-Comet manage and store contextual entities and historical time-series data. These FIWARE components facilitate real-time and historical data collection and processing, integrating with MongoDB for NoSQL storage. MQTT protocol support is also available to ensure efficient communication with the ESP32 device. Together, these components ensure a robust foundation for data collection, control commands, and context management.

The IoT device, represented by the ESP32, collects environmental data through luminosity, temperature, and humidity sensors, communicating with the back-end via HTTP/NGSIv2 protocols. The ESP32 firmware constantly monitors sensor values and sends updates to the central application, as well as responding to commands received from the dashboard. This integration enables remote control and continuous monitoring of the environment in which the ESP32 is placed.

Note:
This application is designed for research and proof-of-concept (PoC) development. For secure deployment in production, it is recommended to use FIWARE security components, such as Keyrock (identity management), Wilma PEP Proxy, and AuthZForce, along with best security practices in the operating system or cloud environment, such as encrypted protocols (HTTPS and MQTTs).

![Diagrama fiware drawio](https://github.com/user-attachments/assets/a87638c5-0942-4968-9570-af51865be487)

# Eletric Scheme

![image](https://github.com/user-attachments/assets/abaa8e7d-7ae0-4f47-8b88-e2eacaf6e46a)

Wokwi Link: [https://wokwi.com/projects/413097520238635009](https://wokwi.com/projects/413097520238635009)
