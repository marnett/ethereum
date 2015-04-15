import serpent
from pyethereum import tester, utils, abi

#A mutual credit system will zero out when all debts are paid.

serpent_code = '''
#addr is the public key of the party we are sending the money to
#value is the value of currency we are sending. 
def transfer(addr, value):
    #We are going to max out debt at 1000 credits per person
    if self.storage[msg.sender] - value < -1000:
        return(-1)
    else:
        #If they have not exceeded their debt limit, we do the transaction
        self.storage[msg.sender] -= value
        self.storage[addr] += value
        return(0)

#Simply return the balance at that address
def balance(addr):
    return(self.storage[addr])

'''
public_k0 = utils.privtoaddr(tester.k0)
public_k1 = utils.privtoaddr(tester.k1)

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('balance', [public_k0])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('balance', [public_k1])
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('transfer', [public_k1, 500])
o = translator.decode('transfer', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('balance', [public_k0])
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('balance', [public_k1])
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('transfer', [public_k0, 1500])
o = translator.decode('transfer', s.send(tester.k1, c, 0, data))
print(o)

data = translator.encode('balance', [public_k0])
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('balance', [public_k1])
o = translator.decode('balance', s.send(tester.k0, c, 0, data))
print(o)

