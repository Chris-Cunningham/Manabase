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

# Get the most updated AllCards.json from mtgjson.com. Then we use it here.
import json
json_data=open('AllCards.json')
cardDatabase = json.load(json_data)
json_data.close()

# How many turns out are we going? How many trials? Are we on the play [False] or on the draw [True]?
maxturns = 5
trials = 100
onthedraw = False

# Mulligan 7-card hands with 0,1,6,7 lands,  ... 6-card hands with 0,1,5,6 lands, ... 5-card hands with 0,5 lands.
# With 24 lands, we should end up with 7 lands: 84.4%      6 lands: 11.7%      5 lands: 3.4%      4 lands: 0.5%
mulligans = True

# deckfile = 'decks/scgpc-mardu-midrange-kent-ketter.txt'
deckfile = 'decks/scgpc-abzan-aggro-BBD.txt'
# deckfile = 'decks/scgpc-uw-heroic-tom-ross.txt'
# deckfile = 'decks/scgpc-rg-aggro-logan-mize.txt'
# deckfile = 'decks/scgpc-jeskai-tokens-ross-merriam.txt'
# deckfile = 'decks/scgpc-temur-midrange-jeff-hoogland.txt'
# deckfile = 'decks/scgpc-uw-control-jim-davis.txt'

debug = {}
debug['Minimal'] = False
debug['Trial'] = True
debug['DrawCard'] = False
debug['CastSpell'] = False
debug['parseLands'] = False
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

	def manaAvailable(self):
		# In a certain line of play, we want to know which combination of mana is available. New lands aren't available.
		turn = len(self.plays)

		# Make a list of available lands (so we dont count tapped lands on the turn they come out)
		availablelands = []
		for i in range(turn):
			# lands played before the last turn are always available. First add them all.
			availablelands.extend(self.plays[i])

		# For the one(s) we just played, check whether it is a tapland.
		if turn > 0:
			for landplayedthisturn in self.plays[turn-1]:
				# The only way the land is not available is if the land has text that contains the word 'tapped'
				if 'text' in cardDatabase[landplayedthisturn]:
					if 'tapped' in cardDatabase[landplayedthisturn]['text']:
						availablelands.remove(landplayedthisturn)

		# Now we have a list of lands available to us, but we need to see what combinations of mana we can make.
		# Luckily each land in the deck has already been parsed and has a list of mana (in ManaPool format) available. 
		# For example the dictionary lands has landsDatabase[Island] = [{U}] and landsDatabase[Temple of Malice] = [{R}, {B}]
		# So if your lands available are Island and Temple of Malice, your availablemana should be [{0}, {1}, {R}, {U}, {B}, {2}, {1}{R}, {1}{U}, {1}{B}, {U}{R}, {U}{B}]
		availablemana = [ManaPool('{0}')]
		for land in availablelands:
			if debug['manaAvailable']: print('       Tapping for mana:',land)
			newoptionswiththisland = []
			# If there is an urborg in play, we can tap for black mana.
			for play in self.plays:
				if 'Urborg, Tomb of Yawgmoth' in play:
					for manaoption in availablemana:
						# Each of the options we had before this land needs to get appended with one of these.
						newoptionswiththisland.append(manaoption + ManaPool('{B}'))

			# We can then add on this land's mana symbols. Danger: the mana symbols might include things like 'Scry' or 'FetchU' which we should skip.
			for manasymbol in landsDatabase[land]:
				if manasymbol != 'scry':
					for manaoption in availablemana:
						# Each of the options we had before this land needs to get appended with one of these.
						newoptionswiththisland.append(manaoption + manasymbol)
			# We can also just treat the new one as a colorless.
			manasymbol = ManaPool('{1}')
			for manaoption in availablemana:
				# Each of the options we had before this land needs to get appended with one of these.
				newoptionswiththisland.append(manaoption + manasymbol)

			# Okay, if the new option is actually new, append it.
			for newoption in newoptionswiththisland:
				if newoption not in availablemana:
					availablemana.append(newoption)

			if debug['manaAvailable']: print('       Possible mana pools are now:',availablemana)

		return availablemana

