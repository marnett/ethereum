import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def deposit():
	if not self.storage[msg.sender]:
		self.storage[msg.sender] = 0
	self.storage[msg.sender] += msg.value
	return(1)
def withdraw(amount):
	if self.storage[msg.sender] < amount:
		return(-1)
	else:
		self.storage[msg.sender] -= amount
		send(0, msg.sender, amount)
		return(1)
def transfer(amount, destination):
	if self.storage[msg.sender] < amount:
		return(-1)
	else:
		if not self.storage[destination]:
			self.storage[destination] = 0
		self.storage[msg.sender] -= amount
		self.storage[destination] += amount
		return(1)
def balance():
	log(tx.gasprice)
	if not self.storage[msg.sender]:
		return(-1)
	else:
		return(self.storage[msg.sender])
'''

public_k1 = utils.privtoaddr(tester.k1)

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

s = tester.state()
print(s.block.gas_used)
c = s.evm(evm_code)

print(s.block.gas_used)

data = translator.encode('deposit', [])
o = translator.decode('deposit', s.send(tester.k0, c, 1000, data))
print(o)

print(s.block.gas_used)

data = translator.encode('withdraw', [1000])
o = translator.decode('withdraw', s.send(tester.k0, c, 0, data))
print(o)

print(s.block.gas_used)

data = translator.encode('withdraw', [1000])
o = translator.decode('withdraw', s.send(tester.k0, c, 0, data))
print(o)

print(s.block.gas_used)

data = translator.encode('deposit', [])
o = translator.decode('deposit', s.send(tester.k0, c, 1000, data))
print(o)

print(s.block.gas_used)

data = translator.encode('transfer', [500, public_k1])
o = translator.decode('transfer', s.send(tester.k0, c, 0, data))
print(o)

print(s.block.gas_used)

data = translator.encode('balance', [])
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

print(s.block.gas_used)

data = translator.encode('balance', [])
o = translator.decode('balance', s.send(tester.k1, c, 0, data))
print(o)

print(s.block.gas_used)
