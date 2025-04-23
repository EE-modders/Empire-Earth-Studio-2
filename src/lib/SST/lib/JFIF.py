#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13.10.2020 12:30 CET

@author: zocker_160
"""

from .ImgInterface import ImgInterface

class JFIF(ImgInterface):
    def __init__(self, jfif_binary: bytes):
        self.filetype = ".jfif"
        self.magic_number_jfif = b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46'
        self.offset_correction = 14

        self.jfif_bin = jfif_binary

    def get_Image_parts(self) -> list:
        JFIF_images = list()

        t_offset = self.offset_correction        
        tmp_bin = b'\x03' + self.jfif_bin

        while tmp_bin[:1] == b'\x03':
            color_end = int.from_bytes(tmp_bin[1:5], byteorder='little', signed=False)
            alpha_end = int.from_bytes(tmp_bin[5:9], byteorder='little', signed=False)

            img_color = tmp_bin[ 9 : color_end - t_offset ]
            img_alpha = tmp_bin[ color_end - t_offset : alpha_end - t_offset ]

            JFIF_images.append( (img_color, img_alpha) )

            tmp_bin = tmp_bin[ alpha_end - t_offset : ]
            t_offset = alpha_end
        
        return JFIF_images

    def write_file(self, binary, filename: str) -> None:
        if isinstance(binary, bytes):
            binary = self.get_Image_parts()[0]

        with open(filename + self.filetype, "wb") as jffile:
            jffile.write(binary[0])
        with open(filename + "_a" + self.filetype, "wb") as jffile:
            jffile.write(binary[1])
