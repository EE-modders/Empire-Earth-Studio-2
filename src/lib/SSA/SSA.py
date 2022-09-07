#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28.08.2022 00:19 CET

@author: zocker_160
"""

import os
from io import BufferedReader, BufferedWriter
from typing import Callable

from lib.SSA.DCL import DCL
from lib.SSA.Util import readInt, writeInt, checkNullTerminator


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

    def assemble(self, f: BufferedWriter):
        f.write(self.magic)
        writeInt(f, self.version_major)
        writeInt(f, self.version_minor)
        writeInt(f, self.data_start_offset)

    def __len__(self) -> int:
        return self.length

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

    @staticmethod
    def calcLength(path: str, encoding: str) -> int:
        return len(path.encode(encoding)) + 1 + 4*4

    def __init__(self, path: bytes, start: int, end: int, size: int):
        path = checkNullTerminator(path)

        self.path_length = len(path)
        self.path = path
        self.start_offset = start
        self.end_offset = end
        self.size = size

    def getPath(self, encoding: str) -> str:
        return self.path.strip(b"\0") \
            .decode(encoding) \
            .replace("\\", os.sep)

    def assemble(self, f: BufferedWriter):
        writeInt(f, self.path_length)
        f.write(self.path)
        writeInt(f, self.start_offset)
        writeInt(f, self.end_offset)
        writeInt(f, self.size)

    def __len__(self) -> int:
        return len(self.path) + 4*4

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
        key = checkNullTerminator(key)
        value = checkNullTerminator(value)

        self.key_length = len(key)
        self.value_length = len(value)

        self.key, self.value = key, value

    def getKey(self, encoding: str):
        return self.key.strip(b"\0").decode(encoding)

    def getValue(self, encoding: str):
        return self.value.strip(b"\0").decode(encoding)

    def setKey(self, key: str, encoding: str):
        key = checkNullTerminator(key.encode(encoding))

        self.key_length = len(key)
        self.key = key

    def setValue(self, value: str, encoding: str):
        value = checkNullTerminator(value.encode(encoding))

        self.value_length = len(value)
        self.value = value

    def assemble(self, f: BufferedWriter):
        writeInt(f, self.key_length)
        f.write(self.key)
        writeInt(f, self.value_length)
        f.write(self.value)

    def __len__(self) -> int:
        return len(self.key) + len(self.value) + 2*4

    def __str__(self) -> str:
        return f"key: {self.key}, value: {self.value}"


class Intermediate:
    # num_attributes: int
    attributes: list[Attribute]

    @staticmethod
    def parse(f: BufferedReader):
        numAttr = readInt(f)
        attributes: list[Attribute] = list()

        for _ in range(numAttr):
            attr = Attribute.parse(f)
            attributes.append(attr)

        return Intermediate(attributes)

    @staticmethod
    def fromTuples(data: list[tuple[str, str]], encoding: str):
        attributes: list[Attribute] = list()

        for key, value in data:
            attributes.append(Attribute(key.encode(encoding), value.encode(encoding)))

        return Intermediate(attributes)

    def __init__(self, attributes: list[Attribute]):
        self.attributes = attributes

    def addEntry(self, key: str, value: str, encoding: str):
        self.attributes.append(Attribute(key.encode(encoding), value.encode(encoding)))

    def removeIndex(self, index: int):
        del self.attributes[index]

    def getIndex(self, index: int) -> Attribute:
        return self.attributes[index]

    def assemble(self, f: BufferedWriter):
        writeInt(f, len(self.attributes))

        for attr in self.attributes:
            attr.assemble(f)

    def __len__(self) -> int:
        return sum([len(x) for x in self.attributes]) + 4

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.attributes])


class FileData:
    data: bytes

    @staticmethod
    def parse(f: BufferedReader, start: int, length: int):
        f.seek(start, 0)
        data = f.read(length)

        return FileData(data)

    def __init__(self, data: bytes):
        self.data = data

    def isCompressed(self):
        return self.data.startswith(b"PK01")

    def getDecompressedData(self):
        if self.isCompressed():
            return DCL.parse(self.data).decompress()
        else:
            return self.data

    def assemble(self, f: BufferedWriter):
        f.write(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return f"data length: {len(self)}"


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

    @staticmethod
    def packFolder(folderPath: str, encoding: str, metadata: list[tuple[str, str]]):
        files: list[tuple[str, str]] = list()

        for folder in os.listdir(folderPath):
            fPath = os.path.join(folderPath, folder)
            if not os.path.isdir(fPath):
                continue

            for file in os.listdir(fPath):
                filePath = os.path.join(fPath, file)
                if not os.path.isfile(filePath):
                    continue

                files.append((f"{folder}\\{file}", filePath))

        fileData: list[FileData] = list()

        for _, file in files:
            with open(file, "rb") as f:
                fileData.append(FileData(f.read()))

        fileIndexLength = sum([FileEntry.calcLength(x, encoding) for x, _ in files])
        print(fileIndexLength)

        header = Header(fileIndexLength)
        intermediate = Intermediate.fromTuples(metadata, encoding)

        rawdataStartOffset = len(header) + fileIndexLength + len(intermediate)
        print(rawdataStartOffset)

        fileIndex: list[FileEntry] = list()

        for i, (path, _) in enumerate(files):
            fSize = len(fileData[i])
            fEntry = FileEntry(
                path.encode(encoding),
                rawdataStartOffset,
                rawdataStartOffset+fSize-1,
                fSize
            )
            fileIndex.append(fEntry)

            rawdataStartOffset += fSize

        print(len(fileIndex),  sum([len(x) for x in fileIndex]), fileIndexLength)

        return SSA(header, fileIndex, intermediate, fileData, os.path.dirname(folderPath))

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

    def assemble(self, filePath: str):
        with open(filePath, "wb") as ssafile:
            self.header.assemble(ssafile)

            for index in self.file_index:
                index.assemble(ssafile)

            self.intermediate.assemble(ssafile)

            for data in self.file_data:
                data.assemble(ssafile)

    def getFileList(self) -> list[str]:
        files = list()
        for file in self.file_index:
            files.append(file.getPath(self.encoding))

        return files

    def getMetadata(self) -> list[tuple[str, str]]:
        attributes = list()
        for attr in self.intermediate.attributes:
            attributes.append((attr.getKey(self.encoding), attr.getValue(self.encoding)))

        return attributes

    def addMetadata(self, key: str, value: str):
        self.intermediate.addEntry(key, value, self.encoding)

    def removeMetadata(self, index: int):
        self.intermediate.removeIndex(index)

    def setMetadataKey(self, index: int, key: str):
        self.intermediate.getIndex(index).setKey(key, self.encoding)

    def setMetadataValue(self, index: int, value: str):
        self.intermediate.getIndex(index).setValue(value, self.encoding)

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
