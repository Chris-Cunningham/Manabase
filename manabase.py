#
#
#
#
#
#
# Warning: This program written by a non-professional programmer. 
# This is not the best piece of software that was written today.
# Constructive criticism and updates welcome!
#
# --Chris
#
#
#
#

# We will use random.sample as our shuffler.
import random

# We will deep copy some dictionaries of lists.
from copy import deepcopy

# We need some square roots.
import math

# We will use re.split in the deck parser.
import re

# When we want to exit, we want to just use exit()
from sys import exit

# We will need to import datetime to time our trials.
from datetime import datetime

# Get the most updated AllCards.json from mtgjson.com. Then we use it here.
import json
json_data=open('AllCards.json')
cardDatabase = json.load(json_data)
json_data.close()

# How many turns out are we going? How many trials? Are we on the play [False] or on the draw [True]?
maxturns = 5
trials = 5000
onthedraw = False

# Mulligan 7-card hands with 0,1,6,7 lands,  ... 6-card hands with 0,1,5,6 lands, ... 5-card hands with 0,5 lands.
# With 24 lands, we should end up with 7 lands: 84.4%      6 lands: 11.7%      5 lands: 3.4%      4 lands: 0.5%
mulligans = True

# deckfile = 'decks/scgpc-mardu-midrange-kent-ketter.txt'
# deckfile = 'decks/scgpc-abzan-aggro-BBD.txt'
# deckfile = 'decks/scgpc-uw-heroic-tom-ross.txt'
# deckfile = 'decks/scgpc-rg-aggro-logan-mize.txt'
deckfile = 'decks/scgpc-jeskai-tokens-ross-merriam.txt'
# deckfile = 'decks/scgpc-temur-midrange-jeff-hoogland.txt'
# deckfile = 'decks/scgpc-uw-control-jim-davis.txt'
# deckfile = 'decks/scgiq-gr-monsters-daniel-carten.txt'

debug = {}
debug['Minimal'] = True
debug['Trial'] = True
debug['DrawCard'] = False
debug['CastSpell'] = False
debug['parseMana'] = False
debug['LinesOfPlay'] = False
debug['CastsThisTrial'] = False
debug['parseDecklist'] = False
debug['manaAvailable'] = False
debug['mulligans'] = False

