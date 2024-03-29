#! /usr/bin/env bash

VERSION="v1.2"

function cleanup {
	echo "cleaning up"
	rm -rf ~/Downloads/EES2 || true
}

cleanup
rm -rf ~/Downloads/EEStudio2 || true

echo "copying files"
cp -r ~/Documents/Empire-Earth-Studio-2/src ~/Downloads/EES2

cd ~/Downloads/EES2/
cp assets/EESicon.ico .

echo "running pyinstaller"
pyinstaller --icon=EESicon.ico --noconsole EEStudio2.py

echo "copy files post installation"
cp -r ./assets dist/EEStudio2

mkdir -p dist/EEStudio2/_internal/lib/DCL
cp ~/Downloads/libDCL.dll dist/EEStudio2/_internal/lib/DCL
cp ~/Downloads/LICENSE.txt dist/EEStudio2

cp -r dist/EEStudio2 ~/Downloads

echo "creating archive"
cd ~/Downloads
7z a EEStudioII-$VERSION-Portable.zip EEStudio2/

cleanup
