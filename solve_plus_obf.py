pos = b'33344445568EFLP___________aaadeeefhhiillmnnrsttttvwzzz{}'
#pos = b'33344445568___________aaadeeefhhiillmnnrsttttvwzzz{}'
win = b'\x40\x42\xb8\x4f\x92\xe5\x26\x33\xee\xa0\xc1\x97\xbc\x4f\x81\x43\x81\xe2\xdc\x2b\x92\xf9\x0f\x73\x96\x18\x2b\x33\xd0'


def test(s):
    s = s.encode('ascii')
    global pos
    for c in set(pos):
        if pos.count(c) != s.count(c):
            return False
    return True


from z3 import *

s = Solver()

inp = []
out = [0,]*29
for x in range(0x39):
    v = BitVec('x%d'%x, 8)
    inp.append(v)

    cond = []
    if x in [0, 1, 2, 3, 4, 0x37, 0x38]:
        continue
    for c in pos[:-2]:
        cond.append(v == c)
    s.add(Or(cond))

s.add(inp[0] == ord('E'))
s.add(inp[1] == ord('P'))
s.add(inp[2] == ord('F'))
s.add(inp[3] == ord('L'))
s.add(inp[4] == ord('{'))

# EPFL{3z_disa55ehhi5
s.add(inp[5] == ord('3'))
s.add(inp[6] == ord('z'))
s.add(inp[7] == ord('_'))
s.add(inp[8] == ord('d'))
s.add(inp[9] == ord('i'))
s.add(inp[10] == ord('s'))
s.add(inp[11] == ord('a'))
s.add(inp[12] == ord('5'))
s.add(inp[13] == ord('5'))
s.add(inp[14] == ord('e'))
s.add(inp[15] == ord('m'))
s.add(inp[16] == ord('8'))
s.add(inp[17] == ord('l'))
s.add(inp[18] == ord('e'))
s.add(inp[19] == ord('_'))
s.add(inp[20] == ord('4'))
s.add(inp[21] == ord('_'))
s.add(inp[22] == ord('a'))
s.add(inp[23] == ord('n'))
s.add(inp[24] == ord('_'))
s.add(inp[25] == ord('3'))
s.add(inp[26] == ord('z'))
s.add(inp[27] == ord('_'))
s.add(inp[28] == ord('r'))
s.add(inp[29] == ord('3'))
s.add(inp[30] == ord('v'))
s.add(inp[31] == ord('_'))
s.add(inp[32] == ord('w'))
s.add(inp[33] == ord('i'))
s.add(inp[34] == ord('t'))
s.add(inp[35] == ord('h'))
s.add(inp[36] == ord('_'))

s.add(inp[47] == ord('_'))
s.add(inp[48] == ord('a'))
s.add(inp[49] == ord('t'))
s.add(inp[50] == ord('_'))
s.add(inp[51] == ord('t'))
s.add(inp[52] == ord('h'))
s.add(inp[53] == ord('4'))
s.add(inp[54] == ord('t'))

s.add(inp[55] == ord('}'))
s.add(inp[56] == 0x00)

for x in range(0x39):
    i4 = x*4
    low3 = i4 & 7
    high5 = i4 >> 3


    out[high5] ^= LShR(inp[x], low3)
    
    if (i4 & 7) != 0:
        out[high5 + 1] ^= (inp[x] << (8 - low3))



for x in range(len(out)):
    s.add(out[x] == win[x])

while s.check() == sat:
    m = s.model()
    cond = []

    f = ""
    for c in inp:
        f += chr(m[c].as_long())
        cond.append(c != m[c].as_long())
    s.add(Or(cond))

    if test(f):
        print(f)