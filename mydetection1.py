#!/usr/bin/python3
"""
Object Detection with NVIDIA Jetson Inference Library
This Python script performs object detection on images using the NVIDIA Jetson Inference library. It leverages pre-trained models such as ssd-mobilenet-v2 to identify and classify objects within an image. 
The script also records detection time, CPU usage, and GPU usage, saving these details along with the detection results to a specified .txt file.
Optionally save the processed image with bounding boxes indicating detected objects.

Prerequisites For the script
NVIDIA Jetson device (e.g., Jetson Nano, Jetson Orin)
NVIDIA Jetson Inference library installed
Required Python packages: jetson-inference, jetson-utils, argparse, logging, psutil, subprocess, time

Usage
Run the script with the following command:
python3 mydetection1.py <image_filename> --network <model_name> --threshold <detection_threshold> --output <output_file> --output_image <output_image_file>

For Example:
python3 mydetection1.py myimage.jpg --network ssd-mobilenet-v2 --threshold 0.5 --output detection_results.txt --output_image output_myimage.jpg

"""

import jetson.inference
import jetson.utils
import argparse
import logging
import psutil
import subprocess
import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of the image to process")
    parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="Model to use, e.g., ssd-mobilenet-v2, ssd-inception-v2, etc.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Detection threshold")
    parser.add_argument("--output", type=str, default="detection_results.txt", help="Output file for saving detection results")
    parser.add_argument("--output_image", type=str, help="Output image file to save the image with bounding boxes")
    return parser.parse_args()

def load_image(filename):
    try:
        return jetson.utils.loadImage(filename)
    except Exception as e:
        logging.error(f"Failed to load image {filename}: {e}")
        raise

def perform_detection(net, img, threshold):
    try:
        return net.Detect(img, int(threshold * 100))  # Convert float to integer percentage
    except Exception as e:
        logging.error(f"Detection failed: {e}")
        raise

def save_results(detections, net, output_file, detection_time):
    try:
        with open(output_file, 'w') as f:
            f.write(f"Detected {len(detections)} objects in image\n")
            for detection in detections:
                class_desc = net.GetClassDesc(detection.ClassID)
                f.write(f"Detected {class_desc} (class #{detection.ClassID}) with {detection.Confidence * 100:.2f}% confidence at location ({int(detection.Left)}, {int(detection.Top)}) with dimensions ({int(detection.Width)}, {int(detection.Height)})\n")
            
            f.write(f"\nDetection Time: {detection_time:.4f} seconds\n")

            cpu_usage = psutil.cpu_percent(interval=1)
            f.write(f"CPU Usage: {cpu_usage}%\n")

            gpu_usage = get_gpu_usage()
            f.write(f"GPU Usage: {gpu_usage}\n")

        logging.info(f"Detection results saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to save detection results to {output_file}: {e}")
        raise

def save_image(img, output_image_path):
    try:
        jetson.utils.saveImage(output_image_path, img)
        logging.info(f"Output image saved to {output_image_path}")
    except Exception as e:
        logging.error(f"Failed to save output image to {output_image_path}: {e}")
        raise

def get_gpu_usage():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode('utf-8'))
        return result.stdout.decode('utf-8').strip() + "%"
    except Exception as e:
        logging.error(f"Failed to get GPU usage: {e}")
        return "N/A"

def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()

    img = load_image(args.filename)
    net = jetson.inference.detectNet(args.network, threshold=args.threshold)

    start_time = time.time()
    detections = perform_detection(net, img, args.threshold)
    end_time = time.time()
    detection_time = end_time - start_time

    save_results(detections, net, args.output, detection_time)

    output_image_path = args.output_image if args.output_image else f"output_{args.filename}"
    save_image(img, output_image_path)

if __name__ == "__main__":
    main()
