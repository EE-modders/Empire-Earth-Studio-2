#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05.01.2020 19:47 CET

@author: zocker_160

This is the main lib for SST files from Empire Earth
"""

from .ImgInterface import ImgInterface
from .TGA import TGA
from .DDS import DDSReader
from .JFIF import JFIF

class SST:
    def __init__(self, num_res=0, num_tiles=0, x_res=0, y_res=0, ImageBody=b''):
        self.header = {
            "revision": b'\x00',
            "resolutions": num_res,
            "tiles": num_tiles,
            "placeholder": b'\x00\x00\x00',
            "x-res": x_res,
            "y-res": y_res,    
            "unknown": b'\x00'
        }
        self.ImageBody = ImageBody

    def read_from_file(self, filename: str) -> None:
        """reads an SST input file and parses the SST-header and body"""
        with open(filename, 'rb') as sstfile:

            read_int_buff = lambda x: int.from_bytes(sstfile.read(x), byteorder="little", signed=False)

            print("parsing......")

            self.header["revision"] = sstfile.read(1)
            self.header["resolutions"] = read_int_buff(1)
            self.header["tiles"] = read_int_buff(1)
            self.header["placeholder"] = sstfile.read(3)
            self.header["x-res"] = read_int_buff(4)
            self.header["y-res"] = read_int_buff(4)
            self.header["unknown"] = sstfile.read(1)

            self.ImageBody = sstfile.read(-1)

    def write_to_file(self, filename: str, add_extention=True) -> None:
        """writes SST header and body to a file using the information of the SST object"""    
        outputfile = filename
        if add_extention: outputfile += '.sst'

        with open(outputfile, 'wb') as sstfile:
            print("writing %s.......\n" % outputfile)

            sstfile.write(self.get_header_bytes() + self.ImageBody)

    def get_header_bytes(self) -> bytes:
        """returns the SST header in byte format"""
        result = b''
        #print(self.header)
        result += self.header["revision"]
        result += self.header["resolutions"].to_bytes(1, byteorder='little', signed=False) 
        result += self.header["tiles"].to_bytes(1, byteorder='little', signed=False)
        result += self.header["placeholder"]
        result += self.header["x-res"].to_bytes(4, byteorder='little', signed=False)
        result += self.header["y-res"].to_bytes(4, byteorder='little', signed=False)
        result += self.header["unknown"]
        #print(result)
        return result

    def unpack(self) -> ImgInterface:
        """Returns either a TGA, DDS or JFIF object"""
        if self.header["revision"] == b'\x00' and self.header["unknown"] == b'\x00':
            return TGA(tga_binary=self.ImageBody)
        elif self.header["revision"] == b'\x00' and self.header["unknown"] == b'\x03':
            return JFIF(jfif_binary=self.ImageBody)
        elif self.header["revision"] == b'\x01':
            return DDSReader(dds_binary=self.ImageBody)
        else:
            raise TypeError("This version of the SST format is not supported! - please contact maintainer ;)")


    def __str__(self):
        output = "SST Header: \n"

        header_tmp = self.header
        header_tmp.pop('revision')
        header_tmp.pop('placeholder')        
        header_tmp.pop('unknown')

        for key, value in header_tmp.items():
            output += "%s: %s \n" % (key, value)
        output += "\n"

        return output
