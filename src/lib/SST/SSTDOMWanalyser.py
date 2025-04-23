#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28.01.2020 01:04 CET

@author: zocker_160
"""

import os
import sys


csvfile = "!output.csv"
titles = ["filename", "revision", "has DDS", "number res", "number image", "unknown"]

magic_number_dds = b'\x44\x44\x53\x20\x7c\x00\x00\x00'

with open(csvfile, "w") as csvfile:
    csvfile.write(','.join(titles) + "\n")

    for file in os.listdir():
        if file.endswith(".sst"):
            with open(file, "rb") as sstfile:
                rev = sstfile.read(1).hex()
                numres = str(int.from_bytes(sstfile.read(1), byteorder="little", signed=False))
                numimage = str(int.from_bytes(sstfile.read(1), byteorder="little", signed=False))
                sstfile.read(11)
                unknown = sstfile.read(1)
                magic = sstfile.read(8)
                if magic == magic_number_dds:
                    is_dds = True
                else:
                    is_dds = False
                print(file, magic)
                csvfile.write(','.join([file, rev, str(is_dds), numres, numimage, unknown.hex()]) + "\n")
