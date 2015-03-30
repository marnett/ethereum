import serpent
from pyethereum import tester, utils, abi
from sha3 import sha3_256
import sys
import struct

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
	if self.test_callstack() != 1: return(-1)

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
	if self.test_callstack() != 1: return(-1)

	if self.storage["player1"] == msg.sender:
		self.storage["p1commit"] = player_commitment
		return(1)
	elif self.storage["player2"] ==  msg.sender:
		self.storage["p2commit"] = player_commitment
		return(2)
	else:
		return(0)

def open(choice, nonce):
	if self.test_callstack() != 1: return(-1)

	if self.storage["player1"] == msg.sender:
		if sha3([msg.sender, choice, nonce], items=3) == self.storage["p1commit"]:
			self.storage["p1value"] = choice
			self.storage["p1reveal"] = true
			if self.storage["timer_start"] == null:
				self.storage["timer_start"] = block.number
			return(1)
		else:
			return(0)
	elif self.storage["player2"] == msg.sender:
		if sha3([msg.sender, choice, nonce], items=3) == self.storage["p2commit"]:
			self.storage["p2value"] = choice
			self.storage["p2reveal"] = true
			if self.storage["timer_start"] == null:
				self.storage["timer_start"] = block.number
			return(2)
		else:
			return(0)
	else:
		return(-1)

def check():
	if self.test_callstack() != 1: return(-3)

	#Check to make sure at least 10 blocks have been given for both players to reveal their play.
	if block.number - self.storage["timer_start"] < 10: return(-2)

	#check to see if both players have revealed answer
	if self.storage["p1reveal"] == true and self.storage["p2reveal"] == true:
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
	elif self.storage["p1reveal"] and not self.storage["p2reveal"]:
		send(100,self.storage["player1"], self.storage["WINNINGS"])
		return(1)
	#if p2 revealed but p1 did not, send money to p2
	elif not self.storage["p1reveal"] and self.storage["p2reveal"]:
		send(100,self.storage["player2"], self.storage["WINNINGS"])
		return(2)
	#if neither p1 nor p2 revealed, keep both of their bets
	else:
		return(-1)

def balance_check():
	log(self.storage["player1"].balance)
	log(self.storage["player2"].balance)

def test_callstack():
	return(1)
'''

tobytearr = lambda n, L: [] if L == 0 else tobytearr(n / 256, L - 1)+[n % 256]

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

choice1 = 0x01
nonce1 = 0x01
something1 = struct.unpack("hhhhhhhhhhhhhhhh", tester.k0)

bin = bytearray()

for i in range(0,32):
	sm1 = something1[i]
	print(sm1)
	sm2 = something1[i]
	bin.append(sm1 >> 7)
	print((sm1 >> (8*0)) & 0xFF)
	print((sm2 >> (8*1)) & 0xFF)
	bin.append((sm2 | 0x00001111))

print(bin)


user1 = ''.join(map(chr, tobytearr(something1,32)))
ch1 = ''.join(map(chr, tobytearr(choice1, 32)))
no1 = ''.join(map(chr, tobytearr(nonce1, 32)))
s1 = ''.join([user1, ch1, no1])
comm1 = utils.sha3(s1)

choice2 = 0x02
nonce2 = 0x01
something2 = struct.unpack("hhhhhhhhhhhhhhhh", tester.k1)[0]
user2 = ''.join(map(chr, tobytearr(something2,32)))
ch2 = ''.join(map(chr, tobytearr(choice2, 32)))
no2 = ''.join(map(chr, tobytearr(nonce2, 32)))
s2 = ''.join([user2, ch2, no2])
comm2 = utils.sha3(s2)

data = translator.encode('input', [comm1])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('input', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('input', [comm2])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('input', s.send(tester.k1, c, 0, data))
print(o)

data = translator.encode('open', [1, 0x01])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('input', s.send(tester.k0, c, 0, data))
print(o)

data = translator.encode('open', [2, 0x01])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('input', s.send(tester.k1, c, 0, data))
print(o)

s.mine(11)

data = translator.encode('check', [])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('check', s.send(tester.k1, c, 0, data))
print(o)

data = translator.encode('balance_check', [])
#s = tester.state()
#c = s.evm(evm_code)
o = translator.decode('balance_check', s.send(tester.k0, c, 0, data))
