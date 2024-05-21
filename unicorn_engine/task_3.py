from unicorn import *
from unicorn.x86_const import *
from capstone import *
from pwn import *

uc = Uc(UC_ARCH_X86,UC_MODE_32)
cs = Cs(CS_ARCH_X86,CS_MODE_32)

BASE =  0x08048000
STACK_ADDR = 0x0
STACK_SIZE = 1024*1024

uc.mem_map(STACK_ADDR,STACK_SIZE)
uc.mem_map(BASE,1024*1024)
uc.reg_write(UC_X86_REG_ESP,STACK_ADDR + STACK_SIZE//2 -1)

with open("./function","rb+") as file:
    code = file.read()



def hook_code(uc,address,size,data):
    mem = uc.mem_read(address,size)
    d=next(cs.disasm(mem,address))
    print(f"{hex(d.address)}\t{d.mnemonic} {d.op_str} ")
    if address in to_skip:
        uc.reg_write(UC_X86_REG_EIP,address+size)
        # print(f"address: {address} , size: {size}")
    elif address == 0x80485b0:
        print(f"Return value: {uc.reg_read(UC_X86_REG_EAX)}")
    elif address == 0x8048588:
        ref = uc.reg_read(UC_X86_REG_EBP) + 0x8
        print(f"Crucial value: {hex(ref)}")
        uc.mem_write(ref,p32(0x5))
        print(uc.mem_read(ref,4))
    elif address == 0x8048598:
        uc.reg_write(UC_X86_REG_EAX,STR_ADDR)
        print(f"EDI = {uc.reg_read(UC_X86_REG_EDI)}, ESI ={uc.reg_read(UC_X86_REG_ESI)}")
        print(f"EAX = {hex(uc.reg_read(UC_X86_REG_EAX))}, second arg ={uc.mem_read(uc.reg_read(UC_X86_REG_EBP)+0x8,4)}")
    elif address == 0x804855a:
        uc.reg_write(UC_X86_REG_EAX,STR_ADDR)
        print(f"EAX = {hex(uc.reg_read(UC_X86_REG_EAX))}")
    elif address == 0x80485a0:
        eflags = uc.reg_read(UC_X86_REG_EFLAGS)
        print(eflags)
        eflags |= 0x40
        print(hex(eflags))
        uc.reg_write(UC_X86_REG_EFLAGS,eflags)
        # uc.reg_write(UC_X86_REG_EIP,address + size)
    elif address == 0x80485a2:
        eflags = uc.reg_read(UC_X86_REG_EFLAGS)
        print(eflags)
        eflags |= 0x40
        print(hex(eflags))
        uc.reg_write(UC_X86_REG_EFLAGS,eflags)

    

uc.hook_add(UC_HOOK_CODE,hook_code)

#setting up the arguments
# uc.reg_write(UC_X86_REG_EDI,0x5)
uc.mem_write((STACK_ADDR + 0x4),p32(0x5))
wanted_string = b"batman"
STR_ADDR = BASE + 1024*1024 - 0x200
uc.mem_write(STR_ADDR,wanted_string)
uc.mem_write(STACK_ADDR + 0x8,p32(STR_ADDR))



to_skip = [0x0804857e,0x08048583]
uc.mem_write(BASE,code)
start_addr = 0x0804857c
end_addr = 0x080485b1
try:
    uc.emu_start(start_addr,end_addr)
except UcError as err:
    print(f"Error {err} at {hex(uc.reg_read(UC_X86_REG_EIP))}")