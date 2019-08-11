import doudizhu
import poker
import unittest

print(doudizhu._patterns_all)


class DoudizhuTest(unittest.TestCase):
    """每个牌型检查的test"""
    def test_single(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('J'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 101)
        self.assertEqual(ret.weight, 11)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('2'), ret)
        self.assertTrue(ret2)
        self.assertEqual(ret2.pattern, 101)
        self.assertEqual(ret2.weight, poker.MIN3['2'])

        ret3 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('6'), ret)
        self.assertIsNone(ret3)

        ret4 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('88'), ret)
        self.assertIsNone(ret4)

        ret5 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('JJJJQQQQ'), ret)
        self.assertTrue(ret5)
        self.assertEqual(ret5.pattern, 8)
        self.assertEqual(ret5.weight, poker.MIN3['J'])

    def test_single_straight(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('67890JQK'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 108)
        self.assertEqual(ret.weight, 6)

        ret1 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('7890JQKA'), ret)
        self.assertTrue(ret1)
        self.assertEqual(ret1.pattern, 108)
        self.assertEqual(ret1.weight, 7)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('890JQKA'), ret)
        self.assertIsNone(ret2)

    def test_single_straight2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('34567890JQKA'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 112)
        self.assertEqual(ret.weight, 3)

    def test_single_straight3(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('3456'))
        self.assertIsNone(ret)

    def test_single_straight4(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('23666VW'))
        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('0JQKA2'))
        self.assertIsNone(ret)
        self.assertIsNone(ret2)

    def test_pair(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('KK'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 202)
        self.assertEqual(ret.weight, 13)

    def test_pair2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('2V'))
        self.assertIsNone(ret)

    def test_pair_straight(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('9900JJ'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 206)
        self.assertEqual(ret.weight, 9)

    def test_pair_straight2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('9900JJ55667788QQKKAA'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 220)
        self.assertEqual(ret.weight, 5)

    def test_pair_straight3(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('KKAA22'))
        self.assertIsNone(ret)

    def test_triple(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('222'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 303)
        self.assertEqual(ret.weight, poker.MIN3_2)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('333'), ret)
        self.assertIsNone(ret2)

    def test_triple2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('AAA222'))
        self.assertIsNone(ret)

    def test_triple_single(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('9666777888KK'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 412)
        self.assertEqual(ret.weight, 6)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('JJJQQQKKKAAA'), ret)
        self.assertIsNone(ret2)

    def test_triple_pair(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('AA33344422'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 510)
        self.assertEqual(ret.weight, 3)

    def test_triple_pair2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('000VW'))
        self.assertIsNone(ret)

    def test_four_two(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('JJJJVW'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 606)
        self.assertEqual(ret.weight, 11)

        ret1 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('222200'), ret)
        self.assertTrue(ret1)
        self.assertEqual(ret1.pattern, 606)
        self.assertEqual(ret1.weight, poker.MIN3_2)

    def test_four_two2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('55556666QQQ7'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 612)
        self.assertEqual(ret.weight, 5)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('W'), ret)
        self.assertIsNone(ret2)

    def test_four_two3(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('W66622'))
        self.assertIsNone(ret)

    def test_grand_bomb(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('VW'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 2)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('2222'), ret)
        self.assertIsNone(ret2)

    def test_bombs(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('AAAA'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 4)
        self.assertEqual(ret.weight, 14)

        ret2 = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('333344445555'), ret)
        self.assertTrue(ret2)
        self.assertEqual(ret2.pattern, 12)
        self.assertEqual(ret2.weight, 3)

    def test_bombs2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('77778888'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 8)
        self.assertEqual(ret.weight, 7)

    def test_bombs3(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('AAAA2222'))
        self.assertIsNone(ret)



if __name__ == '__main__':
    unittest.main()

