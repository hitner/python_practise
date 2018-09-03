import doudizhu
import poker
import unittest

print(doudizhu.patterns_all)


class DoudizhuTest(unittest.TestCase):
    """每个牌型检查的test"""
    def test_single(self):
        ret = doudizhu._check_single(poker.min3_from_monocolor_visual('J'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 101)
        self.assertEqual(ret.weight, 11)

    def test_single_straight(self):
        ret = doudizhu._check_all_possible(poker.min3_from_monocolor_visual('67890JQK'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 108)
        self.assertEqual(ret.weight, 6)

    def test_single_straight2(self):
        ret = doudizhu.check_value_deal(poker.min3_from_monocolor_visual('34567890JQKA'))
        self.assertTrue(ret)
        self.assertEqual(ret.pattern, 112)
        self.assertEqual(ret.weight, 3)

    def test_single_straight3(self):
        ret = doudizhu._check_all_possible(poker.min3_from_monocolor_visual('3456'))
        self.assertIsNone(ret)

    def test_single_straight4(self):
        ret = doudizhu._check_all_possible(poker.min3_from_monocolor_visual('23666VW'))
        ret2 = doudizhu._check_all_possible(poker.min3_from_monocolor_visual('34VW'))
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


if __name__ == '__main__':
    unittest.main()

