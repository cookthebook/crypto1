#!/usr/bin/env python
#
# Stanford Crypto1 (Coursera) HW5 - compute Dlog mod prime p.
# 
# Given p, g, and h = g^x in Z_p, 1 <= x <= 2^40, B=2^20
# 
#    * First build a hash table of all possible values of h/g^x_1, x_1=0..B
#    * Foreach x_0=0..B, check if g^Bx_0 is in hash table
#    * If it is, compute x = x_0B + x_1
#      
import sys,gmpy2
from gmpy2 import mpz,powmod,divm,add,mul

p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
B = pow(2,20)
Brange = range(B)

hashtable = dict()

#
# create a hash table of LHS result -- h/g^x1 (mod p)
# note we hash the LHS result, not the indices; the index is the value
for x1 in Brange:
    hashtable[divm(h,powmod(g,x1,p),p)] = x1

#
# check for each RHS result in hash table until a match is found
for x0 in Brange:
    x1 = hashtable.get(powmod(g,mul(B,x0),p))

    # if a match is found, calculate x
    if x1:
        x = add(mul(x0,B),mpz(x1))

        # double-check that h matches, and if so, exit
        i = powmod(g,x,p)
        if (h == i):
            print str(x)
            sys.exit(0)
        