class LineOfPlay:
	# A line of play is a dictionary that keeps track of a sequence of plays. For example,
	# a line of play in human terms would be "Turn 1 play island and pass; turn 2 play Mountain and Goblin Electromancer."
	# The things kept track of in a line of play are:
	# Plays: a sequence of sequences. Plays[0] shows the cards played on turn 0. Plays[1] shows the cards played on turn 1. 
	# Hand: a list of cards still in your hand
	# Deck: a list of cards still remaining in the deck, in order

	def __init__(self, plays, hand, deck):
		self.plays = plays
		self.hand = hand	
		self.deck = deck

	def __repr__(self):
		# A line of play is a list of plays, a sequence of your hand, and the cards in the deck.
		return 'Turns: '+str(len(self.plays))+' Plays: ' + self.plays.__repr__() + ' Hand: ' + self.hand.__repr__() + ' Deck: ' + self.deck.__repr__()

	def draw_card(self):
		# The things we can do with a line of play include "drawing a card":
		# Pop the first item out of the list and put it in your hand.
		self.hand.append(self.deck.pop(0))
		if debug['DrawCard']: print('  Drew a card:',self)

	def turn(self):
		# Plays is a list of lists. The length of this list is the turn we are on.
		return len(self.plays)

	def manaAvailable(self):
		# In a certain line of play, we want to know which combination of mana is available. New lands and summoning-sick guys aren't available.

		# Make a list of available cards (so we dont count tapped lands on the turn they come out and don't count summoning-sick dudes.)
		availablecards = []
		for i in range(self.turn()):
			# most cards played are available for use. First add them all.
			for card in self.plays[i]:
				if card in manaDatabase:
					availablecards.append(card)

		# For the one(s) we just played, check whether it is a tapland or a summoning sick creature.
		if self.turn() > 0:
			for cardplayedthisturn in self.plays[self.turn()-1]:
				# The only way a land is not available is if the land has text that contains the word 'tapped'
				if isLand(cardplayedthisturn) and 'text' in cardDatabase[cardplayedthisturn]:
					if 'tapped' in cardDatabase[cardplayedthisturn]['text']:
						availablecards.remove(cardplayedthisturn)
				# A creature is unusable if it entered play this turn as well. TODO: Dryad Arbor, I guess, ugh why
				if isCreature(cardplayedthisturn):
					if 'text' in cardDatabase[cardplayedthisturn]:
						# Are there hasty mana guys? who knows. If there are, we will let them be available. Lol.
						if 'Haste' not in cardDatabase[cardplayedthisturn]['text']:
							availablecards.remove(cardplayedthisturn)
					else:
						# Vanilla creatures are also summoning sick, so unavailable.
						availablecards.remove(cardplayedthisturn)

		# Now we have a list of manaproducers available to us, but we need to see what combinations of mana we can make.
		# Luckily each manaproducer in the deck has already been parsed and has a list of mana (in ManaPool format) available. 
		# For example the dictionary has manaDatabase['Island'] = [{U}] and manaDatabase['Temple of Malice'] = [{R}, {B}] and manaDatabase['Elvish Mystic'] = [{G}]
		# So if your lands available are Island and Temple of Malice, your availablemana should be [{0}, {1}, {R}, {U}, {B}, {2}, {1}{R}, {1}{U}, {1}{B}, {U}{R}, {U}{B}]
		availablemana = [ManaPool('{0}')]
		for card in availablecards:
			if debug['manaAvailable']: print('       Tapping for mana:',card)
			newoptionswiththiscard = []
			# If there is an urborg in play, we can tap for black mana.
			for play in self.plays:
				if 'Urborg, Tomb of Yawgmoth' in play:
					for manaoption in availablemana:
						# Each of the options we had before this card needs to get appended with one of these.
						newoptionswiththiscard.append(manaoption + ManaPool('{B}'))

			# We can then add on this card's mana symbols. Danger: the mana symbols might include things like 'Scry' or 'FetchU' which we should skip.
			for manasymbol in manaDatabase[card]:
				if manasymbol != 'scry':
					for manaoption in availablemana:
						# Each of the options we had before this card needs to get appended with one of these.
						newoptionswiththiscard.append(manaoption + manasymbol)
			# We can also just treat the new one as a colorless.
			manasymbol = ManaPool('{1}')
			for manaoption in availablemana:
				# Each of the options we had before this card needs to get appended with one of these.
				newoptionswiththiscard.append(manaoption + manasymbol)

			# Okay, if the new option is actually new, append it.
			for newoption in newoptionswiththiscard:
				if newoption not in availablemana:
					availablemana.append(newoption)

			if debug['manaAvailable']: print('       Possible mana pools are now:',availablemana)

		return availablemana

