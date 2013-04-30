#!/usr/bin/env python
#
import sys,gmpy2
from gmpy2 import mpz,powmod,divm,add,mul,isqrt_rem,add,isqrt,sub,c_mod,invert,digits,c_div,c_divmod

#
# Challenge 1
N = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581

# modulus N is a product of two primes p and q where |p-q|<=N^(1/4)

# first find A = ceil(sqrt(N))
A = add((isqrt(N)), 1)

# then get x = sqrt(A^2 - N)
x = isqrt(sub(mul(A,A), N))

# then get p = A - x (smaller factor)
p = sub(A, x)
q = add(A, x)
print str(p) + '\n'
p4 = p
q4 = q
N4 = N

#
# Challenge 2
N = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877

# N is a product of p and q where |p-q| < 2^11*N^(1/4)
# try A from sqrt(N) and up 
A = add((isqrt(N)), 1)
while True:
    x = isqrt(sub(mul(A,A), N))
    p = sub(A, x)
    # use mod to test!
    if (c_mod(N, p) == 0):
        print str(p) + '\n'
        break
    A = add(A, 1)

#
# Challenge 3
N = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929 

# N is a product of p and q where |3p + 2q| < N^(1/4)
# try A as ceil(sqrt(6N)) and x = sqrt(A^2 - 6N)

# first find A = ceil(sqrt(6N))
A = mul(6, N)
A = add(A, 1)
A = isqrt(A)
print 'A = ' + str(A)

# then get x = sqrt(A^2 - 6N)
x = mul(A, A)
x = sub(x, mul(6, N))
x = isqrt(x)
print 'x = ' + str(x)

# then get p = (A - x)/3 (smaller factor)
p = c_div(sub(A, x),3)
q = c_div(add(A, x),2)
N3 = mul(p, q)
print str(p) + '\n'
print str(q) + '\n'
print str(N3) + '\n'
print str(N) + '\n'
print 'three? \n'


#
# Challenge 4
c = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

e = 65537
phi = mul(sub(p4, 1), sub(q4, 1))
d = invert(e, phi)
m = powmod(c, d, N4) 
m = m.digits(16)
print m[m.index('00'):].decode('hex')
