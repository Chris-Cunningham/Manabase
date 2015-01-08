import unittest



from manabase import *

class TestContinuePlaying(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_basic_lands_turn_1_maxturns_1(self):
        """One turn with starting hand of Forest, Mountain, Elvish Mystic, Frenzied Goblin, Destructive Revelry. Swamp on top."""
        self.assertDictEqual( continuePlaying(	LineOfPlay([],['Forest','Mountain','Elvish Mystic','Frenzied Goblin','Destructive Revelry'],['Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1, 'Destructive Revelry': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Destructive Revelry',    'Elvish Mystic',    'Frenzied Goblin'],
                                             [{'Destructive Revelry': 0, 'Elvish Mystic': 0, 'Frenzied Goblin': 0}], 0, 1 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Destructive Revelry': 0, 'Elvish Mystic': 1, 'Frenzied Goblin': 1} )
 
    def test_basic_lands_turn_1_maxturns_2(self):
        """One turn with starting hand of Forest, Mountain, Elvish Mystic, Frenzied Goblin, Destructive Revelry. Swamp on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest','Mountain','Elvish Mystic','Frenzied Goblin','Destructive Revelry'],['Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1, 'Destructive Revelry': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Destructive Revelry',    'Elvish Mystic',    'Frenzied Goblin'],
                                             [{'Destructive Revelry': 0, 'Elvish Mystic': 0, 'Frenzied Goblin': 0},{'Destructive Revelry': 0, 'Elvish Mystic': 0, 'Frenzied Goblin': 0}], 0, 2 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Destructive Revelry': 0, 'Elvish Mystic': 1, 'Frenzied Goblin': 1} )

    def test_basic_lands_turn_2_maxturns_2(self):
        """One turn with starting hand of Forest, Mountain, Elvish Mystic, Frenzied Goblin, Destructive Revelry. Swamp on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest','Mountain','Elvish Mystic','Frenzied Goblin','Destructive Revelry'],['Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1, 'Destructive Revelry': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Destructive Revelry',    'Elvish Mystic',    'Frenzied Goblin'],
                                             [{'Destructive Revelry': 0, 'Elvish Mystic': 0, 'Frenzied Goblin': 0},{'Destructive Revelry': 0, 'Elvish Mystic': 0, 'Frenzied Goblin': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Destructive Revelry': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1} )

    def test_basic_lands_cast_colorless_turn_1_maxturns_2(self):
        """One turn with starting hand of Forest, Mountain, Ornithopter, Voltaic Key, Time Vault. Swamps on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest','Mountain','Ornithopter','Voltaic Key','Time Vault'],['Swamp','Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Ornithopter',    'Voltaic Key',    'Time Vault'],
                                             [{'Ornithopter': 0, 'Voltaic Key': 0, 'Time Vault': 0},{'Ornithopter': 0, 'Voltaic Key': 0, 'Time Vault': 0}], 0, 2 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 0} )

    def test_basic_lands_cast_colorless_turn_2_maxturns_2(self):
        """Two turns with starting hand of Forest, Mountain, Ornithopter, Voltaic Key, Time Vault. Swamps on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest','Mountain','Ornithopter','Voltaic Key','Time Vault'],['Swamp','Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Ornithopter',    'Voltaic Key',    'Time Vault'],
                                             [{'Ornithopter': 0, 'Voltaic Key': 0, 'Time Vault': 0},{'Ornithopter': 0, 'Voltaic Key': 0, 'Time Vault': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 1} )

    def test_basic_lands_cast_offcolor_turn_1_maxturns_2(self):
        """Two turns with starting hand of Forest, Mountain, Ancestral Recall. Swamps on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest','Mountain','Ancestral Recall'],['Swamp','Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Ancestral Recall': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Ancestral Recall'],
                                             [{'Ancestral Recall': 0},{'Ancestral Recall': 0}], 0, 2 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Ancestral Recall': 0} )

    def test_basic_lands_cast_offcolor_turn_2_maxturns_2(self):
        """Two turns with starting hand of Forest, Mountain, Ancestral Recall. Swamps on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest','Mountain','Ancestral Recall'],['Swamp','Swamp']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Ancestral Recall': 1, 'Swamp': 1}),
                                             False, 
                                             [ 'Ancestral Recall'],
                                             [{'Ancestral Recall': 0},{'Ancestral Recall': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Ancestral Recall': 0} )

    def test_basic_lands_cast_multicolored_spell_not_yet(self):
        """Four turns with starting hand of Forest, Mountain, Plains, Swamp, Island, Chromanticore. Grizzly Bears on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest', 'Mountain', 'Plains', 'Swamp', 'Island', 'Chromanticore'],['Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Chromanticore': 1, 'Grizzly Bears': 6}),
                                             False, 
                                             [ 'Chromanticore'],
                                             [{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0}], 0, 6 #maxturns here at the end
                                           )[1][3], #turn number minus 1 here at the end
                           {'Chromanticore': 0} )

    def test_basic_lands_cast_multicolored_spell_success(self):
        """Five turns with starting hand of Forest, Mountain, Plains, Swamp, Island, Chromanticore. Grizzly Bears on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest', 'Mountain', 'Plains', 'Swamp', 'Island', 'Chromanticore'],['Grizzly Bears','Grizzly Bears','Grizzly Bearss','Grizzly Bearss','Grizzly Bearss','Grizzly Bearss']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Chromanticore': 1, 'Grizzly Bears': 6}),
                                             False, 
                                             [ 'Chromanticore'],
                                             [{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0}], 0, 6 #maxturns here at the end
                                           )[1][4], #turn number minus 1 here at the end
                           {'Chromanticore': 1} )

    def test_basic_lands_cast_multicolored_spell_still_a_success(self):
        """Six turns with starting hand of Forest, Mountain, Plains, Swamp, Island, Chromanticore. Grizzly Bears on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Forest', 'Mountain', 'Plains', 'Swamp', 'Island', 'Chromanticore'],['Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Chromanticore': 1, 'Grizzly Bears': 6}),
                                             False, 
                                             [ 'Chromanticore'],
                                             [{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0},{'Chromanticore': 0}], 0, 6 #maxturns here at the end
                                           )[1][5], #turn number minus 1 here at the end
                           {'Chromanticore': 1} )

    def test_basic_lands_on_the_draw_turn_1(self):
        """Topdeck a Forest allowing you to cast Mystic."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                             True, 
                                             [ 'Elvish Mystic'],
                                             [{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0}], 0, 6 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Elvish Mystic': 1} )

    def test_basic_lands_on_the_play_turn_1(self):
        """Fail to topfeck a Forest allowing you to cast Mystic because you are on the play."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                             False, 
                                             [ 'Elvish Mystic'],
                                             [{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0}], 0, 6 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Elvish Mystic': 0} )
    
    def test_basic_lands_on_the_play_turn_2(self):
        """Topdeck a Forest allowing you to cast Mystic turn 2 because you are on the play."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                             False, 
                                             [ 'Elvish Mystic'],
                                             [{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0}], 0, 6 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Elvish Mystic': 1} )

    def test_spellsthistrial(self):
        """If we can cast our spell turn 2 but it is not in spellsthistrial, we should just magically not notice that we cast it."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                             ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                             False, 
                                             [ 'Nicol Bolas, Planeswalker'],
                                             [{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0},{'Elvish Mystic': 0}], 0, 6 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Elvish Mystic': 0} )

    def test_pain_lands_turn_1(self):
        """Painlands can tap for either of two colors on the turn you play them."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Battlefield Forge','Frenzied Goblin','Soldier of the Pantheon','Ancestral Recall'],[]),
                                             ManaBase({'Battlefield Forge': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Ancestral Recall': 1}),
                                             False, 
                                             [ 'Frenzied Goblin',   'Soldier of the Pantheon',   'Ancestral Recall'],
                                             [{'Frenzied Goblin': 0,'Soldier of the Pantheon': 0,'Ancestral Recall': 0}], 0, 1 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Ancestral Recall': 0} )

    def test_anycolor_lands_turn_1(self):
        """Some lands can tap for any color on the turn you play them."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Mana Confluence','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],[]),
                                             ManaBase({'Mana Confluence': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 1}),
                                             False, 
                                             [ 'Frenzied Goblin',   'Soldier of the Pantheon',   'Cloudfin Raptor'],
                                             [{'Frenzied Goblin': 0,'Soldier of the Pantheon': 0,'Cloudfin Raptor': 0}], 0, 1 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 1} )

    def test_tapped_lands_turn_1(self):
        """Some lands come into play tapped. Here we test starting with a tapped red source and an untapped white source."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Wind-Scarred Crag','Plains','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],['Cloudfin Raptor']),
                                             ManaBase({'Wind-Scarred Crag': 1,'Plains': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 2}),
                                             False, 
                                             [ 'Frenzied Goblin',   'Soldier of the Pantheon',   'Cloudfin Raptor'],
                                             [{'Frenzied Goblin': 0,'Soldier of the Pantheon': 0,'Cloudfin Raptor': 0}], 0, 1 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 0,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 0} )

    def test_tapped_lands_turn_2(self):
        """Some lands come into play tapped. Here we test starting with a tapped red source and an untapped white source."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Wind-Scarred Crag','Plains','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],['Cloudfin Raptor','Cloudfin Raptor']),
                                             ManaBase({'Wind-Scarred Crag': 1,'Plains': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 3}),
                                             False, 
                                             [ 'Frenzied Goblin',   'Soldier of the Pantheon',   'Cloudfin Raptor'],
                                             [{'Frenzied Goblin': 0,'Soldier of the Pantheon': 0,'Cloudfin Raptor': 0},{'Frenzied Goblin': 0,'Soldier of the Pantheon': 0,'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 0} )

    def test_scry_land_need_to_keep_on_top(self):
        """This line of play needs to be to play the temple and keep the next card on top."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Temple of Triumph','Swamp','Wojek Halberdiers'],['Plains','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor']),
                                             ManaBase({'Temple of Triumph': 1,'Swamp': 1,'Wojek Halberdiers': 1,'Plains': 1,'Cloudfin Raptor': 3}),
                                             False, 
                                             [ 'Wojek Halberdiers',    'Cloudfin Raptor'],
                                             [{'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0},{'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Wojek Halberdiers': 1, 'Cloudfin Raptor': 0} )

    def test_scry_land_need_to_put_on_bottom(self):
        """This line of play needs to be to play the temple and bottom that cloudfin raptor."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Temple of Triumph','Swamp','Wojek Halberdiers'],['Cloudfin Raptor','Plains','Cloudfin Raptor','Cloudfin Raptor']),
                                             ManaBase({'Temple of Triumph': 1,'Swamp': 1,'Wojek Halberdiers': 1,'Plains': 1,'Cloudfin Raptor': 3}),
                                             False, 
                                             [ 'Wojek Halberdiers',    'Cloudfin Raptor'],
                                             [{'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0},{'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Wojek Halberdiers': 1, 'Cloudfin Raptor': 0} )

    def test_scry_land_doesnt_scry_2_or_backwards(self):
        """This line of play can't cast Wojek Halberdiers unless the land somehow accidentally scries twice or upside down."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Temple of Triumph','Swamp','Wojek Halberdiers'],['Cloudfin Raptor','Cloudfin Raptor','Plains','Cloudfin Raptor']),
                                             ManaBase({'Temple of Triumph': 1,'Swamp': 1,'Wojek Halberdiers': 1,'Plains': 1,'Cloudfin Raptor': 3}),
                                             False, 
                                             [ 'Wojek Halberdiers',    'Cloudfin Raptor'],
                                             [{'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0},{'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0} )

    def test_urborg_is_in_the_manadatabase(self):
        """Just making sure we know Urborg is a land."""
        self.assertListEqual( ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Mountain': 1}).manaDatabase['Urborg, Tomb of Yawgmoth'],
                            [] )

    def test_urborg_is_an_available_manasource(self):
        """Make sure that if Urborg gets played, it counts as a mana source."""
        self.assertListEqual( manaSourcesAvailable(LineOfPlay([['Urborg, Tomb of Yawgmoth']],[],[]), ManaBase({'Urborg, Tomb of Yawgmoth': 1})), 
                            ['Urborg, Tomb of Yawgmoth'] )

    def test_urborg_is_a_swamp(self):
        """This line of play just makes sure Urborg taps for black."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Urborg, Tomb of Yawgmoth','Thoughtseize'],[]),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1,'Thoughtseize': 1}),
                                             False, 
                                             [ 'Thoughtseize',],
                                             [{'Thoughtseize': 0}], 0, 1 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Thoughtseize': 1} )

    def test_urborg_is_not_a_mountain(self):
        """This line of play just makes sure Urborg doesn't tap for red."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Urborg, Tomb of Yawgmoth','Frenzied Goblin'],[]),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1,'Frenzied Goblin': 1}),
                                             False, 
                                             [ 'Frenzied Goblin',],
                                             [{'Frenzied Goblin': 0}], 0, 1 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 0} )

    def test_urborg_makes_mountains_into_swamps(self):
        """This line of play just makes sure Urborg taps for black."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Urborg, Tomb of Yawgmoth','Mountain','Bile Blight'],['Cloudfin Raptor']),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Mountain': 1, 'Bile Blight': 1, 'Cloudfin Raptor': 1}),
                                             False, 
                                             [ 'Bile Blight',    'Cloudfin Raptor'],
                                             [{'Bile Blight': 0, 'Cloudfin Raptor': 0}, {'Bile Blight': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Bile Blight': 1, 'Cloudfin Raptor': 0} )

    def test_urborg_doesnt_ramp(self):
        """This line of play just makes sure Urborg isn't totally broken."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Urborg, Tomb of Yawgmoth','Mountain','Bile Blight'],['Cloudfin Raptor']),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Mountain': 1, 'Bile Blight': 1, 'Cloudfin Raptor': 1}),
                                             False, 
                                             [ 'Bile Blight',    'Cloudfin Raptor'],
                                             [{'Bile Blight': 0, 'Cloudfin Raptor': 0}, {'Bile Blight': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Bile Blight': 0, 'Cloudfin Raptor': 0} )

    def test_urborg_doesnt_untap_lands(self):
        """This line of play draws a tapped land turn 2, so it can't cast Bile Blight turn 2."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Urborg, Tomb of Yawgmoth','Bile Blight'],['Temple of Mystery']),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Temple of Mystery': 1, 'Bile Blight': 1, 'Cloudfin Raptor': 1}),
                                             False, 
                                             [ 'Bile Blight',    'Cloudfin Raptor'],
                                             [{'Bile Blight': 0, 'Cloudfin Raptor': 0}, {'Bile Blight': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][0], #turn number minus 1 here at the end
                           {'Bile Blight': 0, 'Cloudfin Raptor': 0} )

    def test_urborg_doesnt_break_duals(self):
        """This line of play draws a Battlefield Forge turn 2, so it should be fine casting a WB spell."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Urborg, Tomb of Yawgmoth','Zealous Persecution'],['Battlefield Forge', 'Cloudfin Raptor']),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Zealous Persecution': 1, 'Battlefield Forge': 1, 'Cloudfin Raptor': 1}),
                                             False, 
                                             [ 'Zealous Persecution',    'Cloudfin Raptor'],
                                             [{'Zealous Persecution': 0, 'Cloudfin Raptor': 0}, {'Zealous Persecution': 0, 'Cloudfin Raptor': 0}], 0, 2 #maxturns here at the end
                                           )[1][1], #turn number minus 1 here at the end
                           {'Zealous Persecution': 1, 'Cloudfin Raptor': 0} )

    def test_scry_to_swamp_to_get_B(self):
        """Trying to scry to bottom three times to find Swamp for Thoughtseize."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Temple of Triumph','Temple of Triumph','Temple of Triumph','Thoughtseize'],['Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Swamp']),
                                             ManaBase({'Swamp': 1, 'Temple of Triumph': 3, 'Thoughtseize': 1, 'Cloudfin Raptor': 5}),
                                             False, 
                                             [ 'Thoughtseize',    'Cloudfin Raptor'],
                                             [{'Thoughtseize': 0, 'Cloudfin Raptor': 0}, {'Thoughtseize': 0, 'Cloudfin Raptor': 0}, {'Thoughtseize': 0, 'Cloudfin Raptor': 0}, {'Thoughtseize': 0, 'Cloudfin Raptor': 0}], 0, 4 #maxturns here at the end
                                           )[1][3], #turn number minus 1 here at the end
                           {'Thoughtseize': 1, 'Cloudfin Raptor': 0} )


    def test_scry_to_urborg_to_get_BBBB(self):
        """Trying to scry to bottom three times to cast Phyrexian Obliterator with Urborg."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Temple of Triumph','Temple of Triumph','Temple of Triumph','Phyrexian Obliterator'],['Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Urborg, Tomb of Yawgmoth']),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Temple of Triumph': 3, 'Phyrexian Obliterator': 1, 'Cloudfin Raptor': 5}),
                                             False, 
                                             [ 'Phyrexian Obliterator',    'Cloudfin Raptor'],
                                             [{'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}, {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}, {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}, {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}], 0, 4 #maxturns here at the end
                                           )[1][3], #turn number minus 1 here at the end
                           {'Phyrexian Obliterator': 1, 'Cloudfin Raptor': 0} )

    def test_scry_not_enough_to_urborg_to_get_BBBB(self):
        """With one more scry, we could get there, but with two we can't get to Urborg."""
        self.assertDictEqual( continuePlaying(  LineOfPlay([],['Temple of Triumph','Temple of Triumph','Mountain','Phyrexian Obliterator'],['Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Urborg, Tomb of Yawgmoth']),
                                             ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Temple of Triumph': 2, 'Mountain': 1, 'Phyrexian Obliterator': 1, 'Cloudfin Raptor': 5}),
                                             False, 
                                             [ 'Phyrexian Obliterator',    'Cloudfin Raptor'],
                                             [{'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}, {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}, {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}, {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0}], 0, 4 #maxturns here at the end
                                           )[1][3], #turn number minus 1 here at the end
                           {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0} )



if __name__ == '__main__':
    unittest.main()