def parseMana(decklist):
	# This function should take a decklist and go through all the manaproducers creating a small database.
	# For example, a Jeskai decklist might end up with the following manaDatabase:
	# manaDatabase['Island'] = ['{U}']   (not the string {U}, but the ManaPool object)
	# manaDatabase['Mountain'] = ['{R}']
	# manaDatabase['Temple of Epiphany'] = ['{U}','{R}']
	# manaDatabase['Flooded Strand'] = ['FetchU','FetchW']    (the string 'FetchU')
	# However, green decks might have mana dorks, so they and manarocks will live in here too:
	# manaDatabase['Elvish Mystic'] = ['{G}']
	# manaDatabase['Sol Ring'] = ['{2}']

	if debug['parseMana']: print('')
	if debug['parseMana']: print('Beginning Mana Parser.')

	global manaDatabase 
	manaDatabase = {}

	# Every lands database needs some basic lands.
	manaDatabase['Island'] = [ManaPool('{U}')]
	manaDatabase['Mountain'] = [ManaPool('{R}')]
	manaDatabase['Swamp'] = [ManaPool('{B}')]
	manaDatabase['Forest'] = [ManaPool('{G}')]
	manaDatabase['Plains'] = [ManaPool('{W}')]

	for card in decklist:
		if isLand(card) and card not in manaDatabase:
			if debug['parseMana']: print('Parsing land:',card)
			manaDatabase[card] = []
			if 'text' in cardDatabase[card]:
				# Parse through the text looking for mana symbols. We don't want to start counting until after the tap symbol (see Nykthos, Shrine to Nyx).
				# When we get to a { we start a new symbol; a } ends it.
				currentsymbol = ''
				flagAfterTapSymbol = False
				for char in cardDatabase[card]['text']:
					if char =='{':
						currentsymbol = '{'
					elif char == '}':
						# After we get to the tap symbol, it's time to start adding to the list.
						if currentsymbol == '{T':
							flagAfterTapSymbol = True
						elif flagAfterTapSymbol:
							manaDatabase[card].append(ManaPool(currentsymbol+char))
					elif char == '.':
						# Again, see the two tap symbols in Nykthos for why this is here. Many lands have multiple sentences, which are separate abilities.
						flagAfterTapSymbol = False
					else:
						# This is useful if the mana cost is 15, so we don't end up adding 6 to the mana cost.
						currentsymbol += char
				# Parse through the text looking for "scry" or "fetch."
				if 'scry' in cardDatabase[card]['text']:
					manaDatabase[card].append('scry')
				# This mana confluence catcher is definitely going to cause some false positives; TODO
				if 'any color' in cardDatabase[card]['text']:
					manaDatabase[card].append(ManaPool('{W}'))
					manaDatabase[card].append(ManaPool('{U}'))
					manaDatabase[card].append(ManaPool('{R}'))
					manaDatabase[card].append(ManaPool('{B}'))
					manaDatabase[card].append(ManaPool('{G}'))
				# This fetchland catcher is also going to cause some false positives, like Evolving Wilds TODO
				if 'Search your library' in  cardDatabase[card]['text']:
					if 'Plains' in cardDatabase[card]['text']:
						manaDatabase[card].append('FetchW')
					if 'Swamp' in cardDatabase[card]['text']:
						manaDatabase[card].append('FetchB')
					if 'Mountain' in cardDatabase[card]['text']:
						manaDatabase[card].append('FetchR')
					if 'Island' in cardDatabase[card]['text']:
						manaDatabase[card].append('FetchU')
					if 'Forest' in cardDatabase[card]['text']:
						manaDatabase[card].append('FetchG')
			if debug['parseMana']: print('Parsed as ',manaDatabase[card])
		elif card not in manaDatabase:
			# Okay, we're going to try to find all the mana dorks or manarocks.
			if debug['parseMana']: print('Parsing nonland card:',card)
			if 'text' in cardDatabase[card]:
				# Manadorks and rocks should have these phrases:
				if '{T}: Add' in cardDatabase[card]['text'] and 'to your mana pool' in cardDatabase[card]['text']:
					# Start one character after "{T}: Add" and go up to "to your mana pool" and see what we get.
					manaDatabase[card] = []
					startLocation = cardDatabase[card]['text'].index('{T}: Add') + 9
					endLocation = cardDatabase[card]['text'].index('to your mana pool') - 1
					manaToParse = cardDatabase[card]['text'][startLocation:endLocation]
					if debug['parseMana']: print(card,'appears to be a mana producer; now parsing the string "',manaToParse,'"')
					# Split the mana phrase into parts, so Sylvan Caryatid gets ['one','mana','of','any','color'] and Noble Hierarch is ['{G}','{W}','or','{U}']
					for symbol in manaToParse.split():
						# This implementation creates false positive on "of any color that lands you control could produce" type cards; not sure there are any nonland cards that do this.
						if symbol == 'any':
							manaDatabase[card].append(ManaPool('{W}'))
							manaDatabase[card].append(ManaPool('{U}'))
							manaDatabase[card].append(ManaPool('{R}'))
							manaDatabase[card].append(ManaPool('{B}'))
							manaDatabase[card].append(ManaPool('{G}'))
						else:
							# If you pass nonsense to ManaPool, like '{H}', it doesn't error; it just gives you back 0 mana.
							mana = ManaPool(symbol)
							if mana != ManaPool('{0}'):
								manaDatabase[card].append(ManaPool(symbol))
					if debug['parseMana']: print('Parsed as ',manaDatabase[card])

	if debug['parseMana']: print('End of Mana Parser. Results below:')
	if debug['parseMana']: print(manaDatabase)
	if debug['parseMana']: print('')

