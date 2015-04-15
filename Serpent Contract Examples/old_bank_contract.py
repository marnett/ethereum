import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def init():
	self.storage[msg.sender] = 10000
def send_currency_to(value, destination):
	if self.storage[msg.sender] >= value:
		self.storage[msg.sender] = self.storage[msg.sender]  - value
		self.storage[destination] = self.storage[destination] + value
		return(1)
	return(-1)
def balance_check(addr):
	return(self.storage[addr])

'''

public_k0 = utils.privtoaddr(tester.k0)
public_k1 = utils.privtoaddr(tester.k1)

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('send_currency_to', [1000, public_k1])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('send_currency_to', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('balance_check'), [public_k0]
o = translator.decode('balance_check', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('balance_check'), [public_k1]
o = translator.decode('balance_check', s.send(tester.k1, c, 0, data))
print(o)