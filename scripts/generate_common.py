from __future__ import print_function

import yaml
from tf.transformations import *

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
