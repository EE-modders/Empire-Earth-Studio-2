#! /usr/bin/env bash

gcc -fPIC -shared -o libDCL.so blast.c implode.c
x86_64-w64-mingw32-gcc -fPIC -shared -o libDCL.dll blast.c implode.c