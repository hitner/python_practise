import shengji_core_foundation
import card
import unittest



class ShengjiCoreFoundationTest(unittest.TestCase):
    """每个牌型检查的test"""
    def test_single(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('cJ'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 101)
        self.assertEqual(ret.weight, 11)


if __name__ == '__main__':
    unittest.main()