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

# We will work with files and directories, so we need to use os.path() and shutil.copyfile()
import os
import shutil

# When we want to exit, we want to just use exit()
from sys import exit

# We will need to import datetime to time our trials.
from datetime import datetime

# Our topological sorting algorithm uses this.
from functools import reduce

# Get the most updated AllCards.json from mtgjson.com. Then we use it here.
import json
json_data=open('AllCards.json')
cardDatabase = json.load(json_data)
json_data.close()

# How many turns out are we going? How many trials? Are we on the play [False] or on the draw [True]?
maxturns = 5
trials = 250000
onthedraw = False

# Mulligan 7-card hands with 0,1,6,7 lands,  ... 6-card hands with 0,1,5,6 lands, ... 5-card hands with 0,5 lands.
# With 24 lands, we should end up with 7 lands: 84.4%      6 lands: 11.7%      5 lands: 3.4%      4 lands: 0.5%
mulligans = True

debug = {}
debug['Minimal'] = True
debug['Trial'] = False
debug['DrawCard'] = False
debug['CastSpell'] = False
debug['parseMana'] = False
debug['LinesOfPlay'] = False
debug['CastsThisTrial'] = False
debug['parseDecklist'] = False
debug['checkManaAvailability'] = False
debug['mulligans'] = False
debug['storeResults'] = False

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

	def manaSourcesAvailable(self):
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
				# The only way a land is not available is if the land has text that contains the word 'tapped' but it is not a shockland.
				if isLand(cardplayedthisturn) and 'text' in cardDatabase[cardplayedthisturn]:
					if 'tapped' in cardDatabase[cardplayedthisturn]['text'] and 'you may pay 2 life' not in cardDatabase[cardplayedthisturn]['text']:
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

		if debug['checkManaAvailability']: print('        Available mana sources in this line of play:',availablecards)
		return availablecards

