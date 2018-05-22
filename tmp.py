from dual_hash import *
from numba import njit


class kgram():
	ngram = None
	@classmethod
	def setting(self,n):
		kgram.ngram = np.int64(n)
	def __init__(self,string):
		self.string = string
		self.perm = self.get_perm()
		self.encode_string = self.encoding_string()
		self.encode_perm = self.encoding_perm()		
	def get_perm(self):
			ln = []
			for i in range(len(self.string)-kgram.ngram + 1):
				ln.append(self.string[i:i+kgram.ngram])	
			return set(ln)
	def encoding_string(self):
		ln = []
		for i in self.string:
			ln.append(ord(i))
		return np.array(ln,dtype = np.int64)
	def encoding_perm(self):
		total_ln = []
		for i in self.perm:
			ln = []
			for k in i:
				ln.append(ord(k))
			total_ln.append(np.array(ln,dtype = np.int64))
		return np.array(total_ln, dtype = np.int64)

spec = [('encode_string',int64[:]),
		('encode_perm',int64[:,:])]

@jitclass(spec)
class kgram_cal():
	def __init__(self,encode_string, encode_perm):
		self.encode_string  =encode_string
		self.encode_perm = encode_perm
	def frequency(self):
			numdict = dual_hash(20**5)
			for i in range(len(self.encode_perm)):
				numdict.assign(self.encode_perm[i],0)
			for i in range(len(self.encode_string)- 5 + 1):
				numdict.iadd(self.encode_string[i:i+5],1)
			return numdict
	def common_key(self,other):
		ln = np.zeros((1,5),dtype = np.int64)
		for i in range(self.encode_perm.shape[0]):
			for j in range(other.encode_perm.shape[0]):
				if (self.encode_perm[i] == other.encode_perm[j]).all():
					ln = np.vstack((ln,np.reshape(self.encode_perm[i],(1,5))))
		ln = np.delete(ln, 0, 0)
		return ln
	def distance(self,other):
		key_sum = 0
		self_sum = 0
		other_sum = 0
		for i in self.common_key(other):
			key_sum += self.frequency().get(i)* other.frequency().get(i)
			self_sum += self.frequency().get(i)* self.frequency().get(i)
			other_sum += other.frequency().get(i)* other.frequency().get(i)
		return key_sum/(np.sqrt(self_sum)*np.sqrt(other_sum))
#	def distance(self,other):


kgram.setting(5)
A = kgram("ABBBBBCDDDDBCCBBBCCCBCCCBBBCCCBBBCCC")
B = kgram("ABBBBBCDEEDBCCBBBBCCBCCCBBBCCCBBBCCC")
A = kgram_cal(A.encode_string,A.encode_perm)
B = kgram_cal(B.encode_string,B.encode_perm)

A.common_key(B)
A.distance(B)
A.frequency().get(chr2num("BBCCC"))
