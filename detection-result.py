#!/usr/bin/python3

"""
This script performs object detection using the Jetson Inference library on NVIDIA Jetson devices such as the Jetson Nano or Jetson Orin, etc. 
It processes an input image, detects objects, and saves the detection results in a .txt file. By default, the results are saved to 'detection_results.txt', 
but this can be changed using the --output argument. 
Additionally, the script saves an output image with bounding boxes indicating detected objects.

You can find the detection results in the specified .txt file in your mounted directory.

For more details on how to set up and mount a folder for Jetson Inference projects, please refer to the official NVIDIA GitHub repository: 
https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-example-python-2.md#setting-up-the-project

To use a different pre-trained model, modify the --network argument. For a list of available pre-trained detection models, 
please refer to the following GitHub repository: https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-console-2.md#pre-trained-detection-models-available


Usage example:
python3 detection-result.py <image_filename> --network ssd-mobilenet-v2 --threshold 0.5 --output custom_results.txt
"""

import jetson.inference
import jetson.utils
import argparse

# Parse the command line
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="filename of the image to process")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="model to use, can be: ssd-mobilenet-v2, ssd-inception-v2, etc.")
parser.add_argument("--threshold", type=float, default=0.5, help="detection threshold")
parser.add_argument("--output", type=str, default="detection_results.txt", help="output file for saving detection results")
args = parser.parse_args()

# Load an image (into shared CPU/GPU memory)
img = jetson.utils.loadImage(args.filename)

# Load the object detection network
net = jetson.inference.detectNet(args.network, threshold=args.threshold)

# Perform object detection
detections = net.Detect(img)

# Save the detection results to the specified text file
with open(args.output, 'w') as f:
    f.write("Detected {:d} objects in image\n".format(len(detections)))
    for detection in detections:
        class_desc = net.GetClassDesc(detection.ClassID)
        f.write("Detected {:s} (class #{:d}) with {:.2f}% confidence at location ({:d}, {:d}) with dimensions ({:d}, {:d})\n".format(
            class_desc, detection.ClassID, detection.Confidence * 100, 
            int(detection.Left), int(detection.Top), int(detection.Width), int(detection.Height)))

print(f"Detection results saved to {args.output}")

# Save the output image with bounding boxes
output_image_path = "output_" + args.filename
jetson.utils.saveImage(output_image_path, img)
print(f"Output image saved to {output_image_path}")