def parseLands(decklist):
	# This function should take a decklist and go through all the lands creating a small database of lands.
	# For example, a Jeskai decklist might end up with the following landsDatabase:
	# landsDatabase['Island'] = ['{U}']   (not the string {U}, but the ManaPool object)
	# landsDatabase['Mountain'] = ['{R}']
	# landsDatabase['Temple of Epiphany'] = ['{U}','{R}']
	# landsDatabase['Flooded Strand'] = ['FetchU','FetchW']

	# A decklist is a dictionary with key being the name of the card, and value being the number of copies in the deck.
	global landsDatabase 
	landsDatabase = {}
	landsDatabase['Island'] = [ManaPool('{U}')]
	landsDatabase['Mountain'] = [ManaPool('{R}')]
	landsDatabase['Swamp'] = [ManaPool('{B}')]
	landsDatabase['Forest'] = [ManaPool('{G}')]
	landsDatabase['Plains'] = [ManaPool('{W}')]

	if debug['parseLands']: print('')
	if debug['parseLands']: print('Beginning Land Parser.')

	for card in decklist:
		if isLand(card) and card not in landsDatabase:
			if debug['parseLands']: print('Parsing land:',card)
			landsDatabase[card] = []
			if 'text' in cardDatabase[card]:
				# Parse through the text looking for mana symbols. When we get to a { we start a new symbol; a } ends it.
				currentsymbol = ''
				for char in cardDatabase[card]['text']:
					if char =='{':
						currentsymbol = '{'
					elif char == '}':
						# We don't want the tap symbol to make it in here. :)
						if currentsymbol != '{T':
							landsDatabase[card].append(ManaPool(currentsymbol+char))
					else:
						# This is useful if the mana cost is 15, so we don't end up adding 6 to the mana cost.
						currentsymbol += char
				# Parse through the text looking for "scry" or "fetch."
				if 'scry' in cardDatabase[card]['text']:
					landsDatabase[card].append('scry')
				if 'any color' in cardDatabase[card]['text']:
					landsDatabase[card].append(ManaPool('{W}'))
					landsDatabase[card].append(ManaPool('{U}'))
					landsDatabase[card].append(ManaPool('{R}'))
					landsDatabase[card].append(ManaPool('{B}'))
					landsDatabase[card].append(ManaPool('{G}'))
				if 'Search your library' in  cardDatabase[card]['text']:
					if 'Plains' in cardDatabase[card]['text']:
						landsDatabase[card].append('FetchW')
					if 'Swamp' in cardDatabase[card]['text']:
						landsDatabase[card].append('FetchB')
					if 'Mountain' in cardDatabase[card]['text']:
						landsDatabase[card].append('FetchR')
					if 'Island' in cardDatabase[card]['text']:
						landsDatabase[card].append('FetchU')
					if 'Forest' in cardDatabase[card]['text']:
						landsDatabase[card].append('FetchG')
			if debug['parseLands']: print('Parsed as ',landsDatabase[card])

	if debug['parseLands']: print('End of Land Parser. Results below:')
	if debug['parseLands']: print(landsDatabase)
	if debug['parseLands']: print('')

class ManaPool:
	# A mana pool is really an object, for example 1U + 2UR = 3UUR.
	# We will store this as a number, some blue, some red, and so on.
	# A mana cost like {3}{U}{U}{G} needs to be the thing that starts it.
	def __init__(self, manacost):
		# This implementation would completely fail for, say, Boros Reckoner.
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
				else:
					self.colorless += int(currentsymbol)
			else:
				# This is useful if the mana cost is 15, so we don't end up adding 6 to the mana cost.
				currentsymbol += char
	def __repr__(self):
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

	# += is implemented
	def __iadd__(self, other):
		self.colorless += other.colorless
		self.blue += other.blue
		self.green += other.green
		self.white += other.white
		self.red += other.red
		self.black += other.black
		return self

	def __add__(self, other):
		# This feels like a really bad way to implement plus?
		thesum = ManaPool('{0}')
		thesum.colorless = self.colorless + other.colorless
		thesum.blue = self.blue + other.blue
		thesum.green = self.green + other.green
		thesum.white = self.white + other.white
		thesum.red = self.red + other.red
		thesum.black = self.black + other.black
		return thesum

	def __eq__(self, other):
		if type(other) is type(self):
			return self.__dict__ == other.__dict__
		return False

def isLand(card):
	# We just want to check whether this card is a land or not. "card" is a string, so we'll have to use it as the key in the dictionary.
	return ('Land' in cardDatabase[card]['types'])

