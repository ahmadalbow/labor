import subprocess
import concurrent.futures
from .jds6600 import jds6600
class GereateManager:


    
    @staticmethod
    def is_device_connected(ip_address):
        try:
        # Run the ping command with a single packet and a timeout of 2 seconds.
            subprocess.check_output(['ping', '-w', '20', ip_address])
            return True
        except subprocess.CalledProcessError:
            return False      
        
    @staticmethod
    def getAngeschlosseneGereate():
        result = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
           ip_addresses = ['192.168.179.' + str(i) for i in range(4, 11)]
           results = list(executor.map(GereateManager.is_device_connected, ip_addresses))
           connected_ip_addresses = [ip for ip, result in zip(ip_addresses, results) if result]
           print(connected_ip_addresses)
           for r in connected_ip_addresses:
               result.append(('HMP4040',r))
            
           ip_addresses = ['10.10.0.' + str(i) for i in range(30, 40)]
           results = list(executor.map(GereateManager.is_device_connected, ip_addresses))
           connected_ip_addresses = [ip for ip, result in zip(ip_addresses, results) if result]
           for r in connected_ip_addresses:
               result.append(('DMM6500',r))
        import glob

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


            
     