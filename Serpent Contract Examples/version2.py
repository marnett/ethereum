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
		if msg.value == 1000:
			self.storage["WINNINGS"] = self.storage["WINNINGS"] + msg.value
			self.storage["player1"] = msg.sender
			return(1)
		return (0)
	elif not self.storage["player2"]:
		if msg.value == 1000:
			self.storage["WINNINGS"] = self.storage["WINNINGS"] + msg.value
			self.storage["player2"] = msg.sender
			return(2)
		return (0)
	else:
		return(0)

def input(player_commitment):
	if self.storage["player1"] == msg.sender:
		self.storage["p1hash"] = player_commitment
		return(1)
	elif self.storage["player2"] ==  msg.sender:
		self.storage["p2hash"] = player_commitment
		return(2)
	else:
		return(0)

def verify(choice, nonce):
	if self.storage["player1"] == msg.sender:
		player_one_hash = array(1)
		player_one_hash[0] = choice + nonce
		self.storage["p1value"] = choice
	elif self.storage["player2"] == msg.sender:
		player_two_hash = array(1)
		player_two_hash[0] = choice + nonce
		self.storage["p2value"] = choice
	else:
		return(-1)

def check():
	if self.storage["p1value"] and self.storage["p2value"]:
		#If player 1 wins
		if self.winnings_table[self.storage["p1value"]][self.storage["p2value"]] == 1:
			if self.open("player1") == 0:
				send(self.storage["player2"], self.storage["WINNINGS"])
			elif self.open("player2") == 0:
				send(self.storage["player1"], self.storage["WINNINGS"])
			else:
				send(self.storage["player1"], self.storage["WINNINGS"])
		#If player 2 wins
		elif self.winnings_table[self.storage["p1value"]][self.storage["p2value"]] == 2:
			if self.open("player1") == 0:
				send(self.storage["player2"], self.storage["WINNINGS"])
			elif self.open("player2") == 0:
				send(self.storage["player1"], self.storage["WINNINGS"])
			else:
				send(self.storage["player2"], self.storage["WINNINGS"])
		#If no one wins
		else:
			if self.open("player1") == 0:
				send(self.storage["player2"], self.storage["WINNINGS"])
			elif self.open("player2") == 0:
				send(self.storage["player1"], self.storage["WINNINGS"])
			else:
				send(self.storage["player1"], 1000)
				send(self.storage["player2"], 1000)
	else:
		return(-1)

def open(player):
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


data = translator.encode('input', [1])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('input', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('input', [0])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('input', s.send(tester.k1, c, 0, data))
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
