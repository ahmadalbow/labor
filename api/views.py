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
@api_view(['GET'])
def getAngeschlosseneGereate(request):
    return Response(GereateManager.getAngeschlosseneGereate())

@api_view(['GET'])
def hmp4040_measure(request):
    try:
        
        hmp4040 = main.get_device(request.GET.get('ip', None))
        if not hmp4040 == None:
            # Process the data as needed
            response_data = {'1' : [hmp4040.read_volt(1),hmp4040.read_curr(1),hmp4040.read_power(1)],
                            '2' : [hmp4040.read_volt(2),hmp4040.read_curr(2),hmp4040.read_power(2)],
                            '3' : [hmp4040.read_volt(3),hmp4040.read_curr(3),hmp4040.read_power(3)],
                            '4' : [hmp4040.read_volt(4),hmp4040.read_curr(4),hmp4040.read_power(4)]}
            return JsonResponse(response_data, status=200)
        else:
            JsonResponse({}, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@api_view(['POST'])
def auto_corrector_add_ch(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        ip = data.get('ip')
        hmp4040 = main.get_device(ip)

        ch = int(data.get('ch'))
        print("sollwert : ",float(data.get('sollwert')))
        sollwert = float(data.get('sollwert'))
        hmp4040.channels_power[ch] = sollwert
        hmp4040.to_be_corrected_channels.append(ch)
        response_data = {}
        return JsonResponse(response_data, status=200)
    except ZeroDivisionError:
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
@api_view(['POST'])
def auto_corrector_remove_ch(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))
        ip = data.get('ip')
        hmp4040 = main.get_device(ip)
        ch = int(data.get('ch'))
        if (hmp4040.to_be_corrected_channels.__contains__(ch)):
            hmp4040.to_be_corrected_channels.remove(ch)
        # Process the data as needed
        
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)    

@api_view(['POST'])
def channel_aktivieren(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        hmp4040 = main.get_device(data.get('ip'))

                # Process the data as needed
        hmp4040.enable_Channel(int(data.get('ch')))   
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)    
    
@api_view(['POST'])
def channel_deaktivieren(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        hmp4040 = main.get_device(data.get('ip'))

                # Process the data as needed
        hmp4040.disable_Channel(int(data.get('ch')))   
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)    
    
@api_view(['POST'])
def out_aktivieren(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        hmp4040 = main.get_device(data.get('ip'))
                # Process the data as needed
        hmp4040.enable_output()   
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)   
@api_view(['POST'])
def out_deaktivieren(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        hmp4040 = main.get_device(data.get('ip'))

                # Process the data as needed
        hmp4040.disable_output()   
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)  
    
@api_view(['POST'])
def start_saving_Data(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        ip = data.get('ip')
        hmp4040 = main.get_device(ip)
        hmp4040.create_data()
        hmp4040.is_saving_running = True
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)  
    
@api_view(['POST'])
def stop_saving_Data(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        ip = data.get('ip')
        hmp4040 = main.get_device(ip)
        hmp4040.is_saving_running = False
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)  
    

