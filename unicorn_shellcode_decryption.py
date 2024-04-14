from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import *
from unicorn.x86_const import *

mu = Uc(UC_ARCH_X86, UC_MODE_64)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
stackaddr = 0x3000000
stack_size = 0x4000
mu.mem_map(stackaddr, stack_size)
# //rsp and rbp registers are also writtten
mu.reg_write(UC_X86_REG_RSP, stackaddr + stack_size - 8 - 0x200)
mu.reg_write(UC_X86_REG_EBP, stackaddr + stack_size - 8) 
# setting up the stack and the memory write area

global r8_vals
r8_vals = []
global imm_vals
imm_vals = []
# getting a fn to hook or stop the code where i want to stop and analyze the data
def hook_code(mu, address, size, user_data):
    global imm_vals
    global r8_vals
    mem = mu.mem_read(address, size)
    # here i will read the memory and some specific size of it
    d = next(cs.disasm(mem, address))

    # now cmp and xor instrns are seeked and then a list is made of these values to be compared
    if d.mnemonic == "cmp":
        if "r8" in d.op_str:
            temp = d.op_str[3:]
            temp = temp.strip()
            if "0x" in temp:
                temp = temp[2:]
            imm_vals.append(int(temp,16))

    # now xor instrns are seekes and then a list is made of these values to be xored
    if d.mnemonic == "xor":
        if "r8" in d.op_str and "r8, r8" not in d.op_str and "r8 + rdx" not in d.op_str :
            temp = d.op_str[3:]
            temp = temp.strip()
            if "0x" in temp:
                temp = temp[2:]
            r8_vals.append(int(temp,16))
    if d.mnemonic == "jmp" and "r10" in d.op_str:
        next_address = mu.reg_read(UC_X86_REG_RIP) + size
        mu.reg_write(UC_X86_REG_RIP, next_address)
        # increasing the size of the stack and setting the rip to the next address of the program code
        
        


        
# text_addr = 0x7FF7F4311000
text_addr = 0x00007FF7E60E1000
oep = 0x00007FF7E60E1000
endaddr = 0x00007FF7E60F1000

with open('bin_newer.out', 'rb') as f:
    code = f.read()
    


mu.mem_map(text_addr,0x1000000)
mu.mem_write(text_addr,code)
# write the code to the text_addr address starting
mu.mem_write(0x3000000, b'\0' * 0x100) 
# important to initialize the stack with null bytes
mu.reg_write(UC_X86_REG_RIP,oep)
# setting the RIP to the getting address
mu.reg_write(UC_X86_REG_RCX, 0x0)
# setting all the registers to null is important and required
mu.reg_write(UC_X86_REG_R12, stackaddr)
# setting the stack_address to the R12
mu.hook_add(UC_HOOK_CODE, hook_code)
# used to hook the code by adding the hook to it (hook_code is basically the fn )

try:
    mu.emu_start(oep,endaddr)
except UcError as e:
    print("Error: %s" % e)
    print("at : %s" % hex(mu.reg_read(UC_X86_REG_RIP)))
    result = [chr(a ^ b) for a, b in zip(r8_vals, imm_vals)]

    flag = ''.join(map(str, result))
    print(flag)
