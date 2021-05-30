import sys
import unittest

sys.path.append("../")
from codeVF.hand import Hand
from codeVF.deck import Deck
from codeVF.tile import Tile
from codeVF.player import Player

class TestEntities(unittest.TestCase):

    def testPlayer(self):
        test = AI("Minimax")
        self.assertIsInstance(test, Player)        
        test.name = "moi"
        self.assertNotNone(test.name)
        self.assertIsTrue(test.is_ai)

    def testTile(self):
        t = Tile(1,5)
        self.assertIsInstance(t, Tile)
        self.assertIsInstance(t.value1, int)
        self.assertIsInstance(t.value2, int)
        self.assertGreaterEqual(t.value1, 0)
        self.assertLessEqual(t.value1, 6)
        self.assertGreaterEqual(t.value2, 0)
        self.assertLessEqual(t.value2, 6)

    def testDeck(self):
        d = Deck()
        self.assertIsInstance(d, Deck)
        d.add_predefined(6)
        self.assertIsNotNone(d)
        for t in d:
            self.assertIsInstance(t, Tile)
   
    def testCreateHand(self):
        d = Deck()
        h = Hand()
        self.assertIsInstance(h, Hand)
        h.create_from_deck(d,3, False)
        self.assertIsNoteNone(h)

if __name__ == '__main__':
    unittest.main()
