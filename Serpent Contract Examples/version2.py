import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
def init():
	self.storage["MAX_PLAYERS"] = 2
	self.storage["WINNINGS"] = 0

def add_player():
	if not self.storage["player1"]:
		self.storage["player1"] = msg.sender
		self.storage["WINNINGS"] = self.storage["WINNINGS"] + msg.value
		return(1)
	elif not self.storage["player2"]:
		self.storage["player2"] = msg.sender
		self.storage["WINNINGS"] = self.storage["WINNINGS"] + msg.value
		return(2)
	else:
		return(0)

def do(player_hash):
	if self.storage["player1"] == msg.sender:
		self.storage["p1hash"] = player_hash
		return(1)
	elif self.storage["player2"] ==  msg.sender:
		self.storage["p2hash"] = player_hash
		return(2)
	else:
		return(0)

def verify(a, nonce):
	if self.storage["player1"] == msg.sender:
		player_one_hash = array(1)
		player_one_hash[0] = a + nonce
		self.storage["p1value"] = a
	elif self.storage["player2"] == msg.sender:
		player_two_hash = array(1)
		player_two_hash[0] = a + nonce
		self.storage["p2value"] = a
	else:
		return(-1)

def check():
	if self.storage["p1value"] and self.storage["p2value"]:
		if self.storage["p1value"] == self.storage["p2value"]:
			if verify("player1") == 0:
				pay_out_to("player2")
			elif verify("player2") == 0:
				pay_out_to("player1")
			else:
				return(0)
		elif self.storage["p1value"] > self.storage["p2value"] and self.storage["p1value"] - self.storage["p2value"] == 1:
			if verify("player1") == 0:
				pay_out_to("player2")
			elif verify("player2") == 0:
				pay_out_to("player1")
			else
				pay_out_to("player1") 
				return(1)
		elif self.storage["p1value"] > self.storage["p2value"] and self.storage["p1value"] - self.storage["p2value"] == 2:
			if verify("player1") == 0:
				pay_out_to("player2")
			elif verify("player2") == 0:
				pay_out_to("player1")
			else:
				pay_out_to("player2")
				return(2)
		elif self.storage["p2value"] > self.storage["p1value"] and self.storage["p2value"] - self.storage["p1value"] == 1:
			if verify("player1") == 0:
				pay_out_to("player2")
			elif verify("player2") == 0:
				pay_out_to("player1")
			else:
				pay_out_to("player2")		
				return(2)
		elif self.storage["p2value"] > self.storage["p1value"] and self.storage["p2value"] - self.storage["p1value"] == 2:
			if verify("player1") == 0:
				pay_out_to("player2")
			elif verify("player2") == 0:
				pay_out_to("player1")
			else:
				pay_out_to("player1")		
				return(1)
	else:
		return(-1)

def verify(player, a, nonce):
	if player == "player1":
		if sha256(player_one_hash[0], items=1) == self.storage["p1hash"]:
			return 1
		else:
			return 0
	else:
		if sha256(player_two_hash[0], items=1) == self.storage["p2hash"]:
			return 1
		else:
			return 0


def balance_check():
	log(self.storage["player1"].balance)
	log(self.storage["player2"].balance)

def pay_out_to(player):
	send(self.storage[player], self.storage["WINNINGS"])
'''

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('add_player', [])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('add_player', s.send(tester.k0, c, 50, data))
print(o)

data = translator.encode('add_player', [])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('add_player', s.send(tester.k1, c, 50, data))
print(o)


data = translator.encode('do', [1])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('do', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('do', [0])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('do', s.send(tester.k1, c, 0, data))
print(o)

data = translator.encode('check', [])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('check', s.send(tester.k1, c, 0, data))
print(o)

data = translator.encode('balance_check', [])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('balance_check', s.send(tester.k1, c, 0, data))
