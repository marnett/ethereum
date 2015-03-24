import serpent
from pyethereum import tester, utils, abi

serpent_code = '''
data winnings_table[3][3]

def init():
	#If 0, tie
	#If 1, player 1 wins
	#If 2, player 2 wins

	#0 = rock
	#1 = paper
	#2 = scissors

	self.winnings_table[0][0] = 0
	self.winnings_table[1][1] = 0
	self.winnings_table[2][2] = 0

	#Rock beats scissors
	self.winnings_table[0][2] = 1
	self.winnings_table[2][0] = 2

	#Scissors beats paper
	self.winnings_table[2][1] = 1
	self.winnings_table[1][2] = 2

	#Paper beats rock
	self.winnings_table[1][0] = 1
	self.winnings_table[0][1] = 2

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

def do(a):
	if self.storage["player1"] == msg.sender:
		self.storage["p1value"] = a
		return(1)
	elif self.storage["player2"] ==  msg.sender:
		self.storage["p2value"] = a
		return(2)
	else:
		return(0)

def check():
	#If player 1 wins
	if self.winnings_table[self.storage["p1value"]][self.storage["p2value"]] == 1:
		send(self.storage["player1"], self.storage["WINNINGS"])
		return(1)
	#If player 2 wins
	elif self.winnings_table[self.storage["p1value"]][self.storage["p2value"]] == 2:
		send(self.storage["player2"], self.storage["WINNINGS"])
		return(2)
	#If no one wins
	else:
		send(self.storage["player1"], self.storage["p1value"])
		send(self.storage["player2"], self.storage["p2value"])

def balance_check():
	log(self.storage["player1"].balance)
	log(self.storage["player2"].balance)
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
