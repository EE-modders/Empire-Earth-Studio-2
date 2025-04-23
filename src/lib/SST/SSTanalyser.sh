#! /bin/bash

for filename in *.sst;
do
	python3 SSTanalyser.py "$filename";
done
