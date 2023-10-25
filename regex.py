import re
#1

s = 'GeeksforGeeks: A computer science portal for geeks'
 
match = re.search(r'portal', s)
 
print('Start Index:', match.start())
print('End Index:', match.end())

#2

string = "The quick brown fox jumps over the lazy dog"
pattern = "[a-m]"
result = re.findall(pattern, string)
 
print(result)