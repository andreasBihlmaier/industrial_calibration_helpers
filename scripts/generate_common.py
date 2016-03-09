# Copyright (c) 2015 Andreas Bihlmaier <andreas.bihlmaier@gmx.de>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import print_function

import yaml
import cv2
from tf.transformations import *


ppi = 300
size2pixels = ppi * (1.0 / 0.0254)
coords_color = (180, 180, 180)


def save_yaml(filename, yamlnode):
  yaml_str = yaml.dump(yamlnode, default_flow_style = False)
  #print(yaml_str)
  yaml_file = open(filename, 'w')
  yaml_file.write(yaml_str)
  yaml_file.close()


def string2int_list(s, sep = None):
  return [int(i) for i in s.split(sep)]


def string2float_list(s):
  return [float(i) for i in s.split()]


def translation_quaternion2homogeneous(translation, quaternion):
  """
  Translation: [x, y, z]
  Quaternion: [x, y, z, w]
  """
  homogeneous = concatenate_matrices(translation_matrix(translation), quaternion_matrix(quaternion))
  return homogeneous


def drawText(image, point, text):
  fontFace = cv2.FONT_HERSHEY_PLAIN
  fontScale = 4
  thickness = 2
  textSize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
  baseline += thickness
  text_origin = (point[0] - textSize[0]/2, point[1] + textSize[1]/2);
  cv2.putText(image, text, text_origin, fontFace, fontScale, coords_color, thickness)


def m2px(point_m):
  return tuple(int(p * size2pixels) for p in point_m)

