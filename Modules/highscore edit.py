import os # to access operating system 


#def line__get:
file_path = os.path.dirname(os.path.abspath(__file__)) #find file path 
my_file = os.path.join(file_path, "hs.txt")
High=open(my_file,"r")
lines=High.readlines()
High.close()

print (lines [1])
lines[1]="92\n"
print (lines)

High=open(my_file,"w")
for i in range (2): 
	print (lines[i]) 
	High.write(lines[i])
High.close()