import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def register(key, value):
	if not self.storage[key]:
		self.storage[key] = value
		return(1)
	else:
		return(-1)

def get(key):
	if not self.storage[key]:
		return(-1)
	else:
		return(self.storage[key])
'''

public_k1 = utils.privtoaddr(tester.k1)

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('register', ["Bob", 10])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('register', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('register', ["Bob", 15])
o = translator.decode('register', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('get', ["Bob"])
o = translator.decode('get', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('get', ["Bob"])
o = translator.decode('get', s.send(tester.k0, c, 0, data))
print(o)
