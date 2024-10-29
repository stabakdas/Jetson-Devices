"""
# This script will calculate total and average power consumption for Nano series Nvidia Jetson Devices

# This script will run tegrastats for the specified duration, 
collect the power consumption data, sum up the total power consumption, 
and calculate the average power consumption over the duration. 
The variable duration is set to 10 seconds by default but can be easily changed to any other value as needed.

# To run this script use this command sudo python3 nano-pwr-msr.py from linux terminal
Reference for calculation method:
https://forums.developer.nvidia.com/t/power-consumption-monitoring/73608
"""
import subprocess
import time
import re

def run_tegrastats(duration):
    # Start the tegrastats process
    process = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    start_time = time.time()
    total_input_power = 0
    total_gpu_power = 0
    total_cpu_power = 0
    count = 0
    
    try:
        # Read output from tegrastats in real-time
        while time.time() - start_time < duration:
            output = process.stdout.readline()
            if output:
                # Parse the current power consumption values
                power_data = re.findall(r'POM_5V_IN (\d+)/\d+ POM_5V_GPU (\d+)/\d+ POM_5V_CPU (\d+)/\d+', output)
                if power_data:
                    input_power, gpu_power, cpu_power = map(int, power_data[0])
                    total_input_power += input_power
                    total_gpu_power += gpu_power
                    total_cpu_power += cpu_power
                    count += 1

                    print(f"Current POM_5V_IN: {input_power} mW, POM_5V_GPU: {gpu_power} mW, POM_5V_CPU: {cpu_power} mW")
            else:
                break
    finally:
        process.kill()

    if count > 0:
        """
        #total_power = total_input_power + total_gpu_power + total_cpu_power
        """
        average_power = total_input_power / count
        print(f"Total POM_5V_IN: {total_input_power} mW")
        print(f"Total POM_5V_GPU: {total_gpu_power} mW")
        print(f"Total POM_5V_CPU: {total_cpu_power} mW")
        print(f"Total Input Power Consumption: {total_power} mW")
        print(f"Average Power Consumption: {average_power:.2f} mW")
    else:
        print("No power data collected.")

duration = 10
run_tegrastats(duration)
