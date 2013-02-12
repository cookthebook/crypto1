#!/usr/bin/env python
#
# Stanford Crypto1 (Coursera) HW2. parts 3 and 4 (AES CTR ciphers)
# ...implement CTR mode decryption of ciphers with a given key. OK to use 
# library for encrypt() and decrypt(), but implement the block mode here.
# 
import Crypto.Cipher.AES as AES

BS = AES.block_size

ciphertext1 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
ciphertext2 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'

#
# decryption in CTR is as follows:
# for all i 0..n
#     E(k, IV+counter[i]) xor ct[i]
def main():
    key = '36f18357be4dbd77f050515c73fcf9f2'.decode('hex')

    print aes_ctr_decrypt(key, ciphertext1)
    print aes_ctr_decrypt(key, ciphertext2)

## end main()

#
# does a CTR mode decryption, but implements the counter/IV manipulation.
def aes_ctr_decrypt(k, ct):
    result = ''

    # we're using ECB mode so we can encrypt block-by-block... this gives
    # us direct access to the encrypt/decrypt functions and leaves the
    # block mode to us.
    handle = AES.new(k, AES.MODE_ECB)

    # assumes the first block is the IV; assuming hex-encoding, so 
    # there are 2 bytes for every 1 byte of actual data (so grab 
    # twice as many bytes -> BS*2. Use IV to initialize the counter.
    counter = ct[0:BS*2].decode('hex')

    # starting with second block (BS*2) up to the end of the ciphertext:
    for i in range(BS*2,len(ct),BS*2):
        # in BS*2 chunks... isolate next block 
        blk = ct[i:i+BS*2]
        # CTR mode decryption actually involves encryption of the counter...
        pad = handle.encrypt(counter)
        # ...then XORing the pad we just got with the ciphertext to get the pt.
        result += xor(blk, pad.encode('hex')).decode('hex')
        # before we attack the next block, we must add one to the counter.
        counter = incrcounter(counter)

    return result
## end aes_ctr_decrypt()

#
# counter is a long hex-encoded string represtation of a 128-bit number. 
def incrcounter(counter):
    # convert to an int so we can do the math
    counter = counter.encode('hex')
    counter = int(counter, 16)
    counter += 1
    return ("%x" % counter).decode('hex')
## end incrcounter()

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
## end xor()


if __name__ == '__main__':
    main()
