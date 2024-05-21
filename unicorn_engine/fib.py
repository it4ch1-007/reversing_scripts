from unicorn import *
from unicorn.x86_const import *
import struct 
from pwn import *
from capstone import *

# #a function to read a random file
# def read(name):
#     with open(name) as f:
#         return f,read()
# #This function unpacks the packed binary data into tuple of values
# #Also it returns data into Little endian format.

# def u32(data):
#     return struct.unpack("I",data)[0] #the I denotes the unsigned integer type

# #This is the inverse of the u32 function that converts the data into bytes.

# def p32(num):
#     return struct.pack("I",num)


uc=Uc(UC_ARCH_X86,UC_MODE_64)
cs=Cs(CS_ARCH_X86,CS_MODE_64)

#base address of the binary  = 0x400000
#Mapping the stack

BASE = 0x400000
STACK_ADDR = 0x0
STACK_SIZE = 1024*1024

uc.mem_map(BASE,1024*1024)
uc.mem_map(STACK_ADDR,STACK_SIZE)


#we will make a list of those instrns which we have to skip as we are unable to emualte those type of instrns
#the libc fns will not be emulated as we are not having any user interface while emulation

instrns = [0x4004EF,0x4004F6,0x400502,0x40054F] 
FIBONACCI_ENTRY = 0x400670
FIBONACCI_END=[0x4006F1,0x400709] #These are the addresses where the fibonacci function can return the value it wants to return in the rax register
stack=[]
d={}
def hook_code(uc,address,size,user_data):
    # print(">> Tracing instrn at 0x%x with size 0x%x"%(address,size))
    if(address in instrns):
        uc.reg_write(UC_X86_REG_RIP,address + size)
    elif address == 0x400560:
        print(chr(uc.reg_read( UC_X86_REG_RDI)))
        uc.reg_write(UC_X86_REG_RIP,address + size)
    elif address == FIBONACCI_ENTRY:
        arg0 = uc.reg_read(UC_X86_REG_RDI)
        r_rsi = uc.reg_read(UC_X86_REG_RSI)
        arg1 = u32(uc.mem_read(r_rsi,4)) #To read some bytes from the memory.

        #If i have the same args inside the dictionary alresy then i will skip the emulation and will return the function value
        #Then i have to use the RET instrn but cannot use from the given function as it is hooked inside the hook function already 
        #thus we will use the another REt instrn from the main function


        #To remember the arguments during each execution we use the stack 
        #And to remember the pairs during each execution we use the dictionary.
        #Basically this program code is taking time due to the evaluation of the fibonacci function from the start everytime
        #But here we remember the return value everytime the function is executed to make sure that the function when called again then does'nt need to evakluate the same series again and again.
        
        if (arg0,arg1) in d:
            (ret_rax,ret_ref) = d[(arg0,arg1)] #As the function is returning the reference as its second argument
            uc.reg_write(UC_X86_REG_RAX,ret_rax)
            uc.mem_write(r_rsi,p32(ret_ref))
            #Writing at the address stored inside the RSI register
            uc.reg_write(UC_X86_REG_RIP,0x400582)
        
        else:
            stack.append((arg0,arg1,r_rsi))
            #This will push the values into the stack if they are finally obtained at last stage of emulation of the function.
    elif address in FIBONACCI_END:
        (arg0,arg1,r_rsi) = stack.pop()
        ret_rax = uc.reg_read(UC_X86_REG_RAX)
        ret_ref = u32(uc.mem_read(r_rsi,4))
        d[(arg0,arg1)] = (ret_rax,ret_ref)    

uc.hook_add(UC_HOOK_CODE,hook_code)
with open("./fibonacii","rb+") as file:
    code = file.read()

uc.mem_write(BASE,code)
uc.reg_write(UC_X86_REG_RSP,STACK_ADDR+STACK_SIZE-1)

start_addr = 0x00000000004004E0
end_addr = 0x0000000000400575

try:
    uc.emu_start(start_addr,end_addr)
except UcError as e:
    print(f"Error: {e} at {uc.reg_read(UC_X86_REG_RIP)}")
