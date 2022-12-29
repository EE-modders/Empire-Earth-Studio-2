all: clean linux windows
linux:
	gcc -fPIC -shared -o libDCL.so blast.c implode.c
windows:
	x86_64-w64-mingw32-gcc -fPIC -shared -o libDCL.dll blast.c implode.c
clean:
	-rm libDCL.so libDCL.dll
