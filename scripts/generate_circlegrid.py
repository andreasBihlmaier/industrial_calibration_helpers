#!/usr/bin/env python

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

import sys
import os
import argparse
import cv2
import numpy as np

from generate_common import *


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('size', help='Size of circlegrid, e.g. 8x6')
  parser.add_argument('circle', help='Diameter of circles [m], e.g. 0.025')
  parser.add_argument('grid', help='Distance between center of points [m], e.g. 0.035')
  parser.add_argument('filename', help='Output PDF file')
  args = parser.parse_args()

  size_m = (0.29701, 0.20997) # A4 portrait
  circle_m = float(args.circle)
  offset_m = 0.01 + circle_m/2, 0.01 + circle_m/2
  grid_m = float(args.grid), float(args.grid)
  gridsize = string2int_list(args.size, 'x')

  size_px = m2px(size_m)
  img = np.ones(size_px) * 255
  circle_px = circle_m * size2pixels
  radius_px = int(circle_px / 2)
  grid_px = m2px(grid_m)

  print('Drawing %d circles of radius %f [m] (= %d [px]) in image of %fx%f [m] (with %d ppi = %dx%d [px])'
        % (gridsize[0] * gridsize[1], circle_m, circle_px, size_m[0], size_m[1], ppi, size_px[0], size_px[1]))

  rows, cols = gridsize[0], gridsize[1]
  points = []
  for row in range(rows): # x
    for col in range(cols): # y
      point_m = (offset_m[0] + col * grid_m[0], offset_m[1] + row * grid_m[1])
      points.append(point_m)
      point_px = m2px(point_m)
      print('%d %d: %f %f [m] %d %d [px]' % (row, col, point_m[0], point_m[1], point_px[0], point_px[1]))
      cv2.circle(img,
                 point_px,
                 radius_px,
                 (0, 0, 0),
                 -1)

  origin_m = offset_m
  origin_px = m2px(offset_m)
  cv2.line(img,
           (int(origin_px[0] + circle_px/2 + 10), int(origin_px[1] + (rows - 1) * grid_px[1])),
           (int(origin_px[0] + (grid_px[0] - circle_px/2) - 10), int(origin_px[1] + (rows - 1) * grid_px[1])),
           coords_color,
           3)
  drawText(img, (int(origin_px[0] + grid_px[0]/2), int(origin_px[1] + (rows - 1) * grid_px[1] + 30)), "X")
  cv2.line(img,
           (origin_px[0], int(origin_px[1] + (rows - 1) * grid_px[1] - circle_px/2 - 10)),
           (origin_px[0], int(origin_px[1] + (rows - 2) * grid_px[1] + circle_px/2 + 10)),
           coords_color,
           3)
  drawText(img, (origin_px[0] + 30, int(origin_px[1] + (rows - 1) * grid_px[1] - (grid_px[1])/2)), "Y")
  drawText(img, m2px((size_m[1]/2, 0.005)), "%s  circle=%s grid=%s" % (args.size, args.circle, args.grid))

  tmpfile = '/tmp/circlegrid.png'
  cv2.imwrite(tmpfile, img)
  os.system('convert %s -units PixelsPerInch -density %dx%d %s' % (tmpfile, ppi, ppi, args.filename))


if __name__ == '__main__':
  main()
