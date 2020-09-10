import os, json, cv2
from scipy.spatial.transform import Rotation
import scipy.ndimage
import numpy as np

def load_params_from_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def load_scene(file_path):
        with open(os.path.join(file_path, 'scene_gt.json')) as fid:
            scene = json.load(fid)

        images = []
        for im in scene['images']:
            images.append(Dataset(np.array(im['vec']), np.array(im['cam']),im['name'], datapath=file_path))
        img_hw = (scene['img_height'], scene['img_width'])
        K = np.array(scene['K'])

        print('Loaded data containing {} images.'.format(len(images)))
        return images, K, img_hw



class Dataset:
    def __init__(self, vec, cam, name, datapath=''):
        self.vec = vec
        self.cam = cam
        self.name = name
        self._image = self.load_rbg(os.path.join(datapath, name))
        self.extrinsics = self.compute_extrinsic(vec, cam)

    def __repr__(self):
        return '{}: vec={}\n cam={}'.format(self.name, self.vec, self.cam)

    @property
    def image(self):
        return self._image.copy()

    

    @staticmethod
    def load_rbg(path):
        print(path)
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        return im.astype(np.float64) / 255.0

    @staticmethod
    def compute_extrinsic(vec, cam):
        quat = np.roll(vec, -1)
        r = Rotation.from_quat(quat)
        quar_r = np.concatenate([r.as_dcm(), cam[:, None]], axis=1)
        return quar_r




