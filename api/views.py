import datetime
import time
from urllib.parse import quote
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from Gereate.GereateManager import GereateManager
from Gereate.HMP4040 import HMP4040
from main import main
import csv
import os
import socket
import shutil
from pages.models import Measurement, MeasurementValues


# Define an API endpoint to get devices, that are connected to the server
@api_view(['GET'])
def getAngeschlosseneGereate(request):
    # Return a response with the connected devices
    return Response(GereateManager.getAngeschlosseneGereate())

# Define an API endpoint to measure data from an HMP4040 device
@api_view(['GET'])
def hmp4040_measure(request):
    try:
        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(request.GET.get('ip', None))
        if hmp4040 is not None:
            # Read voltage, current, and power for four channels and create a response
            response_data = {'1': [hmp4040.read_volt(1), hmp4040.read_curr(1), hmp4040.read_power(1)],
                             '2': [hmp4040.read_volt(2), hmp4040.read_curr(2), hmp4040.read_power(2)],
                             '3': [hmp4040.read_volt(3), hmp4040.read_curr(3), hmp4040.read_power(3)],
                             '4': [hmp4040.read_volt(4), hmp4040.read_curr(4), hmp4040.read_power(4)]}
            return JsonResponse(response_data, status=200)
        else:
            # Return an empty response if the device is not found
            return JsonResponse({}, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


# Define an API endpoint to add a channel for auto-correction
@api_view(['POST'])
def auto_corrector_add_ch(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))
        ip = data.get('ip')
        hmp4040 = main.get_device(ip)
        ch = int(data.get('ch'))
        sollwert = float(data.get('sollwert'))
        
        # Set the desired power value for the channel and mark it for correction
        hmp4040.channels_power[ch] = sollwert
        hmp4040.to_be_corrected_channels.append(ch)
        response_data = {}
        return JsonResponse(response_data, status=200)
    except ZeroDivisionError:
        # Handle division by zero error if needed
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
# Define an API endpoint to remove a channel from auto-correction
@api_view(['POST'])
def auto_corrector_remove_ch(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))
        ip = data.get('ip')
        hmp4040 = main.get_device(ip)
        ch = int(data.get('ch'))
        
        # Remove the channel from the list of channels to be corrected
        if ch in hmp4040.to_be_corrected_channels:
            hmp4040.to_be_corrected_channels.remove(ch)
        
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)  

