import gdb


gdb.execute("b* 0x0000000000401B5B")
gdb.execute("r")
l1=[]
l2=[]
flag=""
for i in range(20):
	rax=eval(gdb.execute("p $rax",to_string=True).split("= ")[1][:-1])
	rdx = eval(gdb.execute("p $rdx",to_string=True).split("= ")[1][:-1])
	# print(rax)
	# l1.append(rax)
	# l2.append(rdx)
	flag+=chr(rax^rdx)
	print(flag)
	gdb.execute("c")
print(l1)
print(l2)
