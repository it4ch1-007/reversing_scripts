from unicorn import *
from unicorn.x86_const import *



#Function bytes
code = b"H\x89\xe5\x89}\xfc\x89u\xf8\x8bU\xfc\x8bE\xf8\x01\xd0\c3" 

#This should not have ret instrn as it will pop the top value of the stack that is not available
uc = Uc(UC_ARCH_X86,UC_MODE_64)

stack = 0x20000
stack_size=0x1000

#The memory mapped inside the stack should be writable and readable 
uc.mem_map(0x0,0x10000,UC_PROT_ALL)
uc.mem_map(stack,stack_size,UC_PROT_ALL)
uc.mem_write(0x0,code)

#The pointer RSP can go up the stack and also below inside the stack thus we have to set the RSP register at the middle of the stack
uc.reg_write(UC_X86_REG_RSP,stack+stack_size//2)

#Setting the argiuments for the function using the edi and esi registers
uc.reg_write(UC_X86_REG_RDI,2)
uc.reg_write(UC_X86_REG_RSI,10)

#Starting and ending the emulation till the end of the function bytes only 
uc.emu_start(0x0,0x0+len(code))
reg_val = uc.reg_read(UC_X86_REG_RAX)
print(reg_val)