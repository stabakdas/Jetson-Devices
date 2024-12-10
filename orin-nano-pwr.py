import subprocess
import time
import re

def run_tegrastats_vdd_in(duration):
    """
    Monitors the VDD_IN (total input power) using tegrastats for the specified duration
    and calculates the average power consumption.
    """
    # Start the tegrastats process
    process = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    start_time = time.time()
    total_vdd_in = 0
    count = 0

    try:
        # Read output from tegrastats in real-time
        while time.time() - start_time < duration:
            output = process.stdout.readline()
            if output:
                # Parse the VDD_IN value in the format `VDD_IN 3987mW/4000mW`
                vdd_in_data = re.search(r'VDD_IN (\d+)mW/\d+mW', output)
                if vdd_in_data:
                    vdd_in = int(vdd_in_data.group(1))  # Extract the first number (current power)
                    total_vdd_in += vdd_in
                    count += 1

                    # Print the current VDD_IN value
                    print(f"Current VDD_IN: {vdd_in} mW")
            else:
                break
    finally:
        process.kill()

    # Calculate and display the average VDD_IN power consumption
    if count > 0:
        average_vdd_in = total_vdd_in / count
        print(f"\nTotal VDD_IN: {total_vdd_in} mW")
        print(f"Average VDD_IN Power Consumption: {average_vdd_in:.2f} mW")
    else:
        print("No VDD_IN data collected.")

# Specify duration for monitoring in seconds
duration = 10
run_tegrastats_vdd_in(duration)
