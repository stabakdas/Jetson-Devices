"""
# This script will calculate total and average power consumption for agx series Nvidia Jetson Devices

# This script will run tegrastats for the specified duration, 
collect the power consumption data, sum up the total power consumption, 
and calculate the average power consumption over the duration. 
The variable duration is set to 10 seconds by default but can be easily changed to any other value as needed.

# To run this script use this command sudo python3 agx-orin-pwr-msr.py from linux terminal
"""
"""
import subprocess
import re
import time

# Function to parse the tegrastats output
def parse_tegrastats_output(output):
    vdd_gpu_soc = []
    vdd_cpu_cv = []
    vin_sys_5v0 = []
    vddq_vdd2_1v8ao = []

    for line in output:
        if "VDD_GPU_SOC" in line and "VDD_CPU_CV" in line and "VIN_SYS_5V0" in line and "VDDQ_VDD2_1V8AO" in line:
            vdd_gpu_soc_value = re.search(r'VDD_GPU_SOC (\d+)', line)
            vdd_cpu_cv_value = re.search(r'VDD_CPU_CV (\d+)', line)
            vin_sys_5v0_value = re.search(r'VIN_SYS_5V0 (\d+)', line)
            vddq_vdd2_1v8ao_value = re.search(r'VDDQ_VDD2_1V8AO (\d+)', line)

            if vdd_gpu_soc_value:
                vdd_gpu_soc.append(int(vdd_gpu_soc_value.group(1)))
            if vdd_cpu_cv_value:
                vdd_cpu_cv.append(int(vdd_cpu_cv_value.group(1)))
            if vin_sys_5v0_value:
                vin_sys_5v0.append(int(vin_sys_5v0_value.group(1)))
            if vddq_vdd2_1v8ao_value:
                vddq_vdd2_1v8ao.append(int(vddq_vdd2_1v8ao_value.group(1)))

    return vdd_gpu_soc, vdd_cpu_cv, vin_sys_5v0, vddq_vdd2_1v8ao

# Duration for running tegrastats (in seconds)
duration = 10

# Run tegrastats for the specified duration
tegrastats_process = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

output = []
start_time = time.time()
while time.time() - start_time < duration:
    line = tegrastats_process.stdout.readline()
    if line:
        output.append(line.strip())

tegrastats_process.terminate()

# Parse the output
vdd_gpu_soc, vdd_cpu_cv, vin_sys_5v0, vddq_vdd2_1v8ao = parse_tegrastats_output(output)

# Sum the values
total_vdd_gpu_soc = sum(vdd_gpu_soc)
total_vdd_cpu_cv = sum(vdd_cpu_cv)
total_vin_sys_5v0 = sum(vin_sys_5v0)
total_vddq_vdd2_1v8ao = sum(vddq_vdd2_1v8ao)

# Calculate total power consumption and average power consumption
total_power = total_vdd_gpu_soc + total_vdd_cpu_cv + total_vin_sys_5v0 + total_vddq_vdd2_1v8ao
average_power = total_power / duration

print(f"Total VDD_GPU_SOC: {total_vdd_gpu_soc} mW")
print(f"Total VDD_CPU_CV: {total_vdd_cpu_cv} mW")
print(f"Total VIN_SYS_5V0: {total_vin_sys_5v0} mW")
print(f"Total VDDQ_VDD2_1V8AO: {total_vddq_vdd2_1v8ao} mW")
print(f"Total Power Consumption: {total_power} mW")
print(f"Average Power Consumption: {average_power:.2f} mW")
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
            if output:
                # Updated regex pattern to match the new format
                power_data = re.findall(r'VDD_GPU_SOC (\d+) VDD_CPU_CV (\d+) VIN_SYS_5V0 (\d+) VDDQ_VDD2_1V8AO (\d+)', output)
                
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

