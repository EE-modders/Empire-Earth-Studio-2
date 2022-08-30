#! /usr/bin/env bash

gcc -fPIC -shared -o libblast.so libblast.c
x86_64-w64-mingw32-gcc -fPIC -shared -o libblast.dll libblast.c
