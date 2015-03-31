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
		if msg.value >= 1000:
			self.storage["WINNINGS"] = self.storage["WINNINGS"] + msg.value
			self.storage["player1"] = msg.sender
			if msg.value - 1000 > 0:
				send(25,msg.sender,msg.value-1000)
			return(1)
		else:
			send(25,msg.sender,msg.value)
			return(0)
	elif not self.storage["player2"]:
		if msg.value >= 1000:
			self.storage["WINNINGS"] = self.storage["WINNINGS"] + msg.value
			self.storage["player2"] = msg.sender
			if msg.value - 1000 > 0:
				send(25,msg.sender,msg.value-1000)
			return(2)
		else:
			send(25,msg.sender,msg.value)
			return(0)
	else:
		send(25,msg.sender,msg.value)
		return(0)

def input(player_commitment):
	if self.storage["player1"] == msg.sender:
		self.storage["p1commit"] = player_commitment
		return (1)
	elif self.storage["player2"] ==  msg.sender:
		self.storage["p2commit"] = player_commitment
		return(2)
	else:
		return(0)

def open(choice, nonce):
	if self.storage["player1"] == msg.sender:
		if sha3([msg.sender, choice, nonce], items=3) == self.storage["p1commit"]:
			self.storage["p1value"] = choice
			self.storage["p1reveal"] = 1
			return(1)
		else:
			return(0)
	elif self.storage["player2"] == msg.sender:
		if sha3([msg.sender, choice, nonce], items=3) == self.storage["p2commit"]:
			self.storage["p2value"] = choice
			self.storage["p2reveal"] = 1
			return(2)
		else:
			return(0)
	else:
		return(-1)

def check():
	#check to see if both players have revealed answer
	if self.storage["p1reveal"] == 1 and self.storage["p2reveal"] == 1:
		#If player 1 wins
		if self.winnings_table[self.storage["p1value"]][self.storage["p2value"]] == 1:
			send(100,self.storage["player1"], self.storage["WINNINGS"])
			return(1)
		#If player 2 wins
		elif self.winnings_table[self.storage["p1value"]][self.storage["p2value"]] == 2:
			send(100,self.storage["player2"], self.storage["WINNINGS"])
			return(2)
		#If no one wins
		else:
			send(100,self.storage["player1"], 1000)
			send(100,self.storage["player2"], 1000)
			return(0)
	#if p1 revealed but p2 did not, send money to p1
	elif self.storage["p1reveal"] == 1 and not self.storage["p2reveal"] == 1:
		send(100,self.storage["player1"], self.storage["WINNINGS"])
		return(1)
	#if p2 revealed but p1 did not, send money to p2
	elif not self.storage["p1reveal"] == 1 and self.storage["p2reveal"] == 1:
		send(100,self.storage["player2"], self.storage["WINNINGS"])
		return(2)
	#if neither p1 nor p2 revealed, keep both of their bets
	else:
		return(-1)

def balance_check():
	log(self.storage["player1"].balance)
	log(self.storage["player2"].balance)

'''

evm_code = serpent.compile(serpent_code)
translator = abi.ContractTranslator(serpent.mk_full_signature(serpent_code))

data = translator.encode('add_player', [])
s = tester.state()
c = s.evm(evm_code)
o = translator.decode('add_player', s.send(tester.k0, c, 1000, data))
print(o)

data = translator.encode('add_player', [])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('add_player', s.send(tester.k1, c, 1000, data))
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