def toposort(data):
	"""Dependencies are expressed as a dictionary whose keys are items
	and whose values are a set of dependent items. Output is a list of
	sets in topological order. The first set consists of items with no
	dependences, each subsequent set consists of items that depend upon
	items in the preceeding sets.

	>>> print '\\n'.join(repr(sorted(x)) for x in toposort({
	...     2: set([11]),
	...     9: set([11,8]),
	...     10: set([11,3]),
	...     11: set([7,5]),
	...     8: set([7,3]),
	...     }) )
	[3, 5, 7]
	[8, 11]
	[2, 9, 10]

	"""
	# This recipe was taken from http://code.activestate.com/recipes/578272-topological-sort/ on December 31, 2014.

	# Ignore self dependencies.
	for k, v in data.items():
	    v.discard(k)
	# Find all items that don't depend on anything.
	extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
	# Add empty dependences where needed
	data.update({item:set() for item in extra_items_in_deps})
	while True:
		# ordered is the set of items that do not have any dependencies.
	    ordered = set(item for item, dep in data.items() if not dep)
	    # if we don't have any, then we are done.
	    if not ordered:
	        break
	    # okay, return this set of items with no dependencies.
	    yield ordered
	    # then remove the set of items with no dependencies from the dictionary entirely.
	    data = {item: (dep - ordered)
	            for item, dep in data.items()
	                if item not in ordered}
	# if it loops around and everything gets destroyed, then we have a cyclic dependency.
	assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.items())

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
						elif currentsymbol == '{1':
							# Every land is currently assumed to tap for {1}, so skip it
							pass
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
					if 'basic land card' in cardDatabase[card]['text']:
						manaDatabase[card].append('FetchBasic')
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


	# Okay, now comes the mathy part. Suppose you are trying to cast Savage Knuckleblade (cost: RUG) and you have the following lands:
	# Sylvan Caryatid, Mana Confluence, Forest
	# The way a human handles this issue is they say "aha -- the Forest is only useful for Green, so I better tap the Forest for green and the others for something else."
	# The key optimization idea here is that if we need a green mana, we try using Forest for it, and we can't cast the spell, then there is no use trying to use Mana Confluence for the green.
	# We will use what is called a "topological sort" of the lands to stratify things this way. For example, in a deck with lots of weird lands, you might have:
	# Forest, Yavimaya Coast, Frontier Bivouac, Sandsteppe Citadel, Sylvan Caryatid.
	# With respect to green, these can be topologically sorted as follows: [Forest], [Yavimaya Coast, Sandsteppe Citadel], [Frontier Bivouac], [Sylvan Caryatid].
	# This means that if you have a land from one of the lists, you tried tapping it for green and everything still failed, then there is no use trying anything from a later list.

	# At the end of this, we will build a partial ordering of all the mana producers in the deck. This will allow us to choose mana sources intelligently in the future.

	def secondManaSourceIsBetter(card1,card2):
		coloredManaSymbols = ['{W}','{U}','{B}','{R}','{G}']
		# the second mana source is better if its set of colored mana symbols is strictly larger.
		symbolsInCard1 = [symbol for symbol in coloredManaSymbols if (ManaPool(symbol) in manaDatabase[card1])]
		symbolsInCard2 = [symbol for symbol in coloredManaSymbols if (ManaPool(symbol) in manaDatabase[card2])]
		# The second list of symbols is strictly larger if everything in #2 is in #1, and something in #2 is not in #1.
		return (all([symbol in symbolsInCard2 for symbol in symbolsInCard1]) and any([symbol not in symbolsInCard1 for symbol in symbolsInCard2]))

	global manaSourcesBetterThan
	global manaSourcesInOrder
	manaSourcesBetterThan = {}
	for card in manaDatabase:
		# Just make a list of all the othercards that are better than card.
		manaSourcesBetterThan[card] = set([othercard for othercard in manaDatabase if secondManaSourceIsBetter(card,othercard)])

	if debug['parseMana']: print('End of Mana Parser. Results below:')
	if debug['parseMana']: print('     Mana Database:',manaDatabase)
	if debug['parseMana']: print('Mana Partial Order:',manaSourcesBetterThan)

	# Then we can create a topological sort of the mana sources. This is an order to try the lands in.
	toposorted = toposort(manaSourcesBetterThan)
	# toposorted is a list of sets. We want to concatenate them into a list, and we don't care about the order inside the sets.
	manaSourcesInOrder = []
	for cohortofcards in toposorted:
		for card in cohortofcards:
			manaSourcesInOrder.append(card)
	manaSourcesInOrder.reverse()

	if debug['parseMana']: print('Order to try Lands:',manaSourcesInOrder)
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

