import shengji_core_foundation
from shengji_core_foundation import Pattern, first_play, follow_play
import card
import unittest

cs = card.bin_card_from_terminal_string

def print_a_match(trump_card):
    origins = list(card.DOUBLE_DECK)
    card.fisher_yates_shuffle(origins)
    bottom = shengji_core_foundation.sort_by_shengji(origins[0:8],trump_card)
    print(card.bin_card_to_terminal_input(bottom))
    players = []
    for i in range(0,4):
        hands = shengji_core_foundation.sort_by_shengji(origins[8+i:108:4], trump_card)
        print(card.bin_card_to_terminal_input(hands))
        print(card.bin_card_to_terminal_output(hands))
        players.append(hands)

"""
d4sQh6h6cAc7c3dJ

!W!Vc4h4sAsQs8s8s6s5s3hKh0h3cKc9c8c2dQd0d0d9d8d8d5
!W!V♣4♥4♠A♠Q♠8♠8♠6♠5♠3♥K♥0♥3♣K♣9♣8♣2♦Q♦0♦0♦9♦8♦8♦5

c4d4s0s9s3s2hKhQh9h5h3h2cAcQcJcJc0c7c6c3d7d7d6d5d3
♣4♦4♠0♠9♠3♠2♥K♥Q♥9♥5♥3♥2♣A♣Q♣J♣J♣0♣7♣6♣3♦7♦7♦6♦5♦3

!Vs4sJsJs7s7s6s2hAhQhJhJh8h7h5cQc0c6c5dKdQdJd9d6d2
!V♠4♠J♠J♠7♠7♠6♠2♥A♥Q♥J♥J♥8♥7♥5♣Q♣0♣6♣5♦K♦Q♦J♦9♦6♦2

!Ws4h4sAsKsKs0s9s5hAh0h9h8h7h2cKc9c8c5c2dAdAdKd3d2
!W♠4♥4♠A♠K♠K♠0♠9♠5♥A♥0♥9♥8♥7♥2♣K♣9♣8♣5♣2♦A♦A♦K♦3♦2

"""

