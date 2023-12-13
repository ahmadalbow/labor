import platform
import subprocess
import concurrent.futures
from .jds6600 import jds6600
class GereateManager:


    
    @staticmethod
    def is_device_connected(ip_address):
        try:
            os_name = platform.system()
            # Check if the operating system is Windows
            if os_name == 'Windows':
                    
                subprocess.check_output(['ping', "-w" ,'150', ip_address])


            # Check if the operating system is Linux
            elif os_name == 'Linux':
                subprocess.check_output(['ping', '-c', '1', '-W', '0.15', ip_address])
            # Handle other operating systems
            else:
                print(f'This is an unsupported operating system: {os_name}')
            return True
        except subprocess.CalledProcessError:
            return False      
        
    @staticmethod
    def getAngeschlosseneGereate():
        result = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
           ip_addresses = ['192.168.179.' + str(i) for i in range(5, 11)]
           results = list(executor.map(GereateManager.is_device_connected, ip_addresses))
           connected_ip_addresses = [ip for ip, result in zip(ip_addresses, results) if result]
           for r in connected_ip_addresses:
               result.append(('HMP4040',r)) 
        
           ip_addresses = ['10.10.0.' + str(i) for i in range(5, 11)]
           results = list(executor.map(GereateManager.is_device_connected, ip_addresses))
           connected_ip_addresses = [ip for ip, result in zip(ip_addresses, results) if result]
           for r in connected_ip_addresses:
               result.append(('HMP4040',r))
           ip_addresses = ['10.10.0.' + str(i) for i in range(30, 40)]
           results = list(executor.map(GereateManager.is_device_connected, ip_addresses))
           connected_ip_addresses = [ip for ip, result in zip(ip_addresses, results) if result]
           for r in connected_ip_addresses:
               result.append(('DMM6500',r))
        
        import glob
        os_name = platform.system()
            # Check if the operating system is Windows
        if os_name == 'Linux':            
            usb_devices = glob.glob('/dev/ttyUSB*')
            if usb_devices:
                for device in usb_devices:
                    try:
                        j = jds6600(device)        
                        j.getinfo_devicetype()           
                        result.append(('JDS6600',device))
                    except:
                        pass
        return result


            
     