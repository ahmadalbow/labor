import time
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from Gereate.GereateManager import GereateManager
from Gereate.HMP4040 import HMP4040
from main import main
import csv
import os

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