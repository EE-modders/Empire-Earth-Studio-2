/*
libDCL by Zocker_160, 15 Dec 2022

LibDCL was create to make it easier to use blast.c and implode.c
by wrapping the internal structure and exposing a straight forward interface.

This should not only make integration into existing software easier,
but also ease the ability to create c-type bindings to other languages like
Python, Java or Golang.

Make sure you respect the licenses of blast.c by Mark Adler and implode.c by Ladislav Zezula!
*/

/*-----*/
/*
 * - input:       pointer to input data
 * - inLength:    length of the input data
 * - output:      buffer which the output data is written to; make sure it is large enough, otherwise this will segfault
 * - outLength:   the actual length of the written data will be set here
 * 
 * ---
 * 
 * The return codes are:
 *
 * - 2:   ran out of input before completing decompression
 * - 1:   output error before completing decompression
 * - 0:   successful decompression
 * - -1:  literal flag not zero or one
 * - -2:  dictionary size not in 4..6
 * - -3:  distance is too far back
*/
int decompressBytes(char* input, int inLength, 
                    char* output, int* outLength);
/* 
 * - input:        pointer to input data
 * - inLength:     length of the input data
 * - output:       buffer which the output data is written to; make sure it is large enough, otherwise this will segfault
 * - outLength:    the actual length of the written data will be set here
 * - compressType: see defines below
 * - dictSize:     see defines below
 * 
*/
int compressBytes(char* input, int inLength, 
                char* output, int* outLength,
                unsigned int compressType, unsigned int dictSize);

/* The return codes */
#define CMP_NO_ERROR           0
#define CMP_INVALID_DICTSIZE   1
#define CMP_INVALID_MODE       2
#define CMP_BAD_DATA           3
#define CMP_ABORT              4

/* compressTypes */
#define CMP_BINARY             0            // Binary compression (most common)
#define CMP_ASCII              1            // Ascii compression

/* dictSize */
#define CMP_IMPLODE_DICT_SIZE1   1024       // Dictionary size of 1024
#define CMP_IMPLODE_DICT_SIZE2   2048       // Dictionary size of 2048
#define CMP_IMPLODE_DICT_SIZE3   4096       // Dictionary size of 4096 (most common)