class ManaPool:
	# A mana pool is really an object, for example 1U + 2UR = 3UUR.
	# We will store this as a number, some blue, some red, and so on.
	# A mana cost like {3}{U}{U}{G} needs to be the thing that starts it.
	def __init__(self, manacost):
		# This implementation would completely fail for, say, Boros Reckoner -- but that's why it is called
		# a Mana Pool, and not a Mana Cost. This implementation should allow all possible Mana Pools. If you
		# pass a nonsense string in here, like {H}, then you should just get {0} back.
		self.colorless = 0
		self.blue = 0
		self.green = 0
		self.white = 0
		self.red = 0
		self.black = 0

		# Parse through the mana cost. When we get to a { we start a new symbol, a } ends it.
		currentsymbol = ''
		for char in manacost:
			if char =='{':
				currentsymbol = ''
			elif char == '}':
				if currentsymbol == 'U':
					self.blue += 1
				elif currentsymbol == 'G':
					self.green += 1
				elif currentsymbol == 'R':
					self.red += 1
				elif currentsymbol == 'W':
					self.white += 1
				elif currentsymbol == 'B':
					self.black += 1
				elif currentsymbol == 'X':
					# Oh no! I have no idea what to set X to. Apparently we'll go with zero.
					pass
				elif is_int(currentsymbol):
					self.colorless += int(currentsymbol)
			else:
				# This is useful if the mana cost is 15, so we don't end up adding 6 to the mana cost.
				currentsymbol += char

	def __repr__(self):
		# The initializer for a mana pool is something like the string '{3}{W}{W}{G}', so the string representation gives back a string like that.
		string = ''
		if self.colorless > 0:
			string += ('{' + str(self.colorless) + '}')
		for i in range(self.white):
			string += '{W}'
		for i in range(self.blue):
			string += '{U}'
		for i in range(self.black):
			string += '{B}'
		for i in range(self.red):
			string += '{R}'
		for i in range(self.green):
			string += '{G}'
		if string == '':
			return '{0}'
		return string

	def __iadd__(self, other):
		# This implements += for mana pools.
		self.colorless += other.colorless
		self.blue += other.blue
		self.green += other.green
		self.white += other.white
		self.red += other.red
		self.black += other.black
		return self

	def __add__(self, other):
		# This lets us add mana pools with just plus signs.
		thesum = ManaPool('{0}')
		thesum.colorless = self.colorless + other.colorless
		thesum.blue = self.blue + other.blue
		thesum.green = self.green + other.green
		thesum.white = self.white + other.white
		thesum.red = self.red + other.red
		thesum.black = self.black + other.black
		return thesum

	def __isub__(self,other):
		# This implements += for mana pools.
		self.colorless -= other.colorless
		self.blue -= other.blue
		self.green -= other.green
		self.white -= other.white
		self.red -= other.red
		self.black -= other.black
		if self.isValid():
			return self
		else:
			raise ArithmeticError('Cannot subtract these mana pools.')

	def __sub__(self,other):
		# This lets us remove mana from the mana pool.
		thediff = ManaPool('{0}')
		thediff.colorless = self.colorless - other.colorless
		thediff.blue = self.blue - other.blue
		thediff.green = self.green - other.green
		thediff.white = self.white - other.white
		thediff.red = self.red - other.red
		thediff.black = self.black - other.black
		if thediff.isValid():
			return thediff
		else:
			raise ArithmeticError('Cannot subtract these mana pools.')

	def __eq__(self, other):
		# Mana Pools are equal if they have the same type and the dictionaries underneath are the same.
		if type(other) is type(self):
			return self.__dict__ == other.__dict__
		return False

	def isValid(self):
		return ((self.colorless >=0) and (self.blue >=0) and (self.green >= 0) and (self.white >= 0) and (self.black >= 0) and (self.red >= 0))

def isLand(card):
	# We just want to check whether this card is a land or not. "card" is a string, so we'll have to use it as the key in the dictionary.
	return ('Land' in cardDatabase[card]['types'])

def isCreature(card):
	# We just want to check whether this card is a creature or not. "card" is a string, so we'll have to use it as the key in the dictionary.
	return ('Creature' in cardDatabase[card]['types'])

def is_int(s):
	# I feel like Python probably had this function somewhere, but whatever.
    try:
        int(s)
        return True
    except ValueError:
        return False

def landsInHand(lineofplay):
	hand = lineofplay.hand
	landsinhand = 0
	for card in hand:
		if isLand(card):
			landsinhand += 1
	return landsinhand

