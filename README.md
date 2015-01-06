Manabase
========

A simulator that runs a Magic: The Gathering deck through repeated trials to determine the effectiveness of the deck's mana.

To use the tool, you will need a Python interpreter, the allCards.json file from mtgjson, and decklists in text format.

I'm not a professional programmer, so suggestions and constructive criticism about the tool are welcome!

Current featurelist/todo:

Features
* Given an initial hand, the program simply tries all possible lines of play.
* A simple mulligan strategy is implemented to simulate a real player’s mulligans.
* Painlands and other multi-option lands are handled properly.
* Fetchlands and scrylands present decisions that are implemented as lines of play. The simulation has “prescient scries” since it tries both topping and bottoming the card, but it does not have “prescient fetches;” the deck is not shuffled after a fetch to avoid this.
* The most common corner cases in the current standard: Urborg, Tomb of Yawgmoth and Chained to the Rocks are handled appropriately. 
* Mana abilities of cards like Elvish Mystic and Abzan Banner are implemented, but mana abilities that have a cost are not currently handled well, for example a Signet acts like a Sol Ring right now.
* Aggregate results are stored over multiple sets of trials and can be output in text format or HTML tables via a minimal user interface.

To-do
* If we're going to the trouble of creating output in HTML format, we might as well write it to an HTML file.
* Deal with the weirdness of the global variables that are being used, and fix the user interface.
* Tests to make sure things are working before doing the larger-scale changes below.
* Implement Satyr Wayfinder.
* Implement Courser of Kruphix.
* Implement card draw spells.
* Implement Nykthos.
* Clean up debug messages so there are coherent debug levels instead of random debug flags.
* Track pain taken from painlands and fetches; track life gained from lands and Courser.
* Allow an option to scale the percentages so that not making land drops doesn’t count against a spell's castability.
* Do something intelligent with sideboards.

Not Planned
* X spells will probably always be treated as though X = 0.
* Delve and other alternate cost mechanics are probably forever ignored.
* Fetching will never shuffle your library, meaning it does not exactly work correctly with scry or Courser; if it did, another fix would be needed to prevent “prescient fetching.”
* “Curving out”: If your hand is Temple, Mountain, then you can’t cast both your one-drop and your two-drop on curve, but the program notices that you can do either one, so both will probably always count as castable.
 
In case it wasn't clear, this kind of analysis is definitely inspired by Frank Karsten's Frank Analysis series, especially the article here: http://www.channelfireball.com/articles/frank-analysis-how-many-colored-mana-sources-do-you-need-to-consistently-cast-your-spells/ . 