def landCountInHand(lineofplay):
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
			# If it is a fetchland, we'll want to make two lines of play for the two fetch options. TODO: Pay 1 life 
			if 'FetchU' in manaDatabase[card] or 'FetchW' in manaDatabase[card] or 'FetchB' in manaDatabase[card] or 'FetchG' in manaDatabase[card] or 'FetchR' in manaDatabase[card] or 'FetchBasic' in manaDatabase[card]:
				# Figure out what our fetch options are.
				fetchoptions = []
				for fetchOption in manaDatabase[card]:
					if fetchOption == 'FetchU':
						fetchoptions.append(('subtypes','Island'))
					elif fetchOption == 'FetchW':
						fetchoptions.append(('subtypes','Plains'))
					elif fetchOption == 'FetchB':
						fetchoptions.append(('subtypes','Swamp'))
					elif fetchOption == 'FetchG':
						fetchoptions.append(('subtypes','Forest'))
					elif fetchOption == 'FetchR':
						fetchoptions.append(('subtypes','Mountain'))
					elif fetchOption == 'FetchBasic':
						fetchoptions.append(('supertypes','Basic'))
					else:
						continue

				# Here we have something like [('subtypes','Forest'),('subtypes','Mountain')]. If our deck has four distinct cards with subtype forest or mountain, go get them all.
				# Make a dictionary of all the valid targets. The key will be the card title, and the value will be the index of the LAST occurrence of the card in the deck.
				# Grabbing the last occurrence of the card is a good plan because otherwise fetching the top card of your deck in a "try all lines of play" situation makes every fetchland be like a courser fetchland.
				fetchtargets = {}
				for fetch in fetchoptions:
					for i,target in enumerate(lineofplay.deck):
						if fetch[0] in cardDatabase[target]:
							if fetch[1] in cardDatabase[target][fetch[0]]:
								fetchtargets[target] = i

				if debug['LinesOfPlay']: print('       Fetchland',card,'processed; possible fetch targets are',fetchtargets)

				for target in fetchtargets:
					newlineofplay = deepcopy(lineofplay)
					# Remove our card from the hand and away entirely (we don't have a graveyard).
					newlineofplay.hand.remove(card)
					# Pop the appropriate card from the deck and into play.
					i = fetchtargets[target]
					newlineofplay.plays.append([newlineofplay.deck.pop(i)])	
					# Shuffle the deck. Wait! No. If we shuffle the deck, we create a prescience problem where playing a fetch doubles your chances of a good topdeck. Without shuffling, we do the scry/fetch interaction wrong, but that is a much smaller error.
					# newlineofplay.deck = random.sample(newlineofplay.deck, len(newlineofplay.deck))

					# Check if anything is castable and cast it -- this increments caststhisturn and makes new lines of play for spells we know how to handle, then continues playing.
					# One thing: we need to tell castSpells that it should not use the Evolving Wilds lands this turn.
					if 'FetchBasic' in manaDatabase[card]:
						castSpells(newlineofplay, False)
					else:
						castSpells(newlineofplay, True)	
			else:
				# Playing a non-fetchland is much easier.
				newlineofplay = deepcopy(lineofplay)
				# Pop that card out of the hand and into the plays, then. Where is it?
				i = newlineofplay.hand.index(card)
				newlineofplay.plays.append([newlineofplay.hand.pop(i)])
				# Check if anything is castable and cast it -- this increments caststhisturn and makes new lines of play for spells we know how to handle.
				castSpells(newlineofplay, True)

				# If we just played a scryland, then we need to scry to the bottom and cast spells. We only care about this if there are turns left.
				# Here, a land for turn has already been played, so if turn() is 4 and maxturns is 4, we actually don't want to play another turn.
				if newlineofplay.turn() < maxturns:
					if 'scry' in manaDatabase[card]:
						# If the land was a scryland, then we also need a line of play where we bottomed the top card.
						newlineofplay2 = deepcopy(newlineofplay)
						# We don't need to do another castable check here; nothing is new.
						# However, we should definitely bottom the top card before continuing.
						newlineofplay2.deck = newlineofplay.deck[1:] + newlineofplay.deck[:1]
						castSpells(newlineofplay2, True)

	else:
		# All the spells were already cast, so just keep going on to later turns by not playing a land here.

		if debug['CastsThisTrial']: print('     Casts this trial:',caststhistrial)
		if debug['CastsThisTrial'] or debug['LinesOfPlay']: print('       Because of all spells cast or no lands to drop, we arent playing a land this turn.')
		# Also remember to continue this line of play (where you didn't play a land this turn).
		lineofplay.plays.append([])
		# Check if anything is castable and cast it -- this increments caststhisturn and makes new lines of play for spells we know how to handle, then continues playing.
		castSpells(lineofplay, True)

def castSpells(lineofplay, useThisTurnsLands):
	# This function is called when we have a line of play where the current turn has its land played, but the "Casts" have not been updated.

	if debug['LinesOfPlay']: print('   ',lineofplay)
	if debug['CastsThisTrial']: print('  Casts this trial:',caststhistrial)

	spellsToCast = checkCastable(lineofplay, useThisTurnsLands)
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