# Define an API endpoint to enable a channel in HMP4040
@api_view(['POST'])
def channel_aktivieren(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(data.get('ip'))

        # Enable the specified channel
        hmp4040.enable_Channel(int(data.get('ch')))   

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to disable a channel in HMP4040
@api_view(['POST'])
def channel_deaktivieren(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(data.get('ip'))

        # Disable the specified channel
        hmp4040.disable_Channel(int(data.get('ch')))   

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to enable the HMP4040 output
@api_view(['POST'])
def out_aktivieren(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(data.get('ip'))

        # Enable the output of the device
        hmp4040.enable_output()   

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to disable the device's output
@api_view(['POST'])
def out_deaktivieren(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(data.get('ip'))

        # Disable the output of the device
        hmp4040.disable_output()   

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to start saving data
@api_view(['POST'])
def start_saving_Data(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Get the IP address from the data
        ip = data.get('ip')

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(ip)

        # Create csv Data
        hmp4040.create_data()

        # Set a flag indicating that data saving is running
        hmp4040.is_saving_running = True

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
 
    
# Define an API endpoint to stop saving data
@api_view(['POST'])
def stop_saving_Data(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Extract IP address from the data
        ip = data.get('ip')

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(ip)

        # Set a flag to indicate that saving data is no longer running
        hmp4040.is_saving_running = False

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to set power for a channel
@api_view(['POST'])
def set_power(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Extract IP address, channel (ch), and power from the data
        ip = data.get('ip')
        ch = data.get("ch")
        power = data.get("power")

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(ip)

        # Set the power for the specified channel
        hmp4040.set_power(ch, power)

        # Prepare an empty response
        response_data = {}

        # Sleep for 1 second (functionality not explicitly explained)
        time.sleep(1)

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
 
# Define an API endpoint to set voltage for a channel
@api_view(['POST'])
def set_volt(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Extract IP address, channel (ch), and voltage (volt) from the data
        ip = data.get('ip')
        ch = data.get("ch")
        volt = float(data.get("volt"))

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(ip)

        # Set the voltage for the specified channel
        hmp4040.set_volt(ch, volt)

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to read voltage from a channel
@api_view(['GET'])
def read_voltage(request):
    try:
        # Get the HMP4040 device based on the provided IP address (from query parameter)
        hmp4040 = main.get_device(request.GET.get('ip', None))
        
        if hmp4040 is not None:
            # Read voltage for channel 1 and create a response
            response_data = {'volt': hmp4040.read_volt(1)}
            return JsonResponse(response_data, status=200)
        else:
            # Return an empty response if the device is not found
            return JsonResponse({}, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Define an API endpoint to read current from a channel
@api_view(['GET'])
def read_curr(request):
    try:
        # Get the HMP4040 device based on the provided IP address (from query parameter)
        hmp4040 = main.get_device(request.GET.get('ip', None))
        
        if hmp4040 is not None:
            # Read current for channel 1 and create a response
            response_data = {'curr': hmp4040.read_curr(1)}
            return JsonResponse(response_data, status=200)
        else:
            # Return an empty response if the device is not found
            return JsonResponse({}, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


# Define an API endpoint for start a OPUS-Scan and save the data in the database
@api_view(['POST'])
def scan(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Get the HMP4040 device based on the provided IP address
        hmp4040 = main.get_device(data.get('ip'))

        # Extract additional data from the request
        unterverzeichnis = data.get('unterverzeichnis')
        strahlertyp = data.get('strahlertyp')
        strahlernummer = data.get('strahlernummer')
        soll_leistung = data.get('soll_leistung')
        comment = data.get('comment')

        # Enable channel 1, enable the device's output, and set its power
        hmp4040.enable_Channel(1)
        hmp4040.enable_output()
        hmp4040.set_power(1, float(soll_leistung))
        time.sleep(1)

        # Read voltage and current values
        voltage = round(hmp4040.read_volt(1), 2)
        current = round(1000 * hmp4040.read_curr(1), 1)

        # Generate a timestamp for the file name
        formatted_date = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        fileName = f"{formatted_date}_{strahlertyp}_{soll_leistung}W_{voltage}V_{current}mA_{strahlernummer}_{comment}"

        # Create a URL for triggering data measurement
        url = f'http://localhost/OpusCommand.htm?COMMAND_LINE MeasureSample (,{{EXP= EXP_TR_an.xpm,XPP=\'C:\\Users\\Public\\Documents\\Bruker\\OPUS_8.1.29\\XPM\',NSS=16,SFM=\'{fileName}\',PTH=\'C:\\Users\\{get_windows_username()}\\Endress+Hauser\\Infrasolid GmbH - Documents\\07_Produktion\\13_Prozessdaten\\03_FTIR\\{unterverzeichnis}\\\' }});'

        # Send a POST request to trigger data measurement
        send_post_request(url)

        # Define source and temporary folders for file manipulation
        source_folder = f'C:/Users/{get_windows_username()}/Endress+Hauser/Infrasolid GmbH - Documents/07_Produktion/13_Prozessdaten/03_FTIR/{unterverzeichnis}/'
        temp_folder = 'C:/temp/test/'

        # Create a new Measurement instance
        new_measurement = Measurement(
            date=datetime.datetime.now(),
            type=strahlertyp,
            set_power_W=soll_leistung,
            current_mA=current,
            voltage_V=voltage,
            serial_number=strahlernummer,
            comment=comment,
        )

        # Sleep for 6 seconds 
        time.sleep(6)

        # Wait until data measurement progress reaches 0
        while get_progress() != 0:
            print(get_progress())
            time.sleep(1)

        print("Creating files started")

        # Disable the device's output
        hmp4040.disable_output()

        # Define file paths for original and temporary files
        originalFile = source_folder + fileName + ".0"

        # Unload the files in OPUS 
        UnloadAll()

        time.sleep(0.2)

        # Copy the original file to the temporary folder
        shutil.copy(originalFile, temp_folder)

        # Run a macro to convert the .0 file to a .dpt file
        runMacroReq()
        time.sleep(0.2)

        # Define file paths for temporary files
        dptTempFile = temp_folder + fileName + ".0.dpt"
        originalTempFile = temp_folder + fileName + ".0"

        # Copy the DPT and original temporary files to the source folder
        shutil.copy(dptTempFile, source_folder)
        time.sleep(0.2)

        # Delete temporary files
        deleteFile(dptTempFile)
        deleteFile(originalTempFile)

        # Define the path for the original DPT file
        originalDptFile = originalFile + ".dpt"

        # Save the new measurement instance to the database
        new_measurement.save(using='mysql_db')

        # Import measurement values from the original DPT file
        import_measurement_values(originalDptFile, new_measurement)

        print("Scan finished")

        # Prepare an empty response
        response_data = {}

        # Return a JSON response with a success status code (200)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        # Return an error response for invalid JSON data
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


# Define a endpoint to get the Progressbar of current scan in the OPUS
@api_view(['GET'])
def get_progressBar(request):
    try:
        url = '127.0.0.1'
        port = 80
        path = '/OpusCommand.htm?GET_PROGRESSBAR'
        prog = get_url_data(url, port, path).split('\n')[2].replace("\r", "")
        response_data = {'prog' : prog}
        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)



def send_post_request(url):
    try:
        # Send a POST request without data
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print('POST request successful')
            print('Response:', response.text)
        else:
            print(f'Error: {response.status_code} - {response.text}')

    except requests.exceptions.RequestException as e:
        print('Error sending POST request:', e)

# Function to retrieve data from a specified URL using HTTP GET
def get_url_data(host, port, path):
    try:
        request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"  # Create an HTTP GET request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        sock.connect((host, port))  # Connect to the server
        sock.sendall(request.encode())  # Send the HTTP GET request

        response = b''  # Initialize an empty byte string for response data
        while True:
            data = sock.recv(1024)  # Receive data from the server in 1024-byte chunks
            if not data:
                break
            response += data  # Append received data to the response

        response_str = response.decode('utf-8', 'ignore')  # Decode the bytes to a UTF-8 string
        return response_str  # Return the decoded response

    except socket.error as e:
        print(f"Socket error: {e}")  # Handle socket-related errors

# Function to run a macro using an OpusCommand URL
def runMacroReq(): 
    macro_file_name = 'test.mtx'  # Define the name of the macro file
    macro_path = 'C:\\Users\\Public\\Documents\\Bruker\\OPUS_8.1.29\\Macro'  # Define the path to the macro file
    encoded_macro_file_name = quote(macro_file_name)  # URL encode the macro file name
    encoded_macro_path = quote(macro_path)  # URL encode the macro path
    url = f'http://localhost/OpusCommand.htm?COMMAND_LINE RunMacro (,MFN = \'{encoded_macro_file_name}\',MPT = \'{encoded_macro_path}\')'  # Create the OpusCommand URL
    send_post_request(url)  # Send a POST request to run the macro

# Function to unload all data using an OpusCommand URL
def UnloadAll(): 
    url = f'http://localhost/OpusCommand.htm?COMMAND_LINE UnLoadAll (,)'
    send_post_request(url)

def deleteFile(file_to_delete): 
    
# If file exists, delete it.
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)
    else:
    # If it fails, inform the user.
        print("Error: %s file not found" % file_to_delete)
    
def get_progress():
    try:
        url = '127.0.0.1'
        port = 80
        path = '/OpusCommand.htm?GET_PROGRESSBAR'
        prog = get_url_data(url, port, path).split('\n')[2].replace("\r", "")
        response_data = {'prog' : prog}
        return float(prog)

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    

# this method imports the data form a file and saves it in the data base
def import_measurement_values(file_path, measurement_instance):
    measurement_values_list = []

    with open(file_path, 'r') as file:
        for line in file:
            wavelength, amplitude = map(float, line.strip().split())
            measurement_values_list.append(MeasurementValues(
                wavelength=wavelength,
                amplitude=amplitude,
                measurement=measurement_instance,
            ))

            # Save in batches, every 1000 records
            if len(measurement_values_list) >= 1000:
                MeasurementValues.objects.bulk_create(measurement_values_list)
                measurement_values_list = []
                print(1000)

    # Save any remaining records
    if measurement_values_list:
        MeasurementValues.objects.bulk_create(measurement_values_list)


def get_windows_username():
    try:
        # Get the username from the environment variables
        username = os.environ['USERNAME']
        return username
    except KeyError:
        # Handle the case where the 'USERNAME' environment variable is not defined
        return None