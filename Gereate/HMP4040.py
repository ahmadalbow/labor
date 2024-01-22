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

    
    # Constructor for the HMP4040 class, initializes various attributes and starts a periodic task.
    def __init__(self, ipaddresse):
        # Initialize a list to keep track of channels that need correction.
        self.to_be_corrected_channels = []
        
        # Initialize a dictionary to store power values for each channel.
        self.channels_power = {}
        
        # Store the IP address of the device.
        self.ipaddresse = ipaddresse
        
        # Construct the URL for SCPI commands.
        self.url = f"http://{self.ipaddresse}/scpi_response.txt"
        
        # Send an initial SCPI command to query the device's identity.
        self.query("IDN?")
        
        ########################################

        # Set the default interval for the periodic task (in seconds).
        self.interval_seconds = 10
        
        # Create a new asyncio event loop.
        self.loop = asyncio.new_event_loop()
        
        # Flag to track if the data-saving task is running.
        self.is_saving_running = False
        
        # Store the file path where data will be saved.
        self.file_path = None
        
        # Initialize the periodic task.
        self.task = None

        #######################################

        # Start the periodic task for data correction and saving.
        self.start_zyklus()

    # Getter method to retrieve the device's IP address.
    def get_ip(self):
        return self.ipaddresse

    # Getter method to retrieve the device's name (hmp4040).
    def get_name(self):
        return "hmp4040"

    # Send an SCPI command to the device and return the response.
    def query(self, command):
        # Encode the command for use in the URL.
        command = urllib.parse.quote(command)
        
        # Create the request body with the encoded command.
        body = f"request={command}"
        
        try:
            # Send an HTTP POST request to the device's URL with the SCPI command.
            response = requests.post(self.url, data=body)
            
            # Return the response text.
            return response.text
        except:
            # Handle any exceptions and return an empty response on failure.
            return ""

        

    # Set voltage for a specific channel.
    def set_volt(self, channel, volt):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Set the voltage using another SCPI command.
            self.query(f"volt {volt}")
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while setting voltage for channel {channel}: {e}")

    # Read the voltage for a specific channel.
    def read_volt(self, channel):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Use an SCPI command to measure and return the voltage.
            return float(self.query("MEAS:volt?"))
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while reading voltage for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    # Read the voltage limit for a specific channel.
    def read_volt_limit(self, channel):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Use an SCPI command to read and return the voltage limit.
            return float(self.query("volt?"))
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while reading voltage limit for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    # Set current for a specific channel.
    def set_curr(self, channel, curr):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Set the current using another SCPI command.
            self.query(f"CURR {curr}")
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while setting current for channel {channel}: {e}")

    # Read the current for a specific channel.
    def read_curr(self, channel):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Use an SCPI command to measure and return the current.
            return float(self.query("MEAS:CURR?"))
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while reading current for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    # Read the current limit for a specific channel.
    def read_curr_limit(self, channel):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Use an SCPI command to read and return the current limit.
            return float(self.query("CURR?"))
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while reading current limit for channel {channel}: {e}")
            return None  # You might want to handle the error more gracefully.

    # Enable a specific channel.
    def enable_Channel(self, channel):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Use an SCPI command to enable the channel.
            self.query(f"OUTP:SEL 1")
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while enabling channel {channel}: {e}")

    # Disable a specific channel.
    def disable_Channel(self, channel):
        try:
            # Select the channel with an SCPI command.
            self.query(f"INST OUT{channel}")
            
            # Use an SCPI command to disable the channel.
            self.query("OUTP:SEL 0")
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while disabling channel {channel}: {e}")

        

    # Get the status of all channels (enabled or disabled).
    def get_channels_satus(self):
        result = []
        for ch in range(1, 5):
            self.query(f"INST OUT{ch}")
            try:
                status = int(self.query("OUTP:SEL?"))
            except:
                continue
            result.append((ch, status))
        return result

    # Disable the output of the device.
    def disable_output(self):
        try:
            self.query("OUTP:GEN 0")
        except Exception as e:
            print(f"An error occurred while disabling the output: {e}")

    # Enable the output of the device.
    def enable_output(self):
        try:
            self.query("OUTP:GEN 1")
        except Exception as e:
            print(f"An error occurred while enabling the output: {e}")

    # Get the status of the output (enabled or disabled).
    def get_output_status(self):
        try:
            status = self.query("OUTP:GEN?")
            return int(status) if status is not None else None
        except Exception as e:
            print(f"An error occurred while getting the output status: {e}")
            return None


    # Set the power for a specific channel.
    def set_power(self, channel, power):
        self.channels_power[channel] = power
        self.query(f"INST OUT{channel}")
        
        # Set the initial voltage to 0.1V for safety reasons.
        self.set_volt(channel, 0.1)
        time.sleep(0.7)
        
        # Calculate resistance (R) using voltage and current readings.
        R = self.read_volt(channel) / self.read_curr(channel)
        
        # Adjust the voltage to achieve the desired power (power factor correction).
        self.set_volt(channel, math.sqrt(power * R / 2))
        time.sleep(0.7)
        
        # Recalculate resistance (R).
        R = self.read_volt(channel) / self.read_curr(channel)
        
        # Further adjust voltage to fine-tune power.
        self.set_volt(channel, math.sqrt((3/4) * power * R))
        time.sleep(0.7)
        
        # Recalculate resistance (R) again.
        R = self.read_volt(channel) / self.read_curr(channel)
        
        # Final adjustment of voltage to reach the desired power.
        self.set_volt(channel, math.sqrt(power * R))

    # Read the power for a specific channel.
    def read_power(self, channel):
        try:
            # Read voltage and current values for the channel.
            voltage = self.read_volt(channel)
            current = self.read_curr(channel)
            
            if voltage is not None and current is not None:
                # Calculate and return the power by multiplying voltage and current.
                return voltage * current
            else:
                return None
        except Exception as e:
            # Handle any exceptions that may occur during the operation.
            print(f"An error occurred while calculating power for channel {channel}: {e}")
            return None

 
    # Asynchronous method to correct the power for specified channels.
    async def power_correcter(self):
        while True:
            print("")
            print("power_correcter is running ", self.ipaddresse)
            
            # Iterate through channels that need power correction.
            for channel in self.to_be_corrected_channels:
                try:
                    # Get the desired power for the channel.
                    must_power = self.channels_power[channel]
                    
                    # Read the current voltage and current values.
                    V = self.read_volt(channel)
                    I = self.read_curr(channel)
                    
                    # Check if voltage is 0, set power directly to the desired value using the set_power Method.
                    if V == 0:
                        self.set_power(channel, must_power)
                        continue
                    
                    # Calculate resistance (R) using voltage and current.
                    R = V / I
                    
                    # If the current limit is insufficient, adjust current.
                    if self.read_curr_limit(channel) < math.sqrt(must_power / R):
                        self.set_curr(channel, math.sqrt(must_power / R))
                    
                    # Adjust voltage to reach the desired power.
                    self.set_volt(channel, math.sqrt(must_power * R))
                    
                    print("channel ", channel, " corrected to ", must_power)
                except:
                    pass
            
            print("")
            print("-----------------------------------------")
            
            # Asynchronously sleep for the specified interval.
            await asyncio.sleep(self.interval_seconds)




