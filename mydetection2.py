#!/usr/bin/python3
"""
Object Detection with NVIDIA Jetson Inference Library
This Python script performs object detection on images using the NVIDIA Jetson Inference library. It leverages pre-trained models such as ssd-mobilenet-v2 to identify and classify objects within an image. 
The script also records detection time and saves the detection results to a specified .txt file.
Optionally save the processed image with bounding boxes indicating detected objects.

Prerequisites For the script
NVIDIA Jetson device (e.g., Jetson Nano, Jetson Orin)
NVIDIA Jetson Inference library installed
Required Python packages: jetson-inference, jetson-utils, argparse, time

Usage
Run the script with the following command:
python3 mydetection2.py <image_filename> --network <model_name> --threshold <detection_threshold> --output <output_file> --output_image <output_image_file>

For Example:
python3 mydetection2.py myimage.jpg --network ssd-mobilenet-v2 --threshold 0.5 --output detection_results.txt --output_image output_myimage.jpg

"""

import jetson.inference
import jetson.utils
import argparse
import time

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="filename of the image to process")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="model to use, can be: ssd-mobilenet-v2, ssd-inception-v2, etc.")
parser.add_argument("--threshold", type=float, default=0.5, help="detection threshold")
parser.add_argument("--output", type=str, default="detection_results.txt", help="output file for saving detection results")
args = parser.parse_args()

# Measure start time for detection
start_time = time.time()

# Load an image (into shared CPU/GPU memory)
img = jetson.utils.loadImage(args.filename)

# Load the object detection network
net = jetson.inference.detectNet(args.network, threshold=args.threshold)

# Perform object detection
detections = net.Detect(img)

# Measure end time for detection
end_time = time.time()
detection_time = end_time - start_time

# Save the detection results to the specified text file
with open(args.output, 'w') as f:
    f.write(f"Detected {len(detections)} objects in image\n")
    for detection in detections:
        class_desc = net.GetClassDesc(detection.ClassID)
        f.write(f"Detected {class_desc} (class #{detection.ClassID}) with {detection.Confidence * 100:.2f}% confidence at location "
                f"({int(detection.Left)}, {int(detection.Top)}) with dimensions ({int(detection.Width)}, {int(detection.Height)})\n")
    
    # Log detection time and power consumption
    f.write(f"\nDetection time: {detection_time:.4f} seconds\n")
    # If you have power consumption data, append it here as well

print(f"Detection results saved to {args.output}")

# Save the output image with bounding boxes
output_image_path = "output_" + args.filename
jetson.utils.saveImage(output_image_path, img)
print(f"Output image saved to {output_image_path}")
