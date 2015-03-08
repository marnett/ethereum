import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def init():
    contract.storage[((msg.sender * 0x10) + 0x1)] = 0x1
    contract.storage[((msg.sender * 0x10) + 0x2)] = 0x1
def code(rand, value):
    toAsset = (rand * 0x10) + 0x1
    toDebt = (rand * 0x10) + 0x2
    fromAsset = (msg.sender * 0x10) + 0x1
    fromDebt = (msg.sender * 0x10) + 0x2
    if contract.storage[fromAsset] >= value:
        contract.storage[fromAsset] = contract.storage[fromAsset]  - value
        return(fromAsset)   
    else:
        contract.storage[fromDebt] = value - contract.storage[fromAsset]
        contract.storage[fromAsset] = 0
        return(fromDebt)
    if contract.storage[toDebt] >= value:
        contract.storage[toDebt] = contract.storage[toDebt] - value
        return(toDebt)
    else:
        value = value - contract.storage[toDebt]   
        contract.storage[toAsset] = contract.storage[toAsset] + value
        contract.storage[toDebt] = 0
        return(toAsset)
'''

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('code', [123, 1000])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('code', s.send(tester.k0, c, 0, data))
print(o)