#######################################################


    # Method to create a data file for logging measurements.
    def create_data(self):
        try:
            # Get the current directory where this script is located.
            current_directory = os.path.dirname(__file__)

            # Specify the relative path to your data folder.
            relative_folder_path = "Data_log"

            # Create a formatted date-time string.
            formatted_date_time = datetime.datetime.now().strftime("%d_%m_%Y %H_%M_%S")

            # Create the full file path by combining the current directory and relative path.
            self.file_path = os.path.join(current_directory, relative_folder_path, f"{self.ipaddresse}_{formatted_date_time}.csv")
            print(f"{self.ipaddresse}_{formatted_date_time}.csv created")

            # Open the file in append mode and create a CSV writer.
            with open(self.file_path, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)

                # Write the header row with column names.
                csvwriter.writerow(['Zeit', 'Kanal', 'Spannung', 'Strom', 'Leistung'])
        except Exception as e:
            print(f"An exception occurred: {e}")

    # Asynchronous method to continuously save data to the created CSV file.
    async def save_data(self):
        while True:
            # Check if data saving is running.
            if self.is_saving_running:
                print("")
                print("saving is running ", self.ipaddresse)
                with open(self.file_path, 'a', newline='') as csvfile:
                    # Create a CSV writer object.
                    csvwriter = csv.writer(csvfile)

                    # Iterate through channels and log data for active channels.
                    for ch in self.get_channels_satus():
                        if ch[1]:
                            try:
                                formatted_date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                data = [formatted_date_time, ch[0], round(self.read_volt(ch[0]), 3), round(self.read_curr(ch[0]), 3), round(self.read_power(ch[0]), 3)]
                                csvwriter.writerow(data)
                                print(data, " saved")
                            except:
                                pass
            # Asynchronously sleep for the specified interval.
            await asyncio.sleep(self.interval_seconds)

    # Method to run data saving and power correction tasks periodically.
    def run_periodically(self):
        # Set the event loop for asyncio.
        asyncio.set_event_loop(self.loop)

        # Run both the data saving and power correction tasks concurrently.
        self.loop.run_until_complete(asyncio.gather(self.save_data(), self.power_correcter()))

    # Method to start a periodic data saving and power correction task.
    def start_zyklus(self, interval_seconds=10):
        # Set the interval for data saving and power correction.
        self.interval_seconds = interval_seconds

        # Create a new thread for running tasks periodically.
        self.saving_task = threading.Thread(target=self.run_periodically)

        # Set the thread as a daemon thread to allow it to be terminated when the main program exits.
        self.saving_task.daemon = True

        # Start the thread to run the tasks periodically.
        self.saving_task.start()




#######################################################
    
    # Method to initialize the device startup configuration.
    def start_up(self):
        # List of channels to be configured during startup.
        channels = [1, 2, 3, 4]

        # Disable the device's output.
        self.disable_output()

        # Loop through each channel and perform startup configuration.
        for channel in channels:
            # Disable the channel.
            self.disable_Channel(channel)

            # Set the voltage for the channel to 1 volt.
            self.set_volt(channel, 1)


    