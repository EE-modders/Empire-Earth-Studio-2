#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 30.08.2022 14:30 CET

@author: zocker_160
"""

from io import BufferedReader, BufferedWriter


def readInt(f: BufferedReader) -> int:
    return int.from_bytes(f.read(4), byteorder="little", signed=False)

def writeInt(f: BufferedWriter, value: int) -> int:
    return f.write(value.to_bytes(4, byteorder="little", signed=False))

def checkNullTerminator(data: bytes) -> bytes:
    if not data.endswith(b"\0"):
        data += b"\0"
    return data
