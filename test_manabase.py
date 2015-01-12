import unittest



from manabase import *

class TestPlayHand(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_basic_lands_turn_1_maxturns_1(self):
        """One turn with starting hand of Forest, Mountain, Elvish Mystic, Frenzied Goblin, Destructive Revelry. Swamp on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Elvish Mystic','Frenzied Goblin','Destructive Revelry'],['Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1, 'Destructive Revelry': 1, 'Swamp': 1}),
                                      1,       # maxturns here
                                      False 
                                      )[0][0], #turn number minus 1 here at the end
                           {'Destructive Revelry': 0, 'Elvish Mystic': 1, 'Frenzied Goblin': 1} )
 
    def test_basic_lands_turn_1_maxturns_2(self):
        """One turn with starting hand of Forest, Mountain, Elvish Mystic, Frenzied Goblin, Destructive Revelry. Swamp on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Elvish Mystic','Frenzied Goblin','Destructive Revelry'],['Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1, 'Destructive Revelry': 1, 'Swamp': 1}),
                                      1,       # maxturns here
                                      False 
                                      )[0][0], #turn number minus 1 here at the end
                           {'Destructive Revelry': 0, 'Elvish Mystic': 1, 'Frenzied Goblin': 1} )

    def test_basic_lands_turn_2_maxturns_2(self):
        """One turn with starting hand of Forest, Mountain, Elvish Mystic, Frenzied Goblin, Destructive Revelry. Swamp on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Elvish Mystic','Frenzied Goblin','Destructive Revelry'],['Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1, 'Destructive Revelry': 1, 'Swamp': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Destructive Revelry': 1, 'Elvish Mystic': 1, 'Frenzied Goblin': 1} )

    def test_basic_lands_cast_colorless_turn_1_maxturns_2(self):
        """One turn with starting hand of Forest, Mountain, Ornithopter, Voltaic Key, Time Vault. Swamps on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Ornithopter','Voltaic Key','Time Vault'],['Swamp','Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 1, 'Swamp': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 0} )

    def test_basic_lands_cast_colorless_turn_2_maxturns_2(self):
        """Two turns with starting hand of Forest, Mountain, Ornithopter, Voltaic Key, Time Vault. Swamps on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Ornithopter','Voltaic Key','Time Vault'],['Swamp','Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 1, 'Swamp': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Ornithopter': 1, 'Voltaic Key': 1, 'Time Vault': 1} )

    def test_basic_lands_cast_offcolor_turn_1_maxturns_2(self):
        """Two turns with starting hand of Forest, Mountain, Cloudfin Raptor. Swamps on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Cloudfin Raptor'],['Swamp','Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Cloudfin Raptor': 1, 'Swamp': 1}),
                                      1,       # maxturns here
                                      False 
                                      )[0][0], #turn number minus 1 here at the end
                           {'Cloudfin Raptor': 0} )

    def test_basic_lands_cast_offcolor_turn_2_maxturns_2(self):
        """Two turns with starting hand of Forest, Mountain, Cloudfin Raptor. Swamps on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Mountain','Cloudfin Raptor'],['Swamp','Swamp']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Cloudfin Raptor': 1, 'Swamp': 1}),
                                      2,       # maxturns here
                                      False 
                                      )[0][1], #turn number minus 1 here at the end
                           {'Cloudfin Raptor': 0} )

    def test_basic_lands_cast_multicolored_spell_not_yet(self):
        """Four turns with starting hand of Forest, Mountain, Plains, Swamp, Island, Chromanticore. Grizzly Bears on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest', 'Mountain', 'Plains', 'Swamp', 'Island', 'Chromanticore'],['Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Chromanticore': 1, 'Grizzly Bears': 6}),
                                      5,       # maxturns here
                                      False 
                                      )[0][3], #turn number minus 1 here at the end
                           {'Chromanticore': 0} )

    def test_basic_lands_cast_multicolored_spell_success(self):
        """Five turns with starting hand of Forest, Mountain, Plains, Swamp, Island, Chromanticore. Grizzly Bears on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest', 'Mountain', 'Plains', 'Swamp', 'Island', 'Chromanticore'],['Grizzly Bears','Grizzly Bears','Grizzly Bearss','Grizzly Bearss','Grizzly Bearss','Grizzly Bearss']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Chromanticore': 1, 'Grizzly Bears': 6}),
                                      5,       # maxturns here
                                      False
                                      )[0][4], #turn number minus 1 here at the end
                           {'Chromanticore': 1} )

    def test_basic_lands_cast_multicolored_spell_still_a_success(self):
        """Six turns with starting hand of Forest, Mountain, Plains, Swamp, Island, Chromanticore. Grizzly Bears on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest', 'Mountain', 'Plains', 'Swamp', 'Island', 'Chromanticore'],['Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Chromanticore': 1, 'Grizzly Bears': 6}),
                                      6,       # maxturns here
                                      False
                                      )[0][5], #turn number minus 1 here at the end
                           {'Chromanticore': 1} )

    def test_basic_lands_on_the_draw_turn_1(self):
        """Topdeck a Forest allowing you to cast Mystic."""
        self.assertDictEqual(playHand(LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                      1,       # maxturns here
                                      True
                                      )[0][0], #turn number minus 1 here at the end
                           {'Elvish Mystic': 1} )

    def test_basic_lands_on_the_play_turn_1(self):
        """Fail to topfeck a Forest allowing you to cast Mystic because you are on the play."""
        self.assertDictEqual(playHand(LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                      1,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Elvish Mystic': 0} )
    
    def test_basic_lands_on_the_play_turn_2(self):
        """Topdeck a Forest allowing you to cast Mystic turn 2 because you are on the play."""
        self.assertDictEqual(playHand(LineOfPlay([],['Mountain', 'Plains', 'Swamp', 'Island', 'Elvish Mystic'],['Forest','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears','Grizzly Bears']),
                                      ManaBase({'Forest': 1, 'Mountain': 1, 'Plains': 1, 'Swamp': 1, 'Island': 1, 'Elvish Mystic': 1, 'Grizzly Bears': 6}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Elvish Mystic': 1} )

    def test_pain_lands_turn_1(self):
        """Painlands can tap for either of two colors on the turn you play them."""
        self.assertDictEqual(playHand(LineOfPlay([],['Battlefield Forge','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],[]),
                                      ManaBase({'Battlefield Forge': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 1}),
                                      1,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 0} )

    def test_anycolor_lands_turn_1(self):
        """Some lands can tap for any color on the turn you play them."""
        self.assertDictEqual(playHand(LineOfPlay([],['Mana Confluence','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],[]),
                                      ManaBase({'Mana Confluence': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 1}),
                                      1,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 1} )

    def test_tapped_lands_turn_1(self):
        """Some lands come into play tapped. Here we test starting with a tapped red source and an untapped white source."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wind-Scarred Crag','Plains','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],['Cloudfin Raptor']),
                                      ManaBase({'Wind-Scarred Crag': 1,'Plains': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 2}),
                                      1,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 0,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 0} )

    def test_tapped_lands_turn_2(self):
        """Some lands come into play tapped. Here we test starting with a tapped red source and an untapped white source."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wind-Scarred Crag','Plains','Frenzied Goblin','Soldier of the Pantheon','Cloudfin Raptor'],['Cloudfin Raptor','Cloudfin Raptor']),
                                      ManaBase({'Wind-Scarred Crag': 1,'Plains': 1,'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 3}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 1,'Soldier of the Pantheon': 1,'Cloudfin Raptor': 0} )

    def test_scry_land_need_to_keep_on_top(self):
        """This line of play needs to be to play the temple and keep the next card on top."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Triumph','Swamp','Wojek Halberdiers','Cloudfin Raptor'],['Plains','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor']),
                                      ManaBase({'Temple of Triumph': 1,'Swamp': 1,'Wojek Halberdiers': 1,'Plains': 1,'Cloudfin Raptor': 4}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Wojek Halberdiers': 1, 'Cloudfin Raptor': 0} )

    def test_scry_land_need_to_put_on_bottom(self):
        """This line of play needs to be to play the temple and bottom that cloudfin raptor."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Triumph','Swamp','Wojek Halberdiers','Cloudfin Raptor'],['Cloudfin Raptor','Plains','Cloudfin Raptor','Cloudfin Raptor']),
                                      ManaBase({'Temple of Triumph': 1,'Swamp': 1,'Wojek Halberdiers': 1,'Plains': 1,'Cloudfin Raptor': 4}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Wojek Halberdiers': 1, 'Cloudfin Raptor': 0} )

    def test_scry_land_doesnt_scry_2_or_backwards(self):
        """This line of play can't cast Wojek Halberdiers unless the land somehow accidentally scries twice or upside down."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Triumph','Swamp','Wojek Halberdiers','Cloudfin Raptor'],['Cloudfin Raptor','Cloudfin Raptor','Plains','Cloudfin Raptor']),
                                      ManaBase({'Temple of Triumph': 1,'Swamp': 1,'Wojek Halberdiers': 1,'Plains': 1,'Cloudfin Raptor': 4}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Wojek Halberdiers': 0, 'Cloudfin Raptor': 0} )
    
    def test_darksteel_citadel_is_in_the_manadatabase(self):
        """Just making sure we know Citadel is a land."""
        self.assertListEqual( ManaBase({'Darksteel Citadel': 1, 'Mountain': 1}).manaDatabase['Darksteel Citadel'],
                            [] )

    def test_darksteel_citadel_casts_something(self):
        """Does Citadel actually cast a one-mana spell?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Altar of the Brood'],['']),
                                      ManaBase({'Darksteel Citadel': 1,'Altar of the Brood': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Altar of the Brood': 1} )

    def test_darksteel_citadel_plays_with_others_turn_1(self):
        """Does Citadel actually cast a two-mana spell?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Heir of the Wilds', 'Forest'],['Heir of the Wilds']),
                                      ManaBase({'Darksteel Citadel': 1,'Heir of the Wilds': 2, 'Forest': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Heir of the Wilds': 0} )

    def test_darksteel_citadel_plays_with_others_turn_2(self):
        """Does Citadel actually cast a two-mana spell?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Heir of the Wilds', 'Forest'],['Heir of the Wilds']),
                                      ManaBase({'Darksteel Citadel': 1,'Heir of the Wilds': 2, 'Forest': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Heir of the Wilds': 1} )

    def test_darksteel_citadel_plays_with_rampers_turn_2(self):
        """Does Citadel actually cast a two-mana spell?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Sylvan Caryatid', 'Forest','Polukranos, World Eater'],['Forest','Forest']),
                                      ManaBase({'Darksteel Citadel': 1, 'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1, 'Forest': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Sylvan Caryatid': 1, 'Polukranos, World Eater': 0} )
    
    def test_darksteel_citadel_plays_with_rampers_turn_3(self):
        """Does Citadel actually cast a two-mana spell?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Sylvan Caryatid', 'Forest','Polukranos, World Eater'],['Forest','Forest']),
                                      ManaBase({'Darksteel Citadel': 1, 'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1, 'Forest': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1} )

    def test_darksteel_citadel_plays_with_dorks_and_rocks_turn_2(self):
        """Does Citadel play a ramp spell then also cast a 4-drop on turn 3?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Sylvan Caryatid', 'Forest','Polukranos, World Eater'],['Abzan Banner','Abzan Banner','Abzan Banner']),
                                      ManaBase({'Darksteel Citadel': 1, 'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1, 'Forest': 1, 'Abzan Banner': 3}),
                                      4,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Sylvan Caryatid': 1, 'Polukranos, World Eater': 0} )

    def test_darksteel_citadel_plays_with_dorks_and_rocks_turn_3(self):
        """Does Citadel play a ramp spell then also cast a 4-drop on turn 3?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Sylvan Caryatid', 'Forest','Polukranos, World Eater'],['Abzan Banner','Abzan Banner','Abzan Banner']),
                                      ManaBase({'Darksteel Citadel': 1, 'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1, 'Forest': 1, 'Abzan Banner': 3}),
                                      4,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {'Sylvan Caryatid': 1, 'Polukranos, World Eater': 0} )        

    def test_darksteel_citadel_plays_with_dorks_and_rocks_turn_4(self):
        """Does Citadel play a ramp spell then also cast a 4-drop on turn 3?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Darksteel Citadel','Sylvan Caryatid', 'Forest','Polukranos, World Eater'],['Abzan Banner','Abzan Banner','Abzan Banner']),
                                      ManaBase({'Darksteel Citadel': 1, 'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1, 'Forest': 2, 'Abzan Banner': 3}),
                                      4,       # maxturns here
                                      False 
                                     )[0][3], # turn number minus 1 here
                             {'Sylvan Caryatid': 1, 'Polukranos, World Eater': 1} )       

    def test_urborg_is_in_the_manadatabase(self):
        """Just making sure we know Urborg is a land."""
        self.assertListEqual( ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Mountain': 1}).manaDatabase['Urborg, Tomb of Yawgmoth'],
                            [] )

    def test_urborg_is_an_available_manasource(self):
        """Make sure that if Urborg gets played, it counts as a mana source."""
        self.assertListEqual( manaSourcesAvailable(LineOfPlay([['Urborg, Tomb of Yawgmoth']],[],[]), ManaBase({'Urborg, Tomb of Yawgmoth': 1}), 1), 
                            ['Urborg, Tomb of Yawgmoth'] )

    def test_urborg_is_a_swamp(self):
        """This line of play just makes sure Urborg taps for black."""
        self.assertDictEqual(playHand(LineOfPlay([],['Urborg, Tomb of Yawgmoth','Thoughtseize'],[]),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1,'Thoughtseize': 1}),
                                      1,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Thoughtseize': 1} )

    def test_urborg_is_not_a_mountain(self):
        """This line of play just makes sure Urborg doesn't tap for red."""
        self.assertDictEqual(playHand(LineOfPlay([],['Urborg, Tomb of Yawgmoth','Frenzied Goblin'],[]),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1,'Frenzied Goblin': 1}),
                                      1,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Frenzied Goblin': 0} )

    def test_urborg_makes_mountains_into_swamps(self):
        """This line of play just makes sure Urborg taps for black."""
        self.assertDictEqual(playHand(LineOfPlay([],['Urborg, Tomb of Yawgmoth','Mountain','Bile Blight'],['Cloudfin Raptor']),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Mountain': 1, 'Bile Blight': 1, 'Cloudfin Raptor': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Bile Blight': 1} )

    def test_urborg_doesnt_ramp(self):
        """This line of play just makes sure Urborg isn't totally broken."""
        self.assertDictEqual(playHand(LineOfPlay([],['Urborg, Tomb of Yawgmoth','Mountain','Bile Blight'],['Cloudfin Raptor']),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Mountain': 1, 'Bile Blight': 1, 'Cloudfin Raptor': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Bile Blight': 0} )

    def test_urborg_doesnt_untap_lands(self):
        """This line of play draws a tapped land turn 2, so it can't cast Bile Blight turn 2."""
        self.assertDictEqual(playHand(LineOfPlay([],['Urborg, Tomb of Yawgmoth','Bile Blight'],['Temple of Mystery']),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Temple of Mystery': 1, 'Bile Blight': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][0], #turn number minus 1 here at the end
                           {'Bile Blight': 0} )

    def test_urborg_doesnt_break_duals(self):
        """This line of play draws a Battlefield Forge turn 2, so it should be fine casting a WB spell."""
        self.assertDictEqual(playHand(LineOfPlay([],['Urborg, Tomb of Yawgmoth','Zealous Persecution'],['Battlefield Forge', 'Cloudfin Raptor']),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Zealous Persecution': 1, 'Battlefield Forge': 1, 'Cloudfin Raptor': 1}),
                                      2,       # maxturns here
                                      False
                                      )[0][1], #turn number minus 1 here at the end
                           {'Zealous Persecution': 1} )

    def test_scry_to_swamp_to_get_B(self):
        """Trying to scry to bottom three times to find Swamp for Thoughtseize."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Triumph','Temple of Triumph','Temple of Triumph','Thoughtseize','Cloudfin Raptor'],['Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Swamp']),
                                      ManaBase({'Swamp': 1, 'Temple of Triumph': 3, 'Thoughtseize': 1, 'Cloudfin Raptor': 6}),
                                      4,       # maxturns here
                                      False
                                      )[0][3], #turn number minus 1 here at the end
                           {'Thoughtseize': 1, 'Cloudfin Raptor': 0} )


    def test_scry_to_urborg_to_get_BBBB(self):
        """Trying to scry to bottom three times to cast Phyrexian Obliterator with Urborg."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Triumph','Temple of Triumph','Temple of Triumph','Phyrexian Obliterator','Cloudfin Raptor'],['Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Urborg, Tomb of Yawgmoth']),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Temple of Triumph': 3, 'Phyrexian Obliterator': 1, 'Cloudfin Raptor': 6}),
                                      4,       # maxturns here
                                      False
                                      )[0][3], #turn number minus 1 here at the end
                           {'Phyrexian Obliterator': 1, 'Cloudfin Raptor': 0} )

    def test_scry_not_enough_to_urborg_to_get_BBBB(self):
        """With one more scry, we could get there, but with two we can't get to Urborg."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Triumph','Temple of Triumph','Mountain','Phyrexian Obliterator','Cloudfin Raptor'],['Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Cloudfin Raptor','Urborg, Tomb of Yawgmoth']),
                                      ManaBase({'Urborg, Tomb of Yawgmoth': 1, 'Temple of Triumph': 2, 'Mountain': 1, 'Phyrexian Obliterator': 1, 'Cloudfin Raptor': 5}),
                                      4,       # maxturns here
                                      False
                                      )[0][3], #turn number minus 1 here at the end
                           {'Phyrexian Obliterator': 0, 'Cloudfin Raptor': 0} )

    def test_mana_dork_gets_cast(self):
        """This line of play just makes sure we cast the Elvish Mystic."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Elvish Mystic'],['Forest']),
                                      ManaBase({'Forest': 1,'Elvish Mystic': 2}),
                                      1,       # maxturns here
                                      False 
                                      )[0][0], #turn number minus 1 here at the end
                           {'Elvish Mystic': 1} )

    def test_mana_dork_gets_cast_through_playHand(self):
        """This line of play just makes sure we cast the Elvish Mystic a different way."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Elvish Mystic'],['Forest']),
                                      ManaBase({'Forest': 1,'Elvish Mystic': 2}),
                                      1,       # maxturns here
                                      False 
                                      )[0][0], # turn number minus 1 here
                           {'Elvish Mystic': 1} )

    def test_mana_dork_is_a_mana_source(self):
        """This line of play makes sure the Mystic taps for green mana."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Elvish Mystic','Strangleroot Geist'],['Strangleroot Geist']),
                                      ManaBase({'Forest': 1,'Elvish Mystic': 1, 'Strangleroot Geist': 2}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Elvish Mystic': 1, 'Strangleroot Geist': 1} )

    def test_mana_dork_isnt_hasty(self):
        """This line of play makes sure the Mystic doesn't have superhaste."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Elvish Mystic','Strangleroot Geist'],['Strangleroot Geist']),
                                      ManaBase({'Forest': 1,'Elvish Mystic': 1, 'Strangleroot Geist': 2}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Elvish Mystic': 1, 'Strangleroot Geist': 0} )

    def test_this_mana_dork_isnt_hasty_either(self):
        """This line of play makes sure off color dorks don't have haste."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Avacyn's Pilgrim",'Fleecemane Lion'],['Fleecemane Lion']),
                                      ManaBase({'Forest': 1,"Avacyn's Pilgrim": 1, 'Fleecemane Lion': 2}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Fleecemane Lion': 0} )

    def test_mana_dork_ramps_us_once(self):
        """This line of play makes sure ramping works."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Avacyn's Pilgrim",'Forest','Loxodon Smiter'],['Loxodon Smiter']),
                                      ManaBase({'Forest': 2,"Avacyn's Pilgrim": 1, 'Loxodon Smiter': 2}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Loxodon Smiter': 1} )
       
    def test_two_mana_dorks_ramp_us_twice(self):
        """This line of play makes sure ramping works."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Avacyn's Pilgrim","Avacyn's Pilgrim",'Forest','Forest','Wingmate Roc'],['Wingmate Roc','Wingmate Roc']),
                                      ManaBase({'Forest': 3,"Avacyn's Pilgrim": 1, 'Wingmate Roc': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Wingmate Roc': 1} )

    def test_not_doublecasting_two_manadorks_with_one_mana(self):
        """This line of play makes sure even if both mana dorks are possible on one, we don't cast both on one."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Avacyn's Pilgrim",'Elvish Mystic','Forest','Polukranos, World Eater'],['Polukranos, World Eater','Polukranos, World Eater']),
                                      ManaBase({'Forest': 2, "Avacyn's Pilgrim": 1, 'Elvish Mystic': 1, 'Polukranos, World Eater': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Elvish Mystic': 1, 'Polukranos, World Eater': 0} )

    def test_use_at_least_one_of_two_manadorks(self):
        """This line of play makes sure that if you have two mana dorks available, we don't get confused and not use them."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Avacyn's Pilgrim",'Elvish Mystic','Forest','Polukranos, World Eater'],['Polukranos, World Eater','Polukranos, World Eater']),
                                      ManaBase({'Forest': 2, "Avacyn's Pilgrim": 1, 'Elvish Mystic': 1, 'Polukranos, World Eater': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Elvish Mystic': 1, 'Polukranos, World Eater': 1} )

    def cast_both_manadorks_turn_2_to_ramp_twice_turn_1(self):
        """If we can drop two mana dorks turn 2 because of a tapped green source turn 1, let's do it."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Abandon','Elvish Mystic','Elvish Mystic','Polukranos, World Eater'],['Forest','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater']),
                                      ManaBase({'Forest': 1, 'Elvish Mystic': 2, 'Polukranos, World Eater': 5}),
                                      4,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Elvish Mystic': 0, 'Polukranos, World Eater': 0} )

    def cast_both_manadorks_turn_2_to_ramp_twice_turn_2(self):
        """If we can drop two mana dorks turn 2 because of a tapped green source turn 1, let's do it."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Abandon','Elvish Mystic','Elvish Mystic','Polukranos, World Eater'],['Forest','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater']),
                                      ManaBase({'Forest': 1, 'Elvish Mystic': 2, 'Polukranos, World Eater': 5}),
                                      4,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Elvish Mystic': 1, 'Polukranos, World Eater': 0} )

    def cast_both_manadorks_turn_2_to_ramp_twice_turn_3(self):
        """If we can drop two mana dorks turn 2 because of a tapped green source turn 1, let's do it."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Abandon','Elvish Mystic','Elvish Mystic','Polukranos, World Eater'],['Forest','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater']),
                                      ManaBase({'Forest': 1, 'Elvish Mystic': 2, 'Polukranos, World Eater': 5}),
                                      4,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {'Elvish Mystic': 1, 'Polukranos, World Eater': 1} )


    def cast_both_manadorks_turn_2_to_ramp_twice_turn_4(self):
        """If we can drop two mana dorks turn 2 because of a tapped green source turn 1, let's do it."""
        self.assertDictEqual(playHand(LineOfPlay([],['Temple of Abandon','Elvish Mystic','Elvish Mystic','Polukranos, World Eater'],['Forest','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater','Polukranos, World Eater']),
                                      ManaBase({'Forest': 1, 'Elvish Mystic': 2, 'Polukranos, World Eater': 5}),
                                      4,       # maxturns here
                                      False 
                                     )[0][3], # turn number minus 1 here
                             {'Elvish Mystic': 1, 'Polukranos, World Eater': 1} )

    def test_use_a_mana_rock_to_cast_a_mana_dork_that_turn_turn_2(self):
        """This line of play gets us green mana on turn 3 by casting Abzan Banner, allowing us to ramp to turn 4 Wingmate Roc."""
        self.assertDictEqual(playHand(LineOfPlay([],['Plains','Plains','Plains','Abzan Banner',"Avacyn's Pilgrim",'Wingmate Roc'],['Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc']),
                                      ManaBase({'Plains': 3, "Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 6}),
                                      5,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 0, 'Abzan Banner': 0, 'Wingmate Roc': 0} )

    def test_use_a_mana_rock_to_cast_a_mana_dork_that_turn_turn_3(self):
        """This line of play gets us green mana on turn 3 by casting Abzan Banner, allowing us to ramp to turn 4 Wingmate Roc."""
        self.assertDictEqual(playHand(LineOfPlay([],['Plains','Plains','Plains','Abzan Banner',"Avacyn's Pilgrim",'Wingmate Roc'],['Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc']),
                                      ManaBase({'Plains': 3, "Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 6}),
                                      5,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 0} )

    def test_use_a_mana_rock_to_cast_a_mana_dork_that_turn_turn_4(self):
        """This line of play gets us green mana on turn 3 by casting Abzan Banner, allowing us to ramp to turn 4 Wingmate Roc."""
        self.assertDictEqual(playHand(LineOfPlay([],['Plains','Plains','Plains','Abzan Banner',"Avacyn's Pilgrim",'Wingmate Roc'],['Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc']),
                                      ManaBase({'Plains': 3, "Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 6}),
                                      5,       # maxturns here
                                      False 
                                     )[0][3], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 1} )

    def test_use_a_mana_rock_to_cast_a_mana_dork_that_turn_turn_5(self):
        """This line of play gets us green mana on turn 3 by casting Abzan Banner, allowing us to ramp to turn 4 Wingmate Roc."""
        self.assertDictEqual(playHand(LineOfPlay([],['Plains','Plains','Plains','Abzan Banner',"Avacyn's Pilgrim",'Wingmate Roc'],['Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc','Wingmate Roc']),
                                      ManaBase({'Plains': 3, "Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 6}),
                                      5,       # maxturns here
                                      False 
                                     )[0][4], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Abzan Banner': 1, 'Wingmate Roc': 1} )

    def test_mana_rocks_dont_make_every_color_turn_4(self):
        """This line of play makes sure that Temur Banner doesn't tap for white mana."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Plains','Temur Banner','Wingmate Roc'],['Forest','Forest','Forest','Plains']),
                                      ManaBase({'Forest': 5, 'Plains': 2, 'Wingmate Roc': 1, 'Temur Banner': 1}),
                                      4,       # maxturns here
                                      False 
                                     )[0][3], # turn number minus 1 here
                             {"Temur Banner": 1, 'Wingmate Roc': 0} )

    def test_mana_rocks_dont_make_every_color_turn_5(self):
        """This line of play makes sure that even if Temur Banner is useless, it doesn't interfere with hardcasting Wingmate Roc."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Plains','Temur Banner','Wingmate Roc'],['Forest','Forest','Forest','Plains']),
                                      ManaBase({'Forest': 5, 'Plains': 2, 'Wingmate Roc': 1, 'Temur Banner': 1}),
                                      5,       # maxturns here
                                      False 
                                     )[0][4], # turn number minus 1 here
                             {"Temur Banner": 1, 'Wingmate Roc': 1} )

    def test_mana_rocks_make_some_colors_turn_3(self):
        """This line of play makes sure that Abzan Banner doesn't ramp before it should."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Plains','Abzan Banner','Wingmate Roc'],['Forest','Forest','Forest','Plains']),
                                      ManaBase({'Forest': 5, 'Plains': 2, 'Wingmate Roc': 1, 'Abzan Banner': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Abzan Banner": 1, 'Wingmate Roc': 0} )

    def test_mana_rocks_make_some_colors_turn_4(self):
        """This line of play makes sure that Abzan Banner does ramp with white mana."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Plains','Abzan Banner','Wingmate Roc'],['Forest','Forest','Forest','Plains']),
                                      ManaBase({'Forest': 5, 'Plains': 2, 'Wingmate Roc': 1, 'Abzan Banner': 1}),
                                      4,       # maxturns here
                                      False 
                                     )[0][3], # turn number minus 1 here
                             {"Abzan Banner": 1, 'Wingmate Roc': 1} )

    def test_mana_rocks_make_some_colors_turn_5(self):
        """This line of play should just hardcast Wingmate Roc no problem."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Plains','Abzan Banner','Wingmate Roc'],['Forest','Forest','Forest','Plains']),
                                      ManaBase({'Forest': 5, 'Plains': 2, 'Wingmate Roc': 1, 'Abzan Banner': 1}),
                                      5,       # maxturns here
                                      False 
                                     )[0][4], # turn number minus 1 here
                             {"Abzan Banner": 1, 'Wingmate Roc': 1} )

    def test_mana_rocks_dont_instantly_ramp_turn_2(self):
        """This line of play makes sure that Abzan Banner isn't cast yet on turn 2."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Forest','Abzan Banner','Karametra, God of Harvests', 'Polukranos, World Eater'],['Forest','Forest','Forest']),
                                      ManaBase({'Forest': 6, 'Abzan Banner': 1, 'Karametra, God of Harvests': 1, 'Polukranos, World Eater': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Abzan Banner": 0, 'Karametra, God of Harvests': 0, 'Polukranos, World Eater': 0} )

    def test_mana_rocks_dont_instantly_ramp_turn_3(self):
        """Abzan Banner is cast on 3, but we shouldn't be able to use it to cast 4-mana spells on turn 3."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Forest','Abzan Banner','Karametra, God of Harvests', 'Polukranos, World Eater'],['Forest','Forest','Forest']),
                                      ManaBase({'Forest': 6, 'Abzan Banner': 1, 'Karametra, God of Harvests': 1, 'Polukranos, World Eater': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Abzan Banner": 1, 'Karametra, God of Harvests': 0, 'Polukranos, World Eater': 0} )

    def test_mana_rocks_dont_instantly_ramp_turn_4(self):
        """Abzan BAnner being cast on 3 allows us to cast both 4- and 5-mana spells on turn 4."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Forest','Forest','Abzan Banner','Karametra, God of Harvests', 'Polukranos, World Eater'],['Forest','Forest','Forest']),
                                      ManaBase({'Forest': 6, 'Abzan Banner': 1, 'Karametra, God of Harvests': 1, 'Polukranos, World Eater': 1}),
                                      4,       # maxturns here
                                      False 
                                     )[0][3], # turn number minus 1 here
                             {"Abzan Banner": 1, 'Karametra, God of Harvests': 1, 'Polukranos, World Eater': 1} )

    def test_two_mana_dorks_ramp_us_twice(self):
        """If you have two Pilgrims, you should be able to cast 5-mana spells on turn 3."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Avacyn's Pilgrim","Avacyn's Pilgrim",'Forest','Forest','Wingmate Roc'],['Wingmate Roc','Wingmate Roc']),
                                      ManaBase({'Forest': 3,"Avacyn's Pilgrim": 1, 'Wingmate Roc': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Avacyn's Pilgrim": 1, 'Wingmate Roc': 1} )

    def test_noble_hierarch_taps_for_three_colors_turn_1(self):
        """Noble Hierarch is castable with a Forest, but the others aren't."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Noble Hierarch","Thoughtseize",'Strangleroot Geist','Frenzied Goblin','Cloudfin Raptor','Silence'],['Silence']),
                                      ManaBase({'Darksteel Citadel': 1,"Noble Hierarch": 1,"Thoughtseize": 1,'Strangleroot Geist': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 2}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {"Noble Hierarch": 1,"Thoughtseize": 0,'Strangleroot Geist': 0,'Frenzied Goblin': 0,'Cloudfin Raptor': 0,'Silence': 0} )

    def test_noble_hierarch_taps_for_three_colors_turn_2(self):
        """Noble Hierarch should tap for three colors, casting three of these spells."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest',"Noble Hierarch","Thoughtseize",'Strangleroot Geist','Frenzied Goblin','Cloudfin Raptor','Silence'],['Silence']),
                                      ManaBase({'Forest': 1,"Noble Hierarch": 1,"Thoughtseize": 1,'Strangleroot Geist': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 2}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Noble Hierarch": 1,"Thoughtseize": 0,'Strangleroot Geist': 1,'Frenzied Goblin': 0,'Cloudfin Raptor': 1,'Silence': 1} )

    def test_sylvan_caryatid_taps_for_any_color_turn_2(self):
        """Sylvan Caryatid should allow all the spells here except Polukranos to be cast."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Plains',"Sylvan Caryatid","Thoughtseize",'Boon Satyr','Frenzied Goblin','Cloudfin Raptor','Silence', 'Polukranos, World Eater'],['Silence','Silence']),
                                      ManaBase({'Plains': 1, 'Forest': 1, "Sylvan Caryatid": 1,"Thoughtseize": 1,'Boon Satyr': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 3, 'Polukranos, World Eater': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Sylvan Caryatid": 1,"Thoughtseize": 0,'Boon Satyr': 0,'Frenzied Goblin': 0,'Cloudfin Raptor': 0,'Silence': 1, 'Polukranos, World Eater': 0} )

    def test_sylvan_caryatid_taps_for_any_color_turn_3(self):
        """Sylvan Caryatid should allow all the spells here except Polukranos to be cast."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Plains',"Sylvan Caryatid","Thoughtseize",'Boon Satyr','Frenzied Goblin','Cloudfin Raptor','Silence', 'Polukranos, World Eater'],['Silence','Silence']),
                                      ManaBase({'Plains': 1, 'Forest': 1, "Sylvan Caryatid": 1,"Thoughtseize": 1,'Boon Satyr': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 3, 'Polukranos, World Eater': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Sylvan Caryatid": 1,"Thoughtseize": 1,'Boon Satyr': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 1, 'Polukranos, World Eater': 0} )

    def test_sylvan_caryatid_and_citadel_taps_for_any_color_turn_2(self):
        """Sylvan Caryatid should allow all the spells here except Polukranos to be cast."""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Darksteel Citadel',"Sylvan Caryatid","Thoughtseize",'Boon Satyr','Frenzied Goblin','Cloudfin Raptor','Silence', 'Polukranos, World Eater'],['Silence','Silence']),
                                      ManaBase({'Darksteel Citadel': 1, 'Forest': 1, "Sylvan Caryatid": 1,"Thoughtseize": 1,'Boon Satyr': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 3, 'Polukranos, World Eater': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {"Sylvan Caryatid": 1,"Thoughtseize": 0,'Boon Satyr': 0,'Frenzied Goblin': 0,'Cloudfin Raptor': 0,'Silence': 0, 'Polukranos, World Eater': 0} )

    def test_sylvan_caryatid_and_citadel_taps_for_any_color_turn_3(self):
        """Does Sylvan Caryatid work for any color if you have a Citadel?"""
        self.assertDictEqual(playHand(LineOfPlay([],['Forest','Darksteel Citadel',"Sylvan Caryatid","Thoughtseize",'Boon Satyr','Frenzied Goblin','Cloudfin Raptor','Silence', 'Polukranos, World Eater'],['Silence','Silence']),
                                      ManaBase({'Darksteel Citadel': 1, 'Forest': 1, "Sylvan Caryatid": 1,"Thoughtseize": 1,'Boon Satyr': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 3, 'Polukranos, World Eater': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {"Sylvan Caryatid": 1,"Thoughtseize": 1,'Boon Satyr': 1,'Frenzied Goblin': 1,'Cloudfin Raptor': 1,'Silence': 1, 'Polukranos, World Eater': 0} )

    def test_chained_to_the_rocks_is_not_a_one_drop(self):
        """You can't cast Chained to the rocks on turn one with a plains or a battlefield forge, but you can after drawing the mountain."""
        self.assertDictEqual(playHand(LineOfPlay([],['Plains','Battlefield Forge','Chained to the Rocks'],['Mountain']),
                                      ManaBase({'Plains': 1, 'Battlefield Forge': 1, 'Chained to the Rocks': 1, 'Mountain' : 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Chained to the Rocks': 0} )

    def test_chained_to_the_rocks_is_a_two_drop(self):
        """You can't cast Chained to the rocks on turn one with a plains or a battlefield forge, but you can after drawing the mountain."""
        self.assertDictEqual(playHand(LineOfPlay([],['Plains','Battlefield Forge','Chained to the Rocks'],['Mountain']),
                                      ManaBase({'Plains': 1, 'Battlefield Forge': 1, 'Chained to the Rocks': 1, 'Mountain' : 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Chained to the Rocks': 1} )

    def test_chained_to_the_rocks_is_a_one_drop_with_foundry(self):
        """If your untapped mountain produces white, you can cast Chained turn 1. :)"""
        self.assertDictEqual(playHand(LineOfPlay([],['Sacred Foundry','Battlefield Forge','Chained to the Rocks'],['Mountain']),
                                      ManaBase({'Sacred Foundry': 1, 'Battlefield Forge': 1, 'Chained to the Rocks': 1, 'Mountain' : 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Chained to the Rocks': 1} )

    def test_fetching_to_chain_to_the_rocks_part_1(self):
        """You can fetch for a Sacred Foundry to cast Chained to the Rocks turn 1. :)"""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Chained to the Rocks'],['Island','Mountain','Plains','Sacred Foundry','Plains','Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Chained to the Rocks': 1,'Island': 1,'Mountain': 2,'Plains': 2,'Sacred Foundry': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Chained to the Rocks': 1} )

    def test_fetching_to_chain_to_the_rocks_part_2(self):
        """You can fetch for a Sacred Foundry to cast Chained to the Rocks turn 1... but not with Polluted Delta."""
        self.assertDictEqual(playHand(LineOfPlay([],['Polluted Delta','Chained to the Rocks'],['Island','Mountain','Plains','Sacred Foundry','Plains','Mountain']),
                                      ManaBase({'Polluted Delta': 1,'Chained to the Rocks': 1,'Island': 1,'Mountain': 2,'Plains': 2,'Sacred Foundry': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Chained to the Rocks': 0} )

    def test_fetching_to_chain_to_the_rocks_part_3_turn_1(self):
        """You can fetch for a mountain using a non-mountain-fetcher if your lands are right."""
        self.assertDictEqual(playHand(LineOfPlay([],['Windswept Heath','Plains','Chained to the Rocks'],['Island','Mountain','Plains','Stomping Ground','Mountain']),
                                      ManaBase({'Windswept Heath': 1,'Chained to the Rocks': 1,'Island': 1,'Mountain': 2,'Plains': 2,'Stomping Ground': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Chained to the Rocks': 0} )

    def test_fetching_to_chain_to_the_rocks_part_3_turn_2(self):
        """You can fetch for a mountain using a non-mountain-fetcher if your lands are right."""
        self.assertDictEqual(playHand(LineOfPlay([],['Windswept Heath','Plains','Chained to the Rocks'],['Island','Mountain','Plains','Stomping Ground','Mountain']),
                                      ManaBase({'Windswept Heath': 1,'Chained to the Rocks': 1,'Island': 1,'Mountain': 2,'Plains': 2,'Stomping Ground': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Chained to the Rocks': 1} )

    def test_fetching_fails_if_no_basics_are_left_part_1(self):
        """If the only thing in the deck is a mountain, you can only get red."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Thoughtseize','Frenzied Goblin','Charging Badger','Silence','Cloudfin Raptor'],['Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Thoughtseize': 1,'Frenzied Goblin': 1,'Charging Badger': 1,'Silence': 1,'Cloudfin Raptor': 1,'Mountain': 1,'Forest': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Thoughtseize': 0,'Frenzied Goblin': 1,'Charging Badger': 0,'Silence': 0,'Cloudfin Raptor': 0} )

    def test_fetching_fails_if_no_basics_are_left_part_2(self):
        """If the only thing in the deck is a forest, you can only get green."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Thoughtseize','Frenzied Goblin','Charging Badger','Silence','Cloudfin Raptor'],['Forest']),
                                      ManaBase({'Wooded Foothills': 1,'Thoughtseize': 1,'Frenzied Goblin': 1,'Charging Badger': 1,'Silence': 1,'Cloudfin Raptor': 1,'Mountain': 1,'Forest': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Thoughtseize': 0,'Frenzied Goblin': 0,'Charging Badger': 1,'Silence': 0,'Cloudfin Raptor': 0} )

    def test_fetching_fails_if_no_basics_are_left_part_3(self):
        """If the deck is empty, fetching fails. :)"""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Thoughtseize','Frenzied Goblin','Charging Badger','Silence','Cloudfin Raptor'],[]),
                                      ManaBase({'Wooded Foothills': 1,'Thoughtseize': 1,'Frenzied Goblin': 1,'Charging Badger': 1,'Silence': 1,'Cloudfin Raptor': 1,'Mountain': 1,'Forest': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Thoughtseize': 0,'Frenzied Goblin': 0,'Charging Badger': 0,'Silence': 0,'Cloudfin Raptor': 0} )

    def test_fetching_fails_if_no_basics_are_left_part_4(self):
        """If the deck is empty, fetching fails. :)"""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Thoughtseize','Frenzied Goblin','Charging Badger','Silence','Cloudfin Raptor'],['Island']),
                                      ManaBase({'Wooded Foothills': 1,'Thoughtseize': 1,'Frenzied Goblin': 1,'Charging Badger': 1,'Silence': 1,'Cloudfin Raptor': 1,'Mountain': 1,'Forest': 1}),
                                      1,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Thoughtseize': 0,'Frenzied Goblin': 0,'Charging Badger': 0,'Silence': 0,'Cloudfin Raptor': 0} )

    def test_fetching_succeeds_along_with_scrying_turn_1(self):
        """Here we set up a situation where we need to scry a card to the bottom and then fetch the card we scried."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Temple of Triumph','Wojek Halberdiers'],['Mountain','Island','Island','Island','Island','Island']),
                                      ManaBase({'Wooded Foothills': 1,'Temple of Triumph': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 5}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Wojek Halberdiers': 0} )

    def test_fetching_succeeds_along_with_scrying_turn_2(self):
        """Here we set up a situation where we need to scry a card to the bottom and then fetch the card we scried."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Temple of Triumph','Wojek Halberdiers'],['Mountain','Island','Island','Island','Island','Island']),
                                      ManaBase({'Wooded Foothills': 1,'Temple of Triumph': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 5}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Wojek Halberdiers': 1} )

    def test_fetching_does_not_affect_topdecks_if_possible_turn_1(self):
        """Here we fetch for a Mountain when scrying away the top Mountain would be good; fetchlands are not like that, so we should fail to cast until turn 3."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Wojek Halberdiers'],['Mountain','Plains','Island','Island','Island','Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Plains': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Wojek Halberdiers': 0} )

    def test_fetching_does_not_affect_topdecks_if_possible_turn_2(self):
        """Here we fetch for a Mountain when scrying away the top Mountain would be good; fetchlands are not like that, so we should fail to cast until turn 3."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Wojek Halberdiers'],['Mountain','Plains','Island','Island','Island','Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Plains': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Wojek Halberdiers': 0} )

    def test_fetching_does_not_affect_topdecks_if_possible_turn_3(self):
        """Here we fetch for a Mountain when scrying away the top Mountain would be good; fetchlands are not like that, so we should fail to cast until turn 3."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Wojek Halberdiers'],['Mountain','Plains','Island','Island','Island','Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Plains': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {'Wojek Halberdiers': 1} )

    def test_fetching_affects_topdecks_if_no_other_choice_turn_1(self):
        """Here we fetch for a Mountain when scrying away the top Mountain would be good; fetchlands have no way out if there aren't other targets."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Wojek Halberdiers'],['Mountain','Plains','Island','Island','Island']),
                                      ManaBase({'Wooded Foothills': 1,'Plains': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Wojek Halberdiers': 0} )

    def test_fetching_affects_topdecks_if_no_other_choice_turn_2(self):
        """Here we fetch for a Mountain when scrying away the top Mountain would be good; fetchlands have no way out if there aren't other targets."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Wojek Halberdiers'],['Mountain','Plains','Island','Island','Island']),
                                      ManaBase({'Wooded Foothills': 1,'Plains': 1,'Wojek Halberdiers': 1,'Mountain': 1,'Island': 3}),
                                      3,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Wojek Halberdiers': 1} )

    def test_fetching_for_a_forest_to_ramp_us_turn_1(self):
        """Even though it is possible to fetch for R to cast a 2-drop, we want to realize it was also possible to fetch for G to cast the Caryatid to ramp us."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Elvish Mystic','Frenzied Goblin','Fanatic of Xenagos'],['Island','Island','Island','Forest','Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1,'Island': 3,'Forest': 1,'Mountain': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 0} )

    def test_fetching_for_a_forest_to_ramp_us_turn_2(self):
        """Even though it is possible to fetch for R to cast a 2-drop, we want to realize it was also possible to fetch for G to cast the Caryatid to ramp us."""
        self.assertDictEqual(playHand(LineOfPlay([],['Wooded Foothills','Elvish Mystic','Frenzied Goblin','Fanatic of Xenagos'],['Mountain','Island','Island','Forest','Mountain']),
                                      ManaBase({'Wooded Foothills': 1,'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1,'Island': 3,'Forest': 1,'Mountain': 1}),
                                      2,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1} )

    def test_evolving_wilds_isnt_an_untapped_source_turn_1(self):
        """Evolving Wilds can find anything, but not a turn 1 play."""
        self.assertDictEqual(playHand(LineOfPlay([],['Evolving Wilds','Elvish Mystic','Frenzied Goblin','Fanatic of Xenagos', 'Polukranos, World Eater'],['Mountain','Island','Island','Forest','Mountain']),
                                      ManaBase({'Evolving Wilds': 1,'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1,'Island': 3,'Forest': 1,'Mountain': 1, 'Polukranos, World Eater': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][0], # turn number minus 1 here
                             {'Elvish Mystic': 0,'Frenzied Goblin': 0,'Fanatic of Xenagos': 0, 'Polukranos, World Eater': 0} )

    def test_evolving_wilds_isnt_an_untapped_source_turn_2(self):
        """Evolving Wilds can find anything, but not a turn 1 play."""
        self.assertDictEqual(playHand(LineOfPlay([],['Evolving Wilds','Elvish Mystic','Frenzied Goblin','Fanatic of Xenagos', 'Polukranos, World Eater'],['Mountain','Island','Island','Forest','Mountain']),
                                      ManaBase({'Evolving Wilds': 1,'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1,'Island': 3,'Forest': 1,'Mountain': 1, 'Polukranos, World Eater': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][1], # turn number minus 1 here
                             {'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 0, 'Polukranos, World Eater': 0} )

    def test_evolving_wilds_isnt_an_untapped_source_turn_3(self):
        """Evolving Wilds can find anything, but not a turn 1 play."""
        self.assertDictEqual(playHand(LineOfPlay([],['Evolving Wilds','Elvish Mystic','Frenzied Goblin','Fanatic of Xenagos', 'Polukranos, World Eater'],['Mountain','Island','Island','Forest','Mountain']),
                                      ManaBase({'Evolving Wilds': 1,'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1,'Island': 3,'Forest': 1,'Mountain': 1, 'Polukranos, World Eater': 1}),
                                      3,       # maxturns here
                                      False 
                                     )[0][2], # turn number minus 1 here
                             {'Elvish Mystic': 1,'Frenzied Goblin': 1,'Fanatic of Xenagos': 1, 'Polukranos, World Eater': 1} )

if __name__ == '__main__':
    unittest.main()