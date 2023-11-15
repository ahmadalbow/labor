import asyncio
import csv
import datetime
import math
import os
import threading
import time
import requests
import urllib.parse
class HMP4040:

    
    def __init__(self, ipaddresse):
        self.to_be_corrected_channels = []
        self.channels_power = {}
        self.ipaddresse = ipaddresse
        self.url = f"http://{self.ipaddresse}/scpi_response.txt"
        self.query("IDN?")


        ########################################


        self.interval_seconds = 10  # Default interval
        self.loop = asyncio.new_event_loop()
        self.is_saving_running = False
        self.file_path = None
        self.task = None

        #######################################      
                
        
        self.start_zyklus()

    def get_ip(self):
        return self.ipaddresse
    def get_name(self):
        return "hmp4040"
    def query(self,command):
        command = urllib.parse.quote(command)
        body = f"request={command}"
        try: 
            response = requests.post(self.url, data=body)
            return response.text
        except : 
            return 
        

    def set_volt(self, channel, volt):
        try:
            self.query(f"INST OUT{channel}")
            self.query(f"volt {volt}")
        except Exception as e:
            print(f"An error occurred while setting voltage for channel {channel}: {e}")

    def read_volt(self, channel):
        try:
            self.query(f"INST OUT{channel}")
            return float(self.query("MEAS:volt?"))
        except Exception as e:
            print(f"An error occurred while reading voltage for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    def read_volt_limit(self, channel):
        try:
            self.query(f"INST OUT{channel}")
            return float(self.query("volt?"))
        except Exception as e:
            print(f"An error occurred while reading voltage limit for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    def set_curr(self, channel, curr):
        try:
            self.query(f"INST OUT{channel}")
            self.query(f"CURR {curr}")
        except Exception as e:
            print(f"An error occurred while setting current for channel {channel}: {e}")

    def read_curr(self, channel):
        try:
            self.query(f"INST OUT{channel}")
            return float(self.query("MEAS:CURR?"))
        except Exception as e:
            print(f"An error occurred while reading current for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    def read_curr_limit(self, channel):
        try:
            self.query(f"INST OUT{channel}")
            return float(self.query("CURR?"))
        except Exception as e:
            print(f"An error occurred while reading current limit for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    def enable_Channel(self, channel):
        try:
            self.query(f"INST OUT{channel}")
            self.query(f"OUTP:SEL 1")
        except Exception as e:
            print(f"An error occurred while enabling channel {channel}: {e}")

    def disable_Channel(self, channel):
        try:
            self.query(f"INST OUT{channel}")
            self.query("OUTP:SEL 0")
        except Exception as e:
            print(f"An error occurred while disabling channel {channel}: {e}")

        

    def get_channels_satus(self):
        result = []
        for ch in range(1,5):
            self.query(f"INST OUT{ch}")
            try :
                status = int(self.query("OUTP:SEL?"))
            except:
                continue
            result.append((ch,status))
        return result
                

        

            
    def disable_output(self):
        try:
            self.query("OUTP:GEN 0")
        except Exception as e:
            print(f"An error occurred while disabling the output: {e}")

    def enable_output(self):
        try:
            self.query("OUTP:GEN 1")
        except Exception as e:
            print(f"An error occurred while enabling the output: {e}")

    def get_output_status(self):
        try:
            status = self.query("OUTP:GEN?")
            return int(status) if status is not None else None
        except Exception as e:
            print(f"An error occurred while getting the output status: {e}")
            return None



    def set_power(self,channel, power):
        self.channels_power[channel] = power
        self.query(f"INST OUT{channel}")
        self.set_volt(channel,0.1)
        time.sleep(0.7)
        R = self.read_volt(channel) / self.read_curr(channel)
        self.set_volt(channel,math.sqrt(power*R/2))
        time.sleep(0.7)
        R = self.read_volt(channel) / self.read_curr(channel)
        self.set_volt(channel,math.sqrt((3/4)*power * R ))
        time.sleep(0.7)
        R = self.read_volt(channel) / self.read_curr(channel)
        self.set_volt(channel,math.sqrt(power * R ))
    
    def read_power(self, channel):
        try:
            voltage = self.read_volt(channel)
            current = self.read_curr(channel)
            if voltage is not None and current is not None:
                return voltage * current
            else:
                return None
        except Exception as e:
            print(f"An error occurred while calculating power for channel {channel}: {e}")
            return None

    

 
    async def power_correcter(self):
        
        while True:
            print("")
            print("power_correcter is running ", self.ipaddresse)
            for channel in self.to_be_corrected_channels:

                try :
                    must_power = self.channels_power[channel]
                    V = self.read_volt(channel)
                    I = self.read_curr(channel) 
                    if V == 0:
                        self.set_power(channel, must_power)
                        continue
                    R = V/I
                    if self.read_curr_limit(channel) < math.sqrt(must_power / R):
                        self.set_curr(channel, math.sqrt(must_power / R))
                    
                    self.set_volt(channel, math.sqrt(must_power * R))

                    print("channel ",channel, " corrected to ", must_power )
                except :
                    pass
            print("")
            print("-----------------------------------------")                
            await asyncio.sleep(self.interval_seconds)




#######################################################
    def create_data(self):
        try:   
                    
            current_directory = os.path.dirname(__file__)
            # Specify the relative path to your data folder
            relative_folder_path = "Data_log"
            formatted_date_time = datetime.datetime.now().strftime("%d_%m_%Y %H_%M_%S")
            # Create the full file path by combining the current directory and relative path
            self.file_path = os.path.join(current_directory, relative_folder_path, f"{self.ipaddresse}_{formatted_date_time}.csv")
            print(f"{self.ipaddresse}_{formatted_date_time}.csv created")
            with open(self.file_path, 'a', newline='') as csvfile:
                # Create a csv.writer object
                csvwriter = csv.writer(csvfile)
        
                # Write the header row
                csvwriter.writerow(['Zeit', 'Kanal', 'Spannung', 'Strom', 'Leistung'])
                
            
        except Exception as e:
            print(f"An exception occurred: {e}")
    
    async def save_data(self):
        
        while True:           
            if ( self.is_saving_running):
                print("")
                print("saving is running ", self.ipaddresse)   
                with open(self.file_path, 'a', newline='') as csvfile:
                # Create a csv.writer object
                    csvwriter = csv.writer(csvfile)

                    for ch in self.get_channels_satus() :
                        if (ch[1]):                            
                            try :
                                formatted_date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                data = [formatted_date_time,ch[0],round(self.read_volt(ch[0]), 3),round(self.read_curr(ch[0]), 3),round(self.read_power(ch[0]), 3)]
                                csvwriter.writerow(data)
                                print(data, " saved")
                            except: 
                                pass
            await asyncio.sleep(self.interval_seconds)

    def run_periodically(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(asyncio.gather(self.save_data(),self.power_correcter()))

    def start_zyklus(self, interval_seconds = 10):
        self.interval_seconds = interval_seconds
        self.saving_task = threading.Thread(target=self.run_periodically)
        self.saving_task.daemon = True
        self.saving_task.start()





#######################################################
    
    def start_up(self):
        channels = [1,2,3,4]
        self.disable_output()
        for channel in channels:
            self.disable_Channel(channel)
            self.set_volt(channel,1)

 