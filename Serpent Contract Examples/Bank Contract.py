import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def init():
	self.storage[msg.sender] = 10000
	self.storage["Taylor"] = 0
def code(recipient, value):
	to = self.storage[recipient]
	from = msg.sender
	amount = value
	if self.storage[from] >= amount:
		self.storage[from] = self.storage[from]  - amount
		self.storage[recipient] = self.storage[recipient] + amount
		return (self.storage[recipient])
'''

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('code', ["Taylor", 1000])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('code', s.send(tester.k0, c, 0, data))
print(o)
