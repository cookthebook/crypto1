#!/usr/bin/env python
#
# Stanford Crypto1 (Coursera) HW4 - CBC padding oracle 
#
# Reveal plaintext for a CBC-encrypted ciphertext blocks by exploiting a 
# padding oracle.
#
# The server used in the assignment behaves as follows:
#
#    * returns 200 upon correct decryption (?)
#    * returns 403 on bad pad
#    * returns 404 on good pad, bad message
#
# So the procedure is to work backwards byte by byte, XORing the matching
# byte of the previous block with a guess and a fake pad. The pad should be
# appropriate to the position of the byte, so for the last byte, the pad
# would be (0x01). 
#
# If the guess is right, the plaintext and the guess will 
# cancel each other, and the resulting pad will be correct; this will
# be revealed by the error code. By trying all possible 8-bit values (or all
# likely 8-bit values, for speedup) you can discover the value of the byte.
#
# You can repeat this with the next-to-last byte, a pad of (0x02,0x02) xor a
# quantity: guess g concatenated with the previously discovered byte b (g||b).
# 
# This can be extended to longer pads until the entire block is revealed. It
# can repeated for each block until the entire message is revealed.
#
# This code obviously won't work after the target site spins down.
#
import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            if e.code != 403:
                return True # good padding or message
            return False # bad padding or message
        return True

#
# takes prefix b, two AES blocks b0 b1 and reveals b1 using a padding oracle by 
# manipulating b0
def reveal(b, b0, b1):
    # start with an unknown message
    m = ''
    # work through paddings 1, 22, 333, ... ,10101010101010101010101010101010 
    for p in range(0x1, 0x11):
        # store the message in m as we decipher it
        found = asktheoracle(b, b0, b1, p, m) 
        m = found + m
    return m

#
# takes prefix b, blocks b0 b1, pad, and a known m
# combines pad with guesses and consults oracle until it finds the next unknown byte
def asktheoracle(b, b0, b1, p, m):
    pad = ("%02x" % p) * p
    # upper limit dropped for speedup, lower limit to adjust for glitch when
    # reaching pad boundary. adjust to match pads for other messages.
    for guess in range(0x09, 0x7e): 
        # the candidate is (guess||m) xor pad xor b0
        cat = "%02x" % guess + m                    # cat guess to known m
        candidate = ('00' * (16-p)) + xor(cat, pad) # 0-pad, then cat xor pad
        candidate = xor(candidate, b0)              # (cat xor pad) xor b0
        candidate = b + candidate + b1              # string together the whole thing
        po = PaddingOracle()
        if (po.query(candidate)):    # Issue HTTP query with the given argument
            return '%02x' % guess

#
# xor two hex-encoded streams, return hex-encoded stream
def xor(m1, m2):
    # which one is shorter? use it to set the end boundary.
    end = len(m1)
    if(len(m2) < len(m1)):
        end = len(m2)
  
    result = ''
    for i in xrange(0, end, 2):
        n1 = m1[i:i+2]
        n2 = m2[i:i+2]
        b = str(chr((int(n1, 16) ^ int(n2, 16))))
        result += b.encode('hex')
    return result

#
# main
if __name__ == "__main__":
    # here's our target ciphertext:
    c = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4' 

    # split c into array of AES blocks
    ct = []
    for i in range(0, len(c), 32):
        ct.append(c[i:i+32])

    # now reveal
    m = ''
    m += reveal('', ct[0], ct[1])
    m += reveal(ct[0], ct[1], ct[2])
    m += reveal(ct[0]+ct[1], ct[2], ct[3])
  
    print m.decode('hex')

