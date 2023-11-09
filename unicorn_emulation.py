# import capstone

# with open('<filename>','rb'):
#     bytes=fp.read()

# dis_engine = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# disassembly = dis_engine.disasm(bytes[4:],0x400000)

# for item in disassembly:
#     print(f"{item:address:#08x} : {item.mnemonic:8} {item.op_str}")


from unicorn import *
from unicron.x86_const import *
from unicorn.arm64_const import *

with open('<filename>','rb') as fp:
    code = fp.read()
ADDR=0x400000  #random address where you want to write the shellcode or the new dumpes data to be emulated
STACK = 0x100000 #base address of the stack
STACK_SZ = 1024*1024
FLAG_ADDR = 0x400285

emulator = Uc(UC_ARCH_X86, UC_MODE_64) #specifying the properties of the system of the user

emulator.mem_map(ADDR,2*1024*1024) #this is to allocate 2 mb to the given address
emulator.reg_write(UC_X86_REG_RSP,STACK + STACK_SZ)
#this is to make the stack at the given address of a particular size and point the rsp pointer  to that stack

emulator.emu_start(ADDR,FLAG_ADDR)
#starting the emulation of the function at the stack at specified address

required_strings = emulator.mem_read(emulator.reg_read(UC_X86_REG_RSI),50)
#we will read te value of the rsi register at the end of the emulation of th efunction stored at the stack


emulator.mem_map(STACK,STACK_SZ) #this creates an area where the stack can be placed for the emulation







# from unicorn import *
