#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 29.08.2022 22:53 CET

@author: zocker_160
"""

import os
import sys
import ctypes

from io import BytesIO

from lib.Util import readInt

class DecompressException(Exception):
    pass

class DCL:

    magic: bytes = b"PK01"
    uncompressed_size: int
    unknown: int = 0
    data: bytes

    @staticmethod
    def parse(data: bytes):
        f = BytesIO(data)

        assert f.read(4) == DCL.magic

        return DCL(
            readInt(f),
            readInt(f),
            f.read(-1)
        )

    def __init__(self, uncompressedSize: int, unknown: int, data: bytes):
        self.uncompressed_size = uncompressedSize
        self.unknown = unknown
        self.data = data

        # init decompress lib
        if sys.platform.startswith("win"):
            dll = "libblast"
        else:
            dll = "libblast.so"         
        self.libblast = ctypes.CDLL(
            os.path.join(os.path.dirname(__file__), dll))

        self.libblast.decompressBytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        self.libblast.decompressBytes.restype = ctypes.c_int        

    def decompress(self) -> bytes:
        output = bytes(self.uncompressed_size)

        ret = self.libblast.decompressBytes(
            self.data, len(self.data),
            output, len(output)
        )

        if ret != 0:
            raise DecompressException(f"decompressor returned error code {ret}")

        return output

    def __str__(self) -> str:
        return f"magic: {self.magic}, uncompressed size: {self.uncompressed_size}, data length: {len(self.data)}"
