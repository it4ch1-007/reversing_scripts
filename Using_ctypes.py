from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")

libc.srand(0x41)

rand = []
for i in range(50):
    rand += [libc.rand()]

a = '''a1[0] ^ 0x5BCA6BB8 == 0x78011AB4
a1[1] ^ 0xF3F5267A == 0xD928ECE8
a1[2] ^ 0x3B82F339 == 0x68664D35
a1[3] ^ 0xEAC4C498 == 0x8E4D5258
a1[4] ^ 0xA2B8887D == 0xFAB6CE43
a1[5] ^ 0xCB166298 == 0xE120C296
a1[6] ^ 0x98C78E2F == 0xA06B1025
a1[7] ^ 0x77467C39 == 0x647A235A
a1[8] ^ 0x4FC570E9 == 0x25972FBB
a1[9] ^ 0xF7687AC == 0x73D6BCC2
a1[0xA] ^ 0x977A770E == 0xDDEA2CBF
a1[0xB] ^ 0xDE216377 == 0xA042B00A
a1[0xC] ^ 0x7B86D0 == 0x46BEEE16
a1[0xD] ^ 0x2894DA2C == 0x4286423C
a1[0xE] ^ 0xA21E9CC6 == 0x9709446E
a1[0xF] ^ 0xCE6B86A7 == 0xE570249D
a1[0x10] ^ 0x85DD96A9 == 0xE40D8E14
a1[0x11] ^ 0xF83BF65C == 0xE8A62B49
a1[0x12] ^ 0x823FFCAC == 0x8049D738
a1[0x13] ^ 0xEC75721A == 0x907F0D1C
a1[0x14] ^ 0x8C0AC9D == 0x5B858520
a1[0x15] ^ 0xEF4B1FCA == 0xF3C99C49
a1[0x16] ^ 0x35A249B == 0x137A42A4
a1[0x17] ^ 0x3F6029F3 == 0x38A6BC31
a1[0x18] ^ 0x1C7E5A70 == 0x72C12356
a1[0x19] ^ 0x9488AC5 == 0x42BF1DA8
a1[0x1A] ^ 0x9DC415B3 == 0xDA35C4E9
a1[0x1B] ^ 0x82C94E38 == 0x937FFF74
a1[0x1C] ^ 0x186336B8 == 0x6004CF47
a1[0x1D] ^ 0xCB048AAD == 0xACFDF982
a1[0x1E] ^ 0xAFE16726 == 0x9522812D
a1[0x1F] ^ 0x68AA8B33 == 0x735098BA'''.split('\n')

b = '''.text:000056020D93E4D1 mov     [rbp+var_90], 65734Eh
.text:000056020D93E4DB mov     [rbp+var_8C], 58918Ch
.text:000056020D93E4E5 mov     [rbp+var_88], 6B90ABh
.text:000056020D93E4EF mov     [rbp+var_84], 5C843Bh
.text:000056020D93E4F9 mov     [rbp+var_80], 6CFD6Ch
.text:000056020D93E500 mov     [rbp+var_7C], 62CEA3h
.text:000056020D93E507 mov     [rbp+var_78], 692E2Ch
.text:000056020D93E50E mov     [rbp+var_74], 5F23C9h
.text:000056020D93E515 mov     [rbp+var_70], 70DE72h
.text:000056020D93E51C mov     [rbp+var_6C], 5D6478h
.text:000056020D93E523 mov     [rbp+var_68], 63AB2Ch'''.split('\n')[::-1] + \
'''.text:000056020D93E52A mov     [rbp+var_64], 7246F2h
.text:000056020D93E531 mov     [rbp+var_60], 7AB4AFh
.text:000056020D93E538 mov     [rbp+var_5C], 6321F2h
.text:000056020D93E53F mov     [rbp+var_58], 6885A8h
.text:000056020D93E546 mov     [rbp+var_54], 6DC7DCh
.text:000056020D93E54D mov     [rbp+var_50], 5B5422h
.text:000056020D93E554 mov     [rbp+var_4C], 5909DEh
.text:000056020D93E55B mov     [rbp+var_48], 54A1E0h
.text:000056020D93E562 mov     [rbp+var_44], 7B86D0h
.text:000056020D93E569 mov     [rbp+var_40], 875750h'''.split('\n')[::-1] + \
'''.text:000056020D93E570 mov     [rbp+var_3C], 55A466h
.text:000056020D93E577 mov     [rbp+var_38], 79DC2Fh
.text:000056020D93E57E mov     [rbp+var_34], 758CB0h
.text:000056020D93E585 mov     [rbp+var_30], 6124E7h
.text:000056020D93E58C mov     [rbp+var_2C], 7F8221h
.text:000056020D93E593 mov     [rbp+var_28], 7D09D5h
.text:000056020D93E59A mov     [rbp+var_24], 7EC3E0h
.text:000056020D93E5A1 mov     [rbp+var_20], 6247B1h
.text:000056020D93E5A8 mov     [rbp+var_1C], 502FE4h
.text:000056020D93E5AF mov     [rbp+var_18], 787562h
.text:000056020D93E5B6 mov     [rbp+var_14], 668036h'''.split('\n')[::-1]

garbage = []
for idx, i in enumerate(b):
    tmp = int(i.split(', ')[1][:-1], 16)
    garbage += [tmp]


for idx, i in enumerate(a):
    tmp = int(i.split(' == ')[1], 16)
    tmp2 = int(i.split(' ^ ')[1].split(' == ')[0], 16)

    tmp3 = tmp2 ^ tmp ^ rand[idx] ^ garbage[idx]

    print(chr(tmp3), end='')
