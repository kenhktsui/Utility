import random
import numpy as np
import numba

data_max_no = 7
load_factor = 0.75
hash_table_length = int(data_max_no//load_factor)


@numba.jit
def hash_string(string,hash_table_length):
	total = 7
	for j in string:
		total += total * 31 + ord(j) 
	return total % hash_table_length

@numba.jit
def hash_string_2(string,hash_table_length):
	total = 0
	for i,j in enumerate(string):
		total += ord(j)**i 
	return total % hash_table_length

storage =[]
@numba.jit
def hash(string, num, hash_table):
	# if same key, override the existing num, similar to get method
	if string in storage:
		if hash_table[hash_string(string,hash_table_length),1] ==0:
			hash_table[hash_string(string,hash_table_length),2] = int(num)
		if hash_table[hash_string(string,hash_table_length),1] != 0:
			tmp = (hash_string(string,hash_table_length)+ int(hash_table[hash_string(string,hash_table_length),1])) % hash_table_length
			hash_table[tmp,2] = int(num)
	else:		
		tmp =  hash_string(string,hash_table_length)
		count_collision = 0
		tmp_initial = -1
		# Until we find a empty slot and also count the step
		while True:
				if hash_table[tmp,2] == int(-1):
					hash_table[tmp,2] = int(num)
					hash_table[tmp,0] = int(hash_string_2(string,hash_table_length))
					storage.append(string)
					break
				else:
					count_collision += 1
					if count_collision == 1:
						tmp_initial = tmp
					hash_table[tmp_initial,1] = count_collision
					tmp = (tmp+1) % hash_table_length
				if count_collision > hash_table_length:
					print("All slots are occupied")
					break # break infinite loop if all are occupied

@numba.jit
def get(string, hash_table):
	if string not in storage:
		raise KeyError
	else:	
		if hash_table[hash_string(string,hash_table_length),1] ==0:
			if hash_string_2(string,hash_table_length) == hash_table[hash_string(string,hash_table_length),0]:
				return hash_table[hash_string(string,hash_table_length),2]
		if hash_table[hash_string(string,hash_table_length),1] != 0:
			if hash_string_2(string,hash_table_length) != hash_table[hash_string(string,hash_table_length),0]:
				tmp = (hash_string(string,hash_table_length)+ int(hash_table[hash_string(string,hash_table_length),1])) % hash_table_length
				return hash_table[tmp,2]
			else:
				return hash_table[hash_string(string,hash_table_length),2]

table = np.zeros((hash_table_length ,3))
# 1nd Dual Hash Function to enhance uniqueness
# 2nd Collision Count
# 3nd value
def clean():
	global storage
	storage = []
	table[:,2] = int(-1)
	table[:,0:2] = int(0)
