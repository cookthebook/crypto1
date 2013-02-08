#!/usr/bin/env python

import sys

MSGS = ( "stuff in the first one", 
         "stuff2 after that one", 
         "stuff3 is even later you know" )

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def random(size=16):
    return open("/dev/urandom").read(size)

def encrypt(key, msg):
    print
    print "m is " + padprint(msg)
    print "m is " + msg.encode('hex')
    c = strxor(key, msg)
    print "c is " + c.encode('hex')
    print c.encode('hex')
    return c

def padprint(msg):
    r = ' '
    for c in msg: 
        r += c
        r += ' '
    return r

def main():
    key = random(1024)
    print
    print "k is " + key.encode('hex')
    ciphertexts = [encrypt(key, msg) for msg in MSGS]

if __name__ == '__main__': 
    main() 
