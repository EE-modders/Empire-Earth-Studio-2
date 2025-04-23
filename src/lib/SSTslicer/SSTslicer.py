"""
Created on 02.04.2020 19:21 CET

@author: zocker_160
"""

import os
from io import BytesIO

from . import main as slicer
from lib.SST import SST as SSTi


fromCLI = False
magic_number_compressed = b'PK01' # this is the magic number for all compressed files


def _get_new_filename(filename: str, outputloc: str):
    filename_wo_ext = os.path.basename(filename).split('.')[0]
    dir_abs_path = os.path.dirname( os.path.abspath(filename) )
    if not outputloc: outputloc = dir_abs_path

    return os.path.join(outputloc, filename_wo_ext)


def slice(inputfiles: list, filetype="", xTiles=0, yTiles=0, outputlocation="", tga_output=False, reversed=False):
    num_infiles = len(inputfiles)
    filename = inputfiles[0]

    if not filetype:
        _, filetype = os.path.splitext(filename)

    if "sst" in filetype:
        newfilename = _get_new_filename(filename, outputlocation)

        if num_infiles == 1:
            print("got single SST file as input - splitting....")

            if fromCLI:
                xTiles = int(input("input number of tiles on x-axis: "))
                yTiles = int(input("input number of tiles on y-axis: "))

            try:
                with open(filename, 'rb') as infile:
                    print("analysing %s......" % filename)
                    if infile.read(4) == magic_number_compressed:
                        raise TypeError("\nyou need to decompress the file first!\n")
            except FileNotFoundError:
                raise

            SST = SSTi()
            SST.read_from_file(filename)

            if SST.header["tiles"] > 1 or SST.header["resolutions"] > 1:
                raise TypeError("This SST file has more than one tile and/or resolution!")
            
            slicer.slice(BytesIO(SST.ImageBody), newfilename, col=xTiles, row=yTiles, save=True, reversed=reversed)
        else:
            newfilename += "-joined.tga"

            if fromCLI:
                print("\ngot %d SST files as input:  (watch out for the right order!!)\n" % num_infiles)

                for i, f in enumerate(inputfiles):
                    print("%d: %s" % (i+1, f))
                print()
                response = input("is that correct? (y/n) ")
                if response != "y": raise KeyboardInterrupt("canceled by user")

            outputfiles = list()

            for file in inputfiles:
                tmpSST = SSTi()
                tmpSST.read_from_file(file)

                outputfiles.append( (file, BytesIO(tmpSST.ImageBody)) )
            
            image = slicer.join(slicer.get_tiles(outputfiles))
            image.save(newfilename)

            print("written output to file:\n%s" % newfilename)
            print("done!")

    elif "tga" in filetype:
        #prefix = filename.split('.')[-2]

        if num_infiles == 1:
            prefix = _get_new_filename(filename, outputlocation)

            print("got one TGA file as input - splitting....")

            if fromCLI:
                xTiles = int(input("input number of tiles on x-axis: "))
                yTiles = int(input("input number of tiles on y-axis: "))

            tiles = slicer.slice(filename, prefix, col=xTiles, row=yTiles, save=tga_output, reversed=reversed)
            SSTtiles = list()

            for part in tiles:
                x, y = part.image.size
                newfilename = part.generate_filename(prefix=prefix, format='sst', path=False, reversed=reversed)
                
                tmpSST = SSTi(1, 1, x_res=x, y_res=y, ImageBody=part.get_bytes())
                print(newfilename)
                tmpSST.write_to_file(newfilename, add_extention=False)        
            
            print("done!")
        else:
            newfilename = _get_new_filename(filename, outputlocation) + "-joined.tga"
            #newfilename = filenames[0].split('.')[-2].split('_')[-3] + "-joined.tga"

            if fromCLI:
                print("\ngot %d TGA files as input:  (watch out for the right order!!)\n" % num_infiles)

                for i, f in enumerate(inputfiles):
                    print("%d: %s" % (i+1, f))
                print()
                response = input("is that correct? (y/n) ")
                if response != "y": raise KeyboardInterrupt("canceled by user")

            outputfiles = list()

            for file in inputfiles:
                outputfiles.append( (file, file) )

            image = slicer.join(slicer.get_tiles(outputfiles))
            image.save(newfilename)

            print("written output to file:\n%s" % newfilename)
            print("done!")
    else:
        raise TypeError(f"ERROR: unsupported file extention: {filetype} \n only SST and TGA files are supported.")
