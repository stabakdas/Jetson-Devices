"""
# This script will calculate total and average power consumption for agx series Nvidia Jetson Devices

# This script will run tegrastats for the specified duration, 
collect the power consumption data, sum up the total power consumption, 
and calculate the average power consumption over the duration. 
The variable duration is set to 10 seconds by default but can be easily changed to any other value as needed.

# To run this script use this command sudo python3 agx-orin-pwr-msr.py from linux terminal
"""

import subprocess
import time
import re

def run_tegrastats(duration):
    # Start the tegrastats process
    process = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    start_time = time.time()
    
    # Initialize variables to store total power values for each component
    total_vdd_gpu_soc = 0
    total_vdd_cpu_cv = 0
    total_vin_sys_5v0 = 0
    total_vddq_vdd2_1v8ao = 0
    count = 0
    
    try:
        # Read output from tegrastats in real-time
        while time.time() - start_time < duration:
            output = process.stdout.readline().strip()
            #print("Raw output:", output)  # Print raw output for debugging
            if output:
                # Updated regex pattern to match the new format
                power_data = re.findall(r'VDD_GPU_SOC (\d+)mW/.* VDD_CPU_CV (\d+)mW/.* VIN_SYS_5V0 (\d+)mW/.* VDDQ_VDD2_1V8AO (\d+)mW/.*', output)
                #print("Parsed data:", power_data)  # Print parsed data for debugging
                
                if power_data:
                    vdd_gpu_soc, vdd_cpu_cv, vin_sys_5v0, vddq_vdd2_1v8ao = map(int, power_data[0])
                    total_vdd_gpu_soc += vdd_gpu_soc
                    total_vdd_cpu_cv += vdd_cpu_cv
                    total_vin_sys_5v0 += vin_sys_5v0
                    total_vddq_vdd2_1v8ao += vddq_vdd2_1v8ao
                    count += 1

                    print(f"Current Power: VDD_GPU_SOC {vdd_gpu_soc} mW, VDD_CPU_CV {vdd_cpu_cv} mW, VIN_SYS_5V0 {vin_sys_5v0} mW, VDDQ_VDD2_1V8AO {vddq_vdd2_1v8ao} mW")
            else:
                break
    finally:
        process.kill()

    if count > 0:
        # Compute average power for each component
        avg_vdd_gpu_soc = total_vdd_gpu_soc / count
        avg_vdd_cpu_cv = total_vdd_cpu_cv / count
        avg_vin_sys_5v0 = total_vin_sys_5v0 / count
        avg_vddq_vdd2_1v8ao = total_vddq_vdd2_1v8ao / count
        total_average_power = avg_vdd_gpu_soc + avg_vdd_cpu_cv + avg_vin_sys_5v0 + avg_vddq_vdd2_1v8ao

        # Print results
        print("\nAverage Power Consumption over", duration, "seconds:")
        print(f"VDD_GPU_SOC: {avg_vdd_gpu_soc:.2f} mW")
        print(f"VDD_CPU_CV: {avg_vdd_cpu_cv:.2f} mW")
        print(f"VIN_SYS_5V0: {avg_vin_sys_5v0:.2f} mW")
        print(f"VDDQ_VDD2_1V8AO: {avg_vddq_vdd2_1v8ao:.2f} mW")
        print(f"Total Average Power Consumption: {total_average_power:.2f} mW")
    else:
        print("No power data collected.")

# Duration for monitoring (in seconds)
duration = 10
run_tegrastats(duration)

