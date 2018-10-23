class Lint:
	base = 10**9
	base_digits = 9

	def __init__(self, string):
		self.z = []
		self.sign = 1
		self.read(string)

	def __str__(self):
		if self.is_zero():
			return '0'
		string = ""
		if not self.sign == 1:
			string = '-'
		string = "{0}{1}{2}".format(
			string, (0 if len(self.z) == 0 else self.z.pop()),
			''.join([str(i).zfill(self.base_digits) for i in self.z[::-1]]))
		return string

	def __lt__(self, other):
		if self.sign != other.sign:
			return self.sign < other.sign
		if len(self) != len(other):
			return len(self)*self.sign < len(other)*other.sign
		for i in range(len(self)-1, -1, -1):
			if self.z[i] != other.z[i]:
				return self.z[i]*self.sign < other.z[i]*other.sign
		return False

	def __ge__(self, other):
		return not self < other

	def __len__(self):
		return len(self.z)

	def __neg__(self):
		if self.is_zero():
			return self
		self.sign = -self.sign
		return self

	def __add__(self, other):
		if self.sign == other.sign:
			self.__internal_add(other)
		else:
			if Lint.__compare_abs__(self, other) >= 0:
				self.__internal_sub(other)
			else:
				Lint.swap(self, other)
				self.__internal_sub(other)
		return self

	@staticmethod
	def __compare_abs__(lhs, rhs):
		if len(lhs) != len(rhs):
			return -1 if len(lhs) < len(rhs) else 1
		for i in range(len(lhs)-1, -1, -1):
			if lhs.z[i] != rhs.z[i]:
				return -1 if lhs.z[i] < rhs.z[i] else 1
		return 0

	@staticmethod
	def swap(lhs, rhs):
		lhs.z, rhs.z = [i for i in rhs.z], [i for i in lhs.z]
		lhs.sign, rhs.sign = rhs.sign, lhs.sign

	def __internal_add(self, other):
		i = carry = 0
		while i < len(other) or carry:
			if i == len(self):
				self.z.append(0)
			self.z[i] += carry + (0 if i >= len(other) else other.z[i])
			carry = self.z[i] >= Lint.base
			if carry:
				self.z[i] -= Lint.base
			i += 1

	def __internal_sub(self, other):
		i = carry = 0
		while i < len(other) or carry:
			self.z[i] -= carry + (0 if i >= len(other) else other.z[i])
			carry = self.z[i] < 0
			if carry:
				self.z[i] += Lint.base
			i += 1

	def is_zero(self):
		if len(self) == 0:
			return True
		for i in self.z:
			if i != 0:
				return False
		return True

	def read(self, string):
		pos = 0
		if string[pos] == '-':
			self.sign = -1
			pos += 1
		for i in range(len(string)-1, pos-1, -Lint.base_digits):
			x = 0
			for j in range(max(pos, i-self.base_digits+1), i+1):
				x = x * 10 + int(string[j])
			self.z.append(x)
