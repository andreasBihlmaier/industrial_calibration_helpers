#!/usr/bin/env python
"""
Combine multiple target.yaml files into one large target.yaml.
For example multiple printed targets rigidly attached to each other with known
transformations between them.

NOTE: Order of points is defined as follows
- each block is formed by basetarget points in their original order
- the blocks are sorted in horizontal order of bottom-left point
"""

from __future__ import print_function

import sys
import os
import argparse
import yaml
import numpy as np

from generate_common import *


def targetpoints_cmp(lhs, rhs):
  if lhs[0] < rhs[0]:
    return -1
  else:
    return 1


def targetblock_order_cmp(lhs, rhs):
  lhs0 = sorted(lhs, cmp = targetpoints_cmp)[0]
  rhs0 = sorted(rhs, cmp = targetpoints_cmp)[0]
  res = targetpoints_cmp(lhs0, rhs0)
  print(lhs0, rhs0, res)
  return res


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('basetargetfile', help='Input basic YAML target file')
  parser.add_argument('combinedtargetfile', help='Output combined YAML target file')
  parser.add_argument('transformation', nargs='*', help='Transformation string (tx ty tz qx qy qz qw) between base target and another target, i.e. from rosrun tf static_transform_publisher TRANSFORMATION target0_frame targetn_frame')
  args = parser.parse_args()

  base_target_points = []
  targetfile_yaml = yaml.load(file(args.basetargetfile))
  target_yaml = targetfile_yaml['static_targets'][0]
  for point in target_yaml['points']:
    point_coords = point['pnt']
    base_target_points.append(np.array(point_coords).reshape((3,1)))
  #print('base_target_points:\n%s' % base_target_points)

  point_blocks = [base_target_points[:]]
  num_targets = 1 + len(args.transformation)
  for transform_str in args.transformation:
    translation_quaternion = string2float_list(transform_str)
    transform = translation_quaternion2homogeneous(translation_quaternion[:3], translation_quaternion[3:])
    #print(transform_str)
    #print(transform)
    transformed_points = []
    for point in base_target_points:
      transformed_point = (transform * np.concatenate((point, np.matrix(1)), axis=0))[:3,0]
      #print('%s -> %s' % (point, transformed_point))
      transformed_points.append(transformed_point)
    point_blocks.append(transformed_points)
  #print('point_blocks:\n%s' % point_blocks)

  sorted_point_blocks = sorted(point_blocks, cmp = targetblock_order_cmp)
  print('sorted_point_blocks:\n%s' % sorted_point_blocks)
  all_points = []
  for block in sorted_point_blocks:
    all_points.extend(block)
  #print('all_points:\n%s' % all_points)

  rows = int(target_yaml['target_rows'])
  cols = num_targets * int(target_yaml['target_cols'])
  all_points_list = []
  for point in all_points:
    point_list = [p[0] for p in point.tolist()]
    all_points_list.append({'pnt': point_list})

  target = {
    'target_name': 'combined_target',
    'target_type': 2,
    'circle_dia': target_yaml['circle_dia'],
    'target_frame': 'target_frame',
    'target_rows': rows,
    'target_cols': cols,
    'subtarget_rows': target_yaml['target_rows'],
    'subtarget_cols': target_yaml['target_cols'],
    'transform_interface': 'ros_lti',
    'angle_axis_ax': 0.0,
    'angle_axis_ay': 0.0,
    'angle_axis_az': 0.0,
    'position_x': 0.0,
    'position_y': 0.0,
    'position_z': 0.0,
    'num_points': rows * cols,
    'points': all_points_list
  }
  static_targets = [target]
  yaml_dict = {'static_targets': static_targets} 
  save_yaml(args.combinedtargetfile, yaml_dict)

if __name__ == '__main__':
  main()