def continuePlaying(lineofplay,drawacard):
	# Okay; this is the core of the program. To "continue playing" a line of play,
	# you need to first draw a card, then look at all the lands you could play
	# and all the choices you could make from playing those lands. For each of those
	# possible land plays, you check how castable all the spells are with that play, 
	# continuePlaying() from there. This creates a recursive tree of lines of play
	# which is only stopped by the maxturns number at the top of the program.
	# I highly recommend low values of maxturns.
	global lineOfPlayCounter
	lineOfPlayCounter += 1

	# Start by drawing a card, if we are supposed to.
	if drawacard: lineofplay.draw_card()

	# Make a list of lands in the hand.
	landstotry = [card for card in lineofplay.hand if isLand(card)]

	# Optimization: If all the cards we are checking on have already been cast OR if there are no lands to play, then we don't actually have to even play another land.
	# Notice that here, if lineofplay.turn() is 2, then we are actually about to work on turn 3. So we want to check caststhistrial[2+1-1].
	if 0 in caststhistrial[lineofplay.turn()+1-1].values() and landstotry != []:

		for card in set(landstotry):
			# If it is a fetchland, we'll want to make two lines of play for the two fetch options. TODO: Pay 1 life TODO: Evolving Wilds/Terramorphic Expanse
			if 'FetchU' in manaDatabase[card] or 'FetchW' in manaDatabase[card] or 'FetchB' in manaDatabase[card] or 'FetchG' in manaDatabase[card] or 'FetchR' in manaDatabase[card]:
				for fetchOption in manaDatabase[card]:
					if fetchOption == 'FetchU':
						fetch = 'Island'
					elif fetchOption == 'FetchW':
						fetch = 'Plains'
					elif fetchOption == 'FetchB':
						fetch = 'Swamp'
					elif fetchOption == 'FetchG':
						fetch = 'Forest'
					elif fetchOption == 'FetchR':
						fetch = 'Mountain'
					else:
						continue
					newlineofplay = deepcopy(lineofplay)
					# Remove our card from the hand and away entirely (we don't have a graveyard).
					newlineofplay.hand.remove(card)
					if fetch in newlineofplay.deck:
						# TODO: We don't need to get the last Mountain if we are fetching a mountain. There might be lots of different cards with subtype Mountain to go for!
						# We maybe should grab the last instance of the given land to avoid messing up the next cards in the deck too much. But python doesn't have rindex, and this isn't worth it.
						i = newlineofplay.deck.index(fetch)
						# Pop the appropriate card from the deck and into play.
						newlineofplay.plays.append([newlineofplay.deck.pop(i)])	
						# Shuffle the deck. Wait! No. If we shuffle the deck, we create a prescience problem where playing a fetch doubles your chances of a good topdeck. Without shuffling, we do the scry/fetch interaction wrong, but that is a much smaller error.
						# newlineofplay.deck = random.sample(newlineofplay.deck, len(newlineofplay.deck))

						# Check if anything is castable and cast it -- this increments caststhisturn and makes new lines of play for spells we know how to handle, then continues playing.
						castSpells(newlineofplay)	
			else:
				# Playing a non-fetchland is much easier.
				newlineofplay = deepcopy(lineofplay)
				# Pop that card out of the hand and into the plays, then. Where is it?
				i = newlineofplay.hand.index(card)
				newlineofplay.plays.append([newlineofplay.hand.pop(i)])
				# Check if anything is castable and cast it -- this increments caststhisturn and makes new lines of play for spells we know how to handle.
				castSpells(newlineofplay)

				# If we just played a scryland, then we need to scry to the bottom and cast spells. We only care about this if there are turns left.
				# Here, a land for turn has already been played, so if turn() is 4 and maxturns is 4, we actually don't want to play another turn.
				if newlineofplay.turn() < maxturns:
					if 'scry' in manaDatabase[card]:
						# If the land was a scryland, then we also need a line of play where we bottomed the top card.
						newlineofplay2 = deepcopy(newlineofplay)
						# We don't need to do another castable check here; nothing is new.
						# However, we should definitely bottom the top card before continuing.
						newlineofplay2.deck = newlineofplay.deck[1:] + newlineofplay.deck[:1]
						castSpells(newlineofplay2)

	else:
		# All the spells were already cast, so just keep going on to later turns by not playing a land here.

		if debug['CastsThisTrial']: print('     Casts this trial:',caststhistrial)
		if debug['CastsThisTrial'] or debug['LinesOfPlay']: print('       Because of all spells cast or no lands to drop, we arent playing a land this turn.')
		# Also remember to continue this line of play (where you didn't play a land this turn).
		lineofplay.plays.append([])
		# Check if anything is castable and cast it -- this increments caststhisturn and makes new lines of play for spells we know how to handle, then continues playing.
		castSpells(lineofplay)

