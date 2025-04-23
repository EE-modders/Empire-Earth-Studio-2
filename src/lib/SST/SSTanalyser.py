#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 04.01.2020 18:41 CET

@author: zocker_160
"""

import sys
from io import BytesIO

version = "0.1"
silent_mode = False

def get_num_TGA_parts(binary_tga_blob, start_pos=0, num_tga=1):
    tga_blob = BytesIO(binary_tga_blob)
    # This code assumes, that all TGA-tiles have the same TGA-header  #### WHICH IS NOT THE CASE YOU (me) IDIOT!!!!
    tga_blob.seek(start_pos)
    tga_header_blob = tga_blob.read(tga_header_length)
    tga_body = tga_blob.read(-1)
    next_header = tga_body.find(tga_header_blob)

    if next_header == -1:
        return num_tga
    else:    
        return get_num_TGA_parts(tga_body, start_pos=next_header, num_tga=num_tga+1)


def write_header(name: str, header: dict, org_filename: str):
    export_filename = name + ".csv"

    with open(export_filename, 'at') as csvfile:
        #csvfile.write(','.join(header.keys()) + "\n")
        csvfile.write(org_filename + ',' + ','.join(header.values()) + "\n")


header = {
    "delimiter_1":None,
    "x-tile":int(),
    "y-tile":int(),
    "placeholder":None,
    "x-res":int(),
    "y-res":int(),    
    "delimiter_2": None
}
tga_header_length = 18

# print(sys.argv)

if len(sys.argv) <= 1:
    print("USAGE: SSTanalyser <inputfile> [--silent]")
    print("--silent: minimize output and no-confirm on exit - optimal for batch automation")
    print("")
    input("Press Enter to close...")
    sys.exit()

for args in sys.argv:
    if args == "--silent":
        silent_mode = True

if not silent_mode:
    print("### SST Analyser for Empire Earth made by zocker_160")
    print("### version %s" % version)
    print("###-------------------------------------------------\n")

filename = sys.argv[1]
# filename = "textures/air_me262_10t_org.sst"

with open(filename, 'rb') as sstfile:

    read_int_buff = lambda x: str(int.from_bytes(sstfile.read(x), byteorder="little", signed=False))

    print("parsing %s......\n" % filename)

    header["delimiter_1"] = str(sstfile.read(1))
    header["x-tile"] = read_int_buff(1)
    header["y-tile"] = read_int_buff(1)
    header["placeholder"] = str(sstfile.read(3))
    header["x-res"] = read_int_buff(4)
    header["y-res"] = read_int_buff(4)
    header["delimiter_2"] = str(sstfile.read(1))

    ## get the actual number of TGA files inside the SST
    header["actual_num_TGAs"] = str(get_num_TGA_parts(sstfile.read(-1)))


# print(header)

if not silent_mode:
    print("SST Header: \n")

    for key, value in header.items():
        print("%s: %s" % (key, value) )

# write_header("export", header, filename)

print()

if not silent_mode:
    input("Press Enter to close...")
