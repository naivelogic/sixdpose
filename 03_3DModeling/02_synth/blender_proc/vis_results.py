# https://github.com/DLR-RM/BlenderProc

import os
import h5py
import argparse
import numpy as np
from matplotlib import pyplot as plt
import sys
import json
import numpy as np
import cv2

def flow_to_rgb(flow):
    """
    Visualizes optical flow in hsv space and converts it to rgb space.
    :param flow: (np.array (h, w, c)) optical flow
    :return: (np.array (h, w, c)) rgb data
    """
    im1 = flow[:, :, 0]
    im2 = flow[:, :, 1]

    h, w = flow.shape[:2]

    # Use Hue, Saturation, Value colour model
    hsv = np.zeros((h, w, 3), dtype=np.float32)
    hsv[..., 1] = 1

    mag, ang = cv2.cartToPolar(im1, im2)
    hsv[..., 0] = ang * 180 / np.pi
    hsv[..., 2] = cv2.normalize(mag, None, 0, 1, cv2.NORM_MINMAX)

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


def vis_data(key, data, full_hdf5_data, file_label, args):
    # If key is valid and does not contain segmentation data, create figure and add title
    if key in args.flow_keys + args.rgb_keys + args.other_non_rgb_keys:
        plt.figure()
        plt.title("{} in {}".format(key, file_label))

    if key in args.flow_keys:
        # Visualize optical flow
        plt.imshow(flow_to_rgb(data), cmap='jet')
    elif key in args.segmap_keys:
        # Try to find labels for each channel in the segcolormap
        channel_labels = {}
        if args.segmap_keys.index(key) < len(args.segcolormap_keys):
            # Check if segcolormap_key for the current segmap key is configured and exists
            segcolormap_key = args.segcolormap_keys[args.segmap_keys.index(key)]
            if segcolormap_key in full_hdf5_data:
                # Extract segcolormap data
                segcolormap = json.loads(np.array(full_hdf5_data[segcolormap_key]).tostring())
                if len(segcolormap) > 0:
                    # Go though all columns, we are looking for channel_* ones
                    for colormap_key, colormap_value in segcolormap[0].items():
                        if colormap_key.startswith("channel_") and colormap_value.isdigit():
                            channel_labels[int(colormap_value)] = colormap_key[len("channel_"):]

        # Make sure we have three dimensions
        if len(data.shape) == 2:
            data = data[:, :, None]
        # Go through all channels
        for i in range(data.shape[2]):
            # Try to determine label
            if i in channel_labels:
                channel_label = channel_labels[i]
            else:
                channel_label = i

            # Visualize channel
            plt.figure()
            plt.title("{} / {} in {}".format(key, channel_label, file_label))
            plt.imshow(data[:, :, i], cmap='jet')

    elif key in args.other_non_rgb_keys:
        # Make sure the data has only one channel, otherwise matplotlib will treat it as an rgb image
        if len(data.shape) == 3:
            if data.shape[2] != 1:
                print("Warning: The data with key '" + key + "' has more than one channel which would not allow using a jet color map. Therefore only the first channel is visualized.")
            data = data[:, :, 0]
        
        plt.imshow(data, cmap='jet')
    elif key in args.rgb_keys:
        plt.imshow(data)


def vis_file(path, args):
    # Check if file exists
    if os.path.exists(path):
        if os.path.isfile(path):
            with h5py.File(path, 'r') as data:
                print(path + " contains the following keys: " + str(data.keys()))

                # Select only a subset of keys if args.keys is given
                if args.keys is not None:
                    keys = [key for key in data.keys() if key in args.keys]
                else:
                    keys = [key for key in data.keys()]

                # Visualize every key
                for key in keys:
                    vis_data(key, np.array(data[key]), data, os.path.basename(path), args=args)

        else:
            print("The path is not a file")
    else:
        print("The file does not exist: {}".format(args.hdf5))


def get_parser():
    parser = argparse.ArgumentParser("Script to visualize hdf5 files")

    parser.add_argument('hdf5_paths', nargs='+', help='Path to hdf5 file/s')
    parser.add_argument('--keys', nargs='+', help='Keys that should be visualized. If none is given, all keys are visualized.', default=None)
    parser.add_argument('--rgb_keys', nargs='+', help='Keys that should be interpreted as rgb data.', default=["colors", "normals"])
    parser.add_argument('--flow_keys', nargs='+', help='Keys that should be interpreted as optical flow data.', default=["forward_flow", "backward_flow"])
    parser.add_argument('--segmap_keys', nargs='+', help='Keys that should be interpreted as segmentation data.', default=["segmap"])
    parser.add_argument('--segcolormap_keys', nargs='+', help='Keys that point to the segmentation color maps corresponding to the configured segmap_keys.', default=["segcolormap"])
    parser.add_argument('--other_non_rgb_keys', nargs='+', help='Keys that contain additional non-RGB data which should be visualized using a jet color map.', default=["distance", "depth"])
    return parser

def get_BlenderProc_defaults():
    from argparse import Namespace
    default_args = Namespace(flow_keys=['forward_flow', 'backward_flow'], hdf5_paths=['examples/basic/output/0.hdf5'], keys=None, other_non_rgb_keys=['distance', 'depth'], rgb_keys=['colors', 'normals'], segcolormap_keys=['segcolormap'], segmap_keys=['segmap'])
    return default_args


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to visualize hdf5 files")

    parser.add_argument('hdf5_paths', nargs='+', help='Path to hdf5 file/s')
    parser.add_argument('--keys', nargs='+', help='Keys that should be visualized. If none is given, all keys are visualized.', default=None)
    parser.add_argument('--rgb_keys', nargs='+', help='Keys that should be interpreted as rgb data.', default=["colors", "normals"])
    parser.add_argument('--flow_keys', nargs='+', help='Keys that should be interpreted as optical flow data.', default=["forward_flow", "backward_flow"])
    parser.add_argument('--segmap_keys', nargs='+', help='Keys that should be interpreted as segmentation data.', default=["segmap"])
    parser.add_argument('--segcolormap_keys', nargs='+', help='Keys that point to the segmentation color maps corresponding to the configured segmap_keys.', default=["segcolormap"])
    parser.add_argument('--other_non_rgb_keys', nargs='+', help='Keys that contain additional non-RGB data which should be visualized using a jet color map.', default=["distance", "depth"])

    args = parser.parse_args()


    # Visualize all given files
    for path in args.hdf5_paths:
        vis_file(path, args)
    plt.show()
    