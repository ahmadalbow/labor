from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from Gereate.GereateManager import GereateManager
from Gereate.HMP4040 import HMP4040
from main import main
import platform
# Create your views here.

def index(request):
    os_name = platform.system()
    if os_name == 'Windows':
        print('This is a Windows operating system.')
    # Check if the operating system is Linux
    elif os_name == 'Linux':
        print('This is a Linux operating system.')
    # Handle other operating systems
    else:
        print(f'This is an unsupported operating system: {os_name}')
    return render(request, 'pages/index.html',{'ahmad': [1,2,3,4,5]})

def gereate(request):
    AngeschlosseneGereate = GereateManager.getAngeschlosseneGereate()
    return render(request, 'pages/gereate.html',{'AG':AngeschlosseneGereate})

def hmp4040(request,ip):

    if main.contains(ip) and main.get_device(ip).get_name() == "hmp4040":
        hmp4040 = main.get_device(ip)
        to_be_corrected_channels = hmp4040.to_be_corrected_channels
        print('allready exists')
    else :
        try:
            hmp4040 = HMP4040(ip)
            
            main.Devices.append(hmp4040)
            to_be_corrected_channels= []
            print('device created')
        except requests.exceptions.ConnectionError as e:
            return render( request,'pages/notfound.html')
        
    if request.method == 'POST':
        try:
            unit = request.POST.get("custom-radio-group")
            value = request.POST.get("value")
            zyklus = request.POST.get("zyklus")
            if not zyklus == None:
                try : 
                    zyklus = float(zyklus)
                    hmp4040.interval_seconds = zyklus
                    return redirect( f'/HMP4040/{ip}')
                except:
                    return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels, "isSavingRunning" : hmp4040.is_saving_running,"error" : "Du hast keinen gültigen Wert eingegeben"})    


            try :
                value = float(value)
            except:
                return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels, "isSavingRunning" : hmp4040.is_saving_running,"error" : "Du hast keinen gültigen Wert eingegeben"})    

            selected_channels = []
            for i in range(1,5):
                selected_channels.append((i,request.POST.get(f'sel_ch{i}')))
            for i in range(0,4):
                if selected_channels[i][1] == 'on':
                    break
                if (i == 3 ):
                    return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels, "isSavingRunning" : hmp4040.is_saving_running,"error" : "Du hast keinen Kanal ausgewählt"})    
            

            if value:
                for ch in selected_channels:
                    if ch[1]:
                        if (unit == "V"):
                            hmp4040.set_volt(ch[0],float(value))
                        elif (unit == "A"):
                            hmp4040.set_curr(ch[0],float(value))
                        elif (unit == "W"):
                            hmp4040.set_power(ch[0],float(value))
                        else :
                            return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels, "isSavingRunning" : hmp4040.is_saving_running,"error" : "Du hast keine Einheit ausgewählt"})


            return redirect( f'/HMP4040/{ip}')
        except ZeroDivisionError:
            return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels, "isSavingRunning" : hmp4040.is_saving_running,"error" : "Du hast entweder einen ungültigen Wert eingegeben oder der ausgewählte Kanal ist nicht aktiv."})
        except Exception as e:
            return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels, "isSavingRunning" : hmp4040.is_saving_running,"error" : str(e)})    

    return render(request, 'pages/hmp4040.html',{'ip': ip,'channels_status' : hmp4040.get_channels_satus(),'out' : hmp4040.get_output_status(),"to_be_corrected_channels" : to_be_corrected_channels,"isSavingRunning" : hmp4040.is_saving_running,'channels_power' : hmp4040.channels_power,'zyklus' : hmp4040.interval_seconds})