#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05.01.2020 19:01 CET

@author: zocker_160
"""

import os

from .lib.SST import SST as SSTi
from .lib.TGA import TGA
from .lib.DDS import DDSReader


magic_number_compressed = b'PK01' # this is the magic number for all compressed files
file_ignorelist = ["shortcut to tga source 4-bit.sst"]
fromCLI = False  # this is true, when function is called from CLI and not from another python module


def _convert_files(files: list, confirm: bool, force_overwrite: bool, single_res: bool, bundling: bool, outputlocation: str):
    for i, file in enumerate(files):
        # check for file existence and compression
        try:
            with open(file, 'rb') as sstfile:
                print("analysing %s......" % file)
                if sstfile.read(4) == magic_number_compressed:
                    raise TypeError("\nyou need to decompress the file first!\n")
        except EnvironmentError:
            raise FileNotFoundError("File \"%s\" not found!" % file)

        filename = os.path.basename(file) # (!!!) this fucking shit does not work properly on Windows for some fucking reason - WONTFIX
        filename_wo_ext = filename.split('.')[0]
        file_abs_path = os.path.abspath(file)
        dir_abs_path = os.path.dirname(file_abs_path)
        _, file_ext = os.path.splitext(file_abs_path)

        if not outputlocation: outputlocation = dir_abs_path

        # check if file is in ignorelist
        if filename in file_ignorelist:
            print("This file is on the ignorelist! Skipping...")
            continue

        newfilename = os.path.join(outputlocation, filename_wo_ext)
        print(newfilename)

        # check if input file is SST or TGA
        if file_ext == ".sst":
            print("found SST file - extracting image(s).....")

            SST = SSTi()
            SST.read_from_file(file_abs_path)

            tiles_mult = SST.header["resolutions"] * SST.header["tiles"]

            try:
                Image = SST.unpack()
            except TypeError as e:
                raise

            if tiles_mult < 1:
                raise TypeError("there is something wrong with your file! | Error code: res %s; tiles %s" % (SST.header["resolutions"], SST.header["tiles"]))
            else:
                print("converting......\n")
                print(SST)

            if tiles_mult == 1:
                Image.write_file(SST.ImageBody, newfilename)
            else:
                print("found more than one image part (according to header):")
                #print("number of different resolutions: %d" % SST.header["resolutions"])
                #print("number of different image tiles: %d" % SST.header["tiles"])
                print("total number of parts: %d" % tiles_mult)
                if confirm:
                    response = input("continue? (y/n) ")
                else:
                    response = "y"
                if response != "y": raise KeyboardInterrupt("aborted by user...")

                Imageparts = Image.get_Image_parts()
                num_images = len(Imageparts)

                print("\nactually found number of images: %d \n" % num_images)
                for i in range(num_images):
                    if num_images > 1:
                        if SST.header["tiles"] > 1:                
                            Image.write_file(Imageparts[i], f"{newfilename}_{i+1}-{num_images}")
                        elif SST.header["resolutions"] > 1:
                            Image.write_file(Imageparts[i], f"{newfilename}_{i+1}-{num_images}_RES")
                            if single_res: break
                    else:
                        Image.write_file(Imageparts[i], newfilename)

        elif file_ext == ".tga":
            print("found TGA file - will convert to SST.....\n")

            # check if this item is the first of the input list
            if i == 0 and len(files) > 1 and bundling:
                # convert all images into one SST with multiple tiles
                tga_bin = b''
                x_tmp, y_tmp = 0, 0

                if fromCLI:
                    print("following %d images as input:" % len(files) )
                    print("watch out for the right order!!\n")

                    for y, fl in enumerate(files):
                        print("%d: %s" % (y+1, fl))
                    print()
                    if confirm:
                        response = input("is that correct? (y/n) ")
                    else:
                        response = "y"
                    if response != "y": raise KeyboardInterrupt("aborted by user...")

                print("bundling TGA images........")

                for z, f in enumerate(files):
                    with open(f, 'rb') as tgafile:
                        tmpTGA = TGA(tgafile.read())
                    # on multi tile images, all *have to* have the exact same resolution, you cannot mix resolutions!
                    if z == 0:
                        x_tmp, y_tmp = tmpTGA.xRes, tmpTGA.yRes
                    else:
                        if x_tmp != tmpTGA.xRes or y_tmp != tmpTGA.yRes:
                            raise TypeError("ERROR: All tiles have to have the exact same resolution!")
                    tmpTGA.cleanup()
                    tga_bin += tmpTGA.tga_bin
                    tga_bin += b'\x00'

                print("creating SST file........")
                orgTGA = TGA(tga_binary=tga_bin)
                newSST = SSTi(1, num_tiles=len(files), x_res=orgTGA.xRes, y_res=orgTGA.yRes, ImageBody=orgTGA.tga_bin)

                if os.path.exists(newfilename + '.sst') and not force_overwrite:
                    print("This file does already exist! - adding \"_NEW\"")
                    newSST.write_to_file(newfilename + "_NEW", add_extention=True)
                else:
                    newSST.write_to_file(newfilename, add_extention=True)

                # break out of the main loop
                break
            else:
                # convert just this one file
                print("creating SST........")

                with open(file_abs_path, 'rb') as tgafile:
                    tga_bin = tgafile.read()

                orgTGA = TGA(tga_binary=tga_bin)
                orgTGA.cleanup()
                newSST = SSTi(1, num_tiles=1, x_res=orgTGA.xRes, y_res=orgTGA.yRes, ImageBody=orgTGA.tga_bin)
                
                if os.path.exists(newfilename + '.sst') and not force_overwrite:
                    print("This file does already exist! - adding \"_NEW\"")
                    newSST.write_to_file(newfilename + "_NEW", add_extention=True)
                else:
                    newSST.write_to_file(newfilename, add_extention=True)
        else:
            raise TypeError("ERROR: unknown file format! Only TGA and SST are supported \n")
        
    print("done!")


def convert(inputfiles: list, selection: str, confirm=False, overwrite=False, single_res=False, bundling=True, outputlocation=""):

    firstfile: str = inputfiles[0]

    if os.path.isfile(firstfile):
        _convert_files(inputfiles, confirm=confirm, force_overwrite=overwrite, single_res=single_res, bundling=bundling, outputlocation=outputlocation)
    elif os.path.isdir(firstfile):
        filepath = firstfile
        if not filepath.endswith(os.sep): filepath += os.sep
        filelist = list()

        if fromCLI and not selection:
            print("Folder found - what do you want to do? \n")
            print("Convert all files")
            print("(1)\tSST -> TGA / JFIF")
            print("(2)\tTGA -> SST")

            selection = input("selection: ")

        if selection == "1":
            filetype = ".sst"
        elif selection == "2":
            filetype = ".tga"
        else:
            raise TypeError("ERROR: Invalid selection!")

        for f in os.listdir(filepath):
            if f.endswith(filetype):
                print("found file:", f)
                filelist.append(filepath + f)

        _convert_files(filelist, confirm=confirm, force_overwrite=overwrite, single_res=single_res, bundling=bundling, outputlocation=outputlocation)
    else:
        raise TypeError("ERROR: Input is neither file nor folder!")
