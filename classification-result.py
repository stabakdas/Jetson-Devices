#This script will be useful to run a detection program inside the jetson inference and save the output or classification result in a .txt file. 

import jetson.inference
import jetson.utils
import argparse

# Parse the command line
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="filename of the image to process")
parser.add_argument("--network", type=str, default="googlenet", help="model to use, can be:  googlenet, resnet-18, etc. (see --help for others)")
parser.add_argument("--output", type=str, default="result.txt", help="filename of the output text file")
args = parser.parse_args()

# Load the image
img = jetson.utils.loadImage(args.filename)

# Load the recognition network
net = jetson.inference.imageNet(args.network)

# Classify the image
class_idx, confidence = net.Classify(img)

# Find the class information
class_desc = net.GetClassDesc(class_idx)

# Print out the result
result = "image is recognized as '{:s}' (class #{:d}) with {:.2f}% confidence".format(class_desc, class_idx, confidence * 100)
print(result)

# Save the result to a text file
with open(args.output, 'w') as f:
    f.write(result + "\n")
