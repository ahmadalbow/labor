import platform
import subprocess
import concurrent.futures
from .jds6600 import jds6600  # Assuming the jds6600 module is imported from a relative path

# This class manages various devices and provides methods to check device connectivity and retrieve connected devices.
class GereateManager:
    
    # Static method to check if a device with a given IP address is connected.
    @staticmethod
    def is_device_connected(ip_address):
        try:
            os_name = platform.system()
            # Check if the operating system is Windows
            if os_name == 'Windows':
                subprocess.check_output(['ping', '-w', '150', ip_address])
            
            # Check if the operating system is Linux
            elif os_name == 'Linux':
                subprocess.check_output(['ping', '-c', '1', '-W', '0.15', ip_address])
            
            # Handle other operating systems
            else:
                print(f'This is an unsupported operating system: {os_name}')
            
            return True
        except subprocess.CalledProcessError:
            return False

    # Static method to retrieve a list of connected devices.
    @staticmethod
    def getAngeschlosseneGereate():
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Define IP address ranges for different types of devices.
            ip_addresses_hmp4040 = ['192.168.179.' + str(i) for i in range(5, 11)]
            ip_addresses_hmp4040 += ['10.10.0.' + str(i) for i in range(5, 11)]
            
            ip_addresses_dmm6500 = ['10.10.0.' + str(i) for i in range(30, 40)]

            # Check connectivity for HMP4040 devices and add them to the result list.
            results_hmp4040 = list(executor.map(GereateManager.is_device_connected, ip_addresses_hmp4040))
            connected_ip_addresses_hmp4040 = [ip for ip, result in zip(ip_addresses_hmp4040, results_hmp4040) if result]
            for r in connected_ip_addresses_hmp4040:
                result.append(('HMP4040', r))
            
            # Check connectivity for DMM6500 devices and add them to the result list.
            results_dmm6500 = list(executor.map(GereateManager.is_device_connected, ip_addresses_dmm6500))
            connected_ip_addresses_dmm6500 = [ip for ip, result in zip(ip_addresses_dmm6500, results_dmm6500) if result]
            for r in connected_ip_addresses_dmm6500:
                result.append(('DMM6500', r))
            
            # Check for connected JDS6600 devices via USB on Linux.
            import glob
            os_name = platform.system()
            if os_name == 'Linux':
                usb_devices = glob.glob('/dev/ttyUSB*')
                if usb_devices:
                    for device in usb_devices:
                        try:
                            j = jds6600(device)
                            j.getinfo_devicetype()
                            result.append(('JDS6600', device))
                        except:
                            pass
        
        return result