def castSpells(lineofplay):
	# This function is called when we have a line of play where the current turn has its land played, but the "Casts" have not been updated.

	if debug['LinesOfPlay']: print('   ',lineofplay)
	if debug['CastsThisTrial']: print('  Casts this trial:',caststhistrial)

	spellsToCast = checkCastable(lineofplay)
	weCouldNotCastAnything = True

	# We don't actually want to cast very many spells. For now, the only ones we care about are mana producers.
	# TODO: Courser, Card Draw Spells
	for spell in spellsToCast:
		if spell in manaDatabase:
			# This one is a mana producer, so make a new line of play where we cast this.
			weCouldNotCastAnything = False
			newlineofplay = deepcopy(lineofplay)
			i = newlineofplay.hand.index(spell)
			newlineofplay.plays[newlineofplay.turn()-1].append(newlineofplay.hand.pop(i))
			# Keep going, if we should.
			# Here, a land for turn has already been played, so if turn() is 4 and maxturns is 4, we actually don't want to play another turn.
			if newlineofplay.turn() < maxturns:
				continuePlaying(newlineofplay,True)
	if weCouldNotCastAnything:
		# Keep going without casting anything ONLY if it was impossible to cast something. This implementation means we always cast a mana guy if we can.
		# Here, a land for turn has already been played, so if turn() is 4 and maxturns is 4, we actually don't want to play another turn.
		if lineofplay.turn() < maxturns:
			continuePlaying(lineofplay,True)

def checkCastable(lineofplay):
	# We will return the spells that we could have cast, in case castSpells needs to make more lines of play out of them.
	spellsToCast = []

	if debug['CastSpell']: print('     checkCastable on:',lineofplay)
	turn = lineofplay.turn()

	# This returns a sequence of ManaPool objects, the various mana pools we could make with this line of play.
	manaAvailable = lineofplay.manaAvailable()
	if debug['CastSpell']: print('       Mana options available:',manaAvailable)

	# The only spells we are counting are opening hand spells. Those are stored in the global spellsthistrial. But since we are using some spells for mana, we need to try casting everything.
	for card in set(lineofplay.hand).union(spellsthistrial):
		if not isLand(card):
			manaCost = ManaPool(cardDatabase[card]['manaCost'])
			if manaCost in manaAvailable:
				if debug['CastSpell']: print('       Casting',card,'... found',manaCost,' in ', manaAvailable)
				# If the mana is doable, let's make sure we don't have any other requirements, like Chained to the Rocks:
				if card == 'Chained to the Rocks':
					if debug['CastSpell']: print('       mana is okay for '+card)
					haveMountain = 0
					for play in lineofplay.plays:
						for card2 in play:  # Technically an Elvish Mystic might be in here, but it's okay; I guess if we cast a Mountain somehow you could Chain to it.
							if 'subtypes' in cardDatabase[card2]:
								if 'Mountain' in cardDatabase[card2]['subtypes']:
									if debug['CastSpell']: print('       successfully cast turn',turn,card)
									# Okay, it's cool that the spell was castable, but if it isn't in our hand anymore, we don't want to return it.
									if card in lineofplay.hand: spellsToCast.append(card)
									# Again: only count spells that were in our opening hand.
									if card in spellsthistrial: caststhistrial[turn-1][card] = 1
				else:
					# We aren't incrementing this; it is a flag 0 or 1.
					if debug['CastSpell']: print('       successfully cast turn',turn,card)
					# Okay, it's cool that the spell was castable, but if it isn't in our hand anymore, we don't want to return it.
					if card in lineofplay.hand: spellsToCast.append(card)
					# Again: only count spells that were in our opening hand.
					if card in spellsthistrial: caststhistrial[turn-1][card] = 1
	return spellsToCast