@api_view(['POST'])
def set_power(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        ip = data.get('ip')
        ch = data.get("ch")
        power = data.get("power")
        hmp4040 = main.get_device(ip)
        hmp4040.set_power(ch,power)
        response_data = {}
        time.sleep(1)
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)  
@api_view(['POST'])
def set_volt(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        ip = data.get('ip')
        ch = data.get("ch")
        volt = float(data.get("volt"))
        hmp4040 = main.get_device(ip)
        hmp4040.set_volt(ch,volt)
        response_data = {}
        return JsonResponse(response_data, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)  
@api_view(['GET'])
def read_voltage(request):
    try:
        hmp4040 = main.get_device(request.GET.get('ip', None))
        if not hmp4040 == None:
            # Process the data as needed
            response_data = {'volt' : hmp4040.read_volt(1)}
            return JsonResponse(response_data, status=200)
        else:
            JsonResponse({}, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
@api_view(['GET'])
def read_curr(request):
    try:
        hmp4040 = main.get_device(request.GET.get('ip', None))
        if not hmp4040 == None:
            # Process the data as needed
            response_data = {'curr' : hmp4040.read_curr(1)}
            return JsonResponse(response_data, status=200)
        else:
            JsonResponse({}, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    

@api_view(['POST'])
def scan(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        hmp4040 = main.get_device(data.get('ip'))
        unterverzeichnis = data.get('unterverzeichnis')
        strahlertyp = data.get('strahlertyp')
        strahlernummer = data.get('strahlernummer')
        soll_leistung = data.get('soll_leistung')
        comment = data.get('comment')
        hmp4040.enable_Channel(1)
        hmp4040.enable_output()
        hmp4040.set_power(1,float(soll_leistung))
        time.sleep(1)
        voltage =  round(hmp4040.read_volt(1), 2)
        current =  round(1000*hmp4040.read_curr(1), 1)

        formatted_date = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        fileName = f"{formatted_date}_{strahlertyp}_{soll_leistung}W_{voltage}V_{current}mA_{strahlernummer}_{comment}"
        url = f'http://localhost/OpusCommand.htm?COMMAND_LINE MeasureSample (,{{EXP= EXP_TR_an.xpm,XPP=\'C:\\Users\\Public\\Documents\\Bruker\\OPUS_8.1.29\\XPM\',NSS=16,SFM=\'{fileName}\',PTH=\'C:\\Users\\i40014683\\Endress+Hauser\\Infrasolid GmbH - Documents\\07_Produktion\\13_Prozessdaten\\03_FTIR\\{unterverzeichnis}\\\' }});'
        send_post_request(url)
                # Process the data as needed
        source_folder = f'C:/Users/i40014683/Endress+Hauser/Infrasolid GmbH - Documents/07_Produktion/13_Prozessdaten/03_FTIR/{unterverzeichnis}/'
        temp_folder = 'C:/temp/test/'
        
        new_measurement = Measurement(
            date=datetime.datetime.now(),
            type=strahlertyp,
            set_power_W=soll_leistung,
            current_mA=current,
            voltage_V=voltage,
            serial_number=strahlernummer,
            comment=comment,
        )

        time.sleep(6)

        while(get_progress() != 0):
            print(get_progress())
            time.sleep(1)
        print("creating files started")
        hmp4040.disable_output()
        originalFile = source_folder + fileName + ".0"
        UnloadAll()
        time.sleep(0.2)
        shutil.copy(originalFile, temp_folder)
        runMacroReq()
        time.sleep(0.2)
        dptTempFile = temp_folder + fileName + ".0.dpt"
        originalTempFile = temp_folder + fileName + ".0"
        shutil.copy(dptTempFile, source_folder)   
        time.sleep(0.2)
        deleteFile(dptTempFile)
        deleteFile(originalTempFile)
        originalDptFile = originalFile + ".dpt"
        new_measurement.save(using='mysql_db')

        import_measurement_values(originalDptFile,new_measurement)
        print("scan finished")
        response_data = {}
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

def get_url_data(host, port, path):
    try:
        request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        sock.connect((host, port))

        # Send the HTTP GET request
        sock.sendall(request.encode())

        # Receive the response data from the server
        response = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data

        # Decode the bytes to string (optional)
        response_str = response.decode('utf-8', 'ignore')

        return response_str

    except socket.error as e:
        print(f"Socket error: {e}")

def runMacroReq(): 
    macro_file_name = 'test.mtx'
    macro_path = 'C:\\Users\\Public\\Documents\\Bruker\\OPUS_8.1.29\\Macro'

# Encode the URL parameters
    encoded_macro_file_name = quote(macro_file_name)
    encoded_macro_path = quote(macro_path)
    url = f'http://localhost/OpusCommand.htm?COMMAND_LINE RunMacro (,MFN = \'{encoded_macro_file_name}\',MPT = \'{encoded_macro_path}\')'
    send_post_request(url)

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
    

def import_measurement_values(file_path, measurement_instance):
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into wavelength and amplitude
            wavelength, amplitude = map(float, line.strip().split())

            # Create MeasurementValues object
            measurement_values = MeasurementValues(
                wavelength=wavelength,
                amplitude=amplitude,
                measurement=measurement_instance,
            )

            # Save the object to the database
            measurement_values.save(using='mysql_db')