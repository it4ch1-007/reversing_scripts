xored_values = [0x46,0x15,0xF4,0xBD,0xff,0x4c,0xef,0x46,0xeb,0xe6,0xb2,0xeb,0xf1,0xc4,0x34,0x67,0x39,0xb5,0x8e,0xef,0x40,0x1b,0x74,0x0d]
rol_values =   [0x56,0xF5,0xAC,0x1B,0xb5,0x93,0x7e,0xb8,0x23,0xda,0xa,0xf2,0x1,0x61,0x5c,0xc8,0x4c,0xd6,0x16,0x55,0x67,0xb8,0xc1,0xf8]
result =       [0xc3,0xcc,0xba,0x4e,0xf2,0xeb,0x27,0x19,0xc6,0x42,0x6,0x16,0x5d,0x53,0x55,0x0e,0x66,0xf4,0xf9,0x30,0x9a,0x77,0x56]

def rotate_right(value, rotations, bit_length=8):
    """
    Rotate an integer to the right by a specified number of rotations.

    Parameters:
    - value: The integer to be rotated.
    - rotations: The number of rotations to perform.
    - bit_length: The bit length of the integer (default is 32 for 32-bit integers).

    Returns:
    - The rotated integer.
    """
    rotations %= bit_length  # Ensure rotations are within the bit length
    return (value >> rotations) | (value << (bit_length - rotations)) & ((1 << bit_length) - 1)

s=""

for i in range(len(xored_values)):
    s+=chr(xored_values[i]^(rotate_right(result[i],rol_values[i])))
print(s)
# for i in range(len(xored_values)):
#     for i in range(130):
#         if(xored_values^i)
    
    ##########################################################################
# Rotating bits (tested with Python 2.7)
 
  # PEP 3105
 
# max bits > 0 == width of the value in bits (e.g., int_16 -> 16)
 
# Rotate left: 0b1001 --> 0b0011
# max_bits = 16
# rol = lambda val, r_bits, max_bits: \
#     (val << r_bits%max_bits) & (2**max_bits-1) | \
#     ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# # Rotate right: 0b1001 --> 0b1100
# ror = lambda val, r_bits, max_bits: \
#     ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
#     (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
 
#   # For fun, try 2, 17 or other arbitrary (positive!) values
 
# # print()
# # for i in range(0, max_bits*2-1):
# #     value = 0xC000
# #     newval = rol(value, i, max_bits)
# #     print("0x%08x << 0x%02x --> 0x%08x" % (value, i, newval))
 
# # print()
# # for i in range(0, max_bits*2-1):
# #     value = xored_values[i]
# #     newval = ror(value, i, max_bits)
# #     print("0x%08x >> 0x%02x --> 0x%08x" % (value, i, newval))
# l=[]
# for i in range(len(xored_values)):
#     l.append(ror(xored_values[i]^result[i],rol_values[i],max_bits))
# print(l)


#Is_th1s_3v3n_mai_finul_f0arm@flare-on.com