def parseDecklist(deckfile):
	global decklist
	global deck

	decklist = {}

	if debug['parseDecklist']: print('Beginning Decklist Parser.')

	inputfile = open(deckfile)
	for line in inputfile:
		if debug['parseDecklist']: print('Parsing line:',line.strip())
		# Don't include sideboard cards :)
		if 'Sideboard' in line or 'sideboard' in line:
			break

		# Split one time, based on delimiters of space, the letter x, and tab -- that way we can parse '2x 			Flooded Strand' as ['2','Flooded Strand']
		words = re.split(r'[ x\t]+',line,1)
		# Okay, now the lines we want to parse look like ['2','Flooded Strand']
		if len(words) == 2:
			if is_int(words[0]):
				if debug['parseDecklist']: print('Parsed as',int(words[0]),'of card',words[1].strip())
				decklist[words[1].strip()] = int(words[0])
			else:
				if debug['parseDecklist']:print('   skipped.')				
		else:
			if debug['parseDecklist']:print('   skipped.')
	inputfile.close()
	for card in decklist:
		if card not in cardDatabase:
			# TODO: Make capitalization friendly so people don't get frustrated by the 'Hero Of Iroas'
			print('Decklist error: card not found. Check capitalization?',card)
			exit('Decklist error; sorry!! Fix the decklist and run program again.')

	if sum(decklist.values()) not in [40,60]:
		if debug['Minimal'] or debug['parseDecklist']: print('Warning: decklist not 40 or 60 cards.')

	if debug['parseDecklist']: print('Decklist Parsing Complete. Decklist Below:')
	if debug['parseDecklist']: print(decklist)

	# A deck is a list of cards, as opposed to a decklist which is a dictionary, so turn the dictionary into a list with multiplicity.
	deck = []
	for card in decklist:
		deck.extend([card]*decklist[card])

def drawHand(handsize):
	# This function draws a hand of handsize cards.
	# Shuffle the deck. TODO: Is random.sample good enough? I'm not sure actually.
	currentdeck = random.sample(deck, len(deck))
	# Create a new line of play based on this deck.
	lineofplay = LineOfPlay([],[],currentdeck)

	# Draw an initial hand.
	for i in range(handsize):
		lineofplay.draw_card()

	return lineofplay

def displayResults():
	# Okay. draws is a dictionary with keys: spell names and with values: the number of times we drew this spell.
	# casts[0] is a dictionary; its keys are card names and its values are the number of times we cast this card in Turn 1.
	# casts[1] is a dictionary; its keys are card names and its values are the number of times we cast this card by Turn 2.
	# etc. up to maxturns.
	# handsizes is a dictionary; its keys are the numbers 4 through 7, and the values are the number of times we kept hands of that size.
	# onthedraw is a boolean that tells us play or draw.
	if onthedraw: 
		drawplay = 'On the Draw.'
	else:
		drawplay = 'On the Play.'

	print('')
	print('')
	print('Finished running',deckfile,'-',drawplay,'Ran',trials,'trials.')

	print('')
	for handsize in handsizes:
		print('Kept',handsizes[handsize],'hands with',handsize,'cards,','{:>6.1%}'.format(handsizes[handsize]/trials))
	print('')

	percents = {}
	# To justify the text, we need to know the max card length.
	maxcardlength = max([len(card) for card in draws])

	for card in draws:
		spacestojustify = maxcardlength - len(card)
		percents[card] = ' '*spacestojustify + card +':  Draws: '+'{:>6}'.format(str(draws[card]))+'  '
		for i in range(maxturns):
			if draws[card] > 0:
				percent = casts[i][card]/draws[card]
				percent = '{:>6.1%}'.format(percent)
				percents[card] += ('  Cast on '+str(i+1)+': '+percent+'')

				# This basic margin of error calculation is only valid if we have more than 30 trials and at least 5 successes and at least 5 failures.
				if casts[i][card] >= 5 and (draws[card]-casts[i][card]) >= 5 and draws[card] >= 30:
					error = 1.96*math.sqrt(casts[i][card]*(draws[card]-casts[i][card])/math.pow(draws[card],3))
					error = '{:<6.1%}'.format(error)
					percents[card]+= '+-'+error
				else:
					percents[card]+= '        '
					
	for card in draws:
		print(percents[card])


########################################################
#
# Starting here is what the program actually does.
#
########################################################


# A decklist is a dictionary where the key is the card name and the value is the number of copies. This should make importing easy.
# The decklist parser takes a filename and tries to read it.
parseDecklist(deckfile)

# We need to go through all the manaproducers in our deck and figure out what is going on with them.
parseMana(decklist)

