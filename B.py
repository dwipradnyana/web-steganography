# -*- coding: utf-8 -*-
# -*- by: Yogy Kwan -*-

QUANTUM_LUMINANCE=[
            16, 11, 10, 16, 24, 40, 51, 61, 12, 12, 14, 19, 26, 58, 60, 55,
            14, 13, 16, 24, 40, 57, 69, 56, 14, 17, 22,29, 51, 87, 80, 62,
            18, 22, 37, 56, 68, 109, 103, 77, 24, 35, 55, 64, 81, 104, 113, 92,
            49, 64, 78, 87, 103, 121, 120, 101, 72, 92, 95, 98, 112, 100, 103, 99]
QUANTUM_CHROMINANCE=[
            17, 18, 24, 47, 99, 99, 99, 99, 18, 21, 26, 66, 99, 99, 99, 99,
            24, 26, 56, 99, 99, 99, 99, 99, 47, 66, 99, 99, 99, 99, 99, 99,
            99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
            99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
QUANTUM=[QUANTUM_LUMINANCE,QUANTUM_CHROMINANCE]

AAN=[1.0,1.387039845,1.306562965,1.175875602,
                  1.0,0.785694958,0.541196100,0.275899379]

BITS_DC_LUMINANCE   = [0x00, 0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0x00]
BITS_DC_CHROMINANCE = [0x01, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0x00]
BITS_AC_LUMINANCE   = [0x10, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7d]
BITS_AC_CHROMINANCE = [0x11, 0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
BITS = [BITS_DC_LUMINANCE,BITS_AC_LUMINANCE,BITS_DC_CHROMINANCE,BITS_AC_CHROMINANCE]

VAL_DC_LUMINANCE   = range(12)
VAL_DC_CHROMINANCE = range(12)
VAL_AC_LUMINANCE  = [
            0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 
            0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07, 0x22, 0x71,
            0x14, 0x32, 0x81, 0x91, 0xa1, 0x08, 0x23, 0x42, 0xb1, 
            0xc1, 0x15, 0x52, 0xd1, 0xf0, 0x24, 0x33, 0x62, 0x72,
            0x82, 0x09, 0x0a, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x25, 
            0x26, 0x27, 0x28, 0x29, 0x2a, 0x34, 0x35, 0x36, 0x37,
            0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 
            0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
            0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 
            0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x83,
            0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x92, 0x93, 
            0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3,
            0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 
            0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3,
            0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 
            0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
            0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf1, 
            0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa]
VAL_AC_CHROMINANCE = [
            0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 
            0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71, 0x13, 0x22,
            0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 0xa1, 0xb1, 0xc1, 
            0x09, 0x23, 0x33, 0x52, 0xf0, 0x15, 0x62, 0x72, 0xd1,
            0x0a, 0x16, 0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 
            0x19, 0x1a, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x35, 0x36,
            0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 
            0x48, 0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
            0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 
            0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a,
            0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 
            0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a,
            0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 
            0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba,
            0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 
            0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda,
            0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 
            0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa]
VAL=[VAL_DC_LUMINANCE,VAL_AC_LUMINANCE,VAL_DC_CHROMINANCE,VAL_AC_CHROMINANCE]

ZIGZAG = [0, 1, 8, 16, 9, 2, 3, 10,
          17, 24, 32, 25, 18, 11, 4, 5,
          12, 19, 26, 33, 40, 48, 41, 34,
          27, 20, 13, 6, 7, 14, 21, 28,
          35, 42, 49, 56, 57, 50, 43, 36,
          29, 22, 15, 23, 30, 37, 44, 51,
          58, 59, 52, 45, 38, 31, 39, 46,
          53, 60, 61, 54, 47, 55, 62, 63]
ZAGZIG = [0, 1, 5, 6, 14, 15, 27, 28,
          2, 4, 7, 13, 16, 26, 29, 42,
          3, 8, 12, 17, 25, 30, 41, 43,
          9, 11, 18, 24, 31, 40, 44, 53,
          10, 19, 23, 32, 39, 45, 52, 54,
          20, 22, 33, 38, 46, 51, 55, 60,
          21, 34, 37, 47, 50, 56, 59, 61,
          35, 36, 48, 49, 57, 58, 62, 63]

ZZ = [[ 0, 0 ], [ 0, 1 ], [ 1, 0 ], [ 2, 0 ], [ 1, 1 ], [ 0, 2 ], [ 0, 3 ], [ 1, 2 ],
      [ 2, 1 ], [ 3, 0 ], [ 4, 0 ], [ 3, 1 ], [ 2, 2 ], [ 1, 3 ], [ 0, 4 ], [ 0, 5 ],
      [ 1, 4 ], [ 2, 3 ], [ 3, 2 ], [ 4, 1 ], [ 5, 0 ], [ 6, 0 ], [ 5, 1 ], [ 4, 2 ],
      [ 3, 3 ], [ 2, 4 ], [ 1, 5 ], [ 0, 6 ], [ 0, 7 ], [ 1, 6 ], [ 2, 5 ], [ 3, 4 ],
      [ 4, 3 ], [ 5, 2 ], [ 6, 1 ], [ 7, 0 ], [ 7, 1 ], [ 6, 2 ], [ 5, 3 ], [ 4, 4 ],
      [ 3, 5 ], [ 2, 6 ], [ 1, 7 ], [ 2, 7 ], [ 3, 6 ], [ 4, 5 ], [ 5, 4 ], [ 6, 3 ],
      [ 7, 2 ], [ 7, 3 ], [ 6, 4 ], [ 5, 5 ], [ 4, 6 ], [ 3, 7 ], [ 4, 7 ], [ 5, 6 ],
      [ 6, 5 ], [ 7, 4 ], [ 7, 5 ], [ 6, 6 ], [ 5, 7 ], [ 6, 7 ], [ 7, 6 ], [ 7, 7 ]]