import glob, os, shutil, json, random, cv2
import numpy as np
from cam_utils import *

def splitAndCastToFloat(line):
	line = line.split()
	line = line[0:3]
	return list(map(float, line))


def CameraModel():
    # Get 3D model
    with open("demo/obj_01.ply") as f:        
        content = f.readlines()
        content = [x.strip() for x in content]

        skip = 0
        foundVertexEl = False
        foundEndOfHead = False
        lineVals = []
        linesToScan = 0
        while (not foundVertexEl or not foundEndOfHead):
            lineVals = content[skip].split()
            if (lineVals[0] == 'end_header'):
                foundEndOfHead = True
            if (lineVals[0] == 'element'):
                if (lineVals[1] == 'vertex'):
                    linesToScan = int(lineVals[2])
                    foundVertexEl = True
            skip+=1
        content = content[skip:linesToScan+skip]
        copy = []; 

        for line in content: 
            copy.append(splitAndCastToFloat(line))

        # compute Pinhome camera model with intrinsic atrix
        vertices = np.matrix(np.array(copy))
        mins = vertices.min(0)
        maxs = vertices.max(0)
        minsMaxs = np.array([[mins.item(0),mins.item(1),mins.item(2)], [maxs.item(0),maxs.item(1),maxs.item(2)]]).T
        corners = np.array(np.meshgrid(minsMaxs[0,:], minsMaxs[1,:], minsMaxs[2,:])).T.reshape(-1,3)
        R_gt = np.array([[0.09630630, 0.99404401, 0.05100790, -105.35775150], [0.57332098, -0.01350810, -0.81922001, -117.52119142], [-0.81365103, 0.10814000, -0.57120699, 1014.87701320]])
        t_gt = np.array([-105.35775150, -117.52119142, 1014.87701320])
        #Rt_gt        = np.concatenate((R_gt, t_gt), axis=1)
        i_c = np.array([[572.4114, 0. ,325.2611], [  0.   ,  573.5704, 242.0489], [  0. ,      0. ,      1.    ]])

        corners = np.c_[corners, np.ones((len(corners), 1))].transpose()
        print(skip)
        print(corners)
        print(R_gt)
        print(i_c)
        proj_2d_gt   = compute_projection(corners, R_gt, i_c)
        proj_2d_gt = proj_2d_gt.astype(int)
        print(proj_2d_gt[0,:])
        # Make empty black image
        image=cv2.imread('demo/0000.png',1)
        height, width, channels = image.shape

        # Create a named colour
        red = [0,0,255]

        # Change one pixel
        image[proj_2d_gt[1,:],proj_2d_gt[0,:]]=red

        # Save
        cv2.imwrite("../camera_calibration/result.png",image)

        return image, proj_2d_gt

if __name__ == "__main__":
    CameraModel()