# We are going to be counting how many times we draw or cast each nonland card in the list. Starting off, we will want a 0 for each nonland card in the deck.
initialCount = {}
for card in decklist:
	if not isLand(card):
		initialCount[card] = 0

# Draws is a dictionary; its keys are card names and its values are the number of times we saw this card in opening hands.
draws = initialCount.copy()

# casts[0] is a dictionary; its keys are card names and its values are the number of times we cast this card in Turn 1.
# casts[1] is a dictionary; its keys are card names and its values are the number of times we cast this card by Turn 2.
# etc. up to maxturns.
casts = []
for i in range(maxturns):
	casts.append(initialCount.copy())

# handsizes is a dictionary; its keys are hand sizes and its values are the number of times we started with that hand size.
handsizes = {}
for i in range(4,8):
	handsizes[i] = 0

# Let's go!
for trial in range(trials):
	lineOfPlayCounter = 0
	trialStartTime = datetime.now()

	if debug['DrawCard']: print('')
	if debug['Minimal']: 
		if trial % 100 == 0: print('Trial',trial,'starting.')

	# Start by drawing a hand of 7.
	lineofplay = drawHand(7)

	# If we are considering mulligans, then we have to look at how many lands we have. This is Karsten's basic mulligan strategy for simulators.
	if mulligans:
		if landsInHand(lineofplay) in [0,1,6,7]:
			if debug['mulligans']: print('  Mulligan hand of 7 cards,',landsInHand(lineofplay),'lands:',lineofplay.hand)
			lineofplay = drawHand(6)
			if landsInHand(lineofplay) in [0,1,5,6]:
				if debug['mulligans']: print('  Mulligan hand of 6 cards,',landsInHand(lineofplay),'lands:',lineofplay.hand)
				lineofplay = drawHand(5)
				if landsInHand(lineofplay) in [0,5]:
					if debug['mulligans']: print('  Mulligan hand of 5 cards,',landsInHand(lineofplay),'lands:',lineofplay.hand)
					lineofplay = drawHand(4)

	# When we decide to keep a hand, keep track of how large the hand was that we kept.
	handsize = len(lineofplay.hand)
	handsizes[handsize] += 1
	if debug['Trial']: print('Trial #',trial,'kept opening hand of',handsize,'cards:',lineofplay.hand)

	# In this trial, we only care about how many times we cast the spells in the opening hand.
	# spellsthistrial is the list of spells we care about.
	# caststhistrial[0] is a dictionary with keys: spells in this opening hand, values:0 or 1, whether we cast it or not on Turn 1.
	# caststhistrial[1] is a dictionary with keys: spells in this opening hand, values:0 or 1, whether we cast it or not on Turn 2.
	# etc, up to maxturns.
	spellsthistrial = []
	caststhistrial = []
	for i in range(maxturns):
		caststhistrial.append({})
	# If we have two copies of a spell in the opening hand, we don't need to check it twice as often, so use set.
	for card in set(lineofplay.hand):
		if not isLand(card):
			# Optimization: If our deck contains no ramp, we can ignore spells that are too expensive to ever cast.
			# If we are never going to play enough turns to cast this spell, just act like you never even drew it, to save time.
			rampIsPossible = 0
			for manaproducer in manaDatabase:
				if not isLand(manaproducer): rampIsPossible = 1
			if rampIsPossible or cardDatabase[card]['cmc'] <= maxturns:
				draws[card] += 1
				spellsthistrial.append(card)
				for i in range(maxturns):
					caststhistrial[i][card] = 0

	# Continue playing. During "continue playing," we check whether cards are playable and set caststhistrial to 1 when possible.
	# If we are on the draw, we tell continuePlaying to start the turn by drawing a card, otherwise not.
	continuePlaying(lineofplay,onthedraw)

	# After we've played through lots of lines of play, we have some 1s and 0s in caststhistrial.
	# We add that to casts.
	for i in range(maxturns):
		for card in caststhistrial[i]:
			casts[i][card] += caststhistrial[i][card]

	if debug['Trial']: print('   Trial #',trial,'complete after scanning',lineOfPlayCounter,'lines of play,',(datetime.now()-trialStartTime).total_seconds(),'s')

# For now, we just display the results at the end. TODO: Store them, so that if we run 5000 trials and then another 5000 trials, we can combine the data.
displayResults()



