Manabase
========

A simulator that runs a Magic: The Gathering deck through repeated trials to determine the effectiveness of the deck's mana.

To use the tool, you will need a Python interpreter (this was tested with Python 3.4, see https://www.python.org/download/releases/3.4.0/) and decklists in text format.

I'm not a professional programmer, so suggestions and constructive criticism about the tool are welcome!

Current featurelist/todo:

Features
* Given a decklist, the program shuffles the deck, draws an initial hand, and then simply tries all possible lines of play to see if any of them lead to spells being castable. 
* The lines of play can be printed to the screen for the user's inspection, or played silently to collect data as quickly as possible.
* Aggregate results are stored over multiple sets of trials and can be output in text format or HTML files via a minimal user interface.
* A simple mulligan strategy is implemented: 7-card hands with 0, 1, 6, or 7 lands are mulliganed. 6-card hands with 0, 1, 5, or 6 lands are mulliganed. 5-card hands with 0 or 5 lands are mulliganed.
* Multicolored lands are handled properly. Fetchlands and scrylands decisions are implemented as lines of play.
* The most common corner cases in Khans of Tarkir standard, namely Urborg, Tomb of Yawgmoth, Chained to the Rocks, and Evolving Wilds, are handled appropriately. 
* Mana abilities of cards like Elvish Mystic, Noble Hierarch, Sylvan Caryatid, and Abzan Banner are implemented, but mana abilities that have a cost (e.g. Signets) silently give wrong results.
* Casting a spell that allows another spell to be cast that turn also works, e.g. Plains, Plains, Plains, Abzan Banner, Avacyn's Pilgrim, Wingmate Roc successfully casts Avacyn's Pilgrim turn 3 and Wingmate Roc turn 4.
* A comprehensive battery of tests helps ensure that the results we get here are accurate.

To-do
* Implement Satyr Wayfinder.
* Implement Courser of Kruphix.
* Implement card draw spells.
* Implement Nykthos.
* Track pain taken from painlands and fetches somehow; track life gained from lands and Courser.
* Implement Checklands (do people use those or care?)
* Allow an option to scale the percentages so that not making land drops doesn’t count against a spell's castability.
* Do something intelligent with sideboards.

Not Planned
* X spells will probably always be treated as though X = 0.
* Delve and other alternate cost mechanics are probably forever ignored. If you want to check whether you have double blue by turn 5, replace Dig Through Time with Tidebinder Mage in your decklist.
* Fetching will never shuffle your library, meaning it does not exactly work correctly with scry; if it did, another fix would be needed to prevent “prescient fetching.” Courser will turn every fetchland into an untapped scryland, which is pretty close.
* “Curving out”: If your hand is Temple, Mountain, then you can’t cast both your one-drop and your two-drop on curve, but the program notices that you can do either one, so both will probably always count as castable.
 
In case it wasn't clear, this kind of analysis is definitely inspired by Frank Karsten's Frank Analysis series, especially the article here: http://www.channelfireball.com/articles/frank-analysis-how-many-colored-mana-sources-do-you-need-to-consistently-cast-your-spells/ . 

