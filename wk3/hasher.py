#!/usr/bin/env python
#
# Stanford Crypto1 (Coursera) HW3 - authenticated streaming video
#
# Generate a hash h_0 for video files accoring to the following scheme:
#
#   * break file up into 1KB blocks
#   * starting with the last block, compute SHA256 hash
#   * append hash to the end of the next block (the previous block in the file)
#   * hash the combined block + hash, append that to the next block
#   * continue until you're out of blocks
#   * print resultig hash
#
# This hash would be issued to clients of this hypothetical system, who could
# then view each block immediately after a successful MAC, instead of pulling
# and MACing the whole file first.
#
import sys
from Crypto.Hash import SHA256

BS=1024
blocks = []
h = b''

#
# file block generator - read in blocks of BS bytes
def readblock(handle):
    while True:
        block = handle.read(BS)
        if not block:
            break
        yield block

#
# if no file was specified, exit
if (len(sys.argv) <= 1):
    print >> sys.stderr, "\nusage: " + sys.argv[0] + " [file]\n"
    sys.exit(1)

#
# read the file into an array of blocks
fh = open(sys.argv[1])
for block in readblock(fh):
    blocks.append(block)

#
# read each block in reverse, calculate a SHA hash
for block in reversed(blocks):
    #
    # append hash to this block
    block += h

    # 
    # then hash the result
    sha = SHA256.new()
    sha.update(block)
    h = sha.digest()

print h.encode('hex') 
