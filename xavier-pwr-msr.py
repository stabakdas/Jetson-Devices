"""
#Reserved for commenting
# This script will represent various onboard power and  calculate the average total power consumption for the NVIDIA Jetson AGX Xavier Series.

# This script will run tegrastats for the specified duration, 
collect the power consumption data, Average them, and sum them up to compute total power consumption over the duration. 
The variable duration is set to 10 seconds by default but can be easily changed to any other value as needed.

# To run this script use this command sudo python3 xavier-pwr-msr.py from linux terminal on Jetson AGX Xavier

To understand the data generated of tegrastats. https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/text/AT/JetsonLinuxDevelopmentTools/TegrastatsUtility.html
Another Informational note https://forums.developer.nvidia.com/t/power-measurement-difference-on-jetson-agx-xavier/197659

"""
"""
import subprocess
import time
import re

def run_tegrastats(duration):
    # Start the tegrastats process
    process = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    start_time = time.time()
    
    # Initialize variables to store total power values for each component
    total_gpu_power = 0
    total_cpu_power = 0
    total_soc_power = 0
    total_cv_power = 0
    total_vddrq_power = 0
    total_sys5v_power = 0
    count = 0
    
    try:
        # Read output from tegrastats in real-time
        while time.time() - start_time < duration:
            output = process.stdout.readline()
            if output:
                # Parse the current power consumption values for each component
                power_data = re.findall(r'GPU (\d+)/\d+ CPU (\d+)/\d+ SOC (\d+)/\d+ CV (\d+)/\d+ VDDRQ (\d+)/\d+ SYS5V (\d+)/\d+', output)
                if power_data:
                    gpu_power, cpu_power, soc_power, cv_power, vddrq_power, sys5v_power = map(int, power_data[0])
                    total_gpu_power += gpu_power
                    total_cpu_power += cpu_power
                    total_soc_power += soc_power
                    total_cv_power += cv_power
                    total_vddrq_power += vddrq_power
                    total_sys5v_power += sys5v_power
                    count += 1

                    print(f"Current Power: GPU {gpu_power} mW, CPU {cpu_power} mW, SOC {soc_power} mW, CV {cv_power} mW, VDDRQ {vddrq_power} mW, SYS5V {sys5v_power} mW")
            else:
                break
    finally:
        process.kill()

    if count > 0:
        # Compute average power for each component
        avg_gpu_power = total_gpu_power / count
        avg_cpu_power = total_cpu_power / count
        avg_soc_power = total_soc_power / count
        avg_cv_power = total_cv_power / count
        avg_vddrq_power = total_vddrq_power / count
        avg_sys5v_power = total_sys5v_power / count
        total_average_power = avg_gpu_power + avg_cpu_power + avg_soc_power + avg_cv_power + avg_vddrq_power + avg_sys5v_power

        # Print results
        print("\nAverage Power Consumption over", duration, "seconds:")
        print(f"GPU: {avg_gpu_power:.2f} mW")
        print(f"CPU: {avg_cpu_power:.2f} mW")
        print(f"SOC: {avg_soc_power:.2f} mW")
        print(f"CV: {avg_cv_power:.2f} mW")
        print(f"VDDRQ: {avg_vddrq_power:.2f} mW")
        print(f"SYS5V: {avg_sys5v_power:.2f} mW")
        print(f"Total Average Power Consumption: {total_average_power:.2f} mW")
    else:
        print("No power data collected.")

duration = 10  # Duration in seconds
run_tegrastats(duration)
# Did not generate any output
"""
import subprocess
import time
import re

def run_tegrastats(duration):
    # Start the tegrastats process
    process = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    start_time = time.time()
    
    # Initialize variables to store total power values for each component
    total_gpu_power = 0
    total_cpu_power = 0
    total_soc_power = 0
    total_cv_power = 0
    total_vddrq_power = 0
    total_sys5v_power = 0
    count = 0
    
    try:
        # Read output from tegrastats in real-time
        while time.time() - start_time < duration:
            output = process.stdout.readline().strip()
            print("Raw output:", output)  # Print raw output for debugging

            if output:
                # Parse the current power consumption values for each component
                power_data = re.findall(r'GPU (\d+)/\d+ CPU (\d+)/\d+ SOC (\d+)/\d+ CV (\d+)/\d+ VDDRQ (\d+)/\d+ SYS5V (\d+)/\d+', output)
                print("Parsed data:", power_data)  # Print parsed data for debugging
                
                if power_data:
                    gpu_power, cpu_power, soc_power, cv_power, vddrq_power, sys5v_power = map(int, power_data[0])
                    total_gpu_power += gpu_power
                    total_cpu_power += cpu_power
                    total_soc_power += soc_power
                    total_cv_power += cv_power
                    total_vddrq_power += vddrq_power
                    total_sys5v_power += sys5v_power
                    count += 1

                    print(f"Current Power: GPU {gpu_power} mW, CPU {cpu_power} mW, SOC {soc_power} mW, CV {cv_power} mW, VDDRQ {vddrq_power} mW, SYS5V {sys5v_power} mW")
            else:
                break
    finally:
        process.kill()

    if count > 0:
        # Compute average power for each component
        avg_gpu_power = total_gpu_power / count
        avg_cpu_power = total_cpu_power / count
        avg_soc_power = total_soc_power / count
        avg_cv_power = total_cv_power / count
        avg_vddrq_power = total_vddrq_power / count
        avg_sys5v_power = total_sys5v_power / count
        total_average_power = avg_gpu_power + avg_cpu_power + avg_soc_power + avg_cv_power + avg_vddrq_power + avg_sys5v_power

        # Print results
        print("\nAverage Power Consumption over", duration, "seconds:")
        print(f"GPU: {avg_gpu_power:.2f} mW")
        print(f"CPU: {avg_cpu_power:.2f} mW")
        print(f"SOC: {avg_soc_power:.2f} mW")
        print(f"CV: {avg_cv_power:.2f} mW")
        print(f"VDDRQ: {avg_vddrq_power:.2f} mW")
        print(f"SYS5V: {avg_sys5v_power:.2f} mW")
        print(f"Total Average Power Consumption: {total_average_power:.2f} mW")
    else:
        print("No power data collected.")

duration = 10  # Duration in seconds
run_tegrastats(duration)


