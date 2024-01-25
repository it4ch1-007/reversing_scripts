# s="/+9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba"
import base64

encoded = "UDYs1D7bNmdE1o3g5ms1V6RrYCVvODJF1DpxKTxJ9xuAZW=="

custom_b64 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
std_b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
print(len(std_b64))
print(len(custom_b64))
# Use str.maketrans instead of string.maketrans
translation_table = str.maketrans(custom_b64, std_b64)
encoded = encoded.translate(translation_table)

# In Python 3, print is a function and requires parentheses
flag = base64.b64decode(encoded)
print(flag)


# Example usage
# custom_alphabet = "/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA"  # Replace with your custom alphabet
# base64_string = "UDYs1D7bNmdE1o3g5ms1V6RrYCVvODJF1DpxKTxJ9xuAZW=="
s1="flarebearstare"
s=[]
# flag = custom_base64_decode(base64_string, custom_alphabet)
for i in range(len(flag)):
    print(flag[i])
    s.append(((flag[i])-ord(s1[i%14])))
print(s)
real_flag=""
for i in range(len(s)-2):
    real_flag += (chr(s[i]))
print(real_flag)
