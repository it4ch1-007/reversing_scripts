from pwn import *
from unicorn import *
from unicorn.arm_const import *
from capstone import *


uc = Uc(UC_ARCH_ARM,UC_MODE_LITTLE_ENDIAN)
cs = Cs(CS_ARCH_ARM,CS_MODE_LITTLE_ENDIAN)


BASE = 0x10000
STACK_ADDR = BASE + 0x300000
STACK_SIZE = 1024*1024

uc.mem_map(BASE,1024*1024)
uc.mem_map(STACK_ADDR,STACK_SIZE)
uc.reg_write(UC_ARM_REG_SP,STACK_ADDR+STACK_SIZE//2-1)

with open("task4","rb+") as file:
    code = file.read()

d={}
stack=[]
#For a single execution of the fn we have the stack and for the multiple execution of the fn we have the dictionary to remember the values
uc.mem_write(BASE,code)
def hook_code(uc,address,size,data):
    # mem = uc.mem_read(address,size)
    # d=next(cs.disasm(mem,address))
    # print(f"{hex(d.address)}\t{d.mnemonic} {d.op_str}")
    if address == 0x104d0:
        arg0 = uc.reg_read(UC_ARM_REG_R0)

        if arg0 in d:
            ret = d[arg0]
            uc.reg_write(UC_ARM_REG_R0,ret) #write the return value that was already evaluated into the Ro register.
            #Now we have to return the fn manually obn demand thus we will implement the ARM ret instruction
            uc.reg_write(UC_ARM_REG_PC,0x105bc) #A ret instruction
        else:
            stack.append(arg0)
    elif address == 0x10580:
        arg0 =stack.pop() #the last value or simply the last return value of the fn that should be at the end of the fn.
        ret = uc.reg_read(UC_ARM_REG_R0) #R0 is the register that stores the first argument as well as the return value.
        d[arg0] = ret


uc.hook_add(UC_HOOK_CODE,hook_code)
start_addr = 0x00010584
end_addr = 0x000105a8

try:
    uc.emu_start(start_addr,end_addr)
    print(f"Return value: {hex(uc.reg_read(UC_ARM_REG_R1))}")
except UcError as err:
    print(f"Error: {err} at {hex(uc.reg_read(UC_ARM_REG_PC))}")


#ARM Asembly
#R15 is the program counter 
#R13 is the Stack pointer
#R7 is the register that holds the syscall number 