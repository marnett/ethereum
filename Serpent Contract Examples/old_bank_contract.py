import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def init():
	self.storage[msg.sender] = 10000
	self.storage["Taylor"] = 0
def send_currency_to(value):
	to = "Taylor"
	from = msg.sender
	amount = value
	if self.storage[from] >= amount:
		self.storage[from] = self.storage[from]  - amount
		self.storage[to] = self.storage[to] + amount
		return (self.storage[to])
'''

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('send_currency_to', [1000])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('send_currency_to', s.send(tester.k0, c, 0, data))
print(o)