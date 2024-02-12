from unicorn import *
from unicorn.x86_const import *
from pwn import *
context.arch = "amd64"
from capstone import *

#disassembling using pwntools
def disassemble(fn_bytes):
    print(disasm(fn_bytes))


#Hooking the code for various instructions

### hook for interrupts
def hook_intr(uc,intno,user_data):
    uc.emu_stop()
    print(f"Got interrupt signal with interrupt number = {intno}")
    return
### hook for syscalls
def hook_syscall(uc,user_data):
    rax = uc.reg_read(UC_X86_REG_RAX)
    print(f"Syscall with RAX= {rax}")
    return
### hook for a particular code
def hook_code(uc,address,size,user_data):
     print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %(address, size))


def emulate(fn_bytes):
    uc = Uc(UC_ARCH_X86,UC_MODE_64)

    code_base = 0x0
    code_size = 0x10000
    # #Setting up the memory 
    uc.mem_map(code_base,code_size,UC_PROT_ALL)
    # # uc.mem_write(code_base,0x0*code_size)


    stack_size = 0x1000
    stack_base = 0x20000
    # #Setting up the stack
    uc.mem_map(stack_base,stack_size,UC_PROT_ALL)
    # # uc.mem_write(stack_base,stack_size*0x0)

    # #writing the code to the start of the stack to emulate the function
    uc.mem_write(code_base,fn_bytes)

    #Setting the registers
    uc.reg_write(UC_X86_REG_RSP,stack_base + stack_size//2 )
    uc.reg_write(UC_X86_REG_RDI,4)
    uc.reg_write(UC_X86_REG_RSI,10)


    #Hooking signals or instructions and functions
    uc.hook_add(UC_HOOK_INTR, hook_intr)

    #Hooking syscalls and adding any wanted functions
    uc.hook_add(UC_HOOK_INSN,hook_syscall,None, 1, 0, UC_X86_INS_SYSCALL)

    #Hooking function bytes or particular code
    uc.hook_add(UC_HOOK_CODE,hook_code) #hook_code is the function that is taken into input to hook the program at that encounter



    uc.emu_start(code_base,code_base + len(fn_bytes))
    print("Emulation done!!")
    print(f"RAX Value returned = {uc.reg_read(UC_X86_REG_RAX)}")

fn_bytes = b"3\xd2H\x8dM\xd0A\xb8\xa8\x04\x00\x00\xe8=-\x00\x00\xff\x15w\x1e\x01\x00H\x8bK\x08\x0f(\x05\x1c\xd8\x01\x00\x89\x85\xd0\x00\x00\x003\xc0\x89\x85\xa0\x04\x00\x00f\x89\x85\xa4\x04\x00\x00\x8bA\x07\x89\x85\xa0\x04\x00\x00\x0f\xb6A\x0b\x88\x85\xa4\x04\x00\x00\x0f\x11\x07\x0f(\r\xfa\xd7\x01\x00\x0f\x11O\x10\x0f("
disassemble(fn_bytes)

