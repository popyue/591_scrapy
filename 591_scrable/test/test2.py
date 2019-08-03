import requests 
import os
with open("new.txt" , "r") as file_new:
	with open("old.txt" , "r") as file_old:
		for line in file_new:
			print(line)
		print("---------")
		for line2 in file_old:
			print(line2)
		print(set(file_old))
		print(set(file_new))
		same = set(file_old).intersection(file_new)
		additem = set(file_new).difference(file_old) # The New Item
		deleteitem = set(file_old).difference(file_new) # The Delete Item
print('same: %s' % same)
print('additem: %s' % additem)
same.discard('\n')
additem.discard('\n')
deleteitem.discard('\n')
print('same_2: %s' % same)
with open("sametest.txt", 'w') as file_same:
	#file_same.write("This is old item!!\n")
	for line in same:
		file_same.write(line)
file_same.close()