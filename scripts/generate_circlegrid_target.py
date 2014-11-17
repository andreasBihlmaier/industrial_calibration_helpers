#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import argparse
import yaml

from generate_common import *


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('size', help='Size of circlegrid, e.g. 8x6')
  parser.add_argument('circle', help='Diameter of circles [m], e.g. 0.025')
  parser.add_argument('grid', help='Distance between center of points [m], e.g. 0.035')
  parser.add_argument('filename', help='Output YAML target file')
  args = parser.parse_args()

  circle_m = float(args.circle)
  grid_m = float(args.grid), float(args.grid)
  gridsize = string2int_list(args.size, 'x')

  rows, cols = gridsize[0], gridsize[1]
  points = []
  for row in range(rows): # x
    for col in range(cols): # y
      points.append({'pnt': [col * grid_m[1], (rows - 1 - row) * grid_m[0], 0.0]})

  target = {
    'target_name': 'circlegrid__%s__%s__%s' % (args.size, str(circle_m).replace('.', '_'), str(args.grid).replace('.', '_')),
    'target_type': 1,
    'circle_dia': circle_m,
    'target_frame': 'target_frame',
    'target_rows': rows,
    'target_cols': cols,
    'transform_interface': 'ros_lti',
    'angle_axis_ax': 0.0,
    'angle_axis_ay': 0.0,
    'angle_axis_az': 0.0,
    'position_x': 0.0,
    'position_y': 0.0,
    'position_z': 0.0,
    'num_points': rows * cols,
    'points': points
  }
  static_targets = [target]
  yaml_dict = {'static_targets': static_targets} 
  save_yaml(args.filename, yaml_dict)



if __name__ == '__main__':
  main()
