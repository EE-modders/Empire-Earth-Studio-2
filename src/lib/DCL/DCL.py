#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 29.08.2022 22:53 CET

@author: zocker_160
"""

import os
import sys
import ctypes

from io import BytesIO, BufferedReader, BufferedWriter

from lib.Util import readInt, writeInt

# return codes:
CMP_NO_ERROR = 0
CMP_INVALID_DICTSIZE = 1
CMP_INVALID_MODE = 2
CMP_BAD_DATA = 3
CMP_ABORT = 4

# compressTypes:
CMP_BINARY = 0  # Binary compression (most common)
CMP_ASCII = 1  # Ascii compression

# dictSize:
CMP_IMPLODE_DICT_SIZE1 = 1024  # Dictionary size of 1024
CMP_IMPLODE_DICT_SIZE2 = 2048  # Dictionary size of 2048
CMP_IMPLODE_DICT_SIZE3 = 4096  # Dictionary size of 4096 (most common)


class DecompressException(Exception):
    pass


class DCL:
    magic: bytes = b"PK01"
    uncompressed_size: int
    unknown: int = 0
    data: bytes

    @staticmethod
    def parse(data: bytes, raw=False):
        with BytesIO(data) as b:
            if raw:
                return DCL._parseRaw(b)
            return DCL._parse(b)

    @staticmethod
    def parseFile(filename: str, raw=False):
        with open(filename, "rb") as f:
            if raw:
                return DCL._parseRaw(f)
            return DCL._parse(f)

    @staticmethod
    def _parse(f: BufferedReader):
        assert f.read(4) == DCL.magic

        return DCL(
            uncompressedSize=readInt(f),
            unknown=readInt(f),
            data=f.read(-1)
        )

    @staticmethod
    def _parseRaw(f: BufferedReader):
        data = f.read(-1)
        return DCL(len(data), data)

    def __init__(self, uncompressedSize: int, data: bytes, unknown=0):
        self.uncompressed_size = uncompressedSize
        self.unknown = unknown
        self.data = data

        # init decompress lib
        if sys.platform.startswith("win"):
            dll = "libDCL"
        else:
            dll = "libDCL.so"

        self.libdcl = ctypes.CDLL(os.path.join(os.path.dirname(__file__), dll))

        self.libdcl.decompressBytes.argtypes = [
            ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self.libdcl.decompressBytes.restype = ctypes.c_int

        self.libdcl.compressBytes.argtypes = [
            ctypes.c_char_p, ctypes.c_int,
            ctypes.c_char_p, ctypes.POINTER(ctypes.c_int),
            ctypes.c_uint, ctypes.c_uint
        ]
        self.libdcl.compressBytes.restype = ctypes.c_int

    def decompress(self) -> bytes:
        output = bytes(self.uncompressed_size)
        oLength = ctypes.c_int()  # we don't really need this as we have self.uncompressed_size

        ret = self.libdcl.decompressBytes(
            self.data, len(self.data),
            output, ctypes.byref(oLength)
        )

        if ret != 0:
            raise DecompressException(f"decompressor returned error code {ret}")

        return output

    def decompressToFile(self, filename: str):
        with open(filename, "wb") as f:
            f.write(self.decompress())

    def compress(self) -> bytes:
        output = bytes(len(self.data)*2)  # we double the output buffer, that should always be enough
        oLength = ctypes.c_int()

        ret = self.libdcl.compressBytes(
            self.data, len(self.data),
            output, ctypes.byref(oLength),
            CMP_BINARY, CMP_IMPLODE_DICT_SIZE3
        )

        if ret != CMP_NO_ERROR:
            raise DecompressException(f"compressor returned error code {ret}")

        self.data = output[:oLength.value]

    def writeToFile(self, filename: str, raw=False):
        with open(filename, "wb") as f:
            if raw:
                f.write(self.data)
                return
            self.assemble(f)

    def assemble(self, f: BufferedWriter):
        f.write(self.magic)
        writeInt(f, self.uncompressed_size)
        writeInt(f, self.unknown)
        f.write(self.data)

    def __str__(self) -> str:
        return f"magic: {self.magic}, uncompressed size: {self.uncompressed_size}, data length: {len(self.data)}"
