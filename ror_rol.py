def rotate_left(x, n):
    return int(f"{x:08b}"[n:] + f"{x:08b}"[:n], 2)

def rotate_right(x, n):
    return int(f"{x:08b}"[-n:] + f"{x:08b}"[:-n], 2)

encrypted = [0xc7,0xc7,0x25,0x1d,0x63,0xd,0xf3,0x56]
right_png_header = [0x89,0x50,0x4e,0x47,0x0d,0x0a,0x1a,0x0a,0x00]
decryption_key = [-1]*8
for i in range(0,8):
    print(rotate_right(right_png_header[i] + i,i) ^ encrypted[i])
    decryption_key[i] = rotate_right(right_png_header[i]+i,i)^encrypted[i]
print(''.join(chr(decryption_key[i]) for i in range(len(decryption_key))))

#decryption_key = No1Trust
 # You_Have_Awakened_Me_Too_Soon_EXE@flare-on.com
