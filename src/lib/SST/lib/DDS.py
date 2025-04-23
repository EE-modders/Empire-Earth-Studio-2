#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27.01.2020 22:05 CET

@author: zocker_160
"""

from .ImgInterface import ImgInterface

class DDSReader(ImgInterface):
    def __init__(self, dds_binary: bytes):
        self.filetype = ".dds"
        self.magic_number_dds = b'\x44\x44\x53\x20\x7c\x00\x00\x00'        
        self.dds_bin = dds_binary

    def get_Image_parts(self):
        """Function that returns all DDS images inside the binary"""        
        Images = self.dds_bin[8:].split(self.magic_number_dds)
        for i, image in enumerate(Images):
            Images[i] = self.magic_number_dds + image
        return Images

    def write_file(self, binary: bytes, filename: str):
        with open(filename + self.filetype, "wb") as ddsfile:
            ddsfile.write(binary)
    