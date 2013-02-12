#!/usr/bin/env python
#
# Stanford Crypto1 (Coursera) HW2. parts 1 and 2 (AES CBC ciphers)
# ...implement CBC mode decryption of ciphers with a given key. OK to use 
# library for encrypt() and decrypt(), but implement the block mode here.
# 
import Crypto.Cipher.AES as AES

BS = AES.block_size

ciphertext1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
ciphertext2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'

#
# decryption in CBC is as follows:
#     D(k, ct[0]) xor IV
#     for i=1..n
#         D(k, ct[i]) xor ct[i-1]
def main():
    key = '140b41b22a29beb4061bda66b6747e14'.decode('hex')

    print aes_cbc_decrypt(key, ciphertext1)
    print aes_cbc_decrypt(key, ciphertext2)

## end main()

#
# does a CBC mode decryption, but implements the counter/IV manipulation 
def aes_cbc_decrypt(k, ct):
    result = ''

    # we're using ECB mode so we can decrypt block-by-block... this gives
    # us direct access to the encrypt/decrypt functions and leaves the
    # block mode to us.
    handle = AES.new(k, AES.MODE_ECB)

    # assumes the first block is the IV; assuming hex-encoding, so 
    # there are 2 bytes for every 1 byte of actual data (so grab 
    # twice as many bytes -> BS*2. Start with IV for the first block.
    lastpad = ct[0:BS*2]

    # starting with second block (BS*2) up to the end of the ciphertext:
    for i in range(BS*2,len(ct),BS*2):
        # in BS*2 chunks... isolate next block 
        blk = ct[i:i+BS*2]
        # CBC mode decryption uses AES decrypt()...
        decryption = handle.decrypt(blk.decode('hex'))
        # ...and XORs the result with the lastpad (IV, or last ct)    
        result += xor(decryption.encode('hex'), lastpad).decode('hex')
        # before we attack the next block, set lastpad to current ct block.
        lastpad = blk
    return result

## end aes_cbc_decrypt()

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
