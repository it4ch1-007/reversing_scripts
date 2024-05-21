from pwn import *
from capstone import *
from unicorn import *
from unicorn.x86_const import *

uc = Uc(UC_ARCH_X86,UC_MODE_32)
cs = Cs(CS_ARCH_X86,CS_MODE_32)

shellcode = b"\xe8\xff\xff\xff\xff\xc0\x5d\x6a\x05\x5b\x29\xdd\x83\xc5\x4e\x89\xe9\x6a\x02\x03\x0c\x24\x5b\x31\xd2\x66\xba\x12\x00\x8b\x39\xc1\xe7\x10\xc1\xef\x10\x81\xe9\xfe\xff\xff\xff\x8b\x45\x00\xc1\xe0\x10\xc1\xe8\x10\x89\xc3\x09\xfb\x21\xf8\xf7\xd0\x21\xd8\x66\x89\x45\x00\x83\xc5\x02\x4a\x85\xd2\x0f\x85\xcf\xff\xff\xff\xec\x37\x75\x5d\x7a\x05\x28\xed\x24\xed\x24\xed\x0b\x88\x7f\xeb\x50\x98\x38\xf9\x5c\x96\x2b\x96\x70\xfe\xc6\xff\xc6\xff\x9f\x32\x1f\x58\x1e\x00\xd3\x80"

BASE = 0x400000
STACK_ADDR= 0x0
STACK_SIZE = 1024*1024

uc.mem_map(STACK_ADDR,STACK_SIZE)
uc.mem_map(BASE,1024*1024)
uc.mem_write(BASE,shellcode)
uc.reg_write(UC_X86_REG_ESP,STACK_ADDR + STACK_SIZE//2 -1)



#Capstone is much faster than pwntools
def hook_code(uc,address,size,data):
    code = uc.mem_read(address,size)
    d=next(cs.disasm(code,address))
    # code = uc.mem_read(address,size)
    # disas_code = disasm(code,address)
    print(f"{hex(d.address)}   {d.mnemonic} {d.op_str}")
    # print(disas_code)


uc.hook_add(UC_HOOK_CODE,hook_code)
start_addr = BASE
end_addr = BASE-1

try:
    uc.emu_start(BASE,BASE-1) #this is the maximum interval we can give between the start address and the end address given randomly to the emulation
except UcError as err:
    print(f"Error: {err} at {hex(uc.reg_read(UC_X86_REG_RIP))}")