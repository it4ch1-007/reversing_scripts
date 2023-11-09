import gdb 

gdb.execute("b *0x555555555189")
gdb.execute("b *0x55555555520a")

chars="EPFL{3z434465568___________aaadeeefhhiillmnnrsttttvw3zz}"

curr_indx=0
flag=chars
cur_char=0
for i in range(6,len(chars)):
	for j in range(6,len(chars)):
		# flag=flag[:2] + chars[i] + chars[j] + flag[5:]
		flag=flag[:6] + chars[i] + chars[j]
		print(flag,end="\n")
		with open("code.txt","w+") as f:
			f.write(flag)
		gdb.execute("r < code.txt")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		# rsi= gdb.execute(f"p/x $rsi",to_string=True).replace("\t","").strip().split(" ")[2]
		# rsi = int(rsi, 16) 
		# rcx=gdb.execute(f"p/x $rcx",to_string=True).replace("\t","").strip().split(" ")[2]
		# rcx=int(rcx,16)
		# # obt_value = (rsi^rcx)
		# print(hex(obt_value))
		# print(hex(rsi))
		# print(hex(rcx))
		gdb.execute("c")
		# rdi= gdb.execute(f"x/x $rdi",to_string=True).replace("\t","").strip().split(":")[1]
		# rdi = int(rdi, 16) 
		# print(hex(rdi))
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		gdb.execute("c")
		# rsi= gdb.execute(f"p/x $rsi",to_string=True).replace("\t","").strip().split(" ")[2]
		# rsi = int(rsi, 16) 
		# rcx=gdb.execute(f"x/x $rcx",to_string=True).replace("\t","").strip().split(" ")[2]
		# rcx=int(rcx,16)
		# obt_value = (rsi^rcx)
		# print(hex(obt_value))
		# print(hex(rsi))
		# print(hex(rcx))
		rdi= gdb.execute(f"x/x $rdi",to_string=True).replace("\t","").strip().split(":")[1][2:4]
		# rdi = int(rdi, 16) 
		# print(hex(rdi))
		print(rdi)
		# if(rdi==66):
		# 	# curr_indx=curr_indx+1
		# 	gdb.execute("exit")
		# if(obt_value != 69):
