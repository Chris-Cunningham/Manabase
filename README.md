Manabase
========

A simulator that runs a Magic: The Gathering deck through repeated trials to determine the effectiveness of the deck's mana.

To use the tool, you will need a Python interpreter, the allCards.json file from mtgjson, and decklists in text format.

I'm not a professional programmer, so suggestions and constructive criticism about the tool are welcome; any statements that imply I think this is a masterwork of programming will be brutally ignored.

Current featurelist/todo:

Features
* Given an initial hand, the program simply tries all possible lines of play.
* A simple mulligan strategy is implemented to simulate a real player’s mulligans.
* Painlands and other multi-option lands are handled properly.
* Fetchlands and scrylands present decisions that are implemented as lines of play. The simulation has “prescient scries” since it tries both topping and bottoming the card, but it does not have “prescient fetches;” the deck is not shuffled after a fetch to avoid this.
* The most common corner cases in the current standard: Urborg, Tomb of Yawgmoth and Chained to the Rocks are handled appropriately. 

To-do
* Currently, fetchlands do not fetch nonbasic lands; sorry non-Standard players!
* Currently, the effects of any spells cast are completely ignored. This means Satyr Wayfinder and Courser of Kruphix decks can’t yet explore the fixing properties of those cards, and effects like Farseek or Explore just don’t happen.
* All lands are assumed to tap for one colorless as an alternate mode.
* The pain incurred by fetching or tapping a painland is not tracked.
* Allow an option to scale the percentages so that not making land drops doesn’t count against a spell.

Not Planned
* X spells are always treated with X=0.
* Delve and other alternate cost mechanics are ignored.
* Fetching does not shuffle your library so it does not exactly work correctly with scry or (later) Courser; if it did then another fix would be needed to prevent “prescient fetching.”
* “Curving out”: If your hand is Temple, Mountain, then you can’t cast both your one-drop and your two-drop on curve, but the program notices that you can do either one, so both currently count as castable.
 
In case it wasn't clear, this kind of analysis is definitely inspired by Frank Karsten's Frank Analysis series, especially the article here: http://www.channelfireball.com/articles/frank-analysis-how-many-colored-mana-sources-do-you-need-to-consistently-cast-your-spells/ . 