def checkManaAvailability(symbolsToAcquire, manaSourcesAvailable):
	if debug['checkManaAvailability']: print('         Trying to acquire',symbolsToAcquire,'with',manaSourcesAvailable)
	
	# TODO: Some things like Nykthos or Sol Ring might make more than one mana.
	cmc = 0
	for symbol in symbolsToAcquire:
		if is_int(symbol): 
			cmc += int(symbol)
		else:
			cmc += 1
	if cmc > len(manaSourcesAvailable):
		if debug['checkManaAvailability']: print('         Thats not possible with this few sources.')
		return False


	# We return true if there is only one symbol to acquire and we can do it.
	if len(symbolsToAcquire) == 1:
		lastsymbol = symbolsToAcquire[0]

		# TODO: Some things like Nykthos or Sol Ring might make more than one mana.
		if is_int(lastsymbol):
			if int(lastsymbol) <= len(manaSourcesAvailable):
				if debug['checkManaAvailability']: print('         Success! The last symbol was',lastsymbol,'and we had enough left.')
				return True
			else:
				if debug['checkManaAvailability']: print('         Failure! The last symbol was',lastsymbol,'and we didnt have enough left.')
				return False
		elif any([(ManaPool('{'+lastsymbol+'}') in manaDatabase[card]) for card in manaSourcesAvailable]):
			if debug['checkManaAvailability']: print('         Success! The last symbol was',lastsymbol,'and we found it.')
			return True
		else:
			if debug['checkManaAvailability']: print('         Failure! The last symbol was',lastsymbol,'and we couldnt find it.')
			return False
	else:
		nextSymbol = symbolsToAcquire[0]

		manaSourcesTried = []
		# We need to try a variety of mana sources to acquire this mana. We'll try in the order of the list manaSourcesInOrder.
		for manaSource in manaSourcesInOrder:
			if manaSource in manaSourcesAvailable:
				# Okay! We will try this -- but here is the thing. We don't try it if it is better than something we already tried.
				# This is the key optimization. If we tried using "Forest" for {G} and failed, then it is pointless to try using "Temple of Abandon" for the same {G}.
				if not any([manaSource in manaSourcesBetterThan[manaSourceTried] for manaSourceTried in manaSourcesTried]):
					if ManaPool('{'+nextSymbol+'}') in manaDatabase[manaSource]:
						# It's possible to use this card to satisfy this symbol, so we'll try it.
						manaSourcesTried.append(manaSource)
						newsymbolsToAcquire = list(symbolsToAcquire)
						symbolRemoved = newsymbolsToAcquire.pop(0)
						newmanaSourcesAvailable = list(manaSourcesAvailable)
						newmanaSourcesAvailable.remove(manaSource)
						if debug['checkManaAvailability']: print('            With this try we have tried',manaSourcesTried,'for',nextSymbol,'- removing source',manaSource,'for',nextSymbol,': remaining sources',newmanaSourcesAvailable)
						# The only way this ends is if we find a path through this tree that satisfies the final symbol. If so, we win!
						if checkManaAvailability(newsymbolsToAcquire,newmanaSourcesAvailable): return True
				else:
					if debug['checkManaAvailability']: print('            So far we tried',manaSourcesTried,'for',nextSymbol,'- no point trying',manaSource,'for',nextSymbol)
		# If we get here, then I guess we didn't make it.
		if debug['checkManaAvailability']: print('         Failure! We couldnt get',symbolsToAcquire,'from',manaSourcesAvailable)		
		return False

