#!/usr/bin/env python

# Copyright (c) 2016 Andreas Bihlmaier <bihlmaier@robodev.eu>
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
from math import ceil

from generate_common import *


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('size', help='Size of chessboard pattern, e.g. 8x6')
  parser.add_argument('square', help='Size of squares [m], e.g. 0.025')
  parser.add_argument('filename', help='Output PDF file')
  args = parser.parse_args()

  size_m = (0.29701, 0.20997) # A4 portrait
  square_m = float(args.square)
  offset_m = 0.012, 0.01
  gridsize = string2int_list(args.size, 'x')

  size_px = m2px(size_m)
  img = np.ones(size_px) * 255
  square_px = square_m * size2pixels

  print('Drawing %d black squares of size %f [m] (= %d [px]) in image of %fx%f [m] (with %d ppi = %dx%d [px])'
        % (gridsize[0] * gridsize[1], square_m, square_px, size_m[0], size_m[1], ppi, size_px[0], size_px[1]))

  rows, cols = gridsize[0], gridsize[1]
  square_positions = []
  for row in range(rows): # x
    for col in range(cols): # y
      actual_row = 2 * row + (col % 2)
      if actual_row >= rows:
        continue
      square_position_m = (offset_m[0] + col * square_m, offset_m[1] + actual_row * square_m)
      square_positions.append(square_position_m)
      square_position_px = m2px(square_position_m)
      print('%d %d: %f %f [m] %d %d [px]' % (row, col, square_position_m[0], square_position_m[1], square_position_px[0], square_position_px[1]))
      img[square_position_px[0]:(square_position_px[0]+square_px), square_position_px[1]:(square_position_px[1]+square_px)] = 0

  drawText(img, m2px((size_m[1]/2, 0.0075)), "%dx%d  square=%s" % (gridsize[0] - 1, gridsize[1] - 1, args.square))

  tmpfile = '/tmp/chessboard_pattern.png'
  cv2.imwrite(tmpfile, img)
  os.system('convert %s -units PixelsPerInch -density %dx%d %s' % (tmpfile, ppi, ppi, args.filename))


if __name__ == '__main__':
  main()
