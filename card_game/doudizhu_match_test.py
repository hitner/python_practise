import card
import doudizhu_match
import unittest

def test1():
    deal_str = "d0c0h0s2"
    deal_bins = card.bin_card_from_terminal_string(deal_str)
    ret = doudizhu_match.check_valuable_play(deal_bins)
    print(ret)
    assert ret

    deal_str2 = "dAhAsA!W"
    deal_bins2 = card.bin_card_from_terminal_string(deal_str2)
    ret2 = doudizhu_match.check_valuable_play(deal_bins2, ret)
    print(ret2.pattern)
    assert ret2


def test2():
    deal_str = "d3h4h5h6c7c8"
    deal_bins = card.bin_card_from_terminal_string(deal_str)
    ret = doudizhu_match.check_valuable_play(deal_bins)
    print(ret)
    assert ret

    deal_str2 = "!V!W"
    deal_bins2 = card.bin_card_from_terminal_string(deal_str2)
    ret2 = doudizhu_match.check_valuable_play(deal_bins2, ret)
    print(ret2.pattern)
    assert ret2


test1()

test2()




print(doudizhu_match._patterns_all)


class DoudizhuTest(unittest.TestCase):
    """每个牌型检查的test"""
    def test_single(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('cJ'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 101)
        self.assertEqual(ret.weight, 11)

        ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('s2'), ret)
        self.assertTrue(ret2)
        self.assertEqual(ret2.pattern, 101)
        self.assertEqual(ret2.weight, doudizhu_match.MIN3_2)

        ret3 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('c6'), ret)
        self.assertIsNone(ret3)

        ret4 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('h8c8'), ret)
        self.assertIsNone(ret4)

        ret5 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('hJsJcJdJdQhQsQcQ'), ret)
        self.assertTrue(ret5)
        self.assertEqual(ret5.pattern, 8)
        self.assertEqual(ret5.weight, card._color_char_to_bin_map['J'])

    def test_single_straight(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('c6c7c8c9c0cJcQdK'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 108)
        self.assertEqual(ret.weight, 6)

        ret1 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('c7c8c9c0cJcQcKcA'), ret)
        self.assertTrue(ret1)
        self.assertEqual(ret1.pattern, 108)
        self.assertEqual(ret1.weight, 7)

        ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('d8d9d0dJsQdKdA'), ret)
        self.assertIsNone(ret2)

    def test_single_straight2(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('s3s4s5s6s7s8s9s0sJsQsKsA'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 112)
        self.assertEqual(ret.weight, 3)

    def test_single_straight3(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('s3h4c5d6'))
        self.assertIsNone(ret)

    """
        def test_single_straight4(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('23666VW'))
            ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('0JQKA2'))
            self.assertIsNone(ret)
            self.assertIsNone(ret2)
    
        def test_pair(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('KK'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 202)
            self.assertEqual(ret.weight, 13)
    
        def test_pair2(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('2V'))
            self.assertIsNone(ret)
    
        def test_pair_straight(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('9900JJ'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 206)
            self.assertEqual(ret.weight, 9)
    
        def test_pair_straight2(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('9900JJ55667788QQKKAA'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 220)
            self.assertEqual(ret.weight, 5)
    
        def test_pair_straight3(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('KKAA22'))
            self.assertIsNone(ret)
    
        def test_triple(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('222'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 303)
            self.assertEqual(ret.weight, poker.MIN3_2)
    
            ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('333'), ret)
            self.assertIsNone(ret2)
    
        def test_triple2(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('AAA222'))
            self.assertIsNone(ret)
    
        def test_triple_single(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('9666777888KK'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 412)
            self.assertEqual(ret.weight, 6)
    
            ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('JJJQQQKKKAAA'), ret)
            self.assertIsNone(ret2)
    
        def test_triple_pair(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('AA33344422'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 510)
            self.assertEqual(ret.weight, 3)
    
        def test_triple_pair2(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('000VW'))
            self.assertIsNone(ret)
    
        def test_four_two(self):
            ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('JJJJVW'))
            self.assertTrue(ret)
            self.assertEqual(ret.pattern, 606)
            self.assertEqual(ret.weight, 11)
    
            ret1 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('222200'), ret)
            self.assertTrue(ret1)
            self.assertEqual(ret1.pattern, 606)
            self.assertEqual(ret1.weight, poker.MIN3_2)
    """

    def test_four_two2(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('s5s5s5s5s6s6s6s6sQsQsQc7'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 612)
        self.assertEqual(ret.weight, 5)

        ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('!W'), ret)
        self.assertIsNone(ret2)

    def test_four_two3(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('!Wc6c6c6c2c2'))
        self.assertIsNone(ret)

    def test_grand_bomb(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('!V!W'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 2)

        ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('s2s2s2s2'), ret)
        self.assertIsNone(ret2)

    def test_bombs(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('dAdAdAdA'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 4)
        self.assertEqual(ret.weight, 14)

        ret2 = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('d3d3d3d3d4d4d4d4d5d5d5d5'), ret)
        self.assertTrue(ret2)
        self.assertEqual(ret2.pattern, 12)
        self.assertEqual(ret2.weight, 3)

    def test_bombs2(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('s7h7c7c7c8c8c8c8'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 8)
        self.assertEqual(ret.weight, 7)

    def test_bombs3(self):
        ret = doudizhu_match.check_valuable_play(card.bin_card_from_terminal_string('sAsAsAsAs2s2s2s2'))
        self.assertIsNone(ret)




if __name__ == '__main__':
    unittest.main()

