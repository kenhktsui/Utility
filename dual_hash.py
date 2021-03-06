import numpy as np
from numba import jitclass
from numba import int64
import random

spec = [('hash_table_length',int64),
		('table',int64[:,:]),
		('string',int64[:]),
		('num',int64)]

@jitclass(spec)
class dual_hash():
	def __init__(self, hash_table_length):
		self.hash_table_length = hash_table_length
		self.table = np.zeros((self.hash_table_length,4),dtype = np.int64)
		self.table[:,3] = int64(-1)
		self.table[:,0:3] = int64(0)
		# 1nd Independent Hash Function to enhance uniqueness
		# 2nd Dual Hash Function to enhance uniqueness	
		# 3nd Collision Count
		# 4nd value		
	#
	def hash_string(self, string):
		#djb2
		total = 3313
		for i in string:
			total = ((total << 5) + total) + i
		return total % self.hash_table_length
	#
	def hash_string_2(self, string):
		#sdbm
		total = 0
		for i in string:
#			total += total * 31 + i
			total +=  i + (total <<6) + (total<<16) - total
		return total % self.hash_table_length
	#
	def hash_string_3(self, string):
		total = 7 
		for i in string:
#			total += self.hash_string(string) + i * self.hash_string_2(string)
			total += total * 31 + i			
		return total % self.hash_table_length
	#
	def set(self, string, num):
		# if same key, override the existing num, similar to get method
		if (self.table[self.hash_string(string),3] != -1) & (self.table[self.hash_string(string),2] ==0) & (self.hash_string_2(string) == self.table[self.hash_string(string),0]) & (self.hash_string_3(string) == self.table[self.hash_string(string),1]):
			self.table[self.hash_string(string),3] = num
		elif (self.table[self.hash_string(string),3] != -1) & (self.table[self.hash_string(string),2] != 0) & (self.hash_string_2(string) == self.table[((self.hash_string(string)+ int64(self.table[self.hash_string(string),1])) % self.hash_table_length),0]) & (self.hash_string_3(string) == self.table[((self.hash_string(string)+ int64(self.table[self.hash_string(string),1])) % self.hash_table_length),1]):
			self.table[((self.hash_string(string)+ int64(self.table[self.hash_string(string),2])) % self.hash_table_length),3] = num
		# new key
		else:		
			tmp =  self.hash_string(string)
			count_collision = 0
			tmp_initial = -1
			# Until we find a empty slot and also count the step
			while True:
					if self.table[tmp,3] == -1:
						self.table[tmp,3] = num
						self.table[tmp,0] = self.hash_string_2(string)
						self.table[tmp,1] = self.hash_string_3(string)
						break
					else:
						count_collision += 1
						if count_collision == 1:
							tmp_initial = tmp
						self.table[tmp_initial,2] = count_collision
						tmp = (tmp+1) % self.hash_table_length
					if count_collision > self.hash_table_length:
						print("All slots are occupied")
						break # break infinite loop if all are occupied
	#
	def get(self, string):
		# No collision	
		if self.table[self.hash_string(string),2] ==0:
			if (self.hash_string_2(string) == self.table[self.hash_string(string),0]) & (self.hash_string_3(string) == self.table[self.hash_string(string),1]):
				return self.table[self.hash_string(string),3]
		# Collision
		elif self.table[self.hash_string(string),2] != 0:
			if (self.hash_string_2(string) != self.table[self.hash_string(string),0]) | (self.hash_string_3(string) != self.table[self.hash_string(string),1]):
				tmp = (self.hash_string(string)+ int64(self.table[self.hash_string(string),2])) % self.hash_table_length
				if (self.hash_string_2(string) == self.table[tmp,0]) & (self.hash_string_3(string) == self.table[tmp,1]):
					return self.table[tmp,3]
			else:
				if (self.hash_string_2(string) == self.table[self.hash_string(string),0]) & (self.hash_string_3(string) == self.table[self.hash_string(string),1]):
					return self.table[self.hash_string(string),3] 
		else:
			raise KeyError
    #
	def clean(self):
		self.table[:,3] = int64(-1)
		self.table[:,0:3] = int64(0)

def chr2num(string):
	ln = []
	for i in string:
		ln.append(ord(i))
	return np.array(ln,dtype = np.int64)

#Testing 1
A = dual_hash(20)
A.hash_string(chr2num("AAAAA"))
A.hash_string_2(chr2num("AAAAA"))
A.hash_string_3(chr2num("AAAAA"))
A.set(chr2num("AAAAA"),1)
A.get(chr2num("AAAAA"))
A.set(chr2num("AAAAB"),2)
A.get(chr2num("AAAAB"))
A.set(chr2num("AAABB"),3)
A.get(chr2num("AAABB"))
A.set(chr2num("AABBB"),4)
A.get(chr2num("AABBB"))
A.set(chr2num("AABBB"),5)
A.get(chr2num("AABBB"))
A.set(chr2num("ABBBB"),6)
A.get(chr2num("ABBBB"))
A.set(chr2num("ADDDD"),7)
A.get(chr2num("ADDDD"))
A.set(chr2num("AAAEE"),8)
A.get(chr2num("AAAEE"))
A.set(chr2num("AAABA"),9)
A.get(chr2num("AAABA"))


#Testing 2
def testing(n):
	load_factor = 0.75
	hash_table_length = int64(n//load_factor)
	total_sample = []
	for i in range(n):
		sample = []
		for i in range(5):
			sample.append(chr(random.randint(65,80)))
		sample = "".join(sample)
		total_sample.append(sample)
	#
	hit = 0
	A = dual_hash(hash_table_length)
	for i,j in enumerate(total_sample):
		A.set(chr2num(j),i)
		hit += (i == A.get(chr2num(j))) * 1
	#
	print("Hit Rate: ",hit/n,"\n Collision: ", n - hit)

