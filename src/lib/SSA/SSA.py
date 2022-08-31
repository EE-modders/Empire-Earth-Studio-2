#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28.08.2022 00:19 CET

@author: zocker_160
"""

import os
from io import BufferedReader
from typing import Callable

from lib.SSA.DCL import DCL
from lib.SSA.Util import readInt


class ParseException(Exception):
    pass


class ExtractException(Exception):
    pass


class DecompressException(Exception):
    pass


class Header:
    magic: bytes = b'rass'
    version_major: int = 1
    version_minor: int = 0
    data_start_offset: int

    length: int = 16

    @staticmethod
    def parse(f: BufferedReader):
        assert f.read(4) == Header.magic
        assert readInt(f) == Header.version_major
        assert readInt(f) == Header.version_minor

        dso = readInt(f)

        return Header(dso)

    def __init__(self, data_start_offset: int):
        self.data_start_offset = data_start_offset

    def __str__(self) -> str:
        return f"magic: {self.magic}, " \
               + f"version: {self.version_major}.{self.version_minor}, " \
               + f"dso: {self.data_start_offset}"


class FileEntry:
    path_length: int
    path: bytes
    start_offset: int
    end_offset: int
    size: int

    @staticmethod
    def parse(f: BufferedReader):
        pathLength = readInt(f)

        return FileEntry(
            f.read(pathLength),
            readInt(f),
            readInt(f),
            readInt(f)
        )

    def __init__(self, path: bytes, start: int, end: int, size: int):
        self.path_length = len(path)
        self.path = path
        self.start_offset = start
        self.end_offset = end
        self.size = size

    def getPath(self, encoding: str) -> str:
        return self.path.strip(b"\0") \
            .decode(encoding) \
            .replace("\\", os.sep)

    def __str__(self) -> str:
        return f"path: {self.path}, start: {self.start_offset}, end: {self.end_offset}, size: {self.size}"


class Attribute:
    key_length: int
    key: bytes
    value_length: int
    value: bytes

    @staticmethod
    def parse(f: BufferedReader):
        keyLength = readInt(f)
        key = f.read(keyLength)

        valueLength = readInt(f)
        value = f.read(valueLength)

        return Attribute(key, value)

    def __init__(self, key: bytes, value: bytes):
        self.key_length = len(key)
        self.value_length = len(value)

        self.key, self.value = key, value

    def __str__(self) -> str:
        return f"key: {self.key}, value: {self.value}"


class Intermediate:
    num_attributes: int
    attributes: list[Attribute]

    @staticmethod
    def parse(f: BufferedReader):
        numAttr = readInt(f)
        attributes: list[Attribute] = list()

        for _ in range(numAttr):
            attr = Attribute.parse(f)
            attributes.append(attr)

        return Intermediate(attributes)

    def __init__(self, attributes: list[Attribute]):
        self.num_attributes = len(attributes)
        self.attributes = attributes

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.attributes])


class FileData:
    length: int
    data: bytes

    @staticmethod
    def parse(f: BufferedReader, start: int, length: int):
        f.seek(start, 0)
        data = f.read(length)

        return FileData(data)

    def __init__(self, data: bytes):
        self.length = len(data)
        self.data = data

    def isCompressed(self):
        return self.data.startswith(b"PK01")

    def getDecompressedData(self):
        if self.isCompressed():
            return DCL.parse(self.data).decompress()
        else:
            return self.data

    def __str__(self) -> str:
        return f"data length: {self.length}"


class SSA:
    header: Header
    file_index: list[FileEntry]
    intermediate: Intermediate
    file_data: list[FileData]

    archiveName: str
    encoding: str = "ISO-8859-15"

    @staticmethod
    def parseFile(filename: str):
        with open(filename, "rb") as ssafile:
            header = Header.parse(ssafile)
            entries: list[FileEntry] = list()

            while ssafile.tell() < (header.data_start_offset + header.length):
                fe = FileEntry.parse(ssafile)
                entries.append(fe)

            intermediate = Intermediate.parse(ssafile)

            files: list[FileData] = list()

            for entry in entries:
                file = FileData.parse(
                    ssafile, entry.start_offset, entry.size)
                files.append(file)

            archive = os.path.basename(filename)

            return SSA(header, entries, intermediate, files, archive)

    def __init__(self,
                 header: Header,
                 fileIndex: list[FileEntry],
                 intermediate: Intermediate,
                 fileData: list[FileData],
                 archiveName: str = ""):

        self.header = header
        self.file_index = fileIndex
        self.intermediate = intermediate
        self.file_data = fileData
        self.archiveName = archiveName

    def extract(self, outputFolder: str, decompress=False, progressCallback: Callable = None, finishCallback: Callable = None):
        outputFolder = os.path.join(outputFolder, self.archiveName)

        if decompress:
            outputFolder += ".decompressed"
        else:
            outputFolder += ".extracted"

        for i, (file, data) in enumerate(zip(self.file_index, self.file_data)):
            path = os.path.join(
                outputFolder, file.getPath(self.encoding))
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "wb") as f:
                if decompress:
                    f.write(data.getDecompressedData())
                else:
                    f.write(data.data)

            if progressCallback:
                progressCallback(i + 1, len(self.file_index), file.getPath(self.encoding))

            print(
                f"({i + 1}/{len(self.file_index)})",
                "compressed" if data.isCompressed() else "raw")

        if finishCallback:
            finishCallback()

    def extractSingle(self, outputFolder: str, index: int, decompress=False):
        file = self.file_index[index]
        filename = os.path.basename(file.getPath(self.encoding))

        with open(os.path.join(outputFolder, filename), "wb") as f:
            if decompress:
                f.write(self.file_data[index].getDecompressedData())
            else:
                f.write(self.file_data[index].data)

    def getFileList(self) -> list[str]:
        files = list()
        for file in self.file_index:
            files.append(file.getPath(self.encoding))

        return files

    def printFileIndex(self):
        print("\n".join([str(x) for x in self.file_index]))

    def __str__(self) -> str:
        return f"""SSA [
            header: {self.header}
            entries: {len(self.file_index)}
            intermediate: \n{self.intermediate}
            files: {len(self.file_data)}
            encoding: {self.encoding}
        ]
        """