def checkCastable(lineofplay, useThisTurnsLands):
	# We will return the spells that we could have cast, in case castSpells needs to make more lines of play out of them.
	spellsToCast = []

	if debug['CastSpell']: print('     checkCastable on:',lineofplay)
	turn = lineofplay.turn()

	# This tells us which cards are available to tap for mana.
	manaSourcesAvailable = lineofplay.manaSourcesAvailable()
	if not useThisTurnsLands:
		for thisturnsland in [land for land in lineofplay.plays[turn-1] if isLand(land)]:
			manaSourcesAvailable.remove(thisturnsland)

	# The only spells we are counting are opening hand spells. Those are stored in the global spellsthistrial. But since we are using some spells for mana, we need to try casting everything in hand or in opening hand.
	for card in set([spell for spell in lineofplay.hand if not isLand(spell)]).union(spellsthistrial):
		if card not in caststhistrial[turn-1] and card not in manaDatabase:
			# We don't need to care about non-manaproducing spells if they weren't in the opening hand.
			# TODO: Courser or card draw spells do matter.
			continue 
		elif card in caststhistrial[turn-1] and card not in manaDatabase:
			if caststhistrial[turn-1][card] == 1:
				# We don't need to care about non-manaproducing spells if we already found a way to cast them earlier.
				# TODO: Courser or card draw spells do matter.
				continue

		# Go to the card database to get the mana cost.
		manaCost = cardDatabase[card]['manaCost']
		# For now, X is always 0.
		newManaCost = manaCost.replace('{X}','')
		symbolsToAcquire = re.split(r'[{} ]+',newManaCost[1:-1])
		# Acquire the colored symbols first, before the colorless.
		symbolsToAcquire.reverse()

		# If we accidentally killed the mana cost by removing X, make it zero.
		if symbolsToAcquire == []:
			symbolsToAcquire = ['{0}']

		# This function recursively tries to acquire all these symbols given these mana sources.
		if debug['checkManaAvailability']: print('         Starting the chain, trying to get',symbolsToAcquire,'from',manaSourcesAvailable)
		isCastable = checkManaAvailability(symbolsToAcquire, manaSourcesAvailable)

		if isCastable:
			if debug['CastSpell']: print('       Successfully found a way to cast',card,'... we found',manaCost,'in', manaSourcesAvailable,'on turn',turn)
			# If the mana is doable, let's make sure we don't have any other requirements, like Chained to the Rocks:
			if card == 'Chained to the Rocks':
				if debug['CastSpell']: print('       mana is okay for '+card)
				haveMountain = 0
				for play in lineofplay.plays:
					for card2 in play:  # Technically an Elvish Mystic might be in here, but it's okay; I guess if we cast a Mountain somehow you could Chain to it.
						if 'subtypes' in cardDatabase[card2]:
							if 'Mountain' in cardDatabase[card2]['subtypes']:
								if debug['CastSpell']: print('       We successfully cast turn',turn,card,'!')
								# Okay, it's cool that the spell was castable, but if it isn't in our hand anymore, we don't want to return it.
								if card in lineofplay.hand: spellsToCast.append(card)
								# Again: only count spells that were in our opening hand.
								if card in spellsthistrial: 
									caststhistrial[turn-1][card] = 1
									for i in range(turn,maxturns):
										caststhistrial[i-1][card] = 1
			else:
				# We aren't incrementing this; it is a flag 0 or 1.
				if debug['CastSpell']: print('       We successfully cast turn',turn,card,'!')
				# Okay, it's cool that the spell was castable, but if it isn't in our hand anymore, we don't want to return it.
				if card in lineofplay.hand: spellsToCast.append(card)
				# Again: only count spells that were in our opening hand. 
				if card in spellsthistrial: 
					caststhistrial[turn-1][card] = 1
					for i in range(turn,maxturns):
						caststhistrial[i-1][card] = 1

	return spellsToCast

def parseDecklist(deckfile):
	# This will return a tuple of deck, decklist

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

	return deck, decklist

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

def playHand(lineofplay):
	# In this trial, we only care about how many times we cast the spells in the opening hand.
	# spellsthistrial is the list of spells we care about.
	# caststhistrial[0] is a dictionary with keys: spells in this opening hand, values:0 or 1, whether we cast it or not on Turn 1.
	# caststhistrial[1] is a dictionary with keys: spells in this opening hand, values:0 or 1, whether we cast it or not on Turn 2.
	# etc, up to maxturns.
	global spellsthistrial
	global caststhistrial
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

