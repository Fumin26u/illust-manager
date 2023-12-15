from absl import app, flags, logging
import tensorflow as tf
import cv2
import os, sys
import numpy as np

from api.evaluate.face_modules.face_models import RetinaFaceModel
from api.evaluate.face_modules.utils import (load_yaml, pad_input_image, recover_pad_output)

currentDir = 'api/evaluate/'

FLAGS = {
    'cfg_path': f'{currentDir}configs/retinaface_mbv2.yaml',
    'iou_th': 0.4,
    'score_th': 0.5,
    'down_scale_factor': 1.0
}

# init
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

logger = tf.get_logger()
logger.disabled = True
logger.setLevel(logging.FATAL)

cfg = load_yaml(FLAGS['cfg_path'])

# define network
model = RetinaFaceModel(cfg, training=False, iou_th=FLAGS['iou_th'],
                        score_th=FLAGS['score_th'])

# load checkpoint
def load_checkpoint():
    checkpoint_dir = f'{currentDir}checkpoints/' + cfg['sub_name']
    checkpoint = tf.train.Checkpoint(model=model)
    if tf.train.latest_checkpoint(checkpoint_dir):
        checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
        print("[*] load ckpt from {}.".format(
            tf.train.latest_checkpoint(checkpoint_dir)))
    else:
        print("[*] Cannot find ckpt from {}.".format(checkpoint_dir))
        exit()

# if not os.path.exists(FLAGS['img_path']):
#     print(f"cannot find image path from {FLAGS['img_path']}")
#     exit()

def draw_bbox(img, ann, img_height, img_width):
    """draw bboxes and landmarks"""
    # bbox
    x1, y1, x2, y2 = int(ann[0] * img_width), int(ann[1] * img_height), \
                     int(ann[2] * img_width), int(ann[3] * img_height)
    return [x1, y1, x2, y2]
    # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # # confidence
    # text = "{:.4f}".format(ann[15])
    # cv2.putText(img, text, (int(ann[0] * img_width), int(ann[1] * img_height)),
    #             cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

def getFaceRect(img_data):
    FLAGS['img_data'] = img_data

    # print("[*] Processing on single image {}".format(FLAGS['img_path']))

    # img_raw = cv2.imread(FLAGS['img_data'])
    img_raw = FLAGS['img_data']
    img_height_raw, img_width_raw, _ = img_raw.shape
    img = np.float32(img_raw.copy())

    if FLAGS['down_scale_factor'] < 1.0:
        img = cv2.resize(img, (0, 0), fx=FLAGS['down_scale_factor'],
                            fy=FLAGS['down_scale_factor'],
                            interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # pad input image to avoid unmatched shape problem
    img, pad_params = pad_input_image(img, max_steps=max(cfg['steps']))

    # run model
    outputs = model(img[np.newaxis, ...]).numpy()

    # recover padding effect
    outputs = recover_pad_output(outputs, pad_params)

    # draw and save results
    # save_img_path = os.path.join('out_' + os.path.basename(FLAGS['img_path']))
    rects = []
    for prior_index in range(len(outputs)):
        rects.append(draw_bbox(img_raw, outputs[prior_index], img_height_raw,
                        img_width_raw))
        
    return rects
        
    # cv2.imwrite(save_img_path, img_raw)
    # print(f"[*] save result at {save_img_path}")
