#!/usr/bin/env python
#
import Crypto.Cipher.AES as AES
import Crypto.Util.Counter
import sys

BS = AES.block_size

key = '140b41b22a29beb4061bda66b6747e14'.decode('hex')
ciphertext1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
ciphertext2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'


#
# you have to supply a dummy iv to the library; but it's smart enough to grab
# the corect one from the first block of the ciphertext.
handle = AES.new(key, AES.MODE_CBC, '0000000000000000')
print handle.decrypt(ciphertext1.decode('hex'))[BS:]
print handle.decrypt(ciphertext2.decode('hex'))[BS:]