def storeResults():
	# Okay. draws is a dictionary with keys: spell names and with values: the number of times we drew this spell.
	# casts[0] is a dictionary; its keys are card names and its values are the number of times we cast this card in Turn 1.
	# casts[1] is a dictionary; its keys are card names and its values are the number of times we cast this card by Turn 2.
	# etc. up to maxturns.
	# handsizes is a dictionary; its keys are the numbers 4 through 7, and the values are the number of times we kept hands of that size.
	# onthedraw is a boolean that tells us play or draw.

	# The results would be stored in deckfile minus extension plus '-results.txt'
	resultsfile = 'results/'+deckname+'-results.txt'
	cacheddeckfile = 'results/'+deckname+'-cached.txt'

	if debug['storeResults']: print('Storing results in files',resultsfile,'and',cacheddeckfile)

	# However, in the stored file, we need a different number of draws for each turn, in case you run data out to 5 turns once, then out to 7 turns later.
	# So, draws is a list of dictionaries like casts, described above.
	olddraws = []
	oldcasts = []

	global totaldraws
	global totalcasts

	# First we need to check if we have any stored results for this deck.
	if os.path.isfile(resultsfile):
		if debug['storeResults']: print('The results file already exists.')

		# If so, we need to make sure it's the same deck that we have stored results for.
		cacheddeck,cacheddecklist = parseDecklist(cacheddeckfile)
		if cacheddecklist != decklist:
			if debug['storeResults']: print('It looks like the stored results are for a different deck that used the same filename.')
			# If the deck changed, rename the old results so we don't lose them.
			# We want to rename the old results from something-results.txt to something-backup-1-results.txt
			backupnumber = 0
			while True:
				backupnumber += 1
				backupresultsfile = 'results/'+deckfile[:-4]+'-backup-'+backupnumber+'-results.txt'
				backupcacheddeckfile = 'results/'+deckfile[:-4]+'-backup-'+backupnumber+'-cached.txt'
				if debug['storeResults']: print('Storing old results in files',backupresultsfile,'and',backupcacheddeckfile)
				if not os.path.isfile(backupresultsfile):
					os.rename(resultsfile,backupresultsfile)
					os.rename(cacheddeckfile,backupcacheddeckfile)
					break
		# In this case, we can open the old results and store them.
		results = open(resultsfile)
		for result in results:
			# Each line in this file is a card name, then a series of proportions -- tab delimited.
			# For example, Elvish Mystic	4/10 	6/10 	9/10 	10/10

			if debug['storeResults']: print('Trying to parse the results line',result.strip())

			# Start by splitting on tabs.
			resultsequence = result.split('\t')

			# We want a blank dictionary to fill in.
			oldmaxturns = len(resultsequence) - 1
			for i in range(oldmaxturns):
				olddraws.append({})
				oldcasts.append({})

			# Get the card name out of the list first.
			card = resultsequence.pop(0)

			if debug['storeResults']: print('   Figured out it is a result of card "',card,'"')

			# Okay, now populate the right numbers.
			for (turn,fraction) in enumerate(resultsequence):
				numbers = fraction.split('/')

				oldcasts[turn][card] = int(numbers[0].strip())
				olddraws[turn][card] = int(numbers[1].strip())
				if debug['storeResults']: print('   The old data on',card,'on turn',turn+1,'was',oldcasts[turn][card],'out of',olddraws[turn][card])

		results.close()

		# Now that the old numbers are in place, make a new place to hold the new totals.
		totaldraws = []
		totalcasts = []
		for turn in range(max(maxturns, oldmaxturns)):
			totaldraws.append({})
			totalcasts.append({})
			if len(casts) > turn and len(oldcasts) > turn:
				# This is the case where this turn is valid for both old and new.
				
				# We will start by going through all the cards inthe olddraws.
				for card in olddraws[turn]:
					if card in casts[turn]:
						# This is the case where this turn is valid for both old and new and the card was drawn both times.
						if debug['storeResults']: print('   Both old and new data available for',card,'for turn',turn+1,'... adding the numbers.')
						totaldraws[turn][card] = olddraws[turn][card] + draws[card]
						totalcasts[turn][card] = oldcasts[turn][card] + casts[turn][card]

					else:
						# This is the case where this turn is valid for both old and new and the card was drawn in old, but not new.
						if debug['storeResults']: print('   Old data available for',card,'but not new data for turn',turn+1)
						totaldraws[turn][card] = olddraws[turn][card]
						totalcasts[turn][card] = oldcasts[turn][card]
				
				# Now pick up anything in draws that is not in olddraws.
				for card in draws:
					if card not in olddraws[turn]:
						# This is the case where this turn is valid for both old and new and the card was drawn in new, but not old.
						if debug['storeResults']: print('   New data available for',card,'but not old data for turn',turn+1)
						totaldraws[turn][card] = draws[card]
						totalcasts[turn][card] = casts[turn][card]

			elif len(casts) > turn and len(oldcasts) <= turn:
				# This is the case where this turn is valid for new but not old.
				for card in casts[turn]:
					if debug['storeResults']: print('   New data available for',card,'but not old data for turn',turn+1)
					totaldraws[turn][card] = draws[card]
					totalcasts[turn][card] = casts[turn][card]

			elif len(casts) <= turn and len(oldcasts) > turn:
				# This is the case where this turn is valid for old but not new.
				for card in oldcasts[turn]:
					if debug['storeResults']: print('   Old data available for',card,'but not new data for turn',turn+1)
					totaldraws[turn][card] = olddraws[turn][card]
					totalcasts[turn][card] = oldcasts[turn][card]

	else:
		# In this case, we will need to make a blank cached deckfile.
		shutil.copy2(deckfile,cacheddeckfile)

		# Then use our current numbers (in globals draws and casts).
		totaldraws = []
		for i in range(maxturns):
			totaldraws.append(draws)
		totalcasts = casts

	# Output the new data to the file.
	with open(resultsfile,'w') as f:
		for card in totaldraws[0]:
			stringtosave = card
			for turn in range(len(totaldraws)):
				stringtosave += '\t'
				stringtosave += str(totalcasts[turn][card])
				stringtosave += '/'
				stringtosave += str(totaldraws[turn][card])
			stringtosave += '\n'
			f.write(stringtosave)

