#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 30.08.2022 14:30 CET

@author: zocker_160
"""

from io import BufferedReader


def readInt(f: BufferedReader) -> int:
    return int.from_bytes(f.read(4), byteorder="little", signed=False)