def is_int(s):
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

	# If all the cards we are checking on have already been cast, then we don't actually have to even play another land.
	if 0 in caststhistrial[len(lineofplay.plays)].values():
		if debug['DrawCard']: print('  Casts this trial:',caststhistrial)
		# Start by drawing a card, if we are supposed to.
		if drawacard:
			lineofplay.draw_card()
			if debug['DrawCard']: print('  Drew a card:',lineofplay)

		# Go through each card; if that is a land that we haven't tried yet, make a new line of play for it.
		landstotry = []
		for i in range(len(lineofplay.hand)):
			card = lineofplay.hand[i]
			if isLand(card):
				landstotry.append(card)

		for card in set(landstotry):
			# If it is a fetchland, we'll want to make two lines of play for the two fetch options. Todo: Pay 1 life
			if 'FetchU' in landsDatabase[card] or 'FetchW' in landsDatabase[card] or 'FetchB' in landsDatabase[card] or 'FetchG' in landsDatabase[card] or 'FetchR' in landsDatabase[card]:
				for fetchOption in landsDatabase[card]:
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
						i = newlineofplay.deck.index(fetch)
						# Pop the appropriate card from the deck and into play.
						newlineofplay.plays.append([newlineofplay.deck.pop(i)])	
						# Shuffle the deck. Wait! No. If we shuffle the deck, we create a prescience problem where playing a fetch doubles your chances of a good topdeck. Without shuffling, we do the scry/fetch interaction wrong, but that is a much smaller error.
						# newlineofplay.deck = random.sample(newlineofplay.deck, len(newlineofplay.deck))

						# Check if anything is castable -- this increments caststhisturn.
						checkCastable(newlineofplay)
						# Keep going, if we should.
						if len(newlineofplay.plays) < maxturns:
							continuePlaying(newlineofplay,True)
			else:
				# Playing a non-fetchland is much easier.
				newlineofplay = deepcopy(lineofplay)
				# Pop that card out of the hand and into the plays, then. Where is it?
				i = newlineofplay.hand.index(card)
				newlineofplay.plays.append([newlineofplay.hand.pop(i)])
				# Check if anything is castable -- this increments caststhisturn.
				checkCastable(newlineofplay)
				# Keep going, if we should.
				if len(newlineofplay.plays) < maxturns:
					if 'scry' in landsDatabase[card]:
						# If the land was a scryland, then we also need a line of play where we bottomed the top card.
						newlineofplay2 = deepcopy(newlineofplay)
						# We don't need to do another castable check here; nothing is new.
						# However, we should definitely bottom the top card before continuing.
						newlineofplay2.deck = newlineofplay.deck[1:] + newlineofplay.deck[:1]
						continuePlaying(newlineofplay2, True)

					continuePlaying(newlineofplay,True)
	else:
		if debug['DrawCard']: print('     Casts this trial:',caststhistrial)
		if debug['DrawCard']: print('     All spells already cast by this turn; not playing any more lands.')

	# Also remember to continue this line of play (where you didn't play a land this turn).
	lineofplay.plays.append([])
	checkCastable(lineofplay)

	if len(lineofplay.plays) < maxturns:
		continuePlaying(lineofplay,True)

def checkCastable(lineofplay):
	# Here we have a line of play where the current turn has its land played, but the "Casts" have not been updated.
	if debug['CastSpell']: print('     checkCastable on:',lineofplay)
	turn = len(lineofplay.plays)

	# This returns a sequence of ManaPool objects, the various things we could make with this mana.
	manaAvailable = lineofplay.manaAvailable()
	if debug['CastSpell']: print('       Mana options available:',manaAvailable)

	# At the moment the only spells we are counting are opening hand spells. Those are stored in the global spellsthistrial.
	for card in spellsthistrial:
		if caststhistrial[turn-1][card] == 0 and cardDatabase[card]['cmc'] <= (turn):
			manaCost = ManaPool(cardDatabase[card]['manaCost'])
			for pool in manaAvailable:
				# We can stop moving if we already cast this card this turn.				
				if caststhistrial[turn-1][card] == 1: break
				if debug['CastSpell']: print('       trying to cast',card,'... comparing',pool,' to ', manaCost)
				if pool == manaCost:
					# If the mana is doable, let's make sure we don't have any other requirements:
					if card == 'Chained to the Rocks':
						if debug['CastSpell']: print('       mana is okay for '+card)
						haveMountain = 0
						for play in lineofplay.plays:
							for land in play:
								if 'subtypes' in cardDatabase[land]:
									if 'Mountain' in cardDatabase[land]['subtypes']:
										if debug['CastSpell']: print('       successfully cast '+card)
										caststhistrial[turn-1][card] = 1
					else:
						# We aren't incrementing this; it is a flag 0 or 1.
						if debug['CastSpell']: print('       successfully cast '+card)
						caststhistrial[turn-1][card] = 1

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

		# Split one time, based on delimiters of space, the letter x, and tab -- that way we can parse '2x Flooded Strand' is ['2','Flooded Strand']
		words = re.split(r'[ x\t]+',line,1)
		# Okay, now the lines we want to parse look like '2x','Flooded Strand'
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
	# Shuffle the deck.
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

				if casts[i][card] >= 5 and (draws[card]-casts[i][card]) >= 5 and draws[card] >= 30:
					error = 1.96*math.sqrt(casts[i][card]*(draws[card]-casts[i][card])/math.pow(draws[card],3))
					error = '{:<6.1%}'.format(error)
					percents[card]+= 'E:'+error
				else:
					percents[card]+= '        '
					
	for card in draws:
		print(percents[card])




# A decklist is a dictionary where the key is the card name and the value is the number of copies. This should make importing easy.
# Now we have a decklistParse() function that takes a filename and tries to read it.
parseDecklist(deckfile)

# We need to go through all the lands in our deck and figure out what is going on with them.
parseLands(decklist)

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

	if debug['DrawCard']: print('')
	if debug['Minimal']: 
		if trial % 100 == 0: print('Trial',trial,'starting.')

	# Start by drawing a hand of 7.
	lineofplay = drawHand(7)

	# If we are considering mulligans, then we have to look at how many lands we have.
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
			# If we are never going to play enough turns to cast this spell, just act like you never even drew it, to save time.
			if cardDatabase[card]['cmc'] <= maxturns:
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


displayResults()