def displayResults():
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
				percents[card] += ('  Cast by '+str(i+1)+': '+percent+'')

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


# We want to run every deck in the deck folder? Or just one?
runEveryDeck = False

if runEveryDeck:
	deckdirectory = os.listdir( 'decks/' )
else:
	deckdirectory = []
	# If you want to run just one deck, change runEveryDeck to false and type the filename here, without the decks/ prefix.
	deckdirectory.append('benchmark-24-lands.txt')


for deckfilename in deckdirectory:

	# Strip off the extension on the file.
	deckname = deckfilename[:-4]
	deckfile = 'decks/'+deckfilename

	# A decklist is a dictionary where the key is the card name and the value is the number of copies. This should make importing easy.
	# The decklist parser takes a filename and tries to read it.
	deck,decklist = parseDecklist(deckfile)

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
			if trial % 100 == 0: print('Trial',trial,'of deck',deckname,'starting.')

		# Start by drawing a hand of 7.
		lineofplay = drawHand(7)

		# If we are considering mulligans, then we have to look at how many lands we have. This is Karsten's basic mulligan strategy for simulators.
		if mulligans:
			if landCountInHand(lineofplay) in [0,1,6,7]:
				if debug['mulligans']: print('  Mulligan hand of 7 cards,',landCountInHand(lineofplay),'lands:',lineofplay.hand)
				lineofplay = drawHand(6)
				if landCountInHand(lineofplay) in [0,1,5,6]:
					if debug['mulligans']: print('  Mulligan hand of 6 cards,',landCountInHand(lineofplay),'lands:',lineofplay.hand)
					lineofplay = drawHand(5)
					if landCountInHand(lineofplay) in [0,5]:
						if debug['mulligans']: print('  Mulligan hand of 5 cards,',landCountInHand(lineofplay),'lands:',lineofplay.hand)
						lineofplay = drawHand(4)

		# When we decide to keep a hand, keep track of how large the hand was that we kept.
		handsize = len(lineofplay.hand)
		handsizes[handsize] += 1
		if debug['Trial']: print('Trial #',trial,'kept opening hand of',handsize,'cards:',lineofplay.hand,'top few:',lineofplay.deck[:5])

		# Okay, we've set up the line of play, now play it.
		playHand(lineofplay)

		if debug['Trial']: print('   Trial #',trial,'complete after scanning',lineOfPlayCounter,'lines of play,',(datetime.now()-trialStartTime).total_seconds(),'s')

	storeResults()

	displayResults()