class ShengjiCoreFoundationTest(unittest.TestCase):
    """每个牌型检查的test"""
    trump_card = cs('s4')[0]
    player_str = ['!W!Wc4h4sAsQs8s8s6s5s3hKh0h3cKc9c8c2dAd0d0d9d9d8d8d5',
        'c4d4s0s9s3s2hKhQh9h5h3h2cAcQcJcJc0c7c6c3d7d7d6d5d3',
        '!Vs4sJsJs7s7s6s2hAhQhJhJh8h7h5cQc0c6c5dKdQdJd6d2',
        '!Vs4h4sAsKsKs0s9s5hAh0h9h8h7h2cKc9c8c5c2dKdQd3d2']
    players = []
    for i in range(0,4):
        hands = cs(player_str[i])
        players.append(hands)
    bottoms = cs('d4sQh6h6cAc7c3dJ')




    def test_single_weight(self):
        ret = shengji_core_foundation._weight_of_single(cs('sQ')[0], self.trump_card)
        self.assertEqual(ret, 12)

        ret = shengji_core_foundation._weight_of_single(cs('!V')[0], self.trump_card)
        self.assertEqual(ret, card.BLACK_JOKER)

        ret = shengji_core_foundation._weight_of_single(cs('c4')[0], self.trump_card)
        self.assertEqual(ret, 15)

        ret = shengji_core_foundation._weight_of_single(cs('s4')[0], self.trump_card)
        self.assertEqual(ret, 16) 

    def test_check_pair_straight(self):
        ret = shengji_core_foundation._check_pair_straight(cs("h9h9h8h8"), self.trump_card)
        self.assertIsNotNone(ret)
        self.assertEqual(ret.pattern, Pattern.PAIR_STRAIGHT)
        self.assertEqual(ret.weight, 409)

        ret = shengji_core_foundation._check_pair_straight(cs("!W!W!V!Vs4s4"), self.trump_card)
        self.assertIsNotNone(ret)
        self.assertEqual(ret.pattern, Pattern.PAIR_STRAIGHT)
        self.assertEqual(ret.weight, 618) 

        ret = shengji_core_foundation._check_pair_straight(cs("c4c4sAsA"), self.trump_card)
        self.assertIsNotNone(ret)
        self.assertEqual(ret.pattern, Pattern.PAIR_STRAIGHT)
        self.assertEqual(ret.weight, 415) 

        ret = shengji_core_foundation._check_pair_straight(cs("c6c6c5c5c3c3c2c2"), self.trump_card)
        self.assertIsNotNone(ret)
        self.assertEqual(ret.pattern, Pattern.PAIR_STRAIGHT)
        self.assertEqual(ret.weight, 806) 

    def test_check_bucket(self):
        check_bucket_str = ['!W!Vs4c4h4sAsQs8s8s6s5s3hKh0h3cKcKcQc9c8c2dAdQd0d0d9d9d8d8d5',
            'c4d4s0s9s3s2hKhQh9h5h3h2c7c6c3d7d7d6d5d3',
            'sJsJs7s7s6s2hAhQhJhJh8h7h5c6c5dKdQdJd6d2',
            'h4sAsKsKs0s9s5hAh0h9h8h7h2dAdKd3d2']
        bucket_hands = []
        for i in range(0,4):
            bucket_hands.append(cs(check_bucket_str[i]))

        def check_bucket(cards_str) :
            cards = cs(cards_str)
            return shengji_core_foundation._check_bucket(cards,bucket_hands,0,self.trump_card)
        def is_valid_bucket(cards_str) -> bool:
            cd = check_bucket(cards_str)
            return cd.pattern == Pattern.BUCKET
    
        self.assertTrue(is_valid_bucket('cKcKcQc9'))
        self.assertTrue(is_valid_bucket('dAd9d9d8d8'))
        self.assertTrue(is_valid_bucket('!W!Vs4c4h4'))

        cd = check_bucket('dQd0d0d9d9d8d8')
        self.assertTrue(cd.pattern == Pattern.FAIL_TO_BUCKET)
        self.assertListEqual(cd.origin_cards, list(cs('dQ')))

        cd = check_bucket('!W!Vs4c4h4s8s8')
        self.assertEqual(cd.pattern, Pattern.FAIL_TO_BUCKET)
        self.assertListEqual(cd.origin_cards, list(cs('s8s8')))

        cd = check_bucket('h4sAs8s8s6')
        self.assertEqual(cd.pattern, Pattern.FAIL_TO_BUCKET)
        self.assertListEqual(cd.origin_cards, list(cs('s6')))


    def _first_play(self, card_str):
        return first_play(cs(card_str),self.players, 0, self.trump_card)

    def test_first_play(self):
        

        ret = self._first_play("s8s8")
        self.assertEqual(ret.pattern, Pattern.PAIR)
        self.assertEqual(ret.weight, 8) 

        ret = self._first_play("!W")
        self.assertEqual(ret.pattern, Pattern.SINGLE)

        ret = self._first_play("s8c8")
        self.assertIsNone(ret)

        ret = self._first_play("d0d0d9d9d8d8")
        self.assertEqual(ret.pattern, Pattern.PAIR_STRAIGHT)

        ret = self._first_play("dAd0d0d9d9d8d8")
        self.assertEqual(ret.pattern, Pattern.BUCKET)

        ret = self._first_play("dAdQd0d0d8d8")
        self.assertEqual(ret.pattern, Pattern.FAIL_TO_BUCKET)


    def _index1_follow(self, first_str, follow_str):
        """固定是第一个人的跟牌"""
        first_cd = self._first_play(first_str)
        return shengji_core_foundation.follow_play(cs(follow_str),first_cd, \
             self.players[1], self.trump_card)

    def _custom_follow(self, first_str, follow_str, custom_hands):
        """自定义的手牌跟牌，用于测试一些特殊情况"""
        first_cd = self._first_play(first_str)
        return shengji_core_foundation.follow_play(cs(follow_str),first_cd, \
             cs(custom_hands), self.trump_card)

    def test_normal_follow(self):
        """单牌/对子/拖拉机的跟牌"""
        ret = self._index1_follow('dQ','d5')
        self.assertEqual(ret.pattern, Pattern.SINGLE)

        ret = self._index1_follow('d0d0','d7d7')
        self.assertEqual(ret.pattern, Pattern.PAIR)  

        ret = self._index1_follow('d0d0d9d9','d7d7d5d3')
        self.assertEqual(ret.pattern, Pattern.DISCARD)      
        
    def test_bucket_follow(self):
        """甩牌的跟牌"""
        ret = self._index1_follow('dAd0d0d9d9d8d8','c6c3d7d7d6d5d3')
        self.assertEqual(ret.pattern, Pattern.DISCARD)

        ret = self._index1_follow('dAd0d0d9d9d8d8','c4d4s0s9s3s2hK')
        self.assertEqual(ret, None)  

        ret = self._custom_follow('dAdAdQdQ', 'd0d0d9d9', 'dKd0d0d9d9d3')
        self.assertEqual(ret.pattern, Pattern.DISCARD) 

        ret = self._custom_follow('dAdAdKdQdQ', 'dKd0d0d9d3', 'dKd0d0d9d8d7d3')
        self.assertEqual(ret.pattern, Pattern.DISCARD) 

        ret = self._custom_follow('dAdAdQdQ', 'd0d0d9d3', 'dKdQd0d0d9d9d3')
        self.assertEqual(ret, None) 

        ret = self._custom_follow('dAdK', 'd9d3', 'dKd0d0d9d8d7d3')
        self.assertEqual(ret.pattern, Pattern.DISCARD) 



if __name__ == '__main__':
    unittest.main()