import sys, os
from model_3d import Model3D

import math
import random

import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
from torch.nn import functional as F

#sys.path.append("../repos/bop_toolkit")
sys.path.append("/home/redne/pvnet/Pix2Pose_nl/bop_toolkit/")
from bop_toolkit_lib import inout, dataset_params

import json
def load_params_from_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

class BOP_DATASET(Dataset):
    def __init__(self, dataset, scene, object_id):
        super().__init__()
        self.dataset = dataset
        self.scene = scene
        self.object_id = object_id


        # orchestrated dataset prameters
        self.rgb_path = os.path.join(self.scene, "rgb")
        self.depth_path = os.path.join(self.scene, "depth")
        self.mask_path = os.path.join(self.scene, "mask_visib")
        
        self.model_path = os.path.join(self.dataset,"models" ,f'obj_{self.object_id:06d}.ply')
        self.model_info = Model3D().load(self.model_path, scale=0.001) #scale = 0.1
        #read_json(self.model_path)[str(object_id)]
        self.pointcld_path = os.path.join(self.dataset,"models_eval" ,f'obj_{self.object_id:06d}.ply')

        # camera parameters
        self.scene_intrinsics_path = os.path.join(self.scene, "scene_camera.json")
        self.scene_intrinsics = inout.load_scene_camera(self.scene_intrinsics_path)
        self.scene_extrinsics_path = os.path.join(self.scene, "scene_gt.json")
        self.scene_extrinsics = inout.load_scene_gt(self.scene_extrinsics_path) # scene ground truth



class BOP_DS_Detector:
    def __init__(self, dataset):
        ds_path = dataset
        model_infos_path = ds_path + '/models_info.json'
        model_infos = json.loads(model_infos_path.read_text())
        object_list = []
        for obj_id, model_info in model_infos.items():
            obj_id = int(obj_id)
            object_long_id = f'obj_{obj_id:06d}'
            pointcld_path = os.path.join(ds_path, object_long_id).with_suffix('.ply').as_posix()
            obj_dict = dict(
                label=object_long_id,
                category=None,
                mesh=pointcld_path,
                ptcld_size='mm',
            )
            symmetric_flag = False
            for k in ('symmetries_discrete', 'symmetries_continuous'):
                obj_dict[k] = model_info.get(k, [])
                if len(obj_dict[k]) > 0:
                    symmetric_flag = True
            obj_dict['is_symmetric'] = symmetric_flag
            obj_dict['diameter'] = model_info['diameter']
            scale = 0.001 if obj_dict['mesh_units'] == 'mm' else 1.0
            obj_dict['diameter_m'] = model_info['diameter'] * scale
            object_list.append(obj_dict)

        self.object_list = object_list
        self.ds_path = ds_path

    def __getitem__(self, idx):
        return self.object_list[idx]

    def __len__(self):
        return len(self.object_